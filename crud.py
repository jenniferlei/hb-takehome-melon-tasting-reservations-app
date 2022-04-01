"""CRUD operations for User model."""

from model import db, User, Reservation, connect_to_db


def create_user(username):
    """Create and return a new user."""

    user = User(username=username)

    return user


def get_user_by_username(username):
    """Return a user by username."""

    return db.session.query(User).get(username)


def create_reservation(user, date, start_time, end_time):
    """Create and return a new reservation."""

    reservation = Reservation(user=user,
                date=date,
                start_time=start_time,
                end_time=end_time)

    return reservation


def get_reservations_by_id(reservation_id):
    """Return reservations by reservation id."""

    return db.session.query(Reservation).get(reservation_id)


def get_reservations_by_user(username):
    """Return reservations by username."""

    return (db.session.query(Reservation).filter_by(username=username).order_by(Reservation.date.desc()).all())


def get_reservations_by_query(date, start_time, end_time):
    """Return reservations by date and time query"""

    queries = []

    queries.append(Reservation.date == date)

    if start_time != "":
        start_time_formatted = f'{start_time}:00'
        queries.append(Reservation.start_time >= start_time_formatted)
    if end_time != "":
        end_time_formatted = f'{end_time}:00'
        queries.append(Reservation.end_time <= end_time_formatted)

    return db.session.query(Reservation).filter(*queries).order_by(Reservation.start_time.asc()).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)