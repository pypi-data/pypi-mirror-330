import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from mtmai._version import version

default_env_files = [".env", ".env.local", "../gomtm/env/dev.env"]


def bootstrap_core():
    from .config import settings
    from .logging import setup_logging

    load_dotenv()

    for env_file in default_env_files:
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)

    setup_logging()
    logger = logging.getLogger()
    logger.info(
        f"[🚀🚀🚀 mtmai]({version})"  # noqa: G004
    )
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if settings.HTTP_PROXY:
        logger.info(f"HTTP_PROXY: {settings.HTTP_PROXY}")
        os.environ["HTTP_PROXY"] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        logger.info(f"HTTPS_PROXY: {settings.HTTPS_PROXY}")
        os.environ["HTTPS_PROXY"] = settings.HTTPS_PROXY
    if settings.SOCKS_PROXY:
        logger.info(f"SOCKS_PROXY: {settings.SOCKS_PROXY}")
        os.environ["SOCKS_PROXY"] = settings.SOCKS_PROXY

    os.environ["DISPLAY"] = ":1"
