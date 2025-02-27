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
Waveform

This module defines waveform type enumerations and parameter classes
for generating quantum pulse sequences. It provides a standardized
interface to configure and validate waveform parameters across different
waveform types.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, unique
from math import pi

from cqlib.exceptions import CqlibError


@unique
class WaveformType(IntEnum):
    """
    Enumeration of supported waveform types for quantum pulse sequences.

    Members:
        COSINE (0): Cosine-shaped waveform.
        FLATTOP (1): Flat-top waveform with customizable edge length.
        SLEPIAN (2): Slepian tapering waveform defined by time-bandwidth
                     product parameters.
        NUMERIC (3): Arbitrary numeric waveform specified via sample array.
    """
    COSINE = 0
    FLATTOP = 1
    SLEPIAN = 2
    NUMERIC = 3


@dataclass
class Waveform:
    """
    Base dataclass for waveform parameter validation and string representation.

    Attributes:
        waveform (WaveformType): Enumerated waveform type.
        length (int): Total waveform duration (1-1e5).
        amplitude (float): Normalized signal amplitude (0.0-1.0).
        phase (float, optional): Phase shift for PXY modulations.
        drag_alpha (float, optional): Drag coefficient for PXY modulations.
    """
    waveform: WaveformType
    length: int
    amplitude: float
    phase: float = None  # PXY only
    drag_alpha: float = None  # PXY only

    @staticmethod
    def create(
            w_type: WaveformType,
            length: int,
            amplitude: float,
            phase: float = None,
            drag_alpha: float = None,
            **kwargs
    ) -> 'Waveform':
        """
        Factory method to create waveform parameter objects based on the specified type.

        Instantiates a concrete waveform parameter class according to the given waveform type,
        validates parameters, and returns the initialized object.

        Args:
            w_type(WaveformType):  Enumerated waveform type identifier.
            length(int): Total duration of the waveform in samples (1-1e5).
            amplitude: Normalized signal amplitude (0.0-1.0).
            phase (float, optional): Phase shift for PXY. Must be in (-π, π] range.
            drag_alpha (float, optional): DRAG correction coefficient for PXY. Must be positive.
            **kwargs: Type-specific parameters for advanced waveform configurations:
                - FLATTOP: edge (int)
                - SLEPIAN: thf, thi, lam2, lam3 (float)
                - NUMERIC: samples (list[float])
        """
        param_classes = {
            WaveformType.COSINE: CosineWaveform,
            WaveformType.FLATTOP: FlattopWaveform,
            WaveformType.SLEPIAN: SlepianWaveform,
            WaveformType.NUMERIC: NumericWaveform
        }

        if w_type not in param_classes:
            raise ValueError(f"Unsupported waveform type: {w_type}")

        return param_classes[w_type](
            waveform=w_type,
            length=length,
            amplitude=amplitude,
            phase=phase,
            drag_alpha=drag_alpha,
            **kwargs
        )

    def validate(self):
        """Performs basic parameter validation."""
        if not isinstance(self.length, int) or self.length <= 0 or self.length > 1e5:
            raise CqlibError(f"Invalid length: {self.length}. Must be in [0, 1e5]")
        if not 0.0 <= self.amplitude <= 1.0:
            raise CqlibError(f"Invalid amplitude: {self.amplitude}. Must be in [0, 1]")
        if self.phase is not None and (self.phase <= -pi or self.phase >= pi):
            raise CqlibError("The phase value must be within (-pi, pi].")
        if self.drag_alpha is not None and self.drag_alpha < 0:
            raise CqlibError("The drag_alpha value must be positive float.")

    def __str__(self):
        return ' '.join(map(str, self.data))

    @property
    def data(self) -> list[float]:
        """Data list"""
        ps = [self.waveform.value, self.length, self.amplitude]
        if self.phase is not None and self.drag_alpha is not None:
            ps.extend([self.phase, self.drag_alpha])
        return ps

    @classmethod
    def load(cls, waveform: str | list[float | int], gate: str) -> Waveform:
        """
        Constructs Waveform from serialized data.

        Args:
            waveform (str | list[float | int]): Input data as either:
                - Space-separated string of parameters
                - List of numeric values
            gate (str): Target gate operation (PXY/PZ/etc.) determining
                  parameter interpretation

        Returns:
            Waveform: Instantiated waveform object
        """
        if isinstance(waveform, str):
            waveform = map(float, waveform.split())
        ps = waveform
        try:
            waveform_type = WaveformType(ps[0])
        except ValueError as e:
            raise CqlibError(f"Invalid waveform type value: {ps[0]}") from e
        length, amplitude = ps[1:3]
        ps = ps[3:]
        if gate == 'PXY':
            phase, drag_alpha = ps[:2]
            ps = ps[2:]
        else:
            phase, drag_alpha = None, None
        kwargs = {
            'w_type': waveform_type,
            'length': int(length),
            'amplitude': amplitude,
            'phase': phase,
            'drag_alpha': drag_alpha
        }

        if waveform_type == WaveformType.FLATTOP:
            edge = ps[0]
            if edge != int(edge):
                raise CqlibError('')
            kwargs['edge'] = int(edge)
        else:
            ps = [int(p) if p == int(p) else p for p in ps]
            if waveform_type == WaveformType.SLEPIAN:
                kwargs.update({
                    'thf': ps[0],
                    'thi': ps[1],
                    'lam2': ps[2],
                    'lam3': ps[3],
                })
            elif waveform_type == WaveformType.NUMERIC:
                kwargs['data_list'] = ps
        return Waveform.create(**kwargs)


@dataclass
class CosineWaveform(Waveform):
    """Configuration parameters for cosine-shaped waveforms."""

    def __post_init__(self):
        self.validate()


@dataclass
class FlattopWaveform(Waveform):
    """
    Specialized parameters for flat-top waveforms with edge control.

    Additional Attributes:
        edge (int): Length of rising/falling edges (must be < total length/2).
    """
    edge: int = None

    def __post_init__(self):
        self.validate()
        if self.edge < 0 or not isinstance(self.edge, int):
            raise CqlibError(f"Flattop waveform edge parameter must be a positive integer, "
                             f"got {type(self.edge).__name__} {self.edge}")
        if 2 * self.edge >= self.length:
            raise CqlibError(f"Edge ({self.edge}) too large for length {self.length}")

    @property
    def data(self) -> list[float]:
        ps = super().data
        ps.append(self.edge)
        return ps


@dataclass
class SlepianWaveform(Waveform):
    """
    Specialized parameters for slepian waveforms

    Additional Attributes:
        - thf:
        - thi:
        - lam2:
        - lam3:
    """
    thf: float = None
    thi: float = None
    lam2: float = None
    lam3: float = None

    @property
    def data(self) -> list[float]:
        ps = super().data
        ps.extend([self.thf, self.thi, self.lam2, self.lam3])
        return ps


@dataclass
class NumericWaveform(Waveform):
    """
    Specialized parameters for numeric waveforms.

    Additional Attributes:
        - params: List of floats, Values must be in [0.0, 1.0],
                Minimum length of 3 samples;
    """
    data_list: list[float] = None

    def __post_init__(self):
        super().validate()
        if any(not (0.0 <= x <= 1.0) for x in self.data_list):
            raise CqlibError("All data values must be in [0,1]")
        if len(self.data_list) < 3:
            raise CqlibError("The numerical list of data pulses is in the form"
                             " of [d0, d1, ..., dn], and the list length must be >= 3")

    @property
    def data(self) -> list[float]:
        ps = super().data
        ps.extend(self.data_list)
        return ps
