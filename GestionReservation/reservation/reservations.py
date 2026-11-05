from abc import ABC, abstractmethod


class Reservation(ABC):
    """Classe de base des réservations."""

    @abstractmethod
    def reserve(self):
        pass

    @abstractmethod
    def cancel(self):
        pass


class RoomReservation(Reservation):
    """Représente la réservation d'une salle."""

    def __init__(self, requester_id, room, start_time, end_time):
        self.requester_id = requester_id
        self.room = room
        self.start_time = start_time
        self.end_time = end_time
        self.active = False

    def reserve(self):
        if self.start_time >= self.end_time:
            print("La période de réservation est invalide.")
            return False

        if self.active:
            print("Cette réservation est déjà active.")
            return False

        self.active = True
        return True

    def cancel(self):
        self.active = False


class EquipmentReservation(Reservation):
    """Représente la réservation d'un matériel."""

    def __init__(self, requester_id, equipment, start_time, end_time):
        self.requester_id = requester_id
        self.equipment = equipment
        self.start_time = start_time
        self.end_time = end_time
        self.active = False

    def reserve(self):
        if self.start_time >= self.end_time:
            print("La période de réservation est invalide.")
            return False

        if not self.equipment.available:
            print("Le matériel n'est pas disponible.")
            return False

        self.equipment.available = False
        self.active = True
        return True

    def cancel(self):
        if self.active:
            self.active = False
            self.equipment.available = True
