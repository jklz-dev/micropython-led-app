import uasyncio

async_loop = uasyncio.get_event_loop()


def exception_handler(loop, context):
    print('loop exception occurred', loop, context)


async_loop.set_exception_handler(exception_handler)


def create_task(coro):
    return async_loop.create_task(coro)


def run_forever(coro):
    return async_loop.run_forever(coro)


def run_until_complete(coro):
    return async_loop.run_until_complete(coro)
