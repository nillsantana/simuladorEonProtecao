'''
Prop 4Rev, aloca 50% caminho primario e backup, usando lista de caminhos, desalocacao dinamica reversa
'''

import SimPy
from SimPy.Simulation import *
from request import Request
from random import *
from config import *
import networkx as nx
import math
from desalocar import *
from desalocarPorSlotRev import *

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
        Simulador.time = 1
        
        for count in xrange(1, NUM_OF_REQUESTS+1):
            
            yield hold, self,  self.random.expovariate(r)
            src, dst = self.random.sample(self.nodes, 2)
            data = self.random.choice(DATA)
            deadline = self.random.choice(DEAD)    
            duracao = int(deadline/2)
            dmd = int(math.ceil(self.op.calculaTaxaMin(data, duracao)))
            #holdingTime = int(math.ceil(data/float(dmd)))
            holdingTime = duracao

            pular = self.random.randint(0, 1)
            if pular == 1:
                Simulador.time = + 1
            
            req = Request(count, src, dst, Simulador.time, data, deadline)
            req.duracao = duracao
            req.duracaoBkp = duracao
        
            slots = self.op.buscarPathList(req, dmd, self.topology)
            if slots[0] == True:
                req.slotsAlocados = slots[1]
                req.path = slots[2]
                req.numSlots = len(slots[1])
                #print "Req", req

                pathBkp = self.op.buscarPathBackupList(req.path, req.time+duracao, dmd, duracao, self.topology)
                
                if pathBkp[0] == True:
                    req.slotsAlocadosBkp = pathBkp[1] 
                    req.pathBkp = pathBkp[2]
                    req.numSlotsBkp = pathBkp[3]
                    req.timeBkp = req.time+duracao

                    self.op.allocar(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                    self.op.allocar(str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.timeBkp, req.duracao, self.topology) 
                    
                    Simulador.usSlot += req.numSlots
                    Simulador.usBkp += req.numSlotsBkp
                    Simulador.numReqAceita += 1
                    #print "Alocado", req
                    Simulador.requestsAceitas.append(req)        

                    #hts = (holdingTime/(len(req.path)-1))/req.numSlots
                    #htsbkp =  (holdingTime/(len(req.pathBkp)-1))/req.numSlotsBkp

                    #Quando caminho primario menor que bkp, desalocacao normal, desaloca de uma vez
                    if len(req.path) > len(req.pathBkp):
                        #print "opcao 1"
                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        #print "Qtd Slots", num, num2

                        d = Desalocar(duracao)
                        d2 = Desalocar(duracao)
                        SimPy.Simulation.activate(d2, d2.run(req, 2, num2, self.topology))    
                        SimPy.Simulation.activate(d, d.run(req, 1, num, self.topology))    


                    if len(req.path) < len(req.pathBkp):
                        #print "opcao 2"
                        hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                        htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                        
                        retirar = int(hts/htsBkp)
                        #print "params ->", hts, htsBkp, retirar
                        
                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)

                        problema = False                        

                        if hts > 0.0 and htsBkp > 0.0:

                            n = 0
                            m = 0
                            while n < duracao:
                                n += hts
                                d = Desalocar(n)
                                SimPy.Simulation.activate(d, d.run(req, 2, retirar, self.topology))
                                d2 = Desalocar(n)
                                SimPy.Simulation.activate(d2, d2.run(req, 1, 1, self.topology))    
                                    
                        else:
                            problema = True
                            print "problema"
                           
                        if problema == False:
                            totalretiradoBkp = num*retirar 
                            if num2 > totalretiradoBkp:
                                retirar = num2 - totalretiradoBkp
                                d = Desalocar(0)
                                SimPy.Simulation.activate(d, d.run(req, 2, retirar, self.topology))
                        
                    if len(req.path) == len(req.pathBkp):
                        #print "opcao 3"
                        #print "Entrou"

                        num = req.numSlots*(len(req.path)-1)                            
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                        htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                        retirar = int(hts/htsBkp)
            
                        if hts > 0.0 and htsBkp > 0.0:
                            n = 0
                            while n < duracao:
                                    n += hts
                                    d2 = Desalocar(n)
                                    SimPy.Simulation.activate(d2, d2.run(req, 2, 1, self.topology))    
                                    d = Desalocar(n)
                                    SimPy.Simulation.activate(d, d.run(req, 1, 1, self.topology))  
                                    #n += hts    
            
                        else:
                            print "problema"
                            print "params ->",hts, htsBkp, retirar
                            print "Num", num, "NUM2", num2
             
                else:
                    #print "Nao achou BKP", req
                    Simulador.numReqBlocked +=1#'''
        
            else:
                #print "Nao achou espaco", req
                Simulador.numReqBlocked +=1
            
            #self.op.utilizacaoRedeTempoReal(req.idReq, self.topology)
            #print req


        self.op.utilizacaoRede(self.topology)
        self.op.calcularFragmentacao(self.topology)
        #self.op.printTopology(self.topology)
        print "\n\n"
        print "Bloqueadas ", Simulador.numReqBlocked
        print "Aceitas ", Simulador.numReqAceita
        print "Slot ", Simulador.usSlot
        print "SlotBkp ", Simulador.usBkp
        
        Simulador.bloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        Simulador.usSlotMedia = float(Simulador.usSlot) / float(Simulador.numReqAceita)
        Simulador.usBkpMedia = float(Simulador.usBkp) / float(Simulador.numReqAceita)
        
        print "Bloqueio ", Simulador.bloqueioTotal
        