"""module to aftomatizate smta calculation"""

import math

def get_stage_monthes(monthes: tuple ) -> dict:
    """will return a dict with monthes for a stage"""
    stage_monthes = {}
    stages = {month[2] for month in monthes}
    for stage in stages:
        month_list = [month_num for month_num, month_data in enumerate(monthes, 1) if month_data[2] == stage]
        stage_monthes[stage] = month_list
    return stage_monthes

def get_monthes_hour(month_list: set, monthes: tuple) -> int:
    """Will return a sum of working hours in the given monthes"""
    monthes = dict(enumerate(monthes, 1))
    hours = 0
    for month in month_list:
        hours += monthes[month][1]
    return hours

def get_event_worker_list(events: tuple, workers: tuple) -> list:
    """will return a table of event-worker one-to-one connection"""
    event_worker_list = []
    for event in events:
        for worker in event[1]:
            event_worker_list.append((event[0], workers[worker-1][0]))
    return event_worker_list


def get_workers_time_load(workers: tuple, monthes: tuple) -> list:
    """Will return a lis of workers with hour that worker will spend on project"""
    workers_time_load = {}
    if isinstance(workers[0], str):
        workers_list =  {1: workers}
    else:
        workers_list = dict(enumerate(workers, 1))
    for worker_num, worker_data in workers_list.items():
        single_worker_time_load = []
        for month_num, busy_on_project in enumerate([float(load.replace(',','.')) for load in worker_data[2].split(';')]):
            try:
                single_worker_time_load.append(math.ceil(monthes[month_num][1]*busy_on_project))
            except IndexError:
                print(f"Worker {worker_data[0]} have more month of load monthes in project")
        workers_time_load[worker_num] = single_worker_time_load
    return workers_time_load


def get_worker_task_load(events: tuple, workers: tuple) -> dict:
    """Will return a dict with tasks for each worker in list"""
    workers_load = {}
    for worker_num in dict(enumerate(workers, 1)):
        worker_events = []
        for event_num, event_data in enumerate(events, 1):
            if worker_num in event_data[1]:
                worker_events.append(event_num)
        workers_load[worker_num] = [worker_events]
    return workers_load


def get_events_for_stage(monthes: tuple, events: tuple) -> dict:
    """Will split events on stages and reuturn a dict stage: events"""
    stages = get_stage_monthes(monthes)
    events_for_stage = {}
    for stage, stage_monthes in stages.items():
        event_list = []
        for event_num, event_data in enumerate(events, 1):
            for month in stage_monthes:
                if month in event_data[2]:
                    event_list.append(event_num)
        events_for_stage[stage] = set(event_list)
    return events_for_stage

def get_event_list_monthes(event_list: list, events: tuple, monthes: tuple) -> dict:
    """
        Will return a dict with list of month_numbers and working hours \
        goted from month_hours in month description for each event in list
    """
    events = {event[0]: event[1] for event in enumerate(events, 1)}
    event_monthes = {}
    for event_number in event_list:
        event_monthes[event_number] = {'monthes': events[event_number][2], 'hours': 0}
    enum_monthes = dict(enumerate(monthes, 1))
    for event_number, month_data in event_monthes.items():
        for month in month_data['monthes']:
            month_data['hours'] += enum_monthes[month][1]
    return event_monthes


def get_workers_stage_time(workers: tuple, monthes: tuple) -> dict:
    """Will return a dict with working hour for each worker for each stage"""
    workers_monthes_busy = get_workers_time_load(workers, monthes)
    stages = get_stage_monthes(monthes)
    result = {}
    for stage_num, stage_monthes in stages.items():
        result[stage_num] = {}
        for worker_num, worker_busy in workers_monthes_busy.items():
            result[stage_num][worker_num] = 0
            for month in stage_monthes:
                result[stage_num][worker_num] += worker_busy[month-1]
    return result


def get_workers_stage_load(workers: tuple, events: tuple, monthes: tuple) -> dict:
    """Will return a lis of events and working\
    hours according to worker usage procent for each worker splited my stages
    """
    workers_stage_load = {}
    stages_events = get_events_for_stage(monthes, events)
    workers_events = get_worker_task_load(events, workers)
    workers_stage_time = get_workers_stage_time(workers, monthes)
    for stage_num, stage_events in stages_events.items():
        workers_stage_load[stage_num] = {}
        for worker_num, worker_events in workers_events.items():
            event_list = [event for event in worker_events[0] if event in stage_events]
            work_hours = workers_stage_time[stage_num][worker_num]
            try:
                avarage_time = work_hours / len(event_list)
            except ZeroDivisionError:
                avarage_time = 0
            stage_data = {
                "events": event_list,
                "work_hour": work_hours,
                "avarage_time": avarage_time,
            }
            workers_stage_load[stage_num][workers[worker_num-1][0]] = stage_data
    return workers_stage_load
