from .reservations import RoomReservation


class Command:
    """Classe de base des commandes."""

    def execute(self):
        pass

    def undo(self):
        pass


class ReservationCommand(Command):
    """Commande qui effectue une réservation."""

    def __init__(self, reservation, schedule_service=None):
        self.reservation = reservation
        self.schedule_service = schedule_service

    def execute(self):
        success = self.reservation.reserve()

        if not success:
            return False

        if isinstance(self.reservation, RoomReservation):
            added = self.schedule_service.add_reservation(self.reservation)

            if not added:
                self.reservation.cancel()
                return False

        return True

    def undo(self):
        if isinstance(self.reservation, RoomReservation):
            self.schedule_service.remove_reservation(self.reservation)

        self.reservation.cancel()


class CancellationCommand(Command):
    """Commande qui annule une réservation."""

    def __init__(self, reservation, schedule_service=None):
        self.reservation = reservation
        self.schedule_service = schedule_service

    def execute(self):
        if isinstance(self.reservation, RoomReservation):
            self.schedule_service.remove_reservation(self.reservation)

        self.reservation.cancel()
        return True

    def undo(self):
        success = self.reservation.reserve()

        if success and isinstance(self.reservation, RoomReservation):
            self.schedule_service.add_reservation(self.reservation)


class CommandManager:
    """Gère l'historique des commandes."""

    def __init__(self):
        self.history = []
        self.redo_history = []

    def execute_command(self, command):
        success = command.execute()

        if success:
            self.history.append(command)
            self.redo_history.clear()

    def undo(self):
        if not self.history:
            print("Aucune action à annuler.")
            return

        command = self.history.pop()
        command.undo()
        self.redo_history.append(command)

    def redo(self):
        if not self.redo_history:
            print("Aucune action à rétablir.")
            return

        command = self.redo_history.pop()
        success = command.execute()

        if success:
            self.history.append(command)

    def can_undo(self):
        return len(self.history) > 0

    def can_redo(self):
        return len(self.redo_history) > 0
