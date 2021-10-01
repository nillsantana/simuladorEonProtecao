'''
Prop 2, aloca 100% caminho primario e backup, usando lista de caminhos

Caminho de backup eh reservado, permitindo que requisicoes de baixa prioridade possar usar este caminho 

-> Caminho de bkp, vai ser apenas reservado nao ira ser alocado
-> Existe requisicoes de alta e baixa prioridade
-> Req de baixa prioridade poderao ser alocadas no caminho de bkp, desde que sejam disjuntas

'''

import SimPy
from SimPy.Simulation import *
from request import Request
from random import *
from config import *
import networkx as nx
import math
from desalocarUmPorUm import *


class Simulador(SimPy.Simulation.Process):
    
    Bloqueio = []
    numReqBlocked = 0
    numReqAceita = 0
    requests = []
    requestsAceitas = []
    
    bloqueioTotal = 0
    usSlot = 0
    usBkp = 0
    usSlotMedia = 0
    usBkpMedia = 0
    time = 1

    protegido = {}
    baixaPrioridadeAc = 0
    altaPrioridadeAc = 0
    baixaPrioridadeRc = 0
    altaPrioridadeRc = 0

    def __init__(self, topology, operacoes):
        SimPy.Simulation.Process.__init__(self)
        self.nodes = topology.nodes()
        self.edges = topology.edges()
        self.topology = topology
        self.op = operacoes
        self.random = Random()
        
    def execut(self, r):
        Simulador.bloqueioTotal = 0
        Simulador.Bloqueio = []
        Simulador.requestsAceitas = []
        Simulador.numReqAceita = 0
        Simulador.numReqBlocked = 0
        Simulador.requests = []
        Simulador.usSlot = 0
        Simulador.usBkp = 0
        Simulador.usSlotMedia = 0
        Simulador.usBkpMedia = 0
        Simulador.prazomedio = 0
        Simulador.MediaPrazo = 0
        Simulador.utilizacao = 0
        Simulador.fragmentacao = 0
        Simulador.time = 1
        Simulador.baixaPrioridadeAc = 0
        Simulador.altaPrioridadeAc = 0
        Simulador.baixaPrioridadeRc = 0
        Simulador.altaPrioridadeRc = 0
        Simulador.protegido = {}
        Simulador.utilizacaoReal = 0

        for count in xrange(1, NUM_OF_REQUESTS+1):
            
            yield hold, self,  self.random.expovariate(r)
            
            src, dst = self.random.sample(self.nodes, 2)
            data = self.random.choice(DATA)
            deadline = self.random.choice(DEAD)    
            duracao = deadline/2
            dmd = int(math.ceil(self.op.calculaTaxaMin(data, duracao)))
            holdingTime = duracao
            
            '''pular = self.random.randint(0, 1)
            if pular == 1:
                Simulador.time = + 1'''
            
            p = self.random.randint(0, 1)
            prioridade = p

            req = Request(count, src, dst, Simulador.time, data, deadline)
            req.duracao = duracao
            # 0 -> baixa prioridade
            # 1 -> alta prioridade
            req.prioridade = prioridade
             
            slots = self.op.buscarPathListUmPorUm(req, dmd, Simulador.protegido,self.topology)
            
            if slots[0] == True:
                req.slotsAlocados = slots[1]
                req.path = slots[2]
                req.numSlots = len(slots[1])
                pathBkp = self.op.buscarPathBackupList(req.path, req.time, dmd, req.duracao, self.topology)
                
                if pathBkp[0] == True:
                    req.slotsAlocadosBkp = pathBkp[1] 
                    req.pathBkp = pathBkp[2]
                    req.numSlotsBkp = pathBkp[3]

                    self.op.allocarUmPorUm(1, req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                    self.op.allocarUmPorUm(2, str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.time, req.duracao, self.topology)                     
                    Simulador.requestsAceitas.append(req)

                    Simulador.usSlot += req.numSlots
                    Simulador.usBkp += req.numSlotsBkp
                    Simulador.prazomedio += duracao
                    Simulador.numReqAceita += 1

                    if req.prioridade == 0:
                        Simulador.baixaPrioridadeAc += 1
                    else:
                        Simulador.altaPrioridadeAc += 1

                    Simulador.protegido[str(req.idReq)+"Bkp"] = req.path 

                    
                    d = DesalocarUmPorUm(holdingTime)
                    SimPy.Simulation.activate(d, d.run(1, req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology))
                    d2 = DesalocarUmPorUm(holdingTime)
                    SimPy.Simulation.activate(d2, d2.run(2, str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.time, req.duracao, self.topology))
                    
                else:
                    #print "Nao achou BKP", req
                    Simulador.numReqBlocked +=1#'''
                    if req.prioridade == 0:
                        Simulador.baixaPrioridadeRc += 1
                    else:
                        Simulador.altaPrioridadeRc += 1

            else:
                #print "Nao achou espaco", req
                Simulador.numReqBlocked +=1
                if req.prioridade == 0:
                    Simulador.baixaPrioridadeRc += 1
                else:
                    Simulador.altaPrioridadeRc += 1

            Simulador.utilizacaoReal = Simulador.utilizacaoReal + self.op.utilizacaoRedeTempoRealUmPorUm(req.idReq, self.topology)
            #print req
        
        Simulador.utilizacao = Simulador.utilizacaoReal/float(NUM_OF_REQUESTS)

        Simulador.fragmentacao = self.op.calcularFragmentacaoUmPorUm(self.topology)
        
        print "Utilizacao ", Simulador.utilizacao
        print "Fragmentacao ", Simulador.fragmentacao
        
        Simulador.bloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        Simulador.usSlotMedia = float(Simulador.usSlot) / float(Simulador.numReqAceita)
        Simulador.usBkpMedia = float(Simulador.usBkp) / float(Simulador.numReqAceita)
        Simulador.MediaPrazo = float(Simulador.prazomedio) / float(Simulador.numReqAceita)
        
        print "Bloqueio ", Simulador.bloqueioTotal
	print "Tempo ", Simulador.MediaPrazo
	
