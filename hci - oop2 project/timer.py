class Timer:
    def __init__(self, duration):
        self._duration = duration
        self._remainingTime = duration

    def tick(self):  # decrements the time
        if self._remainingTime > 0:
            self._remainingTime -= 1

    def reset(self):  # reset the timer
        self._remainingTime = self._duration

    def isDone(self):  # to check if the timer is done
        return self._remainingTime == 0

    def getRemainingTime(self):  # getter function of remaining time
        return self._remainingTime


class PomodoroTimer(Timer):
    def __init__(self):
        super().__init__(1500 * 10)  # 25 MINS


class ShortBreakTimer(Timer):
    def __init__(self):
        super().__init__(300 * 10)  # 5 MINS


class LongBreakTimer(Timer):
    def __init__(self):
        super().__init__(900 * 10)  # 15 MINS


class CustomTimer(Timer):
    def __init__(self, customDuration):
        super().__init__(customDuration * 10)  # custom duration
