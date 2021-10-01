import SimPy
from SimPy.Simulation import *
from request import *
from slot import *
from operacoes import *

op = Operacoes()

class Desalocar(SimPy.Simulation.Process):
    
    def __init__(self, holdTime):
        SimPy.Simulation.Process.__init__(self)
        self.holdingTime = holdTime

    def desalocar(self, src, dst, slot, inicial, final, topology):
        for t in range(inicial, final):
            topology[src][dst]['capacity'][slot].remove(t)
        #print "Desalocou"
        return True
        #return False

    def verDesalocar(self, idReq, src, dst, slot, inicial, final, topology):
        #print ">>>",idReq
        if topology[src][dst]['capacity'][slot].verificarSlotReq(inicial, idReq) == True:
            veri = self.desalocar(dst, src, slot, inicial, final, topology)
            if veri == True:
                #print idReq, slot
                return True
            return False
        else:
            return False 

    def run(self, req, tipoReq, qtdRetirar, topology):
        yield hold, self, self.holdingTime
        
        #print ">>>>>>>>>>>>>>>>>>>>...", tipoReq
        if tipoReq == 1:
            #print "Escolha1"
            inicial = req.time
            final = req.time + req.duracao             

            ini = 0
           
            for i in range(0, len(req.path)-1):
                for slot in range(0, len(req.slotsAlocados)):
                    if self.verDesalocar(req.idReq, req.path[i], req.path[i+1], req.slotsAlocados[slot], inicial, final, topology) == True:
                        ini += 1
                        if ini == qtdRetirar:
                            '''
                            print "Fim Int"
                            op.printTopology(topology)        
                            print "\n\n" #'''
                            return
                       
        if tipoReq == 2:
            
            #print "Escolha 2"
            inicial = req.timeBkp
            final = req.timeBkp + req.duracaoBkp             
            ini = 0
            tamPath = len(req.pathBkp)
            tamBkp = len(req.slotsAlocadosBkp)
            #print 'TAM', tamPath, tamBkp

            

            for i in range(1, len(req.pathBkp)):
                for slot in range(1, len(req.slotsAlocadosBkp)+1):
                    if self.verDesalocar(str(req.idReq)+"Bkp", req.pathBkp[tamPath-i], req.pathBkp[tamPath-(i+1)], req.slotsAlocadosBkp[tamBkp-slot], inicial, final, topology) == True:
                        ini += 1
                        if ini == qtdRetirar:
                            '''
                            print "Fim Int"
                            op.printTopology(topology)        
                            print "\n\n" #'''
                            return
            
            
            
            
            
            '''
            indice = []
            for i in range(1, len(req.pathBkp)):
                indice.append(i)
            indSlot = []
            for i in range(0, len(req.slotsAlocadosBkp)):
                indSlot.append(i)

            #print ">>>>", indice, indSlot
            
            
            for i in reversed(indice):
                #print "---", i
                for slot in reversed(indSlot):
                    if self.verDesalocar(str(req.idReq)+"Bkp", req.pathBkp[i], req.pathBkp[i-1], req.slotsAlocadosBkp[slot], inicial, final, topology) == True:
                        ini += 1
                        if ini == qtdRetirar:
                            
                            print "Fim Int"
                            op.printTopology(topology)        
                            print "\n\n" 
                            return               
            '''
