import unittest
from unittest.mock import patch
from scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    """ Тестирование методов класса Scheduler
        python -m unittest test.py
    """

    @patch('requests.get')
    def setUp(self, mock_get):

        self.mock_data = {
  "days": [
    {
      "id": 1,
      "date": "2025-02-15",
      "start": "09:00",
      "end": "21:00"
    },
    {
      "id": 2,
      "date": "2025-02-16",
      "start": "08:00",
      "end": "22:00"
    },
    {
      "id": 3,
      "date": "2025-02-17",
      "start": "09:00",
      "end": "18:00"
    },
    {
      "id": 4,
      "date": "2025-02-18",
      "start": "10:00",
      "end": "18:00"
    },
    {
      "id": 5,
      "date": "2025-02-19",
      "start": "09:00",
      "end": "18:00"
    }
  ],
  "timeslots": [
    {
      "id": 1,
      "day_id": 1,
      "start": "17:30",
      "end": "20:00"
    },
    {
      "id": 2,
      "day_id": 1,
      "start": "09:00",
      "end": "12:00"
    },
    {
      "id": 3,
      "day_id": 2,
      "start": "14:30",
      "end": "18:00"
    },
    {
      "id": 4,
      "day_id": 2,
      "start": "09:30",
      "end": "11:00"
    },
    {
      "id": 5,
      "day_id": 3,
      "start": "12:30",
      "end": "18:00"
    },
    {
      "id": 6,
      "day_id": 4,
      "start": "10:00",
      "end": "11:00"
    },
    {
      "id": 7,
      "day_id": 4,
      "start": "11:30",
      "end": "14:00"
    },
    {
      "id": 8,
      "day_id": 4,
      "start": "14:00",
      "end": "16:00"
    },
    {
      "id": 9,
      "day_id": 4,
      "start": "17:00",
      "end": "18:00"
    }
  ]
}

        self.scheduler = Scheduler("https://ofc-test-01.tspb.su/test-task/")

    def test_get_json(self):
        """Сверяет mock_data и json из ендпоинта"""
        data = self.scheduler.get_json()
        self.assertEqual(data, self.mock_data)

    def test_get_busy_slots(self):
        """Сравнивает занятые слоты"""
        busy_slots = self.scheduler.get_busy_slots("2025-02-18")
        expected_slots = [('10:00', '11:00'), ('11:30', '14:00'), ('14:00', '16:00'), ('17:00', '18:00')]
        self.assertEqual(busy_slots, expected_slots)

    def test_get_busy_slots_invalid_date(self):
        with self.assertRaises(ValueError):
            self.scheduler.get_busy_slots("2025-01-15")

    def test_get_free_slots(self):
        """Сравнивает свободные слоты"""
        free_slots = self.scheduler.get_free_slots("2025-02-18")
        expected_slots = [('11:00', '11:30'), ('16:00', '17:00')]
        self.assertEqual(free_slots, expected_slots)

    def test_is_available_true(self):
        """Сравнивает доступность промежутка"""
        self.assertTrue(self.scheduler.is_available("2025-02-18", "16:00", "16:48"))

    def test_is_available_false(self):
        self.assertFalse(self.scheduler.is_available("2025-02-18", "11:30", "12:00"))

    def test_is_available_invalid_order(self):
        with self.assertRaises(ValueError):
            self.scheduler.is_available("2025-02-18", "11:00", "10:00")

    def test_find_slot_for_duration_60(self):
        """Находит первое свободное время для заявки (60 минут) в графике"""
        result = self.scheduler.find_slot_for_duration(60)
        self.assertNotEqual(result, False)
        date, start, end = result
        self.assertEqual(date, "2025-02-15")
        self.assertEqual(start, "20:00")
        self.assertEqual(end, "21:00")

    def test_find_slot_for_duration_90(self):
        """Находит первое свободное время для заявки(90 минут) в графике"""
        result = self.scheduler.find_slot_for_duration(90)
        self.assertNotEqual(result, False)
        date, start, end = result
        self.assertEqual(date, "2025-02-16")
        self.assertEqual(start, "08:00")
        self.assertEqual(end, "09:30")


if __name__ == '__main__':
    unittest.main()