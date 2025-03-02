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

if __name__ == '__main__':
    import asyncio
    import time
    from time import sleep
    
    from threading import Thread
    
    
    def start_loop(loop):
        asyncio.set_event_loop(loop)
        print("start loop", time.time())
        loop.run_forever()
    
    async def do_some_work(x, sem):
        async with sem:
            print('start {}'.format(x))
            await asyncio.to_thread(sleep, 1)
            # await asyncio.sleep(x)
            print('Done after {}s'.format(x))

    new_loop = asyncio.new_event_loop()
    sem = LegendSemaphore(3, 2)
    Thread(target=start_loop, args=(new_loop,)).start()
    
    for i in range(10):
        asyncio.run_coroutine_threadsafe(do_some_work(0.1, sem), new_loop)
    
    while 1:
        pass