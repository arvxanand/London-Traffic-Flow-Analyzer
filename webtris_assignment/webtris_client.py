from requests.exceptions import HTTPError, RequestException, Timeout
from dataclasses import dataclass
from datetime import date, time, datetime
import requests

@dataclass(order=True) #For the class instructions it was said to have the variabls chronicallically. What order= True does is that it checks the 
#observation date. If they both equal then it moves to time period ending. Checks if that is both equal and then keeps moving 
class TrafficObservation:
    def __init__(self, observation_date : date, time_period_ending: time, site_name: str, avg_speed: float | None, total_vehicles: int | None):
        self.observation_date = observation_date
        self.time_period_ending = time_period_ending
        self.site_name = site_name
        self.avg_speed = avg_speed
        self.total_vehicles = total_vehicles

    def has_all_the_data(self) -> bool:
        #Here we are checking to see if the values are both True. If the values are None then the pytest fails. 
        return self.avg_speed is not None and self.total_vehicles is not None

    def __str__(self) -> str:
        speed = "No Value" if self.avg_speed is None else f"{self.avg_speed}"
        vehicles = "No Value" if self.total_vehicles is None else f"{self.total_vehicles}"
        return(
            #.isoformat() turns a date into YYYY-MMM-DD. An example of that is 2026-03-04
            #Had to search this up to figure out how to do this
            f"{self.site_name} {self.observation_date.isoformat()} " 
            #.strftime() turns time into a whatever you decide to set it to
            # In this case I've set it Hour:Minute:Second. Had to search this up to figure out how to do this
            f"{self.time_period_ending.strftime('%H:%M:%S')}" 
            f", Total Vehicles = {vehicles}, Speed = {speed}"
        )


class API():
    def __init__(self, base_url = "https://webtris.nationalhighways.co.uk/api/v1.0"):
        self.base_url = base_url
    #Setting a value for the base url makes it easier to reference the base url without having the long url in our code everyhere. 
    #It makes the code much more readable. 

    def get_json_data(self, parameters: dict):
        try:
            response = requests.get(f"{self.base_url}/reports/daily", params=parameters, timeout = 10) 
            #We first get the base url we created earlier and then add the endpoints to it to tell the computer where we want to go. We then have the parameters
            #to filter it down more to get detailed as to what kind of data we want because there could be hundreds thousands of data in endpoint. 
            #The timeout is there to say that if this doesnt run after 10 seconds then raise an error
            response.raise_for_status()
            return response.json() #From the notes, this Converts 4xx/5xx status codes into exceptions so that we can see what they are 
        except (Timeout, HTTPError, RequestException):
            return [] #returning an empty list and raisining any exceptions. 
    #Values like avg mph in the example are strings or some values can be empty strings. 
    def fix_floats(self, value: str) -> float | None:
        ''' Here we are converting any float strings into actual floats or if the value is empty we return None '''
        if value == "":
            return None
        return float(value)
    
    #Values like total volume in the example are strings or some values can be empty strings. 
    def fix_ints(self, value: str) -> int | None:
        ''' Here we are converting any integer strings into actual integers or if the value is empty we return None '''
        if value == "":
            return None
        return int(value)
    
    def fix_rows(self, row: dict) -> TrafficObservation:
        observation_date = datetime.strptime(row["Report Date"], "%Y-%m-%dT%H:%M:%S").date()

        time_period_ending = datetime.strptime(row["Time Period Ending"], "%H:%M:%S").time()

        avg_speed = self.fix_floats(row["Avg mph"])
        total_vehicles = self.fix_ints(row["Total Volume"])
        #The reason why we are creating all these new values is because when the API gives us JSON data we need to take each row of data and turn it into
        #Traffic obserervations object. The API gives us date and time as strings so we need to take those and turn them into date and time and then 
        #turn the speed and vechiles into floats and int using the functions we created earlier

        return TrafficObservation(observation_date=observation_date, 
            time_period_ending=time_period_ending, 
            site_name=row["Site Name"], 
            avg_speed=avg_speed, 
            total_vehicles=total_vehicles)
        #Here we are simply returning the converted JSON data into actual readable Python obejcts that we can use to calcuate things later on. 
    
    def get_daily_data(self, site_id: int, single_day: date) -> list[TrafficObservation]: 
        '''This method is thee actual method that actually gets all the data about traffic and then turns it into Traffic Observatoom objects'''
        #The reason we do this is because the API doesnt take in python dates so we have to convert it to how it shows in the example that was given in the assigment brief. 
        proper_formatted_day = single_day.strftime("%d%m%Y") #strftime converts a date into a string 
        #date(2025, 10, 19) because "19102025"

        parameters = {
            "sites": site_id, #this just tells the API which certain data we want from a certain site
            "start_date": proper_formatted_day,#assigment says we should onlt get data from a single so tahts why the start and end date are the same
            "end_date": proper_formatted_day, 
            "page": 1,
            "page_size": 500} #reason i have page as 1 and page size as 500 because in the example url this is what was given. 
    
        #The resason we have parameters is because the get_json_data method we made earlier attaches the paramaters to the URL. 
        json_data = self.get_json_data(parameters)

        if not isinstance(json_data, dict) or "Rows" not in json_data:
            return []
        #If it doesnt have a dictionary or doesnt have "Rows" in it just return an empty list

        traffic_data = [] #This is an empty list htat we are going to use to store all the Traffic Observations objects inside. 
        for info in json_data["Rows"]: #loop through each of the traffic record the API gives us from the "Rows" part of the API. the ["Rows"] is they key as to what we want
            a = self.fix_rows(info) #So after we get all the things like site name and avg speed we turn all of that into Traffic Observation objects
            traffic_data.append(a) #this just stores all those objects in the list we made and then we retun it. 
        return traffic_data
    


class SingleSite():
    def __init__(self, site_id: int, site_name: str, traffic_stats: list[TrafficObservation]):
        self.site_id = site_id #The assigment says that we have to store the site_id and site_name as atributes and also an 
        self.site_name = site_name #attribute for storing a sequence of Individual Traffic Observations
        self.traffic_stats = traffic_stats

    def load_from_client(self, client: API, day: date) -> None: #This function is simply just getting the API daat
        ''' Set client as our API class and run get_daily_data to get our API data to use in a list'''
        self.traffic_stats = client.get_daily_data(self.site_id, day)
        #Here we arelling the computer to use the client(which is the WebtisAPI class) to run the get_daily_data method that we made earlier 

    def average_speed(self) -> float | None:
        correct_speed_data = [mph_num for mph_num in self.traffic_stats if mph_num.avg_speed is not None]
        #This is like the for loops we learnt in class.
        #Basicallt means go through every single number in self.traffic_stats and then only keep the ones in the List that are not None. 

        if not correct_speed_data: #We do this because if for some reason every speed is empty we wont get an actual avg speed data so we should just return None instead
            return None

        total_speed = sum(mph_num.avg_speed for mph_num in correct_speed_data) #simplu just getting total number of all the speed combined together
        return total_speed / len(correct_speed_data) #returning the average speed; avg = total# / # of speeds
    
    def total_num_of_vehicles(self) -> int | None:
        correct_vehicle_data = [vehicles for vehicles in self.traffic_stats if vehicles.total_vehicles is not None]

        if not correct_vehicle_data:
            return None
        
        all_vehicles = sum(vehicles.total_vehicles for vehicles in correct_vehicle_data)
        return all_vehicles

    def record_for_certain_hour(self, hour: int) -> list[TrafficObservation]:
        return [data for data in self.traffic_stats if data.time_period_ending.hour == hour]
        #Assigment says we have to get all the records for a ceratin hour. So using a for loop we look through all traffic stats list
        #and if the hour number in the time period ending attribute (one in TrafficObservations) is the same as the hour then we return it. 
    
    def average_speed_per_hour(self, hour: int) -> float | None:
        correct_hours_data = [data for data in self.record_for_certain_hour(hour) if data.avg_speed is not None]
        #Just like for average_speed() we go through every list number for each hour mark and keep the ones that are not None

        if not correct_hours_data:
            return None
        #If speed is empty we wont get an aactual avg speed so we just return None instead

        total_speed_per_hour = sum(data.avg_speed for data in correct_hours_data) 
        #getting the total number of the speed values per hour.
        #If its hour 1 then we only get the total number of all the speeds in that hour range
        return total_speed_per_hour / len(correct_hours_data)
        #returing the avg speed per hour; avg = total / # of speed data in the list
    
    def total_num_of_vehicles_per_hour(self, hour: int) -> int | None:
        correct_vehicle_data = [vehicles for vehicles in self.record_for_certain_hour(hour) if vehicles.total_vehicles is not None]
        #Just like for avg speed per hour we go through every single number in the list based on the hour number and return a new list where the news ones dont have None

        if not correct_vehicle_data:
            return None
        #If none of the values in the new list exists then return None 
        
        all_vehicles = sum(vehicles.total_vehicles for vehicles in correct_vehicle_data)
        #We go through each of the values in the list and we add up the number of cars together into one number
        return all_vehicles
        #Then return that number to find the total number of cars in the certain hour frame
    
    def peak_hour(self) -> int | None:
        if not self.traffic_stats:
            return None
        #Saying that if that there are no values at all then there can not be a peak hour so just return None
        
        busiest_hour = 0 
        most_cars = self.total_num_of_vehicles_per_hour(0)
        #Set the busiest hour to 0 first and then later on we check if any hour is bigger. Busiest hour then gets updated if another hour is bigger
        #most # of cars get set to the number in the 0 hour. So if theres 20 cars in the 0 hour and then 30 in the 1st hour then most_cars gets updated to 30

        for hour in range(1, 24): #loop through all the hours. start at 1 because we already used 0 as starting value
            current_num_of_cars = self.total_num_of_vehicles_per_hour(hour) #current cars is equal to the number of cars we get from the method in a certain hour mark based on our for loop
            if current_num_of_cars is not None: #because method above can return int or None we have to handle None as well in case we dont get any values for num of cars from the method
                if most_cars is None or current_num_of_cars > most_cars: 
                    most_cars = current_num_of_cars
                    busiest_hour = hour
        #Checking if current cars we have is greater then most cars. If so then we change the value of most cars to the current number of cars and then set the busiest hour to what the hour number
        #was in the for loop. We alos check to see if most cars is None

        return busiest_hour
        #simply just returning the busisest hour so we know what the peak hour is. 

    def __len__(self) -> int:
        return len(self.traffic_stats) # Here we are returning the number of values in the list attributre we created

    def __iter__(self):
        return iter(self.traffic_stats) #Here we are returning an iterated list of observations which is just a list of the TrafficObservations class that
        #contains all the values we are pulling from the API. 7


#Amputation in Data and Imputation 