from datetime import date, time
import pytest
from webtris_client import TrafficObservation, API, SingleSite
from unittest.mock import Mock

class TestTrafficObservation:
    ''' Pytest Fixtures for Traffic Observation '''

    @pytest.fixture
    def all_paramaters(self):
        return TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, 100)
    
    @pytest.fixture
    def test_data(self) -> bool:
        a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, 100)
        return a is not None

    @pytest.fixture
    def missing_paramaters(self):
        return TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, None)
    '''
        Fixtures let us use the same test functions in other test cases without having to write the same 
        methods agian. By doing these fixtures, we can add these certain methods as paramters. 
    '''

    ''' Traffic Observation Parameters Test'''
    def test_all_paramaters(self, test_data):
        object1 = test_data
        assert object1 is True
    #This test checks that all the paramaters are filled for Traffic Obseravtion. returns True if has_all_data() method we made is True

    def test_missing_speed_data(self):
        a1 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, 100)
        assert a1.has_all_the_data() is False
    #This test checks that the speed data is missing. It should return False showing that we are missing our speed data

    def test_missing_vehicle_data(self):
        a1 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, None)
        assert a1.has_all_the_data() is False
    #This test is the same thing as above. Returns False when there is no value for the number of cars. 

    def test_missing_speed_and_vehicle(self):
        a1 = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, None)
        assert a1.has_all_the_data() is False
    #Again the same kind of test. this returns false expecting both the speed and number of cars to not have a value


    ''' Traffic Observation __str__ Tests '''
    def test_str_parameters(self, all_paramaters):
        result = str(all_paramaters)
        assert "M25/4432A" in result
        assert "2026-03-03" in result
        assert "00:01:30" in result
        assert "100" in result
        assert "63.0" in result
    '''
    This test takes the all_parameters() method and gets all the str's. We check that __Str__ method makes correctlt formated string that 
    has all the parameters from all_paramertes(). I check each of them indvidually so I know exactly where the error is if one of the test
    falils for some reaosn. 
    '''

    def test_print_speed_error(self, missing_paramaters):
        result = str(missing_paramaters)
        assert "Speed=No Value" in result
    #Here I am testing taht __str__ prints "No Value" when calling from missing_paramaters() method. 




class TestAPI:
    
    @pytest.fixture
    def client(self):
        return API()
    
    @pytest.fixture
    def filled_row(self):
        return 
        {
            "Site Name": "M25/4432A",
            "Report Date": "2026-03-03",
            "Time Period Ending": "00:01:30",
            "Avg mph": "63",
            "Total Volume": "100"
        }
    

    def test_fix_floats_number(self, client):
        assert client.fix_floats("65.0") == 65.0

    def test_fix_floats_None(self, client):
        assert client.fix_floats("") is None
    
    def test_fix_int_number(self, client):
        assert client.fix_ints("100") == 100

    def test_fix_int_None(self, client):
        assert client.fix_floats("") is None
    
    def test_fix_rows(self, client, filled_row):
        pass



class TestSingleSite:
    pass



