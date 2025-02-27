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
Base Class for QCIS Pulse instruction
"""

from abc import ABC, abstractmethod

from cqlib.circuits.instruction import Instruction

from .waveform import Waveform


class BasePulse(Instruction, ABC):
    """
    Abstract base class for Quantum Control Instruction System (QCIS) pulse commands.
    """

    def __init__(
            self,
            name: str,
            waveform: Waveform = None,
            label: str = None
    ):
        """Initialize base pulse instance

        Args:
            name (str): Pulse type identifier (e.g. PZ/PZ0/PXY/G)
            waveform (Waveform): Waveform parameter container storing physical values.
            label (str): Optional operational label for experimental tracking
        """
        self._waveform = waveform
        if waveform:
            params = waveform.data
        else:
            params = []
        super().__init__(name=name, num_qubits=1, params=params, label=label)
        self.validate()

    @abstractmethod
    def validate(self):
        """
        Abstract template method for parameter validation
        """
