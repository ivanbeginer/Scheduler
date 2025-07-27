import requests

class Scheduler:
    def __init__(self,url:str):
        self.url = url

    def get_json(self):
        res = requests.get(self.url).json()
        return res
    def get_busy_slots(self, date:str):
        data = self.get_json()
        busy_slots = []
        day = next((day for day in data['days'] if day['date']==date),None)
        if not day:
            raise ValueError('Такой день отсутсвует')

        for timeslot in data['timeslots']:
            if timeslot['day_id']==day['id']:
                busy_slots.append((timeslot['start'],timeslot['end']))
        busy_slots.sort(key=lambda x: x[0])
        return busy_slots

    def get_free_slots(self, date: str):

        data = self.get_json()
        day = next((d for d in data['days'] if d['date'] == date), None)
        if not day:
            raise ValueError('Такой день отсутсвует')
        work_start = day['start']
        work_end = day['end']
        busy_slots = self.get_busy_slots(date)
        free_slots = []
        last_work_end = work_start

        for slot_start, slot_end in busy_slots:
            if last_work_end < slot_start:
                free_slots.append((last_work_end, slot_start))
            last_work_end = max(last_work_end, slot_end)

        if last_work_end < work_end:
            free_slots.append((last_work_end, work_end))

        return free_slots

    def is_available(self,date,slot_start,slot_end):
        if slot_start < slot_end:
            free_slots = self.get_free_slots(date)
            for start,end in free_slots:
                if slot_start >= start and slot_end <= end:
                    return True
            return False
        raise ValueError('Введите значение по возрастанию')

    def _time_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def _minutes_to_time(self, minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"
    def find_slot_for_duration(self, duration_minutes=60|90):
        data = self.get_json()
        days = data['days']


        for day in days:
            free_slots = self.get_free_slots(day['date'])
            for start_slot, end_slot in free_slots:
                start = self._time_to_minutes(start_slot)
                end = self._time_to_minutes(end_slot)
                if end - start == duration_minutes:
                    return day['date'], start_slot, end_slot


        for day in days:
            free_slots = self.get_free_slots(day['date'])
            for start_slot, end_slot in free_slots:
                start = self._time_to_minutes(start_slot)
                end = self._time_to_minutes(end_slot)
                if end - start > duration_minutes:
                    new_end = start + duration_minutes
                    new_end_slot = self._minutes_to_time(new_end)
                    return day['date'], start_slot, new_end_slot

        return False
s = Scheduler('https://ofc-test-01.tspb.su/test-task/')
print(s.get_busy_slots('2025-02-15'))
print(s.get_free_slots('2025-02-15'))
print(s.is_available('2025-02-15','11:30','12:30'))
print((s.find_slot_for_duration(duration_minutes=90)))