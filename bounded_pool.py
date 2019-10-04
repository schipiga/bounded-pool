import multiprocessing
import threading


__all__ = (
    'BoundedProcessPool',
    'BoundedThreadPool',
)


class BoundedMixin:

    def submit(self, func, *args, **kwgs):
        self._semaphore.acquire()
        try:
            future = super().submit(func, *args, **kwgs)
        except:
            self._semaphore.release()
            raise
        else:
            future.add_done_callback(self._semaphore.release)
            return future


def __getattr__(name):
    global ProcessPoolExecutor, ThreadPoolExecutor

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
