from datetime import date, time

from webtris_client import TrafficObservation

''' Traffic Observation Test '''
def all_paramaters():
    object1 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, 100)
    assert object1.has_all_the_data is True

def test_traffic_observation():
    object1 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "?", 65.0, 50)
    assert object1.has_all_the_data()

    object2 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "?", None, 50)
    assert not object2.has_all_the_data()

    object3 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "?", 65.0, None)
    assert not object3.has_all_the_data()

def test_traffic_observation_ordering():
    a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "?", 65.0, 50)
    b = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "?", 65.0, 51)
    assert a < b

