'''
Crescimento crescente oK !!
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
    requests = []
    
    def __init__(self, topology, operacoes):
        SimPy.Simulation.Process.__init__(self)
        self.nodes = topology.nodes()
        self.edges = topology.edges()
        self.topology = topology
        self.op = operacoes
        self.random = Random()
        
    def execut(self, r):
        Simulador.Bloqueio = []
        Simulador.numReqBlocked = 0
        Simulador.requests = []
        time = 1
        
        for count in xrange(1, NUM_OF_REQUESTS+1):
            
            yield hold, self,  self.random.expovariate(r)
            
            src, dst = self.random.sample(self.nodes, 2)
            #print src, dst
            dmd = self.random.choice(BANDWIDTH)
            data = self.random.choice(DATA)
            path = nx.dijkstra_path(self.topology, src, dst, weight='weight')
            distance = int(self.op.distance(path, self.topology))
            deadline = self.random.choice(DEAD)    
            duracao = int(math.ceil(self.op.calculaTempoTrans(data,dmd)))
            num_slots = int(math.ceil(self.op.modulation(distance, dmd))) 
            holdingTime = int(math.ceil(data/float(dmd)))
            
            '''            
            print "distance", distance
            print "deadline", deadline
            print "duracao", duracao
            print "Slots", num_slots
            print "data", data
            print "dmd", dmd
            print ""#'''
            
            pular = self.random.randint(0, 1)
            if pular == 1:
                time = + 1
            
            req = Request(count, src, dst, time, data, deadline)
            req.numSlots = num_slots
            req.path = path
            req.duracao = duracao
            
            #print req
        
            slots = self.op.verificaPath(req.path, req.numSlots, req.time, req.duracao, self.topology) 
            #print slots
            #print req
            if slots[0] == True:
                #print "Slots Encontrados", slots
                req.slotsAlocados = slots[1]
                #print "Alocado", req.idReq
                
                self.op.allocar(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                     
                #pathBkp = self.op.buscarPathBackup(req.path, req.time, req.numSlots, req.duracao, self.topology)
                
                d = Desalocar(duracao)
                #SimPy.Simulation.initialize()
                SimPy.Simulation.activate(d, d.run(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology))
                #SimPy.Simulation.simulate(until=duracao)
            else:
                #print "Nao achou espaco", req
                Simulador.numReqBlocked +=1
        
        #self.op.printTopology(self.topology)
        print "Bloqueadas ", Simulador.numReqBlocked
        BloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        print "Bloqueio ", BloqueioTotal