import multiprocessing
import threading
import weakref

from multilock import MultiRLock
from pebble import ProcessPool, ThreadPool


__all__ = (
    'BoundedProcessPool',
    'BoundedThreadPool',
)


class BoundedMixin:

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self._lock = MultiRLock()
        self._futures = weakref.WeakSet()

    def acquire(self):
        return self._semaphore.acquire()

    def release(self, future):
        with self._lock(future):
            if future not in self._futures:
                return False
            self._futures.remove(future)
            self._semaphore.release()
            return True

    def schedule(self, *args, **kwgs):
        self.acquire()
        try:
            future = super().schedule(*args, **kwgs)
        except:
            self._semaphore.release()
            raise
        else:
            self._futures.add(future)
            self._lock.add(future)
            future.add_done_callback(lambda future: self.release(future))
            return future


class BoundedProcessPool(BoundedMixin, ProcessPool):

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self._semaphore = multiprocessing.BoundedSemaphore(self._context.workers)


class BoundedThreadPool(BoundedMixin, ThreadPool):

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self._semaphore = threading.BoundedSemaphore(self._context.workers)
