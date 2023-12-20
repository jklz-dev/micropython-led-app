import uasyncio


class AsyncProvider:

    def __init__(self):
        self.loop = uasyncio.get_event_loop()

    def create_task(self, coro):
        return self.loop.create_task(coro)

    def run_main(self, coro):
        self.create_task(coro)
        self.loop.run_forever()


asyncProvider = AsyncProvider()
