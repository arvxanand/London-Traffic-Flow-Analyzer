class Graph:
    def __init__(self, road_system: dict):
        self.road_system = road_system
    '''
    Here we are using a dictionary to store the road system. 
    Each place is a key (ex. J7). For example J7 is the place we can leave from.
    The value we get (ex. "J8": {"J9", 30.1} are all the roads that i acn get to going from J7. 
    The numbers in there are called weights or the in plain english the average speed between the two roads.
    {
        #   "J7":  {"J8", 45.2}, #From J7 we can only go to J8 and the road that takes us there has an average speed of 45.2 mph
    }
    '''
    
    def add_node(self, road: str) -> None: #nodes are the physcial places on the map like Gatwick, J7, J8....
        if road not in self.road_system:
            self.road_system[road] = {}
        #We are checking that exists first because we dont want to make a new one accidently and delete out any of the edges that were apart of it
    
    def add_edges(self, start_node: str, end_node: str, weight: float): #Edges are the roads between two places. EX: Road between J7 and J8
        if start_node not in self.road_system:
            raise ValueError(f"{start_node} not in list.")
        if end_node not in self.road_system:
            raise ValueError(f"{end_node} not in list")
        #I am raising errors here because....
        
        self.road_system[start_node][end_node] = weight
        '''
        When we do 'self.road_system[road] = {}' this gets created: "J7": {}
        Now when we do the [][] = weight above, we then create {"J7": {"J8": 45.2}}
        '''

    def get_all_roads(self, node: str) -> list:
        if node not in self.road_system:
            raise ValueError()
        
        return self.road_system[node]
    
    