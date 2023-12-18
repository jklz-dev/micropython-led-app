from .display_demo import run_demo
import uasyncio


def run():
    # run app from package
    print('running ledapp')
    uasyncio.run(run_demo())
