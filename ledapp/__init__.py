from .display_demo import run_demo
from .pixel import pixel


async def run(is_online: bool = False) -> None:
    # run app from package
    print('running ledapp')
    # attempt to display from config
    await pixel.apply_from_config()

    if is_online:
        await run_demo()
