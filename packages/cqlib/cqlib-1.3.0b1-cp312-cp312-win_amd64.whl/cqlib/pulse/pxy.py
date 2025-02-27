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

"""
Sequential AC(Alternating Current) pulse controller for data qubit XY channels.
"""
from cqlib.exceptions import CqlibError
from .base_pulse import BasePulse
from .waveform import Waveform, NumericWaveform


class PXY(BasePulse):
    """
    Pulse controller for data qubit XY channels.

    For PXY pulses, the numerical list of data pulses is in the form of
    [i0, i1, ..., in, q0, q1, ..., qn]. The first half describes the
    pulse values of I channel, and the second half describes the
    pulse values of Q channel. The length of its list is >=6 and
    must be even.
    """

    def __init__(self, waveform: Waveform, label: str = None):
        """
        Initialize XY channel pulse with waveform parameters
        """
        super().__init__('PXY', waveform=waveform, label=label)

    def validate(self):
        """
        Verify PXY-specific waveform constraints.
        """
        waveform = self._waveform
        if waveform.phase is None or waveform.drag_alpha is None:
            raise CqlibError('PXY must have phase and drag_alpha params')
        if isinstance(waveform, NumericWaveform) \
                and (len(waveform.data_list) < 6 or len(waveform.data_list) % 2 == 1):
            raise CqlibError('The length of its list must >=6 and must be even.')
