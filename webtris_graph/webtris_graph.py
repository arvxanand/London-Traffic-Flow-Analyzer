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

def make_road_system_graph(day: date) -> Graph:
    client = API()
    graph = Graph({})
    #objectts for API and Graph class to use

    for node in ["J7", "J12", "J13", "J14", "Heathrow"]:
        graph.add_node(node)
    #Adding each of the nodes to the road system list 

    #each edge is stored as (start_node, end_node, the edge key, and the distance)
    edges = [
        ("J7", "J12", "7-12", 23),
        ("J12", "J13", "12-13", 3),
        ("J13", "J14", "13-14", 3),
        ("J14", "Heathrow", "14-Heathrow", 3),
        ("J13", "Heathrow", "A30", 3.8),
    ]

    #Looping through each edge and find its travel time
    for start_node, end_node, key, distance in edges:
        sensors = EDGE_SENSORS[key] #get a list of sensors from our sensors dictionary 
        speed = get_average_speed(sensors, client, day) #call the function that gets the speed from every snesor and averages them
        if speed is None or speed == 0:
            #Handle missing data or zero speed data
            travel_time = None
        else:
            travel_time = (distance / speed) * 60
        if travel_time is not None:
            #Check if value exists because you cant round a 0 or a value that doesnt exist
            rounded_travel_time = round(travel_time, 2)
            graph.add_edges(start_node, end_node, rounded_travel_time)
        print(f"{start_node} -> {end_node}: {rounded_travel_time} mins (avg speed {speed} mph)")

    # Route B has no sensors so we hardcoded it as 20 minutes
    graph.add_edges("J12", "Heathrow", ROUTE_B_HARDCODED_MINUTES)
    print("J12 -> Heathrow: 20.0 mins (hardcoded, no sensors)")

    #reutns the fully built graoh with all the nodes and edges 
    return graph
    
