from datetime import datetime

from reservation import Equipment, ReservationService


class FakeRoom:
    """Représente une salle simple pour la démonstration."""

    def __init__(self, room_id, name):
        self.id = room_id
        self.name = name


service = ReservationService()
room = FakeRoom("room-a101", "A101")

print("Réservation de la salle A101 de 10h à 12h")
reservation = service.reserve_room(
    "student-001",
    room,
    datetime(2026, 9, 17, 10),
    datetime(2026, 9, 17, 12),
)

print("Tentative de réservation de 11h à 13h")
service.reserve_room(
    "student-002",
    room,
    datetime(2026, 9, 17, 11),
    datetime(2026, 9, 17, 13),
)

print("Annulation de la dernière action")
service.undo_last_action()

print("Rétablissement de la dernière action")
service.redo_last_action()

print("Annulation de la réservation")
service.cancel_reservation(reservation)

print("Réservation d'un vidéoprojecteur")
equipment = Equipment("projector-001", "Vidéoprojecteur")
service.reserve_equipment(
    "student-001",
    equipment,
    datetime(2026, 9, 17, 10),
    datetime(2026, 9, 17, 12),
)
