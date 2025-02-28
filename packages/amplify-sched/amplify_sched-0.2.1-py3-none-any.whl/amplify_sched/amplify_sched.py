# Copyright (c) Fixstars Amplify Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import json
import re
import warnings
from datetime import date, datetime, time, timedelta
from time import sleep
from typing import Any, List, Optional, Union, overload

import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import requests


def _get_model(obj: Any) -> Optional["Model"]:
    """Return the :obj:`Model` to which the object belongs.

    Args:
        obj: object

    Returns:
        An instance of the :obj:`Model` class to which the input object belongs. Returns ``None`` if it is not found.
    """
    parent = obj
    while parent is not None:
        if isinstance(parent, Model):
            return parent
        parent = parent._parent
    return None


def _is_registered(obj: Any) -> bool:
    """Checks if the input object is registered with another object.

    Args:
        obj : object

    Returns:
        Returns ``True`` if registered, ``False`` otherwise.
    """
    assert obj is not None
    assert getattr(obj, "index", None) is not None
    return obj.index >= 0  # type: ignore


class DatetimeUnit:
    """The time unit of the :obj:`Model` class.

    Args:
        start : The start time of the scheduling problem. Defaults to `time()`.
        unit : The time unit for the scheduling problem. Defaults to `timedelta(minutes=1)`.

    Examples:
        >>> from amplify_sched import *
        >>> dtime = DatetimeUnit(start=datetime(year=2023, month=1, day=1), unit=timedelta(seconds=60))
        >>> dtime
        {'start': datetime.datetime(2023, 1, 1, 0, 0), 'unit': datetime.timedelta(seconds=60)}
    """

    __slots__ = (
        "_start",
        "_unit",
        "_today",
        "_dtime_start",
        "_used",
    )  # FIXME: used はこのオブジェクトが"有効"に使われたかを表すフラグ (汚い)

    def __init__(
        self,
        start: Union[datetime, time] = time(),
        unit: timedelta = timedelta(minutes=1),
    ):
        self._start = start
        self._unit = unit
        self._today: date = date.today()
        self._dtime_start: datetime = (
            datetime.combine(self._today, self._start) if isinstance(self._start, time) else self._start
        )
        self._used = False

    @property
    def start(self) -> Union[datetime, time]:
        """start time"""
        return self._start

    @property
    def unit(self) -> timedelta:
        """time unit"""
        return self._unit

    def to_int_datetime(self, dtime: Union[datetime, time]) -> int:
        """Convert :obj:`datetime` to :obj:`int` using the time unit.

        to_int_datetime converts dtime to an integer value representing the time duration between dtime and the
        specified start time, in the specified time unit.

        Args:
            dtime : :obj:`datetime` object

        Returns:
            the time duration
        """
        if isinstance(self.start, time) and isinstance(dtime, datetime):
            raise ValueError("Argument type must be 'datetime.datetime' since 'start' type is 'datetime.time'")

        # datetime.time -> datetime.datetime
        if isinstance(dtime, time):
            dtime = datetime.combine(self._today, dtime)

        if dtime < self._dtime_start:
            raise ValueError(f"The argument date or time {dtime} must be later than 'start' time {self._dtime_start}")

        self._used = True  # FIXME
        return (dtime - self._dtime_start) // self.unit

    def to_int_timedelta(self, delta: timedelta) -> int:
        """convert :obj:`timedelta` to int using the specified time unit

        Args:
            dtime : :obj:`timedelta` to convert to :obj:`int`

        Returns:
            An integer value representing the :obj:`timedelta` in the specified time unit
        """
        self._used = True  # FIXME
        return delta // self.unit

    def from_int_datetime(self, int_datetime: int) -> Union[datetime, timedelta]:
        """convert :obj:`int` to :obj:`datetime` using the specified time unit

        Args:
            int_datetime : :obj:`int` to convert to :obj:`datetime`

        Returns:
            A :obj:`datetime` or :obj:`timedelta` value representing int_datetime converted using the specified
                time unit.
        """
        if isinstance(self.start, time):
            return self._dtime_start + int_datetime * self.unit - datetime.combine(self._today, time())

        return self.start + int_datetime * self.unit

    def from_int_timedelta(self, int_timedelta: int) -> timedelta:
        """convert :obj:`int` to :obj:`timedelta` using the specified time unit

        Args:
            int_timedelta : :obj:`int` to convert to :obj:`timedelta`

        Returns:
            A :obj:`timedelta` value representing int_timedelta converted using the specified time unit.
        """
        return int_timedelta * self.unit

    def _astuple(self) -> tuple[Union[datetime, time], timedelta]:
        return (self.start, self.unit)

    def _asdict(self) -> dict[str, Union[datetime, time, timedelta]]:
        return {"start": self.start, "unit": self.unit}

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)


def _to_int_datetime(dtime_unit: Optional[DatetimeUnit], dtime: Union[int, datetime, time]) -> int:
    """convert dtime to int using dtime_unit"""
    if isinstance(dtime, int):
        return dtime
    if dtime_unit is None:
        raise ValueError("start time or time unit is not given")
    return dtime_unit.to_int_datetime(dtime)


def _to_int_timedelta(dtime_unit: Optional[DatetimeUnit], delta: Union[int, timedelta]) -> int:
    """convert delta to int using dtime_unit"""
    if isinstance(delta, int):
        return delta
    if dtime_unit is None:
        raise ValueError("start time or time unit is not given")
    return dtime_unit.to_int_timedelta(delta)


class Schedule:
    """Solution of a scheduling problem.
    :obj:`Schedule` is generated from solve method of :obj:`Model`.
    """

    def __init__(self, result: list[dict[str, int]], status: str, model: "Model"):
        """:obj:`Schedule` is generated from solve method of :obj:`Model`.

        Args:
            result : solution of the scheduling problem
            status : the status of the solution of the scheduling problem
            model : the scheduling problem model
        """
        self._model = model
        self._status = status
        self._table = pd.DataFrame(result)

        # rename columns
        self._table.rename({"job": "Job"}, axis=1, inplace=True)
        self._table.rename({"machine": "Machine"}, axis=1, inplace=True)
        self._table.rename({"start": "Start"}, axis=1, inplace=True)
        self._table.rename({"end": "Finish"}, axis=1, inplace=True)
        self._table.rename({"process": "Process"}, axis=1, inplace=True)

        # conversion
        self._table["Machine"] = self._table["Machine"].apply(lambda x: self._model.machines._names()[x])
        self._table["Job"] = self._table["Job"].apply(lambda x: self._model.jobs._names()[x])
        self._time_type: type
        if self._model._datetime_unit._used:
            self._time_type = type(self._model._datetime_unit.start)
            self._table["Start"] = self._table["Start"].apply(lambda x: self._model._datetime_unit.from_int_datetime(x))
            self._table["Finish"] = self._table["Finish"].apply(
                lambda x: self._model._datetime_unit.from_int_datetime(x)
            )
        else:
            self._time_type = int
        self._table = self._table.reindex(columns=["Job", "Process", "Machine", "Start", "Finish"])

    @property
    def status(self) -> str:
        """status of the solution"""
        return self._status

    @property
    def table(self) -> pd.DataFrame:
        """solution in table format"""
        return self._table

    def timeline(
        self,
        machine_view: bool = False,
        separated_by_task: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> plotly.graph_objs.Figure:
        """Solution timeline figure.

        Args:
            machine_view : ``True`` to show a timeline for each machine, ``False`` for each job. Defaults to ``False``.
            separated_by_task: True to separate GanttChart by process index or False to not separate it.
                Defaults to ``False``.
            width : The figure width in pixels. Defaults to ``None``.
            height : The figure height in pixels. Defaults to ``None``.

        Returns:
            plotly.graph_objects.Figure: timeline figure
        """

        def __atoi(text: str) -> object:
            return int(text) if text.isdigit() else text

        def natural_keys(text: str) -> list[object]:
            return [__atoi(c) for c in re.split(r"(\d+)", text)]

        df = self._table.copy()

        if self._time_type == int:
            df["Start"] = df["Start"].astype("datetime64[ms]")
            df["Finish"] = df["Finish"].astype("datetime64[ms]")
        elif self._time_type != datetime:
            df["Start"] = df["Start"].apply(lambda x: datetime.combine(date.today(), time()) + x)
            df["Finish"] = df["Finish"].apply(lambda x: datetime.combine(date.today(), time()) + x)

        df.Machine = df.Machine.astype(str)
        y_axis = "Job"
        color_axis = "Machine"
        facet_row = None
        if machine_view:
            y_axis = "Machine"
            color_axis = "Job"
        if separated_by_task:
            facet_row = "Process"

        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y=y_axis,
            facet_row=facet_row,
            color=color_axis,
            hover_data={
                "Start": True,
                "Finish": True,
                "Job": True,
                "Machine": True,
                "Process": True,
            },
            category_orders={
                "Job": sorted(df.Job.unique(), key=natural_keys),
                "Machine": sorted(df.Machine.unique(), key=natural_keys),
            },
            width=width,
            height=height,
        )

        if self._time_type == int:
            s = re.compile("xaxis")
            for i in dir(fig.layout):
                if s.search(i):
                    setattr(getattr(fig.layout, i), "type", "linear")
            _data: go.Bar
            for _data in fig.data:  # type: ignore
                _xs: np.ndarray = _data.x  # type: ignore
                _data.x = _xs.astype("timedelta64[ms]").astype(int)
                _bases: np.ndarray = _data.base  # type: ignore
                _data.base = _bases.astype("datetime64[ms]").astype(int)
        return fig

    def resource(
        self,
        avail_view: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> plotly.graph_objs.Figure:
        """Solution resource figure.

        Args:
            avail_view : ``True`` to show a timeline for available resources, ``False`` for requirements. Defaults to ``False``.
            width : The figure width in pixels. Defaults to ``None``.
            height :  The figure height in pixels. Defaults to ``None``.

        Returns:
            plotly.graph_objects.Figure:resource figure
        """
        if len(self._model.resources) == 0:
            raise ValueError("no resource is registered in model")
        df_result = self._table.copy()

        def get_required_resources(x):
            required_resources = self._model.jobs[x["Job"]][x["Process"]].required_resources
            ret = []
            for resource in required_resources:
                if isinstance(resource, tuple):
                    if resource[1].name == x["Machine"]:
                        ret.append(resource[0])
                else:
                    ret.append(resource)
            return ret

        df_result["Resource"] = df_result.apply(
            lambda x: get_required_resources(x),
            axis=1,
        )
        df_resource = df_result.explode("Resource").copy().dropna()
        df_resource["Resource"] = df_resource["Resource"].apply(lambda x: x.name)
        df_resource["time_requirement"] = df_resource.apply(
            lambda x: [
                {"time": x["Start"], "requirement": 1},
                {"time": x["Finish"], "requirement": -1},
            ],
            axis=1,
        )
        df_resource = (
            df_resource.explode("time_requirement")
            .set_index("Resource")["time_requirement"]
            .apply(pd.Series)
            .reset_index()
            .sort_values(["Resource", "time"])
        )
        if self._time_type == int:
            df_resource = pd.concat(
                [
                    df_resource,
                    pd.DataFrame(
                        {
                            "Resource": list(self._model.resources.keys()),
                            "time": [0 for _ in range(len(self._model.resources))],
                            "requirement": [0 for _ in range(len(self._model.resources))],
                        }
                    ),
                ]
            )
        else:
            df_resource = pd.concat(
                [
                    df_resource,
                    pd.DataFrame(
                        {
                            "Resource": list(self._model.resources.keys()),
                            "time": [self._model.start for _ in range(len(self._model.resources))],
                            "requirement": [0 for _ in range(len(self._model.resources))],
                        }
                    ),
                ]
            )
        df_resource = df_resource.groupby(["Resource", "time"]).sum().reset_index()
        df_resource["requirement"] = df_resource.groupby("Resource")["requirement"].cumsum()
        df_resource["available"] = [
            self._model.resources[row["Resource"]].capacity - row["requirement"] for _, row in df_resource.iterrows()
        ]
        if avail_view:
            fig = px.line(
                df_resource,
                x="time",
                y="available",
                color="Resource",
                markers=True,
                line_shape="hv",
            )
        else:
            fig = px.line(
                df_resource,
                x="time",
                y="requirement",
                color="Resource",
                markers=True,
                line_shape="hv",
            )
        return fig


class TimeRange(tuple):  # type: ignore
    """Start and end times expressed as :obj:`int`/:obj:`datetime`."""

    __slots__ = ()

    def __new__(cls, start: Union[datetime, time, int], end: Union[datetime, time, int]) -> TimeRange:
        if type(start) is not type(end):
            raise ValueError("'start' and 'end' must be the same type")
        if start > end:  # type: ignore
            raise ValueError("'start' must be smaller than or equal to 'end'")
        return tuple.__new__(cls, (start, end))

    @property
    def start(self) -> Union[int, datetime, time]:
        """start time of the range"""
        return tuple.__getitem__(self, 0)  # type: ignore

    @property
    def end(self) -> Union[int, datetime, time]:
        """end time of the range"""
        return tuple.__getitem__(self, 1)  # type: ignore

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> tuple[int, int]:
        if isinstance(self.start, int) or isinstance(self.end, int):
            return self.start, self.end  # type: ignore
        if dtime_unit is None:
            raise ValueError("start time or time unit is not given")
        return dtime_unit.to_int_datetime(self.start), dtime_unit.to_int_datetime(self.end)

    def _astuple(self) -> tuple[Union[datetime, time, int], Union[datetime, time, int]]:
        return self.start, self.end

    def _asdict(self) -> dict[str, Union[datetime, time, int]]:
        return {"start": self.start, "end": self.end}


class ProcessingTimes:
    """ProcessingTimes is container of processing time.

    Processing times is managed as dict; key is :obj:`Machine` and value is processing time.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Task"):
        self._times: dict[Machine, Union[int, timedelta]] = {}
        self._parent = parent

    def __getitem__(self, key: Union["Machine", str]) -> Union[int, timedelta]:
        if isinstance(key, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            key = model.machines[key]

        return self._times[key]

    def __setitem__(self, key: Union["Machine", str], value: Union[int, timedelta]) -> None:
        if isinstance(value, int) and value < 0:
            raise ValueError("value must be positive")

        if isinstance(key, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            key = model.machines[key]

        self._times[key] = value

    def __iter__(self):  # type: ignore
        return iter(self._times)

    def __contains__(self, value: Union["Machine", str]) -> bool:
        if isinstance(value, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            value = model.machines[value]
        return value in self._times

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> list[list[int]]:
        return [[_to_int_timedelta(dtime_unit, v), k.index] for k, v in self._times.items()]

    def _asdict(self) -> dict[str, Union[int, timedelta]]:
        return {k.name: v for k, v in self._times.items()}

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._times)

    def __len__(self) -> int:
        return len(self._times)

    def __delitem__(self, key: Union["Machine", str]) -> None:
        if isinstance(key, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            key = model.machines[key]

        del self._times[key]

    def keys(self):  # type: ignore
        """Return machine list registered in processing times."""
        return self._times.keys()

    def values(self):  # type: ignore
        """Return processing times."""
        return self._times.values()

    def items(self):  # type: ignore
        """Return machine and processing time."""
        return self._times.items()

    def clear(self) -> None:
        return self._times.clear()

    def get(self, key: Union["Machine", str], default: Any = None) -> Union[int, timedelta]:
        if isinstance(key, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            key = model.machines[key]

        return self._times.get(key, default)

    def pop(self, key: Union["Machine", str], default: Any = None) -> Union[int, timedelta]:
        if isinstance(key, str):
            model = _get_model(self)
            if model is None:
                raise ValueError("task is not registered in model")
            key = model.machines[key]

        return self._times.pop(key, default)

    def popitem(self) -> tuple[Machine, Union[int, timedelta]]:
        return self._times.popitem()


class SetupTimes:
    """SetupTimes is container of setup time.

    Setup times is managed as list of tuple.
    Each element represents one setup time, and each setup time is a tuple with 1 to 3 elements.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Machine"):
        self._times: list[
            Union[
                tuple[
                    Union[int, timedelta],
                    Union["Job", "Task", str],
                    Union["Job", "Task", str],
                ],
                tuple[Union[int, timedelta], Union["Job", "Task", str]],
                int,
                timedelta,
            ]
        ] = []
        self._parent = parent

    def _check_element(
        self,
        element: Union[
            tuple[
                Union[int, timedelta],
                Union["Job", "Task", str],
                Union["Job", "Task", str],
            ],
            tuple[Union[int, timedelta], Union["Job", "Task", str]],
            int,
            timedelta,
        ],
    ) -> Union[
        tuple[Union[int, timedelta], Union["Job", "Task", str], Union["Job", "Task", str]],
        tuple[Union[int, timedelta], Union["Job", "Task", str]],
        int,
        timedelta,
    ]:
        """Check setup time element and return itself.

        Args:
            element: setup time

        Raises:
            AttributeError: If there is an object that has not been registered to the model in the element.
            ValueError: If there is an inappropriate type in the element, or if there are multiple registered models.

        Returns:
            element itself
        """
        if isinstance(element, int) or isinstance(element, timedelta):
            return element
        if not isinstance(element, tuple):
            raise ValueError("element type must be tuple, int or timedelta")
        if len(element) == 2:
            model = _get_model(self)
            if model is None:
                raise AttributeError("machine is not registered in model")

            prev_task = element[1]
            if isinstance(prev_task, str):
                prev_task = model.jobs[prev_task]
            else:
                model_prev = _get_model(prev_task)
                if model_prev is None:
                    raise ValueError("prev_task is not registered in model")
                if model != model_prev:
                    raise ValueError("prev_task does not belong to the same model")

            return element[0], prev_task
        if len(element) == 3:
            model = _get_model(self)
            if model is None:
                raise AttributeError("machine is not registered in model")

            prev_task = element[1]
            if isinstance(prev_task, str):
                prev_task = model.jobs[prev_task]
            else:
                model_prev = _get_model(prev_task)
                if model_prev is None:
                    raise ValueError("prev_task is not registered in model")
                if model != model_prev:
                    raise ValueError("prev_task does not belong to the same model")

            next_task = element[2]  # type: ignore
            if isinstance(next_task, str):
                next_task = model.jobs[next_task]
            else:
                model_next = _get_model(next_task)
                if model_next is None:
                    raise ValueError("next_task is not registered in model")
                if model != model_next:
                    raise ValueError("next_task does not belong to the same model")

            return element[0], prev_task, next_task
        raise ValueError("element size must be 2 or 3")

    def __getitem__(self, index: int) -> Union[
        tuple[Union[int, timedelta], Union["Job", "Task", str], Union["Job", "Task", str]],
        tuple[Union[int, timedelta], Union["Job", "Task", str]],
        int,
        timedelta,
    ]:
        return self._times[index]

    def __setitem__(
        self,
        index: int,
        value: tuple[Union[int, timedelta], Union["Job", "Task", str], Union["Job", "Task", str]],
    ) -> None:
        self._times[index] = self._check_element(value)

    def append(
        self,
        setup_time: Union[
            tuple[
                Union[int, timedelta],
                Union["Job", "Task", str],
                Union["Job", "Task", str],
            ],
            tuple[Union[int, timedelta], Union["Job", "Task", str]],
            int,
            timedelta,
        ],
    ) -> None:
        """append setup_time

        Args:
            setup_time: setup_time for appending
        """
        self._times.append(self._check_element(setup_time))

    def __iter__(self):  # type: ignore
        return iter(self._times)

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> list[list[Union[int, list[int]]]]:
        def __f(s: Union["Job", "Task"]) -> list[int]:
            if isinstance(s, Job):
                return [s.index]
            if s._parent is None:
                raise RuntimeError(
                    "'_create_request_data' cannot be called because a contained 'Task' object does not belong to a 'Job' object"
                )
            return [s._parent.index, s.index]

        return [
            (
                [_to_int_timedelta(dtime_unit, t)]
                if isinstance(t, int) or isinstance(t, timedelta)
                else [_to_int_timedelta(dtime_unit, v) if i == 0 else __f(v) for (i, v) in enumerate(t)]
            )  # type: ignore
            for t in self._times
        ]

    def _tolist(
        self,
    ) -> list[tuple[Union[int, timedelta], list[Union[str, int]], list[Union[str, int]]]]:
        def __f(s: Union["Job", "Task"]) -> list[Union[str, int]]:
            if isinstance(s, Job):
                return [s.name]
            if s._parent is None:
                raise RuntimeError(
                    "'_tolist' cannot be called because a contained 'Task' object does not belong to a 'Job' object"
                )
            return [s._parent.name, s.index]

        return [
            (
                s[0],  # type: ignore
                __f(s[1]),  # type: ignore
                __f(s[2]),  # type: ignore
            )
            for s in self._times
        ]

    def __str__(self) -> str:
        return str(self._tolist())

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._times)

    def __len__(self) -> int:
        return len(self._times)


class Resource:
    """A class managing a resource.

    Args:
        name: resource name. Defaults to ""
    """

    def __init__(
        self,
        name: str = "",
    ) -> None:
        self._name = name
        self._index = -1
        self._parent: Optional["Resources"] = None
        self._capacity = 1

    @property
    def name(self) -> str:
        """resource name

        Examples:
            >>> model = Model()
            >>> model.resources.add("Resource A")
            >>> model.resources["Resource A"].name
            'Resource A'
        """
        return self._name

    @property
    def index(self) -> int:
        """resource index

        Examples:
            >>> model = Model()
            >>> model.resources.add("Resource A")
            >>> model.resources["Resource A"].index
            0
            >>> model.resources.add("Resource B")
            >>> model.resources["Resource B"].index
            1
        """
        return self._index

    @property
    def capacity(self) -> int:
        """resource capacity

        Capacity must be positive number.

        Examples:
            >>> model = Model()
            >>> model.resources.add("Resource A")
            >>> model.resources["Resource A"].capacity = 2
            >>> model.resources["Resource A"].capacity
            2
        """
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("capacity must be positive number")
        self._capacity = value

    def _create_request_data(self) -> dict[str, int]:
        return self._asdict()

    def _asdict(self) -> dict[str, int]:
        return {"capacity": self._capacity}

    def __int__(self) -> int:
        return self._capacity

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)


class Resources:
    """Resources is container of resource.

    Resources is managed as dict. Key is resource name and value is :obj:`Resource`.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Model"):
        self._parent = parent
        self._resources_set: set[Resource] = set()
        self._resources_dict: dict[str, Resource] = {}

    def __getitem__(self, key: str) -> Resource:
        return self._resources_dict[key]

    def __setitem__(self, key: str, value: Resource) -> None:
        if key in self._resources_dict:
            raise KeyError(f"key already exists: {key}")
        if _is_registered(value):
            raise ValueError("resource is already registered")

        if value.name and value.name != key:
            warnings.warn(f"resource name will be renamed from {value.name} to {key}")

        value._name = key
        value._index = len(self._resources_dict)
        value._parent = self
        self._resources_set.add(value)
        self._resources_dict[key] = value

    def add(self, resource: Union[str, Resource]) -> None:
        """add resource as dict
        Key is resource.name and value is resource itself.

        Args:
            resource : resource to adding. If resource type is str, create new :obj:`Resource` instance using resource as name.

        Raises:
            ValueError: If resource is no name.
        """
        if isinstance(resource, str):
            resource = Resource(resource)
        if not resource.name:
            raise ValueError('resource is no name, use `resource["name"] = value` instead')
        self.__setitem__(resource.name, resource)

    def __iter__(self):  # type: ignore
        return iter(self._resources_dict)

    def __contains__(self, value: Union[str, Resource]) -> bool:
        if isinstance(value, str):
            return value in self._resources_dict
        else:
            return value in self._resources_set

    def _create_request_data(self) -> list[int]:
        return [m.capacity for m in sorted(self._resources_set, key=lambda m: m.index)]

    def __str__(self) -> str:
        return str(self._resources_dict)

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self) -> reversed[str]:
        return reversed(self._resources_dict)

    def __len__(self) -> int:
        return len(self._resources_dict)

    def keys(self):  # type: ignore
        return self._resources_dict.keys()

    def values(self):  # type: ignore
        return self._resources_dict.values()

    def items(self):  # type: ignore
        return self._resources_dict.items()

    def copy(self) -> dict[str, Resource]:
        return self._resources_dict.copy()

    def get(self, key: str, default: Any = None) -> Union[str, Resource]:
        return self._resources_dict.get(key, default)


class RequiredResources:
    """RequiredResources is container of required resource.

    RequiredResources is managed as list of :obj:`Resource`.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Task"):
        self._resources: list[Union[Resource, tuple[Resource, Machine]]] = []
        self._parent = parent

    def _check_element(
        self,
        element: Union[
            Resource,
            str,
            tuple[Resource, Machine],
            tuple[str, str],
            tuple[Resource, str],
            tuple[str, Machine],
        ],
    ) -> Union[Resource, tuple[Resource, Machine]]:
        """check required resource and return itself.

        Args:
            element : required resource

        Raises:
            AttributeError: If there is an task that has not been registered to the model in the element
            ValueError: If there is an resource that has not been registered to the model in the element,
                or if there are multiple registered models

        Returns:
            element itself
        """
        model = _get_model(self)
        if model is None:
            raise AttributeError("task is not registered in model")

        def _check_resource(element: Resource) -> None:
            model_rsc = _get_model(element)
            if model_rsc is None:
                raise ValueError("resource is not registered in model")
            if model != model_rsc:
                raise ValueError("resource does not belong to the same model")

        def _check_machine(element: Machine) -> None:
            model_mch = _get_model(element)
            if model_mch is None:
                raise ValueError("machine is not registered in model")
            if model != model_mch:
                raise ValueError("machine does not belong to the same model")

        if isinstance(element, Resource):
            _check_resource(element)
            return element

        if isinstance(element, str):
            return model.resources[element]

        if len(element) != 2:
            raise ValueError("element size must be 2")

        if isinstance(element[0], Resource) and isinstance(element[1], Machine):
            _check_resource(element[0])
            _check_machine(element[1])
            return element[0], element[1]
        elif isinstance(element[0], str) and isinstance(element[1], str):
            return model.resources[element[0]], model.machines[element[1]]
        elif isinstance(element[0], Resource) and isinstance(element[1], str):
            _check_resource(element[0])
            return element[0], model.machines[element[1]]
        elif isinstance(element[0], str) and isinstance(element[1], Machine):
            _check_machine(element[1])
            return model.resources[element[0]], element[1]
        else:
            raise ValueError(
                "element type must be Resource, str, tuple[Resource, Machine] or "
                "tuple[str, str] or tuple[Resource, str] or tuple[str, Machine]"
            )

    def __getitem__(self, index: int) -> Union[Resource, tuple[Resource, Machine]]:
        return self._resources[index]

    def __setitem__(
        self,
        index: int,
        value: Union[
            Resource,
            str,
            tuple[Resource, Machine],
            tuple[str, str],
            tuple[Resource, str],
            tuple[str, Machine],
        ],
    ) -> None:
        self._resources[index] = self._check_element(value)

    def append(
        self,
        value: Union[
            Resource,
            str,
            tuple[Resource, Machine],
            tuple[str, str],
            tuple[Resource, str],
            tuple[str, Machine],
        ],
    ) -> None:
        """append required resource

        Args:
            value: required resource
        """
        self._resources.append(self._check_element(value))

    def __iter__(self):  # type: ignore
        return iter(self._resources)

    def _create_request_data(self) -> list[Union[int, list[int]]]:
        return [m.index if isinstance(m, Resource) else [m[0].index, m[1].index] for m in self._resources]

    def __str__(self) -> str:
        return str([m.name if isinstance(m, Resource) else [m[0].name, m[1].name] for m in self._resources])

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._resources)

    def __len__(self) -> int:
        return len(self._resources)


class Machine:
    """A class managing a machine

    In a scheduling problem, a machine processes tasks in a specified time range.

    Args:
        name: machine name. Defaults to ""

    """

    def __init__(self, name: str = ""):
        self._name = name
        self._index = -1
        self._parent: Optional["Machines"] = None
        self._buffer_size: Optional[int] = None
        self._setup_times: SetupTimes = SetupTimes(self)
        self._maintenance_times: List[TimeRange] = []

    @property
    def name(self) -> str:
        """machine name

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].name
            'Machine A'
        """
        return self._name

    @property
    def index(self) -> int:
        """machine index

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].index
            0
            >>> model.machines.add("Machine B")
            >>> model.machines["Machine B"].index
            1
        """
        return self._index

    @property
    def buffer_size(self) -> Optional[int]:
        """machine buffer size

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].buffer_size = 10
            >>> model.machines["Machine A"].buffer_size
            10
        """
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size: int) -> None:
        self._buffer_size = buffer_size

    @property
    def setup_times(self) -> SetupTimes:
        """machine setup times

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs.add("Job B")
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].setup_times.append((10, "Job A", "Job B"))
            >>> model.machines["Machine A"].setup_times
            [(10, ['Job A'], ['Job B'])]
        """
        return self._setup_times

    @property
    def maintenance_times(self) -> List[TimeRange]:
        """machine maintenance times

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].maintenance_times.append((10, 15))
            >>> model.machines["Machine A"].maintenance_times
            [(10, 15)]
        """
        return self._maintenance_times

    def add_maintenance_time(self, start: Union[datetime, time, int], end: Union[datetime, time, int]) -> None:
        """add maintenance time

        Args:
            start: maintenance start time
            end: maintenance end time

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].add_maintenance_time(10, 15)
            >>> model.machines["Machine A"].maintenance_times
            [(10, 15)]
        """
        self._maintenance_times.append(TimeRange(start, end))

    def add_setup_time(
        self,
        setup_time: Union[int, timedelta],
        prev_task: Union["Job", "Task", str],
        next_task: Union["Job", "Task", str],
    ) -> None:
        """add setup time

        Add setup_time (time taken to switch from previous task to next task).

        Args:
            setup_time: setup time
            prev_task: previous task
            next_task: next task
        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs.add("Job B")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job B"].append(Task())
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].add_setup_time(10, "Job A", "Job B")
            >>> model.machines["Machine A"].setup_times
            [(10, ['Job A'], ['Job B'])]
        """
        self._setup_times.append((setup_time, prev_task, next_task))

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if len(self._maintenance_times) != 0:
            d["maintenance_times"] = [mt._create_request_data(dtime_unit) for mt in self._maintenance_times]
        if self._buffer_size is not None:
            d["buffer_size"] = self._buffer_size
        if len(self._setup_times) != 0:
            d["setup_times"] = self._setup_times._create_request_data(dtime_unit)
        return d

    def _asdict(self) -> dict[str, Any]:
        return {
            "maintenance_times": self._maintenance_times,
            "buffer_size": self._buffer_size,
            "setup_times": self._setup_times,
        }

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)


class Machines:
    """Machines is container of :obj:`Machine`.

    Machines is managed as dict. Key is machine name and value is :obj:`Machine`.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Model"):
        self._parent = parent
        self._machines_set: set[Machine] = set()
        self._machines_dict: dict[str, Machine] = {}

    def __getitem__(self, key: str) -> Machine:
        return self._machines_dict[key]

    def __setitem__(self, key: str, value: Machine) -> None:
        if key in self._machines_dict:
            raise KeyError(f"key already exists: {key}")
        if _is_registered(value):
            raise ValueError("machine is already registered")

        if value.name and value.name != key:
            warnings.warn(f"Machine name will be renamed from {value.name} to {key}")

        value._name = key
        value._index = len(self._machines_dict)
        value._parent = self
        self._machines_set.add(value)
        self._machines_dict[key] = value

    def add(self, machine: Union[str, Machine]) -> None:
        """add machine as dict
        key is machine.name and value is machine itself

        Args:
            machine : machine to adding. If machine type is str, create new :obj:`Machine` instance using machine as name.

        Raises:
            ValueError: If machine is no name
        """
        if isinstance(machine, str):
            machine = Machine(machine)
        if not machine.name:
            raise ValueError('machine is no name, use `machine["name"] = value` instead')
        self.__setitem__(machine.name, machine)

    def __iter__(self):  # type: ignore
        return iter(self._machines_dict)

    def __contains__(self, value: Union[str, Machine]) -> bool:
        if isinstance(value, str):
            return value in self._machines_dict
        else:
            return value in self._machines_set

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> list[Any]:
        return [m._create_request_data(dtime_unit) for m in sorted(self._machines_set, key=lambda m: m.index)]

    def _names(self) -> list[str]:
        return [m.name for m in sorted(self._machines_set, key=lambda j: j.index)]

    def __str__(self) -> str:
        return str(self._machines_dict)

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._machines_dict)

    def __len__(self) -> int:
        return len(self._machines_dict)

    def keys(self):  # type: ignore
        return self._machines_dict.keys()

    def values(self):  # type: ignore
        return self._machines_dict.values()

    def items(self):  # type: ignore
        return self._machines_dict.items()

    def copy(self) -> dict[str, Machine]:
        return self._machines_dict.copy()

    def get(self, key: str, default: Any = None) -> Machine:
        return self._machines_dict.get(key, default)


class TransportationTimes:
    """TransportationTimes is container of transportation time.

    Transportation times is managed as list of tuple.
    Each element represents one transportation time, and each transportation time is a tuple with 1 to 3 elements.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Task"):
        self._times: list[
            Union[
                tuple[Union[int, timedelta], Machine, Machine],
                tuple[Union[int, timedelta], Machine],
                int,
                timedelta,
            ]
        ] = []
        self._parent = parent

    def _check_element(
        self,
        element: Union[
            tuple[Union[int, timedelta], Union[Machine, str], Union[Machine, str]],
            tuple[Union[int, timedelta], Union[Machine, str]],
            int,
            timedelta,
        ],
    ) -> Union[
        tuple[Union[int, timedelta], Machine, Machine],
        tuple[Union[int, timedelta], Machine],
        int,
        timedelta,
    ]:
        """check transportaion time element and return itself.

        Args:
            element: transportaion time

        Raises:
            AttributeError: If there is an object that has not been registered to the model in the element
            ValueError: If there is an inappropriate type in the element, or if there are multiple registered models

        Returns:
            element itself
        """
        if isinstance(element, int) or isinstance(element, timedelta):
            return element
        if len(element) == 2:
            model = _get_model(self)
            src_machine = element[1]
            if model is None:
                raise AttributeError("task is not registered in model")
            if isinstance(src_machine, str):
                src_machine = model.machines[src_machine]
            else:
                model_src = _get_model(src_machine)
                if model_src is None:
                    raise ValueError("src_machine is not registered in model")
                if model != model_src:
                    raise ValueError("src_machine does not belong to the same model")
            return element[0], src_machine
        if len(element) == 3:
            model = _get_model(self)
            src_machine = element[1]
            if model is None:
                raise AttributeError("task is not registered in model")
            if isinstance(src_machine, str):
                src_machine = model.machines[src_machine]
            else:
                model_src = _get_model(src_machine)
                if model_src is None:
                    raise ValueError("src_machine is not registered in model")
                if model != model_src:
                    raise ValueError("src_machine does not belong to the same model")
            dst_machine = element[2]  # type: ignore
            if isinstance(dst_machine, str):
                dst_machine = model.machines[dst_machine]
            else:
                model_dst = _get_model(dst_machine)
                if model_dst is None:
                    raise ValueError("dst_machine is not registered in model")
                if model != model_dst:
                    raise ValueError("dst_machine does not belong to the same model")

            return element[0], src_machine, dst_machine
        raise ValueError("element size must be 2 or 3")

    def __getitem__(self, index: int) -> Union[
        tuple[Union[int, timedelta], Machine, Machine],
        tuple[Union[int, timedelta], Machine],
        int,
        timedelta,
    ]:
        return self._times[index]

    def __setitem__(self, index: int, value: tuple[Union[int, timedelta], Machine, Machine]) -> None:
        self._times[index] = self._check_element(value)

    def append(
        self,
        value: Union[
            tuple[Union[int, timedelta], Union[Machine, str], Union[Machine, str]],
            tuple[Union[int, timedelta], Union[Machine, str]],
            int,
            timedelta,
        ],
    ) -> None:
        """append transportaion_time

        Args:
            value: transportaion_time for appending
        """
        self._times.append(self._check_element(value))

    def __iter__(self):  # type: ignore
        return iter(self._times)

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> list[list[int]]:
        return [
            (
                [_to_int_timedelta(dtime_unit, t)]
                if isinstance(t, int) or isinstance(t, timedelta)
                else [_to_int_timedelta(dtime_unit, v) if i == 0 else v.index for (i, v) in enumerate(t)]
            )  # type: ignore
            for t in self._times
        ]

    def __str__(self) -> str:
        return str([(t[0], t[1].name, t[2].name) for t in self._times])  # type: ignore

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._times)

    def __len__(self) -> int:
        return len(self._times)


class DependentJob:
    """DependentJob contains the properties of dependency

    Args:
        parent: parent object which this object belong to
        job: dependent job to append
        interval_time: interval time or times (lower and upper bounds)
    """

    def __init__(
        self,
        parent: DependentJobs,
        job: Job | str,
        interval_times: tuple[int | None, int | None] | int | None = None,
    ):
        self._parent = parent
        self._job = self._check_job(job)
        self._interval_time_lower_bound, self._interval_time_upper_bound = self._check_times(interval_times)

    def _check_job(self, job: Union["Job", str]) -> "Job":
        """check dependent job and return Job.

        Args:
            job : dependent job

        Raises:
            AttributeError: If there is an job that has not been registered to the model

        Returns:
            Job object specified by job
        """
        if isinstance(job, str):
            model = _get_model(self)
            if model is None:
                raise AttributeError("job is not registered in model")
            job = model.jobs[job]
        return job

    def _check_times(self, interval_time: tuple[int | None, int | None] | int | None) -> tuple[int | None, int | None]:
        """check interval times and return interval times.

        Args:
            interval_time : Interval time

        Raises:
            AttributeError: If the interval_time is negative integer
            AttributeError: If the interval_time is a tuple of the bounds and lower > upper bounds
            AttributeError: If the interval_time is a tuple of the bounds and lower bound is a negative integer
            AttributeError: If the interval_time is a tuple of the bounds and upper bound is a negative integer

        Returns:
            Interval times
        """

        self._interval_time_lower_bound: int | None = None
        self._interval_time_upper_bound: int | None = None
        if isinstance(interval_time, int):
            if interval_time < 0:
                raise AttributeError("negative interval time is specified")
            self._interval_time_lower_bound = interval_time
            self._interval_time_upper_bound = interval_time
        elif isinstance(interval_time, tuple):
            if interval_time[0] is not None and interval_time[1] is not None and interval_time[0] > interval_time[1]:
                raise AttributeError("lower bound is greater than upper bound")
            if interval_time[0] is not None and interval_time[0] < 0:
                raise AttributeError("negative interval time lower bound is specified")
            if interval_time[1] is not None and interval_time[1] < 0:
                raise AttributeError("negative interval time upper bound is specified")
            self._interval_time_lower_bound, self._interval_time_upper_bound = interval_time
        return self._interval_time_lower_bound, self._interval_time_upper_bound

    def _create_request_data(self) -> dict[str, int]:
        d: dict[str, int] = {}
        d["job_id"] = self._job._index
        if self._interval_time_lower_bound is not None:
            d["interval_time_lower_bound"] = self._interval_time_lower_bound
        if self._interval_time_upper_bound is not None:
            d["interval_time_upper_bound"] = self._interval_time_upper_bound
        return d

    def __str__(self) -> str:
        return str(
            {
                "job_id": self._job._index,
                "interval_time_lower_bound": self._interval_time_lower_bound,
                "interval_time_upper_bound": self._interval_time_upper_bound,
            }
        )

    def __repr__(self) -> str:
        return str(self)


class DependentJobs:
    """DependentJobs is container of dependent job.

    DependentJobs is managed as list of Job.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Job"):
        self._dependent_jobs: list[DependentJob] = []
        self._parent = parent

    def __getitem__(self, index: int) -> DependentJob:
        return self._dependent_jobs[index]

    def __setitem__(
        self,
        index: int,
        value: Job | str | tuple[Job | str, tuple[int | None, int | None] | int | None],
    ) -> None:
        if isinstance(value, tuple):
            self._dependent_jobs[index] = DependentJob(self, value[0], value[1])
        else:
            self._dependent_jobs[index] = DependentJob(self, value)

    def append(
        self,
        value: Job | str | tuple[Job | str, tuple[int | None, int | None] | int | None],
    ) -> None:
        """append dependent job

        Args:
            value: job or tuple of job and interval_time (either a time or times to specify lower and upper bounds.)
        """

        if isinstance(value, tuple):
            self._dependent_jobs.append(DependentJob(self, value[0], value[1]))
        else:
            self._dependent_jobs.append(DependentJob(self, value))

    def __iter__(self):  # type: ignore
        return iter(self._dependent_jobs)

    def _create_request_data(self) -> list[dict[str, int]]:
        return [dj._create_request_data() for dj in self._dependent_jobs]

    def __str__(self) -> str:
        return str([dj for dj in self._dependent_jobs])

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._dependent_jobs)

    def __len__(self) -> int:
        return len(self._dependent_jobs)


class Task:
    """A class managing a task.

    In a scheduling problem, a task is processed by a machine at a specified processing time.
    The main target for optimization is the task start time.

    """

    def __init__(self) -> None:
        self._index = -1
        self._parent: Optional["Job"] = None
        self._processing_times = ProcessingTimes(self)
        self._required_resources = RequiredResources(self)
        self._required_buffer_size: Optional[int] = None
        self._transportation_times = TransportationTimes(self)
        self._release_time: Optional[Union[int, datetime, time]] = None
        self._deadline: Optional[Union[int, datetime, time]] = None

    @property
    def index(self) -> int:
        """task index

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].index
            0
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][1].index
            1
        """
        return self._index

    @property
    def required_buffer_size(self) -> Optional[int]:
        """required buffer size for this task

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].required_buffer_size = 2
            >>> model.jobs["Job A"][0].required_buffer_size
            2
        """
        return self._required_buffer_size

    @required_buffer_size.setter
    def required_buffer_size(self, required_buffer_size: int) -> None:
        self._required_buffer_size = required_buffer_size

    @property
    def release_time(self) -> Optional[Union[int, datetime, time]]:
        """release time size for this task

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].release_time = 20
            >>> model.jobs["Job A"][0].release_time
            20
        """
        return self._release_time

    @release_time.setter
    def release_time(self, release_time: Union[int, datetime, time]) -> None:
        self._release_time = release_time

    @property
    def deadline(self) -> Optional[Union[int, datetime, time]]:
        """deadline for this task

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].deadline = 30
            >>> model.jobs["Job A"][0].deadline
            30
        """
        return self._deadline

    @deadline.setter
    def deadline(self, deadline: Union[int, datetime, time]) -> None:
        self._deadline = deadline

    @property
    def processing_times(self) -> ProcessingTimes:
        """processing times for this task

        Processing times is managed as dict; key is the machine name and value is processing time.
        During registration, the existence of the machine in the model is checked.
        Registering a machine name that does not exist in the model will result in a ValueError.
        If this task is not registered in the model, a ValueError will occur because the existence of the
        machine cannot be checked.

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.machines.add("Machine A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].processing_times["Machine A"] = 10
            >>> model.jobs["Job A"][0].processing_times["Machine A"]
            10
        """
        return self._processing_times

    @property
    def required_resources(self) -> RequiredResources:
        """required resources for this task

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.resources.add("Resource A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].required_resources.append("Resource A")
            >>> model.jobs["Job A"][0].required_resources
            ['Resource A']
        """
        return self._required_resources

    @property
    def transportation_times(self) -> TransportationTimes:
        """transportation time for this task

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.machines.add("Machine A")
            >>> model.machines.add("Machine B")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].transportation_times.append((10, "Machine A", "Machine B"))
            >>> model.jobs["Job A"][0].transportation_times
            [(10, 'Machine A', 'Machine B')]
        """
        return self._transportation_times

    def add_required_resource(self, resource: Union[Resource, str]) -> None:
        """add required resource

        Args:
            resource: required resource

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.resources.add("Resource A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].add_required_resource("Resource A")
            >>> model.jobs["Job A"][0].required_resources
            ['Resource A']
        """
        if self._required_resources is None:
            self._required_resources = RequiredResources(self)
        self._required_resources.append(resource)

    def add_transportation_time(
        self,
        transportation_time: Union[int, timedelta],
        src_machine: Union[Machine, str],
        dst_machine: Union[Machine, str],
    ) -> None:
        """add transportation time

        add transportation time from a source machine to a destination machine

        Args:
            transportation_time: transportation time
            src_machine: source machine
            dst_machine: destination machine

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.machines.add("Machine A")
            >>> model.machines.add("Machine B")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0].add_transportation_time(10, "Machine A", "Machine B")
            >>> model.jobs["Job A"][0].transportation_times
            [(10, 'Machine A', 'Machine B')]
        """
        # TODO: 登録されていないMachineをModelに登録する
        self._transportation_times.append((transportation_time, src_machine, dst_machine))

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> dict[str, Any]:
        d: dict[str, Any] = {}

        if len(self._processing_times) == 0:
            raise RuntimeError(f"There is no 'processing_times' in the task: {self}")

        d["processing_times"] = self._processing_times._create_request_data(dtime_unit)
        if len(self._required_resources) != 0:
            d["required_resources"] = self._required_resources._create_request_data()
        if self._required_buffer_size is not None:
            d["required_buffer_size"] = self._required_buffer_size
        if len(self._transportation_times) != 0:
            d["transportation_times"] = self._transportation_times._create_request_data(dtime_unit)
        if self._release_time is not None:
            d["release_time"] = _to_int_datetime(dtime_unit, self._release_time)
        if self._deadline is not None:
            d["deadline"] = _to_int_datetime(dtime_unit, self._deadline)
        return d

    def _asdict(self) -> dict[str, Any]:
        return {
            "index": self._index,
            "processing_times": self._processing_times,
            "required_resources": self._required_resources if self._required_resources else None,
            "required_buffer_size": self._required_buffer_size,
            "transportation_times": self._transportation_times if self._transportation_times else None,
            "release_time": self._release_time,
            "deadline": self._deadline,
        }

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)


class Job:
    """A class managing a Job.

    In a scheduling problem, a Job is a collection of multiple tasks.
    A job is completed by processing each task in turn.

    Args:
        name: job name. Defaults to ""
    """

    def __init__(self, name: str = "") -> None:
        self._name = name
        self._index = -1
        self._parent: Optional["Jobs"] = None
        self._tasks: list[Task] = []
        self._dependent_jobs = DependentJobs(self)
        self._no_wait: Optional[bool] = None
        self._num_process = 0

    @property
    def name(self) -> str:
        """job name

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].name
            'Job A'
        """
        return self._name

    @property
    def index(self) -> int:
        """job index

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].index
            0
            >>> model.jobs.add("Job B")
            >>> model.jobs["Job B"].index
            1
        """
        return self._index

    @property
    def num_process(self) -> int:
        """number of processes

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].num_process
            0
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"].num_process
            1
        """
        return self._num_process

    def __getitem__(self, index: int) -> Task:
        return self._tasks[index]

    def append(self, task: Optional[Task] = None) -> None:
        """append task

        Args:
            task: task for appending. Defaults to ``None``.

        Raises:
            ValueError: If task is already registerd

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"][0]  # doctest: +NORMALIZE_WHITESPACE
            {'index': 0, 'processing_times': {}, 'required_resources': None, 'required_buffer_size': None,
             'transportation_times': None, 'release_time': None, 'deadline': None}
        """
        if task is None:
            task = Task()
        elif _is_registered(task):
            raise ValueError("Task is already registered")

        task._index = len(self._tasks)
        task._parent = self
        self._tasks.append(task)
        self._num_process += 1

    @property
    def no_wait(self) -> Optional[bool]:
        """no wait flag

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].no_wait = True
            >>> model.jobs["Job A"].no_wait
            True
        """
        return self._no_wait

    @no_wait.setter
    def no_wait(self, no_wait: bool) -> None:
        self._no_wait = no_wait

    @property
    def dependent_jobs(self) -> DependentJobs:
        """dependent jobs for this job

        Dependent jobs is managed as list.
        During registration, the existence of the job in the model is checked.
        Registering a machine name that does not exist in the model will result in a ValueError.

        Args:
            job : depandent job

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs.add("Job B")
            >>> model.jobs["Job A"].dependent_jobs.append("Job B")
            >>> model.jobs["Job A"].dependent_jobs
            [{'job_id': 1, 'interval_time_lower_bound': None, 'interval_time_upper_bound': None}]
        """
        return self._dependent_jobs

    def task(self, process: int) -> Task:
        """returns a task for the given process

        Args:
            process : task index

        Returns:
            a task for the given process

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].append(Task())
            >>> model.jobs["Job A"].task(0)  # doctest: +NORMALIZE_WHITESPACE
            {'index': 0, 'processing_times': {}, 'required_resources': None, 'required_buffer_size': None,
             'transportation_times': None, 'release_time': None, 'deadline': None}
        """
        return self._tasks[process]

    def add_dependent_jobs(
        self,
        job: Job | str,
        interval_time: tuple[int | None, int | None] | int | None = None,
    ) -> None:
        """add dependent jobs

        Args:
            job : depandent job
            interval_time : interval time

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs.add("Job B")
            >>> model.jobs.add("Job C")
            >>> model.jobs["Job A"].add_dependent_jobs("Job B")
            >>> model.jobs["Job A"].add_dependent_jobs("Job C", (5, 10))
            >>> model.jobs["Job A"].dependent_jobs
            [{'job_id': 1, 'interval_time_lower_bound': None, 'interval_time_upper_bound': None}, {'job_id': 2, 'interval_time_lower_bound': 5, 'interval_time_upper_bound': 10}]
        """  # noqa: E501
        self._dependent_jobs.append((job, interval_time))

    def __iter__(self):  # type: ignore
        return iter(self._tasks)

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> dict[str, Any]:
        d: dict[str, Any] = {}

        if len(self._tasks) == 0:
            raise RuntimeError(f"There is no 'tasks' in the job: {self}")

        d["tasks"] = [t._create_request_data(dtime_unit) for t in self._tasks]
        if self._no_wait is not None:
            d["no_wait"] = self._no_wait
        if len(self._dependent_jobs) != 0:
            d["dependent_jobs"] = self._dependent_jobs._create_request_data()
        return d

    def __str__(self) -> str:
        return str(
            {
                "tasks": self._tasks,
                "no_wait": self._no_wait,
                "dependent_jobs": self._dependent_jobs._create_request_data(),
            }
        )

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)


class Jobs:
    """Jobs is container of :obj:`Job`.

    Jobs is managed as dict. Key is job name and value is :obj:`Job`.

    Args:
        parent: parent object which this object belong to
    """

    def __init__(self, parent: "Model"):
        self._parent = parent
        self._jobs_set: set[Job] = set()
        self._jobs_dict: dict[str, Job] = {}

    @overload
    def __getitem__(self, key: str) -> Job: ...  # type: ignore

    @overload
    def __getitem__(self, key: tuple[str, int]) -> Task: ...  # type: ignore

    def __getitem__(self, key: Union[str, tuple[str, int]]) -> Union[Job, Task]:
        if isinstance(key, str):
            return self._jobs_dict[key]
        return self._jobs_dict[key[0]][key[1]]

    def __setitem__(self, key: str, value: Job) -> None:
        if key in self._jobs_dict:
            raise KeyError(f"Key already exists: {key}")
        if value.index >= 0:
            raise ValueError("Job is already registered")

        if value.name and value.name != key:
            warnings.warn(f"Job name will be renamed from {value.name} to {key}")

        value._name = key
        value._index = len(self._jobs_dict)
        value._parent = self
        self._jobs_set.add(value)
        self._jobs_dict[key] = value

    def add(self, job: Union[str, Job]) -> None:
        """add job

        Args:
            job : job to adding

        Raises:
            ValueError: If job has no name
        """
        if isinstance(job, str):
            job = Job(job)
        if not job.name:
            raise ValueError('job has no name, use `job["name"] = value` instead')
        self.__setitem__(job.name, job)

    def __iter__(self):  # type: ignore
        return iter(self._jobs_set)

    def __contains__(self, value: Union[str, Job]) -> bool:
        if isinstance(value, str):
            return value in self._jobs_dict
        else:
            return value in self._jobs_set

    def _create_request_data(self, dtime_unit: Optional[DatetimeUnit] = None) -> list[dict[str, Any]]:
        return [j._create_request_data(dtime_unit) for j in sorted(self._jobs_set, key=lambda j: j.index)]

    def _names(self) -> list[str]:
        return [j.name for j in sorted(self._jobs_set, key=lambda j: j.index)]

    def __str__(self) -> str:
        return str(self._jobs_dict)

    def __repr__(self) -> str:
        return str(self)

    def __reversed__(self):  # type: ignore
        return reversed(self._jobs_dict)

    def __len__(self) -> int:
        return len(self._jobs_dict)

    def keys(self):  # type: ignore
        return self._jobs_dict.keys()

    def values(self):  # type: ignore
        return self._jobs_dict.values()

    def items(self):  # type: ignore
        return self._jobs_dict.items()

    def copy(self) -> dict[str, Job]:
        return self._jobs_dict.copy()

    def get(self, key: str, default: Any = None) -> Job:
        return self._jobs_dict.get(key, default)


class Model:
    """A class managing model.

    A model defines a scheduling problem in terms of jobs, machines and resources.
    Use the solve method to solve the defined scheduling problem using the Amplify Scheduling Engine.

    Examples::

        from amplify_sched import *
        # Define Model
        model = Model()
        # Define Jobs
        model.jobs.add("Job A")
        model.jobs.add("Job B")
        model.jobs.add("Job C")
        model.jobs.add("Job D")
        # Define Machines
        model.machines.add("Machine X")
        model.machines.add("Machine Y")
        model.machines.add("Machine Z")
        # Add Task to Job
        model.jobs["Job A"].append(Task())
        model.jobs["Job A"][0].processing_times["Machine X"] = 10
        model.jobs["Job A"].append(Task())
        model.jobs["Job A"][1].processing_times["Machine Y"] = 20
        model.jobs["Job A"].append(Task())
        model.jobs["Job A"][2].processing_times["Machine Z"] = 15
        model.jobs["Job B"].append(Task())
        model.jobs["Job B"][0].processing_times["Machine Y"] = 10
        model.jobs["Job B"].append(Task())
        model.jobs["Job B"][1].processing_times["Machine Z"] = 20
        model.jobs["Job B"].append(Task())
        model.jobs["Job B"][2].processing_times["Machine X"] = 15
        model.jobs["Job C"].append(Task())
        model.jobs["Job C"][0].processing_times["Machine Z"] = 10
        model.jobs["Job C"].append(Task())
        model.jobs["Job C"][1].processing_times["Machine X"] = 20
        model.jobs["Job C"].append(Task())
        model.jobs["Job C"][2].processing_times["Machine Y"] = 15
        model.jobs["Job D"].append(Task())
        model.jobs["Job D"][0].processing_times["Machine Z"] = 10
        model.jobs["Job D"].append(Task())
        model.jobs["Job D"][1].processing_times["Machine Y"] = 20
        model.jobs["Job D"].append(Task())
        model.jobs["Job D"][2].processing_times["Machine X"] = 15
        # solve using Amplify Scheduling Engine
        token = "YOUR TOKEN"
        gantt = model.solve(token=token, timeout=1)
        # visualize solution
        gantt.timeline()

    """

    def __init__(self) -> None:
        self._machines = Machines(self)
        self._jobs = Jobs(self)
        self._resources = Resources(self)
        self._datetime_unit = DatetimeUnit()

    @property
    def machines(self) -> Machines:
        """machine list

        Machines is managed as dict. Key is machine name and value is :obj:`Machine` object.

        Examples:
            >>> model = Model()
            >>> model.machines.add("Machine A")
            >>> model.machines["Machine A"].index
            0
            >>> model.machines["Machine A"].name
            'Machine A'
            >>> model.machines["Machine A"]
            {'maintenance_times': [], 'buffer_size': None, 'setup_times': []}
        """
        return self._machines

    @property
    def jobs(self) -> Jobs:
        """job list

        Jobs is managed as dict. Key is job name and value is :obj:`Job` object.

        Examples:
            >>> model = Model()
            >>> model.jobs.add("Job A")
            >>> model.jobs["Job A"].index
            0
            >>> model.jobs["Job A"].name
            'Job A'
            >>> model.jobs["Job A"]
            {'tasks': [], 'no_wait': None, 'dependent_jobs': []}
        """
        return self._jobs

    @property
    def resources(self) -> Resources:
        """resource list

        Resources is managed as dict. Key is resource name and value is :obj:`Resource` object.

        Examples:
            >>> model = Model()
            >>> model.resources.add("Resource A")
            >>> model.resources["Resource A"].index
            0
            >>> model.resources["Resource A"].name
            'Resource A'
            >>> model.resources["Resource A"]
            {'capacity': 1}
        """
        return self._resources

    @property
    def start(self) -> Union[datetime, time]:
        """start time of scheduling problem

        Examples:
            >>> model = Model()
            >>> model.start = datetime(year=2023, month=1, day=1)
            >>> model.start
            datetime.datetime(2023, 1, 1, 0, 0)
        """
        return self._datetime_unit.start

    @start.setter
    def start(self, value: Union[datetime, time]) -> None:
        self._datetime_unit = DatetimeUnit(value, self.time_unit)
        self._datetime_unit._used = True  # FIXME

    @property
    def time_unit(self) -> timedelta:
        """time unit of scheduling problem

        Examples:
            >>> model = Model()
            >>> model.time_unit = timedelta(minutes=15)
            >>> model.time_unit
            datetime.timedelta(seconds=900)
        """
        return self._datetime_unit.unit

    @time_unit.setter
    def time_unit(self, value: timedelta) -> None:
        self._datetime_unit = DatetimeUnit(self.start, value)
        self._datetime_unit._used = True  # FIXME

    def _create_request_data(self, timeout: int) -> dict[str, Any]:
        d: dict[str, Any] = {}
        d["model"] = {}
        d["model"]["jobs"] = self._jobs._create_request_data(self._datetime_unit)
        d["model"]["machines"] = self._machines._create_request_data(self._datetime_unit)
        d["model"]["resources"] = self._resources._create_request_data()
        d["timeout"] = timeout
        return d

    def _asdict(self) -> dict[str, Any]:
        return {
            "jobs": self._jobs,
            "machines": self._machines,
            "resources": self._resources,
            "start": self.start,
            "time_unit": self.time_unit,
        }

    def __str__(self) -> str:
        return str(self._asdict())

    def __repr__(self) -> str:
        return str(self)

    def solve(
        self,
        token: str,
        timeout: int,
        base_url: str = "https://amplify.fixstars.com/api/schd",
    ) -> Schedule:
        """solve the scheduling problem

        Args:
            token: token of Amplify Scheduling Engine
            timeout: search timeout seconds of Amplify Scheduling Engine
            base_url: base url of Amplify Scheduling Engine

        Returns:
            Solution obtained from Amplify Scheduling Engine
        """
        data = self._create_request_data(timeout)
        headers = {"Authorization": f"Bearer {token}"}
        conn_timeout = 16
        read_timeout = max(600, 10 * timeout)
        max_retry = 3

        response: requests.Response | None = None
        for i in range(max_retry + 1):
            try:
                response = requests.post(
                    base_url + "/solve",
                    headers=headers,
                    json=data,
                    timeout=(conn_timeout, read_timeout),
                )
                if response.status_code != 200:
                    response.raise_for_status()
                break
            except requests.ConnectTimeout as e:
                if i < max_retry:
                    warnings.warn(str(e))
                    sleep(1)
                    continue
                raise

        assert response is not None
        self._ret = json.loads(response.text)
        if self._ret["status"] in ["OPTIMAL", "FEASIBLE"]:
            return Schedule(result=self._ret["gantt"], status=self._ret["status"], model=self)
        elif self._ret["status"] == "INFEASIBLE":
            raise RuntimeError("Infeasible")
        else:
            raise RuntimeError(self._ret)
