from .commands import CancellationCommand, CommandManager, ReservationCommand
from .factories import EquipmentReservationFactory, RoomReservationFactory
from .schedule import ScheduleService


class ReservationService:
    """Regroupe les différentes fonctions de réservation."""

    def __init__(self):
        self.schedule_service = ScheduleService()
        self.command_manager = CommandManager()

    def reserve_room(self, requester_id, room, start_time, end_time):
        if not self.schedule_service.is_available(room, start_time, end_time):
            print("La salle n'est pas disponible.")
            return None

        factory = RoomReservationFactory()
        reservation = factory.create_reservation(
            requester_id,
            room,
            start_time,
            end_time,
        )

        command = ReservationCommand(reservation, self.schedule_service)
        self.command_manager.execute_command(command)
        return reservation

    def reserve_equipment(self, requester_id, equipment, start_time, end_time):
        factory = EquipmentReservationFactory()
        reservation = factory.create_reservation(
            requester_id,
            equipment,
            start_time,
            end_time,
        )

        command = ReservationCommand(reservation)
        self.command_manager.execute_command(command)
        return reservation

    def cancel_reservation(self, reservation):
        command = CancellationCommand(reservation, self.schedule_service)
        self.command_manager.execute_command(command)

    def undo_last_action(self):
        self.command_manager.undo()

    def redo_last_action(self):
        self.command_manager.redo()

    def is_room_available(self, room, start_time, end_time):
        return self.schedule_service.is_available(room, start_time, end_time)
