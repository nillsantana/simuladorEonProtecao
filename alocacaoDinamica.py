import SimPy
from SimPy.Simulation import *
from request import *
from slot import *
from operacoes import *

op = Operacoes()

class AlocarDin(SimPy.Simulation.Process):
    
    def __init__(self, holdTime):
        SimPy.Simulation.Process.__init__(self)
        self.holdTime = holdTime

    def run(self, tipoReq, idReq, path, listSlots, timeInicial, duracao, topology, requisicoes):
        yield hold, self, self.holdTime
        final = timeInicial + duracao
        if tipoReq == 2:
            print "timeHolding", self.holdTime
            for p in range(len(path)-1):
                for slot in range(len(listSlots)):
                    for t in range(timeInicial, final):
                        s = topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t) 
                        
                        if type(s) == list:
                            #falta tratar o caso ['bkp', 999]

                            if ('r' in s): 
                                #print "slot", s
                                if len(s) == 1:
                                    topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].useTimeInSlot(t, [idReq])
                                    #print "Slot agora ", topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t)
                                #-----------------
                                else:   
                                    #e = requisicoes[c]
                                    print "Tem algo a mais ", s, " Slot ", listSlots[slot], idReq
                                #----------------------
                            else:
                                print "Problema nao contem, Eh um Erro"
                        else:
                            print "**-- Nao foi possivel alocar AlocDinamica", [idReq]
                            print "Conteudo ", s
                            #print req
                            break
            #print "Alocado ", idReq

        #op.printTopology(topology)