from .reservations import EquipmentReservation, RoomReservation


class ReservationFactory:
    """Classe de base des fabriques de réservations."""

    def create_reservation(self):
        pass


class RoomReservationFactory(ReservationFactory):
    """Fabrique une réservation de salle."""

    def create_reservation(self, requester_id, room, start_time, end_time):
        return RoomReservation(requester_id, room, start_time, end_time)


class EquipmentReservationFactory(ReservationFactory):
    """Fabrique une réservation de matériel."""

    def create_reservation(self, requester_id, equipment, start_time, end_time):
        return EquipmentReservation(requester_id, equipment, start_time, end_time)
