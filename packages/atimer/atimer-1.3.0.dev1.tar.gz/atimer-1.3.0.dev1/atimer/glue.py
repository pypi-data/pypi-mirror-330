#
# atimer - timer library for asyncio
#
# Copyright (C) 2016 - 2024 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Timer based on Linux `timerfd` interface.
"""

import asyncio
import logging
import os
import struct
import typing as tp
from collections.abc import Awaitable

from ._atimer import atimer_init, atimer_start, atimer_close  # type: ignore

logger = logging.getLogger(__name__)

class Timer(Awaitable[int]):
    """
    Timer based on Linux `timerfd` interface.

    Timer object is a Python asynchronous coroutine. It waits for timer
    expiration. An awaited coroutine returns number of timer expirations.

    The number of expirations is usually `1` until timer overrun happens.
    Refer to POSIX documentation for definition of the timer overrun.

    :param interval: Interval, in seconds, at which the timer expires.
    :param shift: Shift edge of the interval by specified time, in seconds.
    """
    def __init__(self, interval: float, shift: float=0.0):
        """
        Create timer object.

        :param interval: Interval, in seconds, at which the timer expires.
        :param shift: Time, in seconds, to shift the edge of the interval by.
        """
        self._fd = atimer_init()
        self._interval = interval
        self._shift = shift
        self._task: asyncio.Future[int] | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    def start(self) -> None:
        """
        Arm the timer.
        """
        self._loop = asyncio.get_running_loop()
        self._loop.add_reader(self._fd, self._timer_expired)
        atimer_start(self._fd, self._interval, self._shift)
        if __debug__:
            logger.debug('timer armed: interval={}, shift={}'.format(
                self._interval, self._shift
            ))

    def __await__(self) -> tp.Generator[tp.Any, None, int]:
        assert self._loop is not None
        self._task = self._loop.create_future()
        return (yield from self._task)

    def close(self) -> None:
        """
        Stop and disarm the timer.
        """
        assert self._loop is not None
        self._loop.remove_reader(self._fd)
        atimer_close(self._fd)

        task = self._task
        if task and not task.done():
            task.set_exception(asyncio.CancelledError())

        if __debug__:
            logger.debug('timer disarmed')

    def _timer_expired(self) -> None:
        """
        Handle notification of timer expiration from the timer.

        Number of expirations is read from timer file descriptor and set as
        result of current task. If timer object is not awaited yet, then
        return null.
        """
        task = self._task
        if task and not task.done():
            value = os.read(self._fd, 8)
            value = struct.unpack('Q', value)[0]
            self._task.set_result(value)  # type: ignore

# vim: sw=4:et:ai
