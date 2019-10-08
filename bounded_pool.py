import multiprocessing
import threading

from pebble import ProcessPool, ThreadPool


__all__ = (
    'BoundedProcessPool',
    'BoundedThreadPool',
)


class BoundedMixin:

    def schedule(self, *args, **kwgs):
        self._semaphore.acquire()
        try:
            future = super().schedule(*args, **kwgs)
        except:
            self._semaphore.release()
            raise
        else:
            future.add_done_callback(lambda _: self._semaphore.release())
            return future


class BoundedProcessPool(BoundedMixin, ProcessPool):

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self._semaphore = multiprocessing.BoundedSemaphore(self._context.workers)


class BoundedThreadPool(BoundedMixin, ThreadPool):

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self._semaphore = threading.BoundedSemaphore(self._context.workers)
