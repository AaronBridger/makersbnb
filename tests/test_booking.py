from lib.booking import *
def test_class_booking_constructs():
    booking = Booking(1, 1, 2, '2024-10-12', '2024-10-13', 'pending')
    assert booking.id == 1
    assert booking.listing_id == 1
    assert booking.user_id == 2

    assert booking.check_in == datetime.strptime('2024-10-12', "%Y-%m-%d").date()
    assert booking.check_out == datetime.strptime('2024-10-13', "%Y-%m-%d").date()
    assert booking.status == 'pending'

def test_equality():
    booking_1 = Booking(1, 3, 3, '2024-01-01', '2024-01-02', 'confirmed')
    booking_2 = Booking(1, 3, 3, '2024-01-01', '2024-01-02', 'confirmed')
    assert booking_1 == booking_2

def test_bookings_format():
    booking = Booking(1, 2, 3, '2024-02-02', '2024-02-03', 'confirmed')
    assert str(booking) == "Booking(1, 2, 3, 2024-02-02, 2024-02-03, confirmed)"
