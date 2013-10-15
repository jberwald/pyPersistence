# must be in the local directory
import persistence_diagrams as pd
import persistence_tools as ptools

# opaque wrapper around Diagram pd.Diagram class
class PersistenceDiagram( pd.Diagram ):
    """
    Wraps pd.Diagram and provides narrow interface.
    """
    def __init__( self, diagram, dim=None ):
        """
        diagram : numpy.array ( N x 2 ) or path to a text file containing such an array.
        """
        pd.Diagram.__init__( self, diagram, dim )

    # Add custom diagram methods below

class DiagramCollection( PersistenceDiagram ):
    """
    """
    def __init__( self, diagrams=None ):
        """
        diagrams : Initialize with a set of PersistenceDiagrams, or
        initialize empty object and add using add_diagram() method.
        """
        if diagrams is not None:
            if not hasattr( diagrams, '__getitem__' ):
                raise AttributeError, "diagrams collection must be iterable!"
            else:
                self.diagrams = diagrams
        else:
            self.diagrams = []

    def add_diagram( self, new_diagram ):
        """
        new_diagram : PersistenceDiagram object, or N x 2 array of
        birth/death times.
        """
        if new_diagram.__class__ != 'diagram.PersistenceDiagram':
            new_diagram = PersistenceDiagram( new_diagram )
        self.diagrams.append( new_diagram )
