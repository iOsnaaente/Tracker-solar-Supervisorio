from threading import Thread

class Async_function( Thread ):
    def __init__(self, func, args = 0 ):
        Thread.__init__(self)
        self.func = func 
        self.args = args 
        self.retr = 0 
    
    def run( self ):
        self.retr = self.func( self.args )
    
    def return_val(self):
        return self.retr 
