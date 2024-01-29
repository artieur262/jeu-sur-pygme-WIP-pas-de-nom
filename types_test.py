"""Script to test lens on python on types
"""
import typing
from typing import Any
import numpy

_ = numpy is True and typing is True

array = typing.NewType("coordinate", (numpy.ndarray, int, float, list, tuple))


class myArray(numpy.ndarray, int, float, list, tuple):
    def __instancecheck__(self, __instance: Any) -> bool:
        return super().__instancecheck__(__instance)


def cord(pos: array):
    print(isinstance(pos, myArray))
    print(isinstance(pos, (int, float, list, tuple, numpy.ndarray)))


cord(numpy.array((1, 2, 3)))
