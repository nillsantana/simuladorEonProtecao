# Utilizada na tematica 1+1

import SimPy
from SimPy.Simulation import *
from request import *

class Desalocar(SimPy.Simulation.Process):
    
    def __init__(self, holdTime):
        SimPy.Simulation.Process.__init__(self)
        self.holdTime = holdTime

    def run(self, idReq, Path, listSlots, TimeUse, duracao, topology):
        ini = TimeUse
        final = ini + duracao
        
        yield hold, self, self.holdTime
        
        for p in range(len(Path)-1):
            for i in range(len(listSlots)):
                for t in range(ini, final):
                    topology[Path[p]][Path[p+1]]['capacity'][listSlots[i]].remove(t)
            
            #print "Desalocado", idReq
