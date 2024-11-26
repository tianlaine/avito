import asyncio
import os

from asyncio import Task
from typing import Optional
from bot.poller import Poller
from bot.worker import Worker
from clients.tg import TgClient
from clients.tg.dcs import UpdateObj
from bot.base import Bot

class Bot:
   def __init__(self, token: str, n: int):
       self.queue = asyncio.Queue()
       self.poller = Poller(token, self.queue)
       self.worker = Worker(token, self.queue, n)

   async def start(self):
       await self.poller.start()
       await self.worker.start()

   async def stop(self):
       await self.poller.stop()
       await self.worker.stop()

class Worker:
   def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
       self.tg_client = TgClient(token)
       self.queue = queue
       self.concurrent_workers = concurrent_workers

   async def handle_update(self, upd: UpdateObj):
       print("before", upd)
       await asyncio.sleep(1)
       print("after", upd)

   async def _worker(self):
       while True:
           try:
               upd = await self.queue.get()
               await self.handle_update(upd)
           finally:
               self.queue.task_done()

   async def start(self):
       for _ in range(self.concurrent_workers):
           asyncio.create_task(self._worker())

async def start():
   q = asyncio.Queue()
   poller = Poller(os.getenv("BOT_TOKEN"), q)
   await poller.start()

class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        self.tg_client = TgClient(token)
        self.queue = queue
        self._task: Optional[Task] = None

async def _worker(self):
   offset = 0
   while True:
      res = await self.tg_client.get_updates_in_objects(offset=offset, timeout=60)
      for u in res.result:
         offset = u.update_id + 1
         print(u)
         self.queue.put_nowait(u)


async def start(self):
    self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]


async def stop(self):
    await self.queue.join()
    for t in self._tasks:
        t.cancel()
def run():
   loop = asyncio.get_event_loop()

   bot = Bot(os.getenv("BOT_TOKEN"), 2)
   try:
       print('bot has been started')
       loop.create_task(bot.start())
       loop.run_forever()
   except KeyboardInterrupt:
       try:
           print('bot has been started')
           loop.create_task(bot.start())
           loop.run_forever()
       except KeyboardInterrupt:
           print("\nstopping", datetime.datetime.now())
           loop.run_until_complete(bot.stop())
           print('bot has been stopped', datetime.datetime.now())

if __name__ == "__main__":
   run()
