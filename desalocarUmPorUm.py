# Utilizada na tematica 1:1

import SimPy
from SimPy.Simulation import *
from request import *

class DesalocarUmPorUm(SimPy.Simulation.Process):
    
    def __init__(self, holdTime):
        SimPy.Simulation.Process.__init__(self)
        self.holdTime = holdTime

    def run(self, tipoReq, idReq, Path, listSlots, TimeUse, duracao, topology):
        ini = TimeUse
        final = ini + duracao
        
        yield hold, self, self.holdTime
        
        if tipoReq == 1:
            
            for p in range(len(Path)-1):
                for i in range(len(listSlots)):
                    for t in range(ini, final):
                        #Tem um erro aki
                        topology[Path[p]][Path[p+1]]['capacity'][listSlots[i]].removePath(t, idReq)
                        
            #print "Desalocado", idReq, "Tipo Remocao ", tipoReq

        if tipoReq == 2:

            for p in range(len(Path)-1):
                for i in range(len(listSlots)):
                    for t in range(ini, final):
                        topology[Path[p]][Path[p+1]]['capacity'][listSlots[i]].removeBkp(t, idReq)


            #print "Desalocado", idReq, "Tipo Remocao ", tipoReq
