# -*- coding: utf-8 -*-

"""
  SouthPay own signals,

  Here defines some signals for async task.

  TODO: More signals
"""
from vwalila.logger_helper import log
import socket
from blinker import Namespace

signal = Namespace().signal
logger = log


# async task
before_task_called = signal('before_task_called')
after_task_called = signal('after_task_called')
after_get_task_result = signal('after_get_task_result')

registered = False


def register_signals_receivers():
    global registered
    if registered:
        return logger.warn("Signals are already registered, skipping")
    register_task_signals()


def register_task_signals():
    before_task_called.connect(on_signal_before_task_called)
    after_task_called.connect(on_signal_after_task_called)


def on_signal_before_task_called(ctx):
    """Invoke before task called"""
    # ctx.logger.info("%s got args -> %s, kwargs -> %s",
    #                 ctx.task, ctx.args, ctx.kwargs)


def on_signal_after_task_called(ctx):
    """Invoke after task finish"""
    # statsd_client.incr(ctx.task)
    # statsd_client.timing(ctx.task, ctx.cost)
    # do some db connection close
    # DBSession.remove()  # no cover!


class SignalContext(object):
    """"""


class TaskCallSignalContext(SignalContext):

    @property
    def cost(self):
        return 1000 * (self.end_at - self.start_at)

    @property
    def server_ip(self):
        return socket.gethostname()
