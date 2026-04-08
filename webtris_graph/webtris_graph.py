from webtris_assignment.webtris_client import API, SingleSite
from datetime import date

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
            return f"{node} -> {neighbours}\n"
        return a