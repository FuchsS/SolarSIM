# -*- coding: utf-8 -*-

from particle import Particle
import models.agglomerate as modelType

class Agglomerate(Particle):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, *args, **kwargs ):
        Particle.__init__( self, *args, **kwargs )

    # METHODS
    def createModel( self, *args, **kwargs ):
        self.model = modelType.Agglomerate( self, *args, **kwargs )
