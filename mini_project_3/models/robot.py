class Robot:
    # can carry products of only one type at a time, but no more than 40kg
    WAITING = 'waiting'
    UNLOAD = 'unload' # should take the product from [0,8] to the storage cell
    PICKUP = 'pickup' # should take the product from the storage cell to [0,9]
    
  
    def __init__(self, ) -> None:
        self.currentLocation = [0,8]
        self.route = None # the route will be created when the robot gets a task
        self.products = [] # the products the robot carries
        self.action = self.WAITING
        self.product_to_pick_up = None
    
    def available(self):
        return (self.route is None)
    
    def get_action(self):
        #waiting
        if self.available():
            return self.WAITING
        
        if len(self.products) == 0 and not self.available():
            return self.PICKUP
        
        else:
            return self.PICKUP
    

    
