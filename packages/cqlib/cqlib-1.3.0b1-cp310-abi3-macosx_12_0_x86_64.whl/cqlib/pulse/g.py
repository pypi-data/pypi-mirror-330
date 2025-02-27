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

""" G: Adjust and control the coupling function of the coupling qubit. """
from cqlib.exceptions import CqlibError
from .base_pulse import BasePulse


class G(BasePulse):
    """
    Coupling strength controller for coupling qubits via sequential DC(Direct Current) pulses.
    Applies tunable interaction between adjacent qubits by setting duration (DAC cycles)
    and coupling amplitude (Hz). Exclusively operates on coupling qubits.

    Parameters:
        - length: Coupling activation duration in DAC sampling cycles (1 cycle=0.5ns)
        - coupling_strength: Interaction magnitude in Hertz (Hz)

    Example:
        `G G107 100 -3E6` sets 3MHz coupling on G107 for 50ns (100 cycles).
    """

    def __init__(self, length: int, coupling_strength: int, label: str = None):
        self.length = length
        self.coupling_strength = coupling_strength
        super().__init__('G', waveform=None, label=label)
        self.params = [length, coupling_strength]

    def validate(self):
        """
        Validate pulse parameters for G-type coupling operations.

        Ensures:
            - Duration (length) is within valid range [0, 1e5] DAC cycles
            - Coupling strength meets implementation constraints
        """
        if self.length < 0 or self.length > 1e5:
            raise CqlibError(f"Invalid duration {self.length}: "
                             f"Must be 0-100,000 DAC cycles (1 cycle=0.5ns)")

    def __str__(self):
        return f'{self.__class__.__name__}({self.length},{self.coupling_strength})'
