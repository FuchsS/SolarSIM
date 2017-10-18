# -*- coding: utf-8 -*-

from agglomerate import Agglomerate
import models.moon as modelType

class Moon(Agglomerate):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, *args, **kwargs ):
        Agglomerate.__init__( self, *args, **kwargs )

    # METHODS
    def createModel( self, *args, **kwargs ):
        self.model = modelType.Moon( self, *args, **kwargs )
