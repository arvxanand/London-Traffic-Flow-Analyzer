from webtris_assignment.webtris_client import API, SingleSite
from datetime import date
import time

class Graph:
    def __init__(self, road_system: dict):
        self.road_system = road_system
    #create an init function with a road system dictionary
    #The keys for the dict are the names of the node (ex. J7) and the values are the dictionaries of any conecting nodes and weights
    '''
    Here we are using a dictionary to store the road system. 
    Each place is a key (ex. J7). For example J7 is the place we can leave from.
    The value we get (ex. "J7": {"J8", 30.1} are all the roads that i acn get to going from J7. 
    The numbers in there are called weights or the in plain english the average speed between the two roads.
    {
        #   "J7":  {"J8", 45.2}, #From J7 we can only go to J8 and the road that takes us will take us 45.2 minutes. 
    }
    '''
    
    def add_node(self, road: str) -> None: #nodes are the physcial places on the map like Gatwick, J7, J8....
        if road not in self.road_system:
            self.road_system[road] = {}
        #We are checking that exists first because we dont want to make a new one accidently and delete out any of the edges that were apart of it
    
    def add_edges(self, start_node: str, end_node: str, weight: float): #Edges are the roads between two places. EX: Road between J7 and J8
        #Raises an error if either of the nodes dont exist in the graph
        if start_node not in self.road_system:
            raise ValueError(f"{start_node} not in list.")
        if end_node not in self.road_system:
            raise ValueError(f"{end_node} not in list")
        #add_edges("J7", "J8", 25) means that the road from J7 to J8 takes 25 minutes
        
        self.road_system[start_node][end_node] = weight
        '''
        When we do 'self.road_system[road] = {}' this gets created: "J7": {}
        Now when we do the [][] = weight above, we then go inside J7's dictionary and add the destination 
        and average speed into it, giving us: {"J7": {"J8": 45.2}}
        This means from J7 you can travel to J8 in 45.2 minutes
        '''

    def get_all_roads(self, node: str) -> dict:
        ''' Returns all the connecting nodes and the weights for a certain node '''
        if node not in self.road_system:
            raise ValueError(f"{node} not in list.")
        #Raises an error if the node does not exist
        
        return self.road_system[node]
    
    def __str__(self) -> str:
        ''' Returns a string of the graph '''
        a = ""
        for node, neighbours in self.road_system.items():
            a += f"{node} -> {neighbours}\n"
        return a

if __name__ == "__main__":
    sample_road_system = {
        "J7": {"J8": 45.2},
        "J8": {"J9": 30.1},
        "J9": {}
    }
    g = Graph(sample_road_system)
    print(g)

EDGE_SENSORS = {
    "7-12": [138, 144, 479, 544, 547, 598, 699, 752, 778, 885,
1069, 1135, 1221, 1270, 1442, 1479, 1914, 1990, 2005, 2089,
2097, 2149, 2419, 2486, 2530, 2636, 3003, 3323, 3437, 3714,
3835, 3897, 4000, 4092, 4145, 4202, 4223, 4714, 4719, 4761,
4894, 5107, 5118, 5138, 5176, 5261, 5288, 5457, 5526, 5546,
5712, 5842, 5875, 5914, 5990, 6156, 6252],
    "12-13":        [8, 1811, 1910, 2952, 2992, 3319, 5245, 5662, 5681],
    "13-14":        [279, 737, 3671, 4053, 4354, 5317],
    "14-Heathrow":  [746, 2153, 2977],
    "A30":          [9005],
}

# Storing the distances separately that came from the AE3 dataset
EDGE_DISTANCES = {
    "7-12":         23,
    "12-13":        3,
    "13-14":        3,
    "14-Heathrow":  3,
    "A30":          3.8,
}

ROUTE_B_HARDCODED_MINUTES = 20.0

def get_average_speed(sensor_ids: list, client: API, day: date) -> float | None:
    ''' Getting data from WebtrisAPI and finding the avg speed of the '''
    all_speeds = [] #create an empty list that we will add the speeds to
    for id in sensor_ids:
        s = SingleSite(site_id=id, site_name=str(id), traffic_stats=[]) #we create a singleSite object for the sensor and then we load the data from that day
        s.load_from_client(client, day)
        avg_speed = s.average_speed() #one sensor mightt have multiple recording of speed so we get the avg of all of them and turn them into one number
        if avg_speed is not None:
            all_speeds.append(avg_speed) #If data is not None, add that one number to the list where we will later find the avg of them 
        time.sleep(2) #dataset said to add 2 secone delays between API requets so we dont get blocked
    
    if not all_speeds:
        return None
    return sum(all_speeds) / len(all_speeds) #average all the speeds to get one number that we will use to calcuate the travel time
    '''
    For example if J7 to J12 has has multiple senors like [138, 144, ... ]and they return random speeds like [62, 36, 48....],
    We can then find the avg speed of all those speeds to find the time it takes to get from node to node. 
    '''

def make_road_system(day: date) -> Graph:
    client = API()
    graph = Graph({})

    for node in ["J7", "J12", "J13", "J14", "Heathrow"]:
        graph.add_node(node)
    
    #Edge 1 from J7 to J12 (23 miles + 57 sensors)
    edge1_distance = EDGE_DISTANCES["7-12"]
    edge1_sensors = EDGE_SENSORS["7-12"]
    speed = get_average_speed(edge1_sensors, client, day)
    if speed is None or speed == 0:
        travel_time = None
    else:
        travel_time = (edge1_distance / speed) * 60

    if travel_time is not None:
        rounded_travel_time = round(travel_time, 2)

    graph.add_edges("J7", "J12", rounded_travel_time)
    print(f"J7 -> J12: {rounded_travel_time} minutes (average speed: {speed} mph)")

    #Edge 2 from J12 to J13 (3 miles + 9 sensors)
    edge2_distance = EDGE_DISTANCES["12-13"]
    edge2_sensors = EDGE_SENSORS["12-13"]
    speed = get_average_speed(edge2_sensors, client, day)
    if speed is None or speed == 0:
        travel_time = None
    else:
        travel_time = (edge2_distance / speed) * 60
    if travel_time is not None:
        rounded_travel_time = round(travel_time, 2)
    graph.add_edges("J12", "J13", rounded_travel_time)
    print(f"J12 -> J13: {rounded_travel_time} mph (average speed: {speed} mph)")

    return graph
    
