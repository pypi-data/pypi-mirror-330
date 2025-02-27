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
A specialized quantum circuit class designed for pulse-level control
of qubits and coupler qubits.
"""
import re
from collections.abc import Sequence

from cqlib.circuits.circuit import Circuit, Qubits
from cqlib.circuits.instruction import Instruction
from cqlib.circuits.instruction_data import InstructionData
from cqlib.circuits.parameter import Parameter
from cqlib.circuits.qubit import Qubit
from cqlib.exceptions import CqlibError

from .coupler_qubit import CouplerQubit
from .g import G
from .pxy import PXY
from .pz import PZ
from .pz0 import PZ0
from .waveform import Waveform
from .base_pulse import BasePulse

CouplerQubits = int | CouplerQubit | Sequence[int | CouplerQubit]

PULSE_GATES = ['PZ', 'PZ0', 'PXY', 'G']


class PulseCircuit(Circuit):
    """
    Circuit with pulse support.
    """

    def __init__(
            self,
            qubits: Qubits,
            coupler_qubits: CouplerQubits,
            parameters: Sequence[Parameter | str] | None = None
    ) -> None:
        """
        Initialize PulseCircuit.

        Args:
            qubits(Qubits): Specification for standard qubits.
            coupler_qubits(CouplerQubits): Specification for coupler qubits.
            parameters(Sequence[Parameter | str] | None): Circuit parameters.
        """
        super().__init__(qubits, parameters)
        self._coupler_qubits = self._initialize_coupler_qubits(coupler_qubits)

    @property
    def coupler_qubits(self) -> list[CouplerQubit]:
        """
        A list of initialized coupler qubit objects in the circuit.
        """
        return list(self._coupler_qubits.values())

    def append_pulse(self, instruction: Instruction, qubit: CouplerQubit | Qubit):
        """
        Appends a pulse instruction to the circuit.

        Args:
            instruction (Instruction): Pulse instruction to add.
            qubit (Qubit | CouplerQubit): Target qubit or coupler qubit.
        """
        if isinstance(qubit, CouplerQubit) and str(qubit) not in self._coupler_qubits:
            raise CqlibError(f"Coupler qubit {qubit} is not registered in the circuit. "
                             f"Available coupler qubits: {self.coupler_qubits}")
        if isinstance(qubit, Qubit) and str(qubit) not in self._qubits:
            raise CqlibError(f"Qubit {qubit} is not registered in the circuit. "
                             f"Available qubits: {self.qubits}")
        self._circuit_data.append(InstructionData(instruction=instruction, qubits=[qubit]))

    def g(self, couple_qubit: CouplerQubit | int, length: int, coupling_strength: int):
        """
        Applies a G-pulse (coupling pulse) to a coupler qubit.

        Args:
            couple_qubit(CouplerQubit | int): Target coupler qubit or its index.
            length(int): Duration of the pulse in time steps.
            coupling_strength(int): Strength of the coupling interaction.
        """
        if isinstance(couple_qubit, int):
            couple_qubit = CouplerQubit(couple_qubit)
        self.append_pulse(G(length, coupling_strength), couple_qubit)

    def pxy(self, qubit: Qubit | int, waveform: Waveform):
        """
        Applies a PXY-pulse (XY control pulse) to a standard qubit.

        Args:
            qubit(Qubit | int): Target qubit or its index.
            waveform(Waveform): Waveform object defining the pulse shape.
        """
        if isinstance(qubit, int):
            qubit = Qubit(qubit)
        self.append_pulse(PXY(waveform=waveform), qubit)

    def pz(self, qubit: CouplerQubit | Qubit, waveform: Waveform):
        """
        Applies a PZ-pulse (Z control pulse) to a qubit or coupler qubit.

        Args:
            qubit(CouplerQubit | Qubit): Target CouplerQubit or Qubit.
            waveform (Waveform): Waveform object defining the pulse shape.
        """
        self.append_pulse(PZ(waveform=waveform), qubit)

    def pz0(self, qubit: CouplerQubit | Qubit, waveform: Waveform):
        """
        Applies a PZ0-pulse (parallel) to a qubit or coupler qubit.

        Args:
            qubit(CouplerQubit | Qubit): Target CouplerQubit or Qubit.
            waveform (Waveform): Waveform object defining the pulse shape.
        """
        self.append_pulse(PZ0(waveform=waveform), qubit)

    def add_coupler_qubits(self, couple_qubits: CouplerQubits):
        """
        Adds a coupler qubit(or list) to the circuit, ensuring it does not already exist.

        Args:
            couple_qubits (CouplerQubits): The coupler qubits to add, specified as an
                integer index or a Qubit object.
        """
        if not isinstance(couple_qubits, Sequence):
            couple_qubits = [couple_qubits]

        for qubit in couple_qubits:
            if isinstance(qubit, int):
                qubit = CouplerQubit(qubit)
            elif not isinstance(qubit, CouplerQubit):
                raise TypeError(f"{qubit} must be an int or CouplerQubit instance.")
            if str(qubit) in self._qubits:
                raise ValueError(f"CouplerQubit {qubit} already exists in the circuit.")
            self._coupler_qubits[str(qubit)] = qubit

    @staticmethod
    def _initialize_coupler_qubits(coupler_qubits: CouplerQubits) -> dict[str, CouplerQubit]:
        """
        Helper function to initialize coupler_qubits.

        Args:
            coupler_qubits (CouplerQubits): Input coupler qubits specification.

        Returns:
            dict[int, CouplerQubit]: Dictionary of CouplerQubit objects.
        """
        if isinstance(coupler_qubits, int):
            if coupler_qubits < 0:
                raise ValueError("Number of coupler qubits must be non-negative.")
            return {str(Qubit(i)): CouplerQubit(i) for i in range(coupler_qubits)}
        if isinstance(coupler_qubits, CouplerQubit):
            return {str(coupler_qubits): coupler_qubits}
        if not isinstance(coupler_qubits, (list, tuple)):
            raise ValueError("Invalid coupler_qubits input. Expected int, CouplerQubit,"
                             " or list/tuple of these.")

        qs = {}
        for qubit in coupler_qubits:
            if isinstance(qubit, int):
                qubit = CouplerQubit(qubit)
            elif not isinstance(qubit, CouplerQubit):
                raise TypeError("CouplerQubit must be an int or CouplerQubit instance.")
            if qubit.index in qs:
                raise ValueError(f"Duplicate qubit detected: {qubit}")
            qs[str(qubit)] = qubit
        return qs

    def to_qasm2(self) -> str:
        """
        Generate a QASM 2.0 string representation of the circuit.

        Note:
            Circuits containing coupler qubits cannot be exported to QASM 2.0 format,
            as the standard does not support coupler qubit operations.

        Returns:
            str: QASM 2.0 compliant code representing the circuit

        Raises:
            CqlibError: If the circuit contains coupler qubits, as they are not supported
                in QASM 2.0.
        """
        if self._coupler_qubits:
            raise CqlibError(f"QASM 2.0 export not supported for circuits with coupler qubits. "
                             f"Found  coupler(s): {self.coupler_qubits}")
        return super().to_qasm2()

    @classmethod
    def load(cls, qcis: str) -> 'PulseCircuit':
        """
        Loads quantum circuit with pulse-level instructions from QCIS string.

        Extends base Circuit functionality with support for:
        - Coupler qubits (G-prefixed identifiers)
        - Pulse waveforms (PXY, PZ, PZ0)
        - Hybrid circuits mixing gates and pulses

        Args:
            qcis: String containing hybrid quantum instructions.

        Returns:
            PulseCircuit: Circuit with pulse capabilities initialized.
        """
        circuit = cls(qubits=[], coupler_qubits=[])
        pattern = re.compile(r'^([A-Z][A-Z0-9]*)\s+((?:[QG][0-9]+\s*)+)'
                             r'((?:[+-]?(?:\d*\.\d+|\d+)(?:[Ee][+-]?\d+)?\s*)*)$')
        for line in qcis.split('\n'):
            line = re.sub(r'(#|//).*', '', line).strip()
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                raise ValueError(f'Invalid instruction format: {line}')
            gate, qubits_str, params_str = match.groups()
            qubits, coupler_qubits = cls._parse_pulse_qubits_str(circuit, qubits_str)
            params = [float(p) for p in params_str.split()] if params_str else []
            if gate in PULSE_GATES:
                cls._process_pulse_instruction(circuit, gate, qubits, coupler_qubits, params)
            else:
                cls._process_instruction(circuit, gate, qubits, params)

        return circuit

    def _parse_pulse_qubits_str(
            self,
            qubits_str: str
    ) -> tuple[list[Qubit], list[CouplerQubit]]:
        """
        Parses and categorizes qubit identifiers from QCIS instruction string.

        Processes space-separated qubit tokens distinguishing between:
        - Standard qubits (Q-prefixed)
        - Coupler qubits (G-prefixed)

        Args:
            qubits_str: Raw qubit specification from QCIS instruction line.

        Returns:
            tuple: Contains two lists respectively holding:
                [0] Parsed standard Qubit objects
                [1] Parsed CouplerQubit objects
        """
        qubits, coupler_qubits = [], []
        for q_str in qubits_str.split():
            if q_str.startswith('Q'):
                qubit = self._qubits.setdefault(q_str, Qubit(int(q_str[1:])))
                qubits.append(qubit)
            elif q_str.startswith('G'):
                coupler_qubit = self._coupler_qubits.setdefault(q_str, CouplerQubit(int(q_str[1:])))
                coupler_qubits.append(coupler_qubit)
            else:
                raise ValueError(f"Invalid qubit format: {q_str}")
        return qubits, coupler_qubits

    def _process_pulse_instruction(
            self,
            gate: str,
            qubits: list[Qubit],
            coupler_qubits: list[CouplerQubit],
            params: list[float | int]
    ):
        """
        Processes pulse-specific quantum instructions from parsed components.

         Handles three categories of pulse operations:
        1. G-type coupling pulses
        2. PXY parametric XY control pulses
        3. General pulse operations (PZ/PZ0 and dynamically resolved instructions)

        Args:
            gate(str): Uppercase gate identifier (e.g., 'G', 'PXY', 'PZ')
            qubits( list[Qubit]): Standard qubit targets parsed from instruction
            coupler_qubits(list[CouplerQubit]): Coupler qubit targets parsed from instruction
            params(list[float | int]): Numerical parameters following the qubit specification
        """
        if gate == 'G':
            if len(params) != 2:
                raise CqlibError("G gate requires exactly 2 parameters (length, coupling_strength)")
            length, coupling_strength = params
            if length != int(length):
                raise CqlibError(
                    f"G pulse length parameter must be integer value, "
                    f"received {type(length).__name__} {length}"
                )
            if coupling_strength != int(coupling_strength):
                raise CqlibError(
                    f"G pulse coupling_strength parameter requires integer value, "
                    f"got {type(coupling_strength).__name__} {coupling_strength}"
                )
            self._circuit_data.append(
                InstructionData(instruction=G(int(length), int(coupling_strength)),
                                qubits=coupler_qubits)
            )
            return
        # Create waveform for pulse operations
        waveform = Waveform.load(params, gate)
        if gate == 'PXY':
            if not qubits:
                raise CqlibError("PXY pulse requires valid qubit targets")
            self._circuit_data.append(
                InstructionData(instruction=PXY(waveform), qubits=qubits)
            )
            return
        # For PZ/PZ0, validate mutual exclusivity of qubit types
        if bool(qubits) == bool(coupler_qubits):
            raise CqlibError("Must provide exactly one of qubits or coupler_qubits for PZ/PZ0")
        qubits = qubits if len(qubits) > 0 else coupler_qubits

        # Dynamic gate resolution
        try:
            # pylint: disable=import-outside-toplevel, cyclic-import
            from cqlib import pulse
            instruction_class = getattr(pulse, gate)
        except AttributeError as ex:
            raise CqlibError(f"Unknown pulse instruction: {gate}") from ex
        if not issubclass(instruction_class, BasePulse):
            raise CqlibError(f"{gate} is not a valid pulse instruction")
        self._circuit_data.append(
            InstructionData(instruction=instruction_class(waveform=waveform), qubits=qubits)
        )
