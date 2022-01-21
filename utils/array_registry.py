class Array_registry: 
    def __init__(self, array : list = [], MAX_LEN : int = 10 ) -> None:
        self.MAX_LENGTH = MAX_LEN
        self.array = self.check_length( array )

    def check_length( self, array : list = None ) -> list:
        if array is None: 
            if len(self.array) > self.MAX_LENGTH: 
                self.array = self.array[-self.MAX_LENGTH : ]
        else: 
            if len(array) > self.MAX_LENGTH: 
                return array[-self.MAX_LENGTH : ]
            else: 
                return array 
            
    def add_value(self, value : float ) -> list : 
        self.array.append( value )
        self.check_length() 
        return self.array 
    
    def extend_array( self, array : list ) -> list : 
        self.array.extend( array )
        self.check_length() 
        return self.array

    def remove_index( self, index : float, qnt : int = 1 ) -> list :
        for _ in range( qnt ):
            self.array.pop( index )
        return self.array 
