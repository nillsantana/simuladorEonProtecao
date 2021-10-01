'''
Prop 1, aloca 100% caminho primario e backup
'''

import SimPy
from SimPy.Simulation import *
from request import Request
from random import *
from config import *
import networkx as nx
import math
from desalocar import Desalocar


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
        Simulador.numReqAceita = 0
        Simulador.numReqBlocked = 0
        Simulador.requests = []
        Simulador.requestsAceitas = []
        Simulador.usSlot = 0
        Simulador.usBkp = 0
        Simulador.usSlotMedia = 0
        Simulador.usBkpMedia = 0
        
        for count in xrange(0, NUM_OF_REQUESTS+1):
            
            yield hold, self,  self.random.expovariate(r)
            src, dst = self.random.sample(self.nodes, 2)
            dmd = self.random.choice(BANDWIDTH)
            data = self.random.choice(DATA)
            path = nx.dijkstra_path(self.topology, src, dst, weight='weight')
            distance = int(self.op.distance(path, self.topology))
            deadline = self.random.choice(DEAD)    
            duracao = int(math.ceil(self.op.calculaTempoTrans(data,dmd)))
            num_slots = int(math.ceil(self.op.modulation(distance, dmd))) 
            holdingTime = int(math.ceil(data/float(dmd)))
            
            pular = self.random.randint(0, 1)
            if pular == 1:
                Simulador.time = + 1
            
            req = Request(count, src, dst, Simulador.time, data, deadline)
            req.numSlots = num_slots
            req.path = path
            req.duracao = duracao

            slots = self.op.verificarPathPrimario(req.path, req.numSlots, req.time, req.duracao, self.topology) 
            
            if slots[0] == True:
                #print "Slots Encontrados", slots
                req.slotsAlocados = slots[1]
                #print "Alocado", req.idReq
                pathBkp = self.op.buscarPathBackup(req.path, req.time, dmd, req.duracao, self.topology)
                
                if pathBkp[0] == True:
                    req.slotsAlocadosBkp = pathBkp[1] 
                    req.pathBkp = pathBkp[2]
                    req.numSlotsBkp = pathBkp[3]

                    self.op.allocar(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                    self.op.allocar(str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.time, req.duracao, self.topology) 
                    #print "Alocado", req

                    Simulador.usSlot += req.numSlots
                    Simulador.usBkp += req.numSlotsBkp
                    Simulador.numReqAceita += 1
                    Simulador.requestsAceitas.append(req)
                    
                    #d = Desalocar(holdingTime)
                    #SimPy.Simulation.activate(d, d.run(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology))
                    #d2 = Desalocar(holdingTime)
                    #SimPy.Simulation.activate(d2, d2.run(req.idReq, req.pathBkp, req.slotsAlocadosBkp, req.time, req.duracao, self.topology))
                    
                else:
                    #print "Nao achou BKP", req
                    Simulador.numReqBlocked +=1        
            else:
                #print "Nao achou espaco", req
                Simulador.numReqBlocked +=1
        
            #self.op.utilizacaoRedeTempoReal(req.idReq, self.topology)
            #print req

        self.op.utilizacaoRede(self.topology)
        self.op.calcularFragmentacao(self.topology)
        #self.op.printTopology(self.topology)
        print "Bloqueadas ", Simulador.numReqBlocked
        #print "Aceitas ", Simulador.numReqAceita
        #print "Slot ", Simulador.usSlot
        #print "SlotBkp ", Simulador.usBkp
        
        Simulador.bloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        #Simulador.usSlotMedia = float(Simulador.usSlot) / float(Simulador.numReqAceita)
        #Simulador.usBkpMedia = float(Simulador.usBkp) / float(Simulador.numReqAceita)
        
        print "Bloqueio ", Simulador.bloqueioTotal
