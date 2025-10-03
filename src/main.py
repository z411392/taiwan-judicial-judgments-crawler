from os import environ, getcwd

environ["ROOT_PATH"] = getcwd()


if __name__ == "__main__":
    from asyncio import new_event_loop, set_event_loop
    from fire import Fire
    from taiwan_judicial_judgments_crawler.entrypoints.cli import create_entrypoints
    from taiwan_judicial_judgments_crawler.utils.lifespan.startup import startup
    from taiwan_judicial_judgments_crawler.utils.lifespan.shutdown import shutdown

    loop = new_event_loop()
    set_event_loop(loop)
    injector = loop.run_until_complete(startup())
    try:
        Fire(create_entrypoints(injector))
    finally:
        loop.run_until_complete(shutdown(injector))
        loop.close()
