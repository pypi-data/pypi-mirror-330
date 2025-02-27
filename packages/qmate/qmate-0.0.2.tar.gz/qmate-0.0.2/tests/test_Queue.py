from qmate import Queue, Task
import unittest
from unittest import mock


class TestQueue(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestQueue, self).__init__(*args, **kwargs)

        self.dummy = mock.MagicMock()
        self.dummy.__name__ = "MagicMock"

        self.queue = Queue()
        self.task = Task(
            func=self.dummy,
            name='Do Later',
            at=["00", "30"],
            args=[3, "Doing Later"]
        )

    def test_task(self):
        self.queue.schedule(self.task)
        self.assertIn(self.task, self.queue.tasks)

    def test_everyday_task(self):
        task = Task(
            func=self.dummy,
            name='Do Later',
            at=["00", "30"],
            on=["everyday"],
            args=[3, "Doing Later"]
        )
        self.queue.schedule(task)
        days = [
            'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday'
        ]
        self.assertEqual(task.times[0]['on'], days)

    def test_during_task(self):
        self.queue.schedule(self.task)
        months = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        self.assertEqual(self.task.times[0]['during'], months)

    def test_schedule(self):
        self.queue.schedule(self.task)
        self.assertIsInstance(self.queue.schedule(self.task), list)

    def test_listTasks(self):
        self.queue.schedule(self.task)
        self.assertIsInstance(self.queue.listTasks(), list)

    def test_transformEvery(self):

        seconds = self.task._transformEvery("02:00:00")
        self.assertEqual(seconds, 7200)

        seconds = self.task._transformEvery("20:00")
        self.assertEqual(seconds, 1200)

        seconds = self.task._transformEvery("20")
        self.assertEqual(seconds, 20)


if __name__ == '__main__':
    unittest.main()
