class ScheduleService:
    """Gère le planning des salles."""

    def __init__(self):
        self.reservations = []

    def is_available(self, room, start_time, end_time):
        if start_time >= end_time:
            return False

        for reservation in self.reservations:
            same_room = reservation.room.id == room.id
            overlap = (
                start_time < reservation.end_time
                and end_time > reservation.start_time
            )

            if reservation.active and same_room and overlap:
                return False

        return True

    def add_reservation(self, reservation):
        if reservation in self.reservations:
            return True

        if not self.is_available(
            reservation.room,
            reservation.start_time,
            reservation.end_time,
        ):
            print("La salle n'est pas disponible.")
            return False

        self.reservations.append(reservation)
        return True

    def remove_reservation(self, reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)

    def get_reservations(self, room):
        room_reservations = []

        for reservation in self.reservations:
            if reservation.room.id == room.id:
                room_reservations.append(reservation)

        return room_reservations

    def has_reservation(self, requester_id, room, at):
        for reservation in self.reservations:
            same_user = reservation.requester_id == requester_id
            same_room = reservation.room.id == room.id
            correct_time = reservation.start_time <= at < reservation.end_time

            if reservation.active and same_user and same_room and correct_time:
                return True

        return False
