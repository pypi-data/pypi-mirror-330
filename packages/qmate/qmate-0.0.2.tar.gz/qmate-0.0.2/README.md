# QMate
Create asynchronous and asynchronous task queues that run on a schedule... symantically.

## Examples


### Full Example
#### Run the function ```PrintSomething``` every quarter of every minute:
```py
from qmate import Queue, Task
import time


def PrintSomething(text):
    print(text)


queue = Queue(True)
queue.schedule(
    Task(
        func=PrintSomething,
        name='Print Something',
        at=["00", "15", "30", "45"],
        args=["Working"]
    )
)

while True:
    time.sleep(0.001)
```

#### `Queue.schedule` takes a single task or a list of tasks.
```py
queue.schedule(
    [
        Task(
            func=PrintSomething,
            name='Quarterly Print',
            at=["00", "15", "30", "45"],
            args=["Working"]
        ),
        Task(
            func=PrintSomething,
            name='10PM Print',
            at=["22:00:00"],
            args=["It's 10PM."]
        )
    ]
)

``` 

## Task Time Parameters
`Every` cannot be combined with other time parameters.  `At`, `On`, and `During` can be combined.  `At` is required, unless using `Every`.


### On

Run tasks on specific days.  If empty, run everyday.
```py
on=["Sunday", "Monday"] # on Sundays and Mondays
on=["everyday"] # on everyday of the week
```
---
### At
Run tasks at certain times.
```py
at=["17:30:00"] # at 5:30 PM
at=["30:00"] # at 30 minutes past every hour
at=["15", "45"] # at a quarter past and a quarter till every hour
```
---
### During
Run tasks during specfic months.  If empty, run every month.
```py
during=["May", "July"] # during the months of may and july
```
---
### Every
Run tasks on certain intervals.  Max time: `23:59:59`
```py
every=["3:30:00"] # every 3 hours, 30 minutes
every=["03:00"] # every 3 minutes
every=["30"] # every 30 seconds
```
---
### Examples

#### Create a task to ```PrintSomething``` everyday of the week at 10AM and 10PM, during the month of September:
```py
Task(
    func=PrintSomething,
    name='Print Something',
    on=["Everyday"],
    at=["10:00:00", "22:00:00"],
    during=["September"],
    args=["Working"]
)
```

#### Create a task to ```PrintSomething``` on Saturday and Sunday ten minutes past every hour:
```py
Task(
    func=PrintSomething,
    name='Print Something',
    on=["Saturday", "Sunday"],
    at=["10:00"],
    during=["September"],
    args=["Working"]
)
```

#### Create a task to run every 10 seconds and pass it multiple arguments:
 Acceptable formats: 23:59:59, 59:59, 59
```py
Task(
    func=MultipleArgument,
    name='Run every 10 seconds',
    every=["10"],
    args=["Houston", 713]
)
```