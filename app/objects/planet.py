# -*- coding: utf-8 -*-

from agglomerate import Agglomerate
import models.planet as modelType

class Planet(Agglomerate):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, *args, **kwargs ):
        Agglomerate.__init__( self, *args, **kwargs )

    # METHODS
    def createModel( self, *args, **kwargs ):
        self.model = modelType.Planet( self, *args, **kwargs )
