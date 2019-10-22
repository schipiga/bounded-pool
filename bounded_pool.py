import multiprocessing
import threading
import weakref

from multilock import MultiRLock


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

    def submit(self, func, *args, **kwgs):
        self.acquire()
        try:
            future = super().submit(func, *args, **kwgs)
        except:
            self._semaphore.release()
            raise
        else:
            self._futures.add(future)
            self._lock.add(future)
            future.add_done_callback(lambda future: self.release(future))
            return future


def __getattr__(name):
    global BoundedProcessPool, BoundedThreadPool

    if name == 'BoundedProcessPool':
        from concurrent.futures import ProcessPoolExecutor

        class BoundedProcessPool(BoundedMixin, ProcessPoolExecutor):

            def __init__(self, *args, **kwgs):
                super().__init__(*args, **kwgs)
                self._semaphore = multiprocessing.BoundedSemaphore(self._max_workers)

        return BoundedProcessPool

    if name == 'BoundedThreadPool':
        from concurrent.futures.thread import ThreadPoolExecutor

        class BoundedThreadPool(BoundedMixin, ThreadPoolExecutor):

            def __init__(self, *args, **kwgs):
                super().__init__(*args, **kwgs)
                self._semaphore = threading.BoundedSemaphore(self._max_workers)
        
        return BoundedThreadPool

    raise AttributeError(f"module {__name__} has no attribute {name}")
