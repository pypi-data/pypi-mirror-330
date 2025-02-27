import os
import signal
from typing import Callable


def ignore_sigint():
    # https://stackoverflow.com/q/1408356
    # We avoid the KeyboardInterrupt bug by
    # ignore SIGINT altogether at the child
    # process
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def raise_sigint(*_):
    os.kill(os.getpid(), signal.SIGINT)


def raise_sigint_on_sigterm(*_):
    signal.signal(signal.SIGTERM, raise_sigint)


def sigint_hook(callback: Callable[[], None]):
    signal.signal(signal.SIGINT, lambda *_: callback())
    signal.signal(signal.SIGTERM, lambda *_: callback())
