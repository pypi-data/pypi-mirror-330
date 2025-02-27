# This code is part of cqlib.
#
# Copyright (C) 2025 China Telecom Quantum Group, QuantumCTek Co., Ltd.,
# Center for Excellence in Quantum Information and Quantum Physics.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Coupler Qubit"""

from __future__ import annotations

import weakref

from cqlib.circuits.bit import Bit


class CouplerQubit(Bit):
    """A class representing a coupled qubit in a quantum system."""

    _cache = weakref.WeakValueDictionary[int, 'CouplerQubit']()

    def __new__(cls, index: int) -> CouplerQubit:
        if index < 0:
            raise ValueError("CouplerQubit index must be non-negative.")
        inst = cls._cache.get(index)
        if inst is None:
            inst = super().__new__(cls)
            inst._index = index
            inst._initialized = True
            inst._hash = None
            cls._cache[index] = inst
        return inst

    def __str__(self):
        return f'G{self.index}'
