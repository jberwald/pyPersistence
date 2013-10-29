import cyWasserstein as cw
import Wasserstein as w
import numpy as np

d1 = [[1,7],[1,1.1],[5,5.5]]
d2 = [[2,6],[3,3.5],[5,6]]
d3 = [[1,2],[2,4]]
d4 = [[1,4]]

e1 = np.random.normal( size=(100,2) ).tolist()
e2 = np.random.normal( size=(100,2) ).tolist()

cw_out1 = cw.WassDistDiagram( e1, e2, bottleneck=False, returnPairing=True )

print "cw out1: ", cw_out1
print "-----"
print ""


w_out1 = w.WassDistDiagram( e1, e2, bottleneck=False, returnPairing=True )
print "w out1: ", w_out1
