import asyncio
import inspect
import re
import threading
from datetime import datetime


class Queue(object):

    tasks = []

    def __init__(self, printTime=False, printTask=False):
        self._loop = _Loop(onUpdate=self.onUpdate)
        self._printTime = printTime
        self._printTask = printTask

    def schedule(self, tasks):
        if isinstance(tasks, list):
            for t in tasks:
                self.tasks.append(t)
            return

        self.tasks.append(tasks)
        return self.tasks

    def listTasks(self):
        for task in self.tasks:
            print(
                f"Task: {task.name}"
                f"Function: {task.func.__name__}"
                f"Args: {task.args}"
            )

        return self.tasks

    def onUpdate(self, **kwargs):
        current_time = kwargs['current_time']
        current_month = kwargs['current_month']
        current_day = kwargs['current_day']
        # current_hour = kwargs['current_hour']
        current_minute = kwargs['current_minute']
        current_second = kwargs['current_second']

        if self._printTime:
            print(f"Current Time: {current_time}", end="\r")

        for task in self.tasks:

            trigger = False

            for time in task.times:
                if (current_day in time['on'] and
                        current_month in time['during']):

                    for t in time['at']:
                        parts = t.split(':')
                        if len(parts) == 1:
                            if current_second in time['at']:
                                trigger = True

                        elif len(parts) == 2:
                            if (current_second == parts[1] and
                                    current_minute == parts[0]):
                                trigger = True

                        elif len(parts) == 3:
                            if current_time in time['at']:
                                trigger = True

            if trigger:
                if inspect.iscoroutinefunction(task.func):
                    asyncio.run(task.func(*task.args))
                else:
                    task.func(*task.args)

                if self._printTask:
                    print(f"Task {task.name} ran at {datetime.now()}")


class Task(object):
    def __init__(self, name, func, at=[], on=[], during=[], every=[], args=[]):

        if len(every) > 0 and (len(on) > 0 or len(at) > 0 or len(during) > 0):
            raise Exception(
                "'on', 'at', and 'during' can't be used with 'every'"
            )

        if len(every) == 0 and len(at) == 0:
            raise Exception("'at' is required, unless using 'every'")

        if (not all(isinstance(item, str) for item in on) or
                not all(isinstance(item, str) for item in at) or
                not all(isinstance(item, str) for item in during) or
                not all(isinstance(item, str) for item in every)):

            raise TypeError(
                "'on', 'at', 'during', and 'every' be string lists."
            )

        on = [x.lower() for x in on]
        during = [x.lower() for x in during]
        every = [x.lower() for x in every]

        if len(every) == 0:
            if "everyday" in on or len(on) == 0:
                on = _days

            if len(during) == 0:
                during = _months

        self.name = name
        self.func = func
        self.args = args
        self.times = [
            {
                'during': during,
                'on': on,
                'at': at
            }
        ]

        for val in every:
            expression = "^([0-2][0-3]:)?([0-5][0-9]:)?[0-5][0-9]$"
            if not re.search(expression, val):
                raise Exception("'every' value malformed.  Max time: 23:59:59")

            multiplier = self._transformEvery(val)
            self._setupEveryThread(multiplier)

    def _transformEvery(self, value):
        parts = value.split(":")
        multiplier = 1

        parts = [int(x) for x in parts]

        if len(parts) == 1:
            multiplier *= parts[0]

        elif len(parts) == 2:
            multiplier *= parts[1] + (60 * parts[0])

        elif len(parts) == 3:
            multiplier *= parts[2] + (60 * parts[1]) + (3600 * parts[0])

        if multiplier < 1:
            raise Exception("Minimum 'every' time is 1 second")

        return multiplier

    def _setupEveryThread(self, multiplier):

        def loop(*args):
            if inspect.iscoroutinefunction(self.func):
                asyncio.run(self.func(*args))
            else:
                self.func(*args)
            run()

        def run():
            t = threading.Timer(multiplier, loop, self.args)
            t.daemon = True
            t.start()

        run()


_days = [
    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
    'saturday'
]
_months = [
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december'
]


class _Loop(object):

    def __init__(self, onUpdate):
        self.onUpdate = onUpdate
        self.STOPPED = False
        self.run()

    def timeKeeper(self):
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        current_month = now.strftime('%B').lower()
        current_day = now.strftime("%A").lower()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        current_second = now.strftime("%S")

        self.onUpdate(
            current_time=current_time,
            current_month=current_month,
            current_day=current_day,
            current_hour=current_hour,
            current_minute=current_minute,
            current_second=current_second
        )

        if not self.STOPPED:
            self.run()

    def run(self):
        self.timer = threading.Timer(1.0, self.timeKeeper)
        self.timer.daemon = True
        self.timer.start()
