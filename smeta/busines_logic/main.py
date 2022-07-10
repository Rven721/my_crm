"""Main file to create a stage workers load"""

import sys
from openpyxl import Workbook
from . import logic as l
from . import data_extractor as de


def count_stage_load(file_name: str) -> None:
    """Will return an xlsx file with descripton of workers stage load\
       based on data from given file
    """
    events = de.get_events(file_name)
    workers = de.get_workers(file_name)
    monthes = de.get_monthes(file_name)
    stages = l.get_workers_stage_load(workers, events, monthes)
    work_book = Workbook()
    work_sheet = work_book.active
    work_sheet.append(['Worker', 'Events', 'Hours', 'Avarage_time'])
    for stage in stages.values():
        work_sheet.append(['New Stage'])
        for worker, data in stage.items():
            events = ','.join([str(i) for i in data['events']])
            hours = data['work_hour']
            avarage_time = data['avarage_time']
            work_sheet_data = [worker, events, hours, avarage_time]
            work_sheet.append(work_sheet_data)
    return work_book

if __name__ == '__main__':
    base_data = sys.argv[1]
    count_stage_load(base_data)
