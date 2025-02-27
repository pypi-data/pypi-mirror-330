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

""" Sequential DC pulse controller for data/coupling qubit Z channels. """
from cqlib.exceptions import CqlibError
from .base_pulse import BasePulse
from .waveform import Waveform


class PZ(BasePulse):
    """
    Sequential DC pulse controller for data/coupling qubit Z channels.
    """

    def __init__(self, waveform: Waveform, label: str = None):
        """Initialize Z-axis DC pulse with Stark shift parameters"""
        super().__init__('PZ', waveform=waveform, label=label)

    def validate(self):
        p = self._waveform
        if p.phase is not None or p.drag_alpha is not None:
            raise CqlibError('PZ must not have phase and drag_alpha params')
