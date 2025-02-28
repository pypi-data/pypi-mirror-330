#! 代码来自 https://aureliano90.github.io/blog/2022/04/19/Implement_Rate_Limiter_in_Python_asyncio.html
import time, asyncio, collections

class LegendSemaphore(asyncio.Semaphore):
    def __init__(self, value: int, interval: int):
        """控制多线程处理速率

        :param value: 限制并发数
        :param interval: 并发时间间隔
        """
        super().__init__(value)
        # Queue of inquiry timestamps
        self._inquiries = collections.deque(maxlen=value)
        self._loop = asyncio.get_event_loop()
        self._interval = interval

    def __repr__(self):
        return f'限制: {self._inquiries.maxlen} inquiries/{self._interval}s'

    async def acquire(self):
        await super().acquire()
        if self._inquiries:
            timelapse = time.monotonic() - self._inquiries.popleft()
            # Wait until interval has passed since the first inquiry in queue returned.
            if timelapse < self._interval:
                await asyncio.sleep(self._interval - timelapse)
        return True

    def release(self):
        self._inquiries.append(time.monotonic())
        super().release()