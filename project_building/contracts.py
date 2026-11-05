"""Small abstractions shared by the building domain components."""

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from .strategies import RegulationInput


@runtime_checkable
class RegulationService(Protocol):
    def calculate_regulation(self, data: "RegulationInput") -> float:
        """Calculate a normalized regulation command."""


@runtime_checkable
class HeatingContext(Protocol):
    @property
    def regulation_input(self) -> "RegulationInput":
        pass

    @property
    def regulator(self) -> RegulationService:
        pass

    def set_heating_level(self, level: float) -> None:
        pass


@runtime_checkable
class LightingContext(Protocol):
    @property
    def occupancy(self) -> float:
        pass

    def set_lighting_level(self, level: float) -> None:
        pass