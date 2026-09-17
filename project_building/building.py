"""Building aggregate and its room specializations."""

from dataclasses import dataclass

from .contracts import HeatingContext, LightingContext, RegulationService
from .states import RoomState
from .strategies import RegulationInput


@dataclass
class Building:
    state: RoomState
    regulator: RegulationService
    regulation_input: RegulationInput
    occupancy: float = 0.0
    heating_level: float = 0.0
    lighting_level: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.state, RoomState):
            raise TypeError("state must implement RoomState")
        if not isinstance(self.regulator, RegulationService):
            raise TypeError("regulator must implement RegulationService")

    def regulate_heating(self) -> None:
        self.state.regulate_heating(self)

    def regulate_lighting(self) -> None:
        self.state.regulate_lighting(self)

    def regulate(self) -> None:
        self.state.regulate(self, self)

    def set_heating_level(self, level: float) -> None:
        self.heating_level = max(-1.0, min(1.0, level))

    def set_lighting_level(self, level: float) -> None:
        self.lighting_level = max(0.0, min(1.0, level))

    def change_state(self, state: RoomState) -> None:
        if not isinstance(state, RoomState):
            raise TypeError("state must implement RoomState")
        self.state = state


class LectureHall(Building):
    pass


class Laboratory(Building):
    pass


class Classroom(Building):
    pass