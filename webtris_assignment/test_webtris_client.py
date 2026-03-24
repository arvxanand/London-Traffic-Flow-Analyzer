from datetime import date, time
import pytest
from webtris_client import TrafficObservation, API, SingleSite
from unittest.mock import patch, Mock
from requests.exceptions import Timeout

class TestTrafficObservation:
    ''' Pytest Fixtures for Traffic Observation '''

    @pytest.fixture
    def all_paramaters(self):
        return TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, 100)

    @pytest.fixture
    def missing_paramaters(self):
        return TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, None)
    '''
        Fixtures let us use the same test functions in other test cases without having to write the same 
        methods agian. By doing these fixtures, we can add these certain methods as paramters. 
    '''

    ''' Traffic Observation Parameters Test'''
    def test_all_paramaters(self):
        a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, 100)
        assert a.has_all_the_data() is True
    #This test checks that all the paramaters are filled for Traffic Obseravtion. returns True if has_all_data() method we made is True

    def test_missing_speed_data(self):
        a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, 100)
        assert a.has_all_the_data() is False
    #This test checks that the speed data is missing. It should return False showing that we are missing our speed data

    def test_missing_vehicle_data(self):
        a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", 63.0, None)
        assert a.has_all_the_data() is False
    #This test is the same thing as above. Returns False when there is no value for the number of cars. 

    def test_missing_speed_and_vehicle(self):
        a = TrafficObservation(date(2026, 3, 3), time(0, 1, 30), "M25/4432A", None, None)
        assert a.has_all_the_data() is False
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
        assert "Speed = No Value" in result
    #Here I am testing taht __str__ prints "No Value" when calling from missing_paramaters() method. 




class TestAPI:
    ''' Pytest Fixtures for WebTrisAPI '''
    @pytest.fixture
    def client(self):
        return API()
    #Making a fixture lets us use a reusable API object so we dont have to create own in every class
    
    @pytest.fixture
    def filled_row(self):
        return {
            "Site Name": "M25/4432A",
            "Report Date": "2026-03-03T00:00:00", 
            "Time Period Ending": "00:01:30",
            "Avg mph": "63",
            "Total Volume": "100"
        }
    #We create a fake row as a fixture so that we can use it tests and not have to write the same dictionary every time 

    @pytest.fixture
    def empty_row(self):
        return {
            "Site Name": "M25/4432A",
            "Report Date": "2026-03-03T00:00:00",
            "Time Period Ending": "00:01:30",
            "Avg mph": "",
            "Total Volume": ""
        }
    #We also create another fake row with empty volume and speed strings. Again we can use this for tests and not have to write the same dictionary every time

    
    @pytest.fixture
    def succesful_mock_response(self):
        m = Mock(status_code = 200)
        m.json.return_value = {
            "Rows": [
                {
                    "Site Name": "M25/4432A",
                    "Report Date": "2025-10-19T00:00:00",
                    "Time Period Ending": "00:14:00",
                    "Avg mph": "65",
                    "Total Volume": "182"
                }
            ]
        }
        m.raise_for_status = Mock()
        return m
    '''
    This pytest fixture makes a fake API call using Mock. From the lecture notes we learned that Mock is an objefct that can act like a real object.
    We set the status code to 200 to simialte a succuslef response and then we use json.return_value to control what the reponse gives us.
    Setting raise_for_status as Mock() makes it do nothing. This fixture is just simoly simulating a real request that would work withoug any errors.
    '''
    
    ''' fix floats tests '''
    def test_fix_floats_number(self, client):
        assert client.fix_floats("65.0") == 65.0
    #The APi gives 65 as a string so we are chekcing that the fix_floats() function correctly turns that string into a float

    def test_fix_floats_None(self, client):
        assert client.fix_floats("") is None
    #The API could have data missing so we have to account for None. Checking from our empty row fixture that the empty string will return None
    
    ''' fix ints tests '''
    def test_fix_int_number(self, client):
        assert client.fix_ints("100") == 100
    #The API gives 100 as a string so we are checking that fix_ints() function correctly turns that string into a integer

    def test_fix_int_None(self, client):
        assert client.fix_floats("") is None
    #Just like for floats, API could have data missing so we can have to account for that. Checking from our empty row fixture that the empty srting will return None
    
    ''' fix rows tests '''
    def test_fix_rows(self, client, filled_row):
        a = client.fix_rows(filled_row)
        assert isinstance(a, TrafficObservation)
    #Here we are checking that fix_rows() function returns a TrafficOBservation objject. the isistance method checks that if it the right type
    
    def test_fix_rows_correct_site_name(self, client, filled_row):
        a = client.fix_rows(filled_row)
        assert a.site_name == "M25/4432A"
    #Here we are checking that the site name is correctly pulled from the sample row and stored in the object
    
    def test_fix_rows_correct_speed(self, client, filled_row):
        a = client.fix_rows(filled_row)
        assert a.avg_speed == 63
    #Here we are cehcking that the speed is correctly pulled from the sample row and stored in the object

    ''' mock tests '''
    @patch("webtris_client.requests.get")
    def test_func_returns_list(self, mock_get, client, succesful_mock_response):
        mock_get.return_value = succesful_mock_response
        a = client.get_daily_data(461, date(2026, 1, 3))
        assert isinstance(a, list)
    '''
    From our lecture notes, we learned that @patch("webtris_client.requests.get") replaces the requests.get with a mock object for our test so we dont have to 
    keep calling the API. This means that we are nevevr actually making a real network request. We then use mock_get.return_value to control what the requests.get
    returns. Just like how we did it in our lecture notes. 
    Afterward we check that our object is an instance of a list by giving our site_id and date. 
    '''
    
    @patch("webtris_client.requests.get")
    def test_func_returns_TrafficObservatin(self, mock_get, client, succesful_mock_response):
        mock_get.return_value = succesful_mock_response
        a = client.get_daily_data(461, date(2026, 1, 3))
        assert isinstance (a[0], TrafficObservation)
    #Here we are checking that each row in the fake response gets converted into a TrafficObservatiin object 

    @patch("webtris_client.requests.get")
    def test_error_handling(self, mock_get, client):
        mock_get.side_effect = Timeout("Connection Timed out")
        a = client.get_json_data({})
        assert a is None
    '''
    From out lecture notes, we leanrt to use side_effect to make requests.get raise an exception instead of returning a reponse
    This test tests that our Timeout block in the get_json_data() function catches the error and returns None instead of crashing
    '''



class TestSingleSite:
    ''' Pytest Fixtures for SingleSite '''
    @pytest.fixture
    def sample(self):
        recordings = [
            TrafficObservation(date(2026, 1, 3), time(8, 14, 0), "M25/4432A", 60.0, 200),
            TrafficObservation(date(2026, 1, 3), time(8, 29, 0), "M25/4432A", 55.0, 250),
            TrafficObservation(date(2026, 1, 3), time(9, 44, 0), "M25/4432A", 70.0, 100),
            TrafficObservation(date(2026, 1, 3), time(9, 59, 0), "M25/4432A", None, None),
        ]
        return SingleSite(site_id=461, site_name="M25/4432A", traffic_stats=recordings)
    
    @pytest.fixture
    def empty_sample(self):
        return SingleSite(site_id=461, site_name="M25/4432A", traffic_stats=[])
    
    ''' Average Speed tests '''
    def test_average_speed(self, sample):
        a = sample.average_speed()
        assert round(a, 2) == 61.67
    
    def test_average_speed_None(self, empty_sample):
        a = empty_sample.average_speed()
        assert a is None
    
    ''' Total # of cars tests '''    
    def test_number_of_cars(self, sample):
        a = sample.total_num_of_vehicles()
        assert a  == 550

    def test_total_num_of_cars_None(self, empty_sample):
        a = empty_sample.total_num_of_vehicles()
        assert a is None
    
    ''' Hour tests '''
    def test_total_num_of_cars_hour(self, sample, empty_sample):
        a = sample.total_num_of_vehicles_per_hour(8)
        b = empty_sample.total_num_of_vehicles_per_hour(7)
        assert a == 450
        assert b is None
    
    def test_peak_hour(self, sample, empty_sample):
        a = sample.peak_hour() 
        b = empty_sample.peak_hour()
        assert a == 8
        assert b is None
    
    ''' Iteration and Length tests '''
    def test_iter_returns_TrafficObservation(self, sample):
         for observation in sample:
            assert isinstance(observation, TrafficObservation)

    def test_length_sample(self, sample):
        assert len(sample) == 4

    def test_record_for_certain_hour(self, sample, empty_sample):
        a = sample.record_for_certain_hour(8)
        b = empty_sample.record_for_certain_hour(6)
        assert len(a) == 2
        assert b == []