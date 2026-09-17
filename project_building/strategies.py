"""Energy regulation algorithms used by :class:`RegulationController`."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RegulationInput:
    """Measurements consumed by regulation algorithms."""

    current_temperature: float
    target_temperature: float
    solar_irradiance: float = 0.0
    occupancy: float = 0.0


class RegulationAlgorithm(ABC):
    @abstractmethod
    def calculate(self, data: RegulationInput) -> float:
        """Return a normalized regulation command in the range [-1, 1]."""


class PIDAlgorithm(RegulationAlgorithm):
    def __init__(self, proportional_gain: float = 1.0, integral_gain: float = 0.0, derivative_gain: float = 0.0):
        self.proportional_gain = proportional_gain
        self.integral_gain = integral_gain
        self.derivative_gain = derivative_gain
        self._integral = 0.0
        self._previous_error = 0.0

    def calculate(self, data: RegulationInput) -> float:
        error = data.target_temperature - data.current_temperature
        self._integral += error
        derivative = error - self._previous_error
        self._previous_error = error
        command = (
            self.proportional_gain * error
            + self.integral_gain * self._integral
            + self.derivative_gain * derivative
        )
        return max(-1.0, min(1.0, command))


class QuickThresholdAlgorithm(RegulationAlgorithm):
    def __init__(self, threshold: float = 0.5):
        if threshold <= 0:
            raise ValueError("threshold must be greater than zero")
        self.threshold = threshold

    def calculate(self, data: RegulationInput) -> float:
        error = data.target_temperature - data.current_temperature
        if error > self.threshold:
            return 1.0
        if error < -self.threshold:
            return -1.0
        return 0.0


class SolarOptimizedAlgorithm(RegulationAlgorithm):
    def __init__(self, solar_gain: float = 0.01):
        if solar_gain < 0:
            raise ValueError("solar_gain cannot be negative")
        self.solar_gain = solar_gain

    def calculate(self, data: RegulationInput) -> float:
        adjusted_target = data.target_temperature - data.solar_irradiance * self.solar_gain
        error = adjusted_target - data.current_temperature
        return max(-1.0, min(1.0, error))