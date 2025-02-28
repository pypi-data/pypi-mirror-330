# Copyright (c) Fixstars Amplify Corporation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime, time, timedelta

import numpy as np
import pytest

from amplify_sched import DatetimeUnit, DependentJob, Job, Machine, Model, Resource, Schedule, Task, TimeRange


def test_DatetimeUnit() -> None:
    dtu = DatetimeUnit(start=datetime(2023, 3, 1, 0, 0, 0), unit=timedelta(minutes=15))
    assert dtu.start == datetime(2023, 3, 1, 0, 0, 0)
    assert dtu.unit == timedelta(minutes=15)
    assert dtu.from_int_datetime(1) == datetime(2023, 3, 1, 0, 15, 0)
    assert dtu.to_int_timedelta(timedelta(minutes=15)) == 1
    assert dtu.to_int_timedelta(timedelta(days=1)) == 1440 // 15
    assert dtu.to_int_datetime(datetime(2023, 3, 1, 1, 0, 0)) == 4
    assert str(dtu) == "{'start': datetime.datetime(2023, 3, 1, 0, 0), 'unit': datetime.timedelta(seconds=900)}"


def test_TimeRange() -> None:
    tr = TimeRange(0, 1)
    assert tr.start == 0
    assert tr.end == 1
    assert tr._create_request_data() == (0, 1)

    dtu = DatetimeUnit(start=time(0), unit=timedelta(minutes=15))
    tr = TimeRange(time(hour=1), time(hour=2))
    assert tr.start == time(hour=1)
    assert tr.end == time(hour=2)
    assert tr._create_request_data(dtu) == (4, 8)

    dtu = DatetimeUnit(start=datetime(2023, 3, 1, 0, 0, 0), unit=timedelta(minutes=15))
    tr = TimeRange(datetime(2023, 3, 1, 0, 0, 0), datetime(2023, 3, 1, 1, 0, 0))
    assert tr.start == datetime(2023, 3, 1, 0, 0, 0)
    assert tr.end == datetime(2023, 3, 1, 1, 0, 0)
    assert tr._create_request_data(dtu) == (0, 4)


def test_Resource() -> None:
    r = Resource(name="A")
    assert r.capacity == 1
    assert r.name == "A"
    assert r.index == -1
    r.capacity = 10
    assert r.capacity == 10
    assert r._create_request_data() == {"capacity": 10}
    assert int(r) == 10
    assert str(r) == "{'capacity': 10}"


def test_Machine() -> None:
    m = Machine("A")
    assert m.name == "A"
    assert m.index == -1
    assert m.buffer_size is None
    assert len(m.setup_times) == 0
    assert len(m.maintenance_times) == 0
    m.buffer_size = 10
    assert m.buffer_size == 10
    m.add_maintenance_time(1, 2)
    assert len(m.maintenance_times) == 1
    assert m.maintenance_times == [(1, 2)]
    assert m._create_request_data() == {"maintenance_times": [(1, 2)], "buffer_size": 10}

    m = Machine("A")
    m.add_maintenance_time(datetime(2023, 3, 1, 0, 0, 0), datetime(2023, 3, 1, 1, 0, 0))
    dtu = DatetimeUnit(start=datetime(2023, 3, 1, 0, 0, 0), unit=timedelta(minutes=15))
    assert m._create_request_data(dtu) == {"maintenance_times": [(0, 4)]}
    # setup_time はmodelまたはJob,Taskを定義しないと追加できないので、Modelのテストで確認する


def test_Task() -> None:
    t = Task()
    assert t.index == -1
    assert len(t.processing_times) == 0
    assert t.required_buffer_size is None
    assert t.release_time is None
    assert t.deadline is None
    assert len(t.required_resources) == 0
    assert len(t.transportation_times) == 0

    t.required_buffer_size = 10
    assert t.required_buffer_size == 10
    t.release_time = 10
    assert t.release_time == 10
    t.deadline = 10
    assert t.deadline == 10

    # required_resources, transportation_times , processing_timeはmodelを定義しないと追加できないので、Modelのテストで確認する


def test_Job() -> None:
    j = Job("A")
    assert j.index == -1
    assert j.name == "A"
    assert j.no_wait is None
    assert len(j.dependent_jobs) == 0
    assert j.num_process == 0
    j.no_wait = True
    assert j.no_wait is True

    # add_dependent_jobs、taskはmodelを定義しないと追加できないので、Modelのテストで確認する


def test_Model() -> None:
    model = Model()
    assert len(model.machines) == 0
    assert len(model.jobs) == 0
    assert len(model.resources) == 0
    model.start = datetime(2023, 3, 1, 0, 0, 0)
    model.time_unit = timedelta(minutes=15)
    model.jobs.add("J1")
    model.jobs.add("J2")
    model.jobs.add("J3")
    model.machines.add("M1")
    model.machines.add("M2")
    model.resources.add("R1")
    model.resources["R1"].capacity = 2
    t = Task()
    model.jobs["J1"].append(t)
    assert model.jobs["J1"].num_process == 1
    t.processing_times["M1"] = 10
    t.processing_times["M2"] = 5
    t.transportation_times.append((10, "M2", "M1"))
    model.jobs["J1"].task(0).add_transportation_time(10, "M1", "M2")
    model.jobs["J1"].task(0).add_required_resource(model.resources["R1"])
    model.jobs["J1"].task(0).add_required_resource([model.resources["R1"], model.machines["M1"]])
    model.jobs["J1"].task(0).add_required_resource(["R1", model.machines["M2"]])
    model.jobs["J1"].task(0).add_required_resource([model.resources["R1"], "M1"])

    t = Task()
    model.jobs["J2"].append(t)

    t.processing_times["M2"] = 5
    model.jobs["J2"].task(0).processing_times["M2"] = 5
    model.jobs["J2"].task(0).required_resources.append("R1")
    model.jobs["J2"].task(0).add_required_resource("R1")
    model.jobs["J2"].dependent_jobs.append("J3")
    model.jobs["J2"].add_dependent_jobs("J1")
    model.jobs["J2"].no_wait = True
    model.jobs["J2"].task(0).required_buffer_size = 10
    model.jobs["J2"].task(0).release_time = 10
    model.jobs["J2"].task(0).deadline = 20
    t = Task()
    model.jobs["J3"].append(t)
    model.jobs["J3"].task(0).required_resources.append(["R1", "M1"])
    model.jobs["J3"].task(0).add_required_resource(["R1", "M2"])
    t.processing_times["M2"] = 5
    model.machines["M1"].add_setup_time(10, "J1", "J2")
    data = model._create_request_data(10)

    dependent_job = model.jobs["J2"].dependent_jobs[0]
    expected_dj = DependentJob(model.jobs["J2"].dependent_jobs, job=model.jobs["J3"])
    assert dependent_job._job == expected_dj._job
    assert dependent_job._interval_time_lower_bound == expected_dj._interval_time_lower_bound
    assert dependent_job._interval_time_upper_bound == expected_dj._interval_time_upper_bound

    dependent_job = model.jobs["J2"].dependent_jobs[1]
    expected_dj = DependentJob(model.jobs["J2"].dependent_jobs, job=model.jobs["J1"])
    assert dependent_job._job == expected_dj._job
    assert dependent_job._interval_time_lower_bound == expected_dj._interval_time_lower_bound
    assert dependent_job._interval_time_upper_bound == expected_dj._interval_time_upper_bound

    assert data == {
        "model": {
            "jobs": [
                {
                    "tasks": [
                        {
                            "processing_times": [[10, 0], [5, 1]],
                            "transportation_times": [[10, 1, 0], [10, 0, 1]],
                            "required_resources": [0, [0, 0], [0, 1], [0, 0]],
                        }
                    ]
                },
                {
                    "tasks": [
                        {
                            "processing_times": [[5, 1]],
                            "required_resources": [0, 0],
                            "required_buffer_size": 10,
                            "release_time": 10,
                            "deadline": 20,
                        }
                    ],
                    "dependent_jobs": [{"job_id": 2}, {"job_id": 0}],
                    "no_wait": True,
                },
                {
                    "tasks": [
                        {
                            "processing_times": [[5, 1]],
                            "required_resources": [[0, 0], [0, 1]],
                        }
                    ],
                },
            ],
            "machines": [{"setup_times": [[10, [0], [1]]]}, {}],
            "resources": [2],
        },
        "timeout": 10,
    }


def test_Model_DependentJobs() -> None:
    model = Model()
    model.jobs.add("J1")
    model.jobs.add("J2")
    model.jobs.add("J3")
    model.machines.add("M1")
    model.machines.add("M2")
    t = Task()
    model.jobs["J1"].append(t)
    t.processing_times["M1"] = 10
    t.processing_times["M2"] = 5
    t = Task()
    model.jobs["J2"].append(t)
    t.processing_times["M2"] = 5
    model.jobs["J2"].add_dependent_jobs("J1", 1)
    model.jobs["J2"].dependent_jobs.append(("J3", (1, 2)))
    t = Task()
    model.jobs["J3"].append(t)
    t.processing_times["M2"] = 5
    data = model._create_request_data(10)

    dependent_job = model.jobs["J2"].dependent_jobs[0]
    expected_dj = DependentJob(model.jobs["J2"].dependent_jobs, job="J1", interval_times=1)
    assert dependent_job._job == expected_dj._job
    assert dependent_job._interval_time_lower_bound == expected_dj._interval_time_lower_bound
    assert dependent_job._interval_time_upper_bound == expected_dj._interval_time_upper_bound

    dependent_job = model.jobs["J2"].dependent_jobs[1]
    expected_dj = DependentJob(model.jobs["J2"].dependent_jobs, job="J3", interval_times=(1, 2))
    assert dependent_job._job == expected_dj._job
    assert dependent_job._interval_time_lower_bound == expected_dj._interval_time_lower_bound
    assert dependent_job._interval_time_upper_bound == expected_dj._interval_time_upper_bound

    assert data == {
        "model": {
            "jobs": [
                {"tasks": [{"processing_times": [[10, 0], [5, 1]]}]},
                {
                    "tasks": [{"processing_times": [[5, 1]]}],
                    "dependent_jobs": [
                        {
                            "job_id": 0,
                            "interval_time_lower_bound": 1,
                            "interval_time_upper_bound": 1,
                        },
                        {
                            "job_id": 2,
                            "interval_time_lower_bound": 1,
                            "interval_time_upper_bound": 2,
                        },
                    ],
                },
                {"tasks": [{"processing_times": [[5, 1]]}]},
            ],
            "machines": [{}, {}],
            "resources": [],
        },
        "timeout": 10,
    }

    model = Model()
    model.jobs.add("J1")
    model.jobs.add("J2")
    model.jobs.add("J3")
    model.machines.add("M1")
    model.machines.add("M2")
    t = Task()
    model.jobs["J1"].append(t)
    t.processing_times["M1"] = 10
    t.processing_times["M2"] = 5
    t = Task()
    model.jobs["J2"].append(t)
    t.processing_times["M2"] = 5
    model.jobs["J2"].add_dependent_jobs("J1", (1, None))
    model.jobs["J2"].dependent_jobs.append(("J3", (None, 2)))
    t = Task()
    model.jobs["J3"].append(t)
    t.processing_times["M2"] = 5

    model.jobs["J2"].dependent_jobs[0] = ("J3", (2, None))
    model.jobs["J2"].dependent_jobs[1] = ("J1", (None, 4))

    data = model._create_request_data(10)
    assert data == {
        "model": {
            "jobs": [
                {"tasks": [{"processing_times": [[10, 0], [5, 1]]}]},
                {
                    "tasks": [{"processing_times": [[5, 1]]}],
                    "dependent_jobs": [
                        {
                            "job_id": 2,
                            "interval_time_lower_bound": 2,
                        },
                        {
                            "job_id": 0,
                            "interval_time_upper_bound": 4,
                        },
                    ],
                },
                {"tasks": [{"processing_times": [[5, 1]]}]},
            ],
            "machines": [{}, {}],
            "resources": [],
        },
        "timeout": 10,
    }

    with pytest.raises(AttributeError) as _:
        model = Model()
        model.jobs.add("J1")
        model.jobs.add("J2")
        t = Task()
        model.jobs["J1"].append(t)
        t = Task()
        model.jobs["J2"].append(t)
        model.jobs["J2"].add_dependent_jobs("J1", -1)

    with pytest.raises(AttributeError) as _:
        model = Model()
        model.jobs.add("J1")
        model.jobs.add("J2")
        t = Task()
        model.jobs["J1"].append(t)
        t = Task()
        model.jobs["J2"].append(t)
        model.jobs["J2"].add_dependent_jobs("J1", (-1, None))

    with pytest.raises(AttributeError) as _:
        model = Model()
        model.jobs.add("J1")
        model.jobs.add("J2")
        t = Task()
        model.jobs["J1"].append(t)
        t = Task()
        model.jobs["J2"].append(t)
        model.jobs["J2"].add_dependent_jobs("J1", (None, -2))


def test_Schedule() -> None:
    model = Model()
    assert len(model.machines) == 0
    assert len(model.jobs) == 0
    assert len(model.resources) == 0
    model.start = datetime(2023, 3, 1, 0, 0, 0)
    model.time_unit = timedelta(minutes=15)
    model.jobs.add(Job("J1"))
    model.jobs.add(Job("J2"))
    model.machines.add(Machine("M1"))
    model.machines.add(Machine("M2"))
    model.resources.add(Resource("R1"))
    model.resources["R1"].capacity = 2
    model.jobs["J1"].append(Task())
    model.jobs["J1"].append(Task())
    model.jobs["J2"].append(Task())
    model.jobs["J2"].append(Task())

    model.jobs["J1"].task(0).processing_times["M1"] = 10
    model.jobs["J1"].task(0).processing_times["M2"] = 5
    model.jobs["J1"].task(0).add_transportation_time(10, "M1", "M2")
    model.jobs["J1"].task(1).processing_times["M1"] = 10
    model.jobs["J1"].task(1).processing_times["M2"] = 5
    model.jobs["J2"].task(0).processing_times["M2"] = 10
    model.jobs["J2"].task(0).add_required_resource("R1")
    model.jobs["J2"].add_dependent_jobs("J1")
    model.jobs["J2"].no_wait = True
    model.jobs["J2"].task(1).processing_times["M1"] = 5

    model.machines["M1"].add_setup_time(10, "J1", "J2")
    gantt_dict = [
        {"job": 0, "process": 0, "machine": 0, "start": 0, "end": 10},
        {"job": 0, "process": 1, "machine": 1, "start": 20, "end": 25},
        {"job": 1, "process": 0, "machine": 1, "start": 10, "end": 20},
        {"job": 1, "process": 1, "machine": 0, "start": 20, "end": 25},
    ]
    sched = Schedule(gantt_dict, "OPTIMAL", model)
    assert sched.status == "OPTIMAL"
    assert sorted(sched.table.columns.tolist()) == sorted(["Job", "Machine", "Finish", "Start", "Process"])
    assert list(sched.table["Job"].values) == ["J1", "J1", "J2", "J2"]
    assert list(sched.table["Machine"].values) == ["M1", "M2", "M2", "M1"]
    assert list(sched.table["Process"].values) == [0, 1, 0, 1]

    assert list(sched.table["Start"].values) == [
        np.datetime64(datetime(2023, 3, 1, 0, 0, 0)),
        np.datetime64(datetime(2023, 3, 1, 5, 00, 0)),
        np.datetime64(datetime(2023, 3, 1, 2, 30, 0)),
        np.datetime64(datetime(2023, 3, 1, 5, 00, 0)),
    ]
    assert list(sched.table["Finish"].values) == [
        np.datetime64(datetime(2023, 3, 1, 2, 30, 0)),
        np.datetime64(datetime(2023, 3, 1, 6, 15, 0)),
        np.datetime64(datetime(2023, 3, 1, 5, 00, 0)),
        np.datetime64(datetime(2023, 3, 1, 6, 15, 0)),
    ]
    for machine_view in [False, True]:
        for separeted_by_task in [False, True]:
            sched.timeline(machine_view=machine_view, separated_by_task=separeted_by_task)
    for avail_view in [False, True]:
        sched.resource(avail_view=avail_view)

    model = Model()
    model.jobs.add(Job("J1"))
    model.jobs.add(Job("J2"))
    model.machines.add(Machine("M1"))
    model.machines.add(Machine("M2"))
    model.resources.add(Resource("R1"))
    model.resources["R1"].capacity = 2
    model.jobs["J1"].append(Task())
    model.jobs["J1"].append(Task())
    model.jobs["J2"].append(Task())
    model.jobs["J2"].append(Task())

    model.jobs["J1"].task(0).processing_times["M1"] = 10
    model.jobs["J1"].task(0).processing_times["M2"] = 5
    model.jobs["J1"].task(0).add_transportation_time(10, "M1", "M2")
    model.jobs["J1"].task(1).processing_times["M1"] = 10
    model.jobs["J1"].task(1).processing_times["M2"] = 5
    model.jobs["J2"].task(0).processing_times["M2"] = 10
    model.jobs["J2"].task(0).add_required_resource("R1")
    model.jobs["J2"].add_dependent_jobs("J1")
    model.jobs["J2"].no_wait = True
    model.jobs["J2"].task(1).processing_times["M1"] = 5

    model.machines["M1"].add_setup_time(10, "J1", "J2")
    gantt_dict = [
        {"job": 0, "process": 0, "machine": 0, "start": 0, "end": 10},
        {"job": 0, "process": 1, "machine": 1, "start": 20, "end": 25},
        {"job": 1, "process": 0, "machine": 1, "start": 10, "end": 20},
        {"job": 1, "process": 1, "machine": 0, "start": 20, "end": 25},
    ]
    sched = Schedule(gantt_dict, "OPTIMAL", model)
    for machine_view in [False, True]:
        for separeted_by_task in [False, True]:
            sched.timeline(machine_view=machine_view, separated_by_task=separeted_by_task)
    for avail_view in [False, True]:
        sched.resource(avail_view=avail_view)

    model = Model()
    model.jobs.add(Job("J1"))
    model.jobs.add(Job("J2"))
    model.machines.add(Machine("M1"))
    model.machines.add(Machine("M2"))
    model.resources.add(Resource("R1"))
    model.resources["R1"].capacity = 2
    model.jobs["J1"].append(Task())
    model.jobs["J1"].append(Task())
    model.jobs["J2"].append(Task())
    model.jobs["J2"].append(Task())

    model.jobs["J1"].task(0).processing_times["M1"] = 10
    model.jobs["J1"].task(0).processing_times["M2"] = 5
    model.jobs["J1"].task(0).add_transportation_time(10, "M1", "M2")
    model.jobs["J1"].task(1).processing_times["M1"] = 10
    model.jobs["J1"].task(1).processing_times["M2"] = 5
    model.jobs["J2"].task(0).processing_times["M2"] = 10
    model.jobs["J2"].task(0).add_required_resource("R1")
    model.jobs["J2"].add_dependent_jobs("J1")
    model.jobs["J2"].no_wait = True
    model.jobs["J2"].task(1).processing_times["M1"] = 5

    model.machines["M1"].add_setup_time(10, "J1", "J2")
    gantt_dict = [
        {"job": 0, "process": 0, "machine": 0, "start": 0, "end": 10},
        {"job": 0, "process": 1, "machine": 1, "start": 20, "end": 25},
        {"job": 1, "process": 0, "machine": 1, "start": 10, "end": 20},
        {"job": 1, "process": 1, "machine": 0, "start": 20, "end": 25},
    ]
    sched = Schedule(gantt_dict, "OPTIMAL", model)
    sched.timeline()
    sched.resource()


def test_shorthand_notation() -> None:
    model = Model()
    model.jobs.add("J1")
    model.jobs.add("J2")
    model.machines.add("M1")
    model.machines.add("M2")
    model.jobs["J1"].append()
    model.jobs["J2"].append()
    model.jobs["J1"].task(0).processing_times["M1"] = 10
    model.jobs["J1"].task(0).processing_times["M2"] = 10
    model.jobs["J1"].task(0).transportation_times.append(10)
    model.jobs["J1"].task(0).transportation_times.append((5, "M1"))
    assert model.jobs["J1"].task(0).transportation_times._create_request_data() == [
        [10],
        [5, model.machines["M1"].index],
    ]
    model.machines["M1"].setup_times.append((10))
    model.machines["M1"].setup_times.append((5, "J1"))
    model.machines["M1"].setup_times.append((5, model.jobs["J1"].task(0)))
    model.machines["M1"].setup_times.append((4, "J1", "J2"))
    model.machines["M1"].setup_times.append((3, model.jobs["J1"].task(0), "J2"))
    model.machines["M1"].setup_times.append((2, "J1", model.jobs["J2"].task(0)))
    model.machines["M1"].setup_times.append((1, model.jobs["J1"].task(0), model.jobs["J2"].task(0)))
    assert model.machines["M1"].setup_times._create_request_data() == [
        [10],
        [5, [model.jobs["J1"].index]],
        [5, [model.jobs["J1"].index, 0]],
        [4, [model.jobs["J1"].index], [model.jobs["J2"].index]],
        [3, [model.jobs["J1"].index, 0], [model.jobs["J2"].index]],
        [2, [model.jobs["J1"].index], [model.jobs["J2"].index, 0]],
        [1, [model.jobs["J1"].index, 0], [model.jobs["J2"].index, 0]],
    ]
