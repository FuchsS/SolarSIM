# -*- coding: utf-8 -*-

from agglomerate import Agglomerate
import models.star as modelType

class Star(Agglomerate):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, *args, **kwargs ):
        Agglomerate.__init__( self, *args, **kwargs )

    # METHODS
    def createModel( self, *args, **kwargs ):
        self.model = modelType.Star( self, *args, **kwargs )
