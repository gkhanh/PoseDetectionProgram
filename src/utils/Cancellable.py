class Cancellable:
    def __init__(self, action):
        self._cancelled = False
        self._action = action

    def cancel(self):
        if not self._cancelled:
            self._action()
        self._cancelled = True

    def isCancelled(self):
        return self._cancelled
