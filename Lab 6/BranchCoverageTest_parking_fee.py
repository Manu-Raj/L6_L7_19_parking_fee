import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee ----------
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_free_boundary_30_minutes():
    assert parking_fee("car", 30, False, False) == 0


def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -5, False, False)


def test_zero_minutes_is_valid():
    assert parking_fee("bike", 0, False, False) == 0


def test_paid_partial_hour_rounds_up():
    assert parking_fee("car", 90, False, False) == 60


def test_paid_exact_hour_no_rounding():
    assert parking_fee("car", 120, False, False) == 60


def test_just_over_free_limit():
    assert parking_fee("bike", 31, False, False) == 10


def test_truck_rate():
    assert parking_fee("truck", 60, False, False) == 60


def test_ev_car_half_price():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_bike_half_price():
    assert parking_fee("bike", 60, True, False) == 5


def test_ev_truck_no_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_non_ev_no_discount():
    assert parking_fee("car", 60, False, False) == 30


def test_lost_ticket_penalty():
    assert parking_fee("bike", 20, False, True) == 200


def test_lost_ticket_with_paid_stay():
    assert parking_fee("car", 60, False, True) == 230


def test_no_lost_ticket():
    assert parking_fee("car", 60, False, False) == 30


# ---------- find_slot ----------
def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_negative_free_slots():
    assert find_slot("car", -1, False) == "full"


def test_slot_full_beats_disabled():
    assert find_slot("car", 0, True) == "full"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_disabled_beats_truck():
    assert find_slot("truck", 5, True) == "ground floor"


def test_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_slot_bike_any_floor():
    assert find_slot("bike", 1, False) == "any floor"


# ---------- monthly_pass ----------
def test_pass_bike():
    assert monthly_pass("bike", False) == 500


def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_pass_car():
    assert monthly_pass("car", False) == 1500


def test_pass_car_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_truck_not_allowed():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
