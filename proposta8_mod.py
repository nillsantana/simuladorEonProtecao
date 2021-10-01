'''
Prop 5, aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4 , usando lista de caminhos, desalocacao dinamica
protecao 1:1
'''

import SimPy
from SimPy.Simulation import *
from request import Request
from random import *
from config import *
import networkx as nx
import math
from desalocar import *
from desalocarPorSlotUmPorUm import *

class Simulador(SimPy.Simulation.Process):
    
    Bloqueio = []
    numReqBlocked = 0
    numReqAceita = 0
    requests = []
    bloqueioTotal = 0
    usSlot = 0
    usBkp = 0
    usSlotMedia = 0
    usBkpMedia = 0
    time = 1

    protegido = {}

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
        Simulador.usSlot = 0
        Simulador.usBkp = 0
        Simulador.usSlotMedia = 0
        Simulador.usBkpMedia = 0
        Simulador.prazomedio = 0
        Simulador.MediaPrazo = 0
        Simulador.utilizacao = 0
        Simulador.fragmentacao = 0
        Simulador.time = 1

        Simulador.protegido = {}
        
        for count in xrange(1, NUM_OF_REQUESTS+1):
            
            yield hold, self, self.random.expovariate(r)
            prazos = []
            prazosbkp = []
            src, dst = self.random.sample(self.nodes, 2)
            data = self.random.choice(DATA)
            deadline = self.random.choice(DEAD)

            prazos.append(int(deadline/4))
            prazos.append(int(deadline/3))
            prazos.append(int(deadline/2))
            #duracao = int(deadline/2)
            #duracao = int(deadline)
            #dmd = int(math.ceil(self.op.calculaTaxaMin(data, duracao)))
            #holdingTime = int(math.ceil(data/float(dmd)))
            #holdingTime = duracao
            prazosbkp.append(int((deadline*3)/4))
            prazosbkp.append(int((deadline*2)/3))
            prazosbkp.append(int((deadline*1)/2))

            '''pular = self.random.randint(0, 1)
            if pular == 1:
                Simulador.time = + 1'''
            
            req = Request(count, src, dst, Simulador.time, data, deadline)
            req.prioridade = 0
            
            for p in range(0, len(prazos)):
                dmd = int(math.ceil(self.op.calculaTaxaMin(data, prazos[p])))
                req.duracao = prazos[p]
                #slots = self.op.buscarPathList(req.src, req.dst, req.data, dmd, req.time, req.duracao, self.topology)
                slots = self.op.buscarPathListUmPorUm(req, dmd, Simulador.protegido,self.topology)

                if slots[0] == True:
                    duracao = prazos[p]
                    duracaobkp = prazosbkp[p]
                    req.duracao = duracao
                    break

            if slots[0] == True:
                req.slotsAlocados = slots[1]
                req.path = slots[2]
                req.numSlots = len(slots[1])

                dmdbkp = int(math.ceil(self.op.calculaTaxaMin(data, duracaobkp)))
                #pathBkp = self.op.buscarPathBackupList(req.path, req.time+duracao, dmdbkp, duracaobkp, self.topology)
                pathBkp = self.op.buscarPathBackupList(req.path, req.time+duracao, dmdbkp, duracaobkp, self.topology)

                if pathBkp[0] == True:
                    req.slotsAlocadosBkp = pathBkp[1] 
                    req.pathBkp = pathBkp[2]
                    req.numSlotsBkp = pathBkp[3]
                    req.timeBkp = req.time+duracao
                    req.duracaoBkp = duracaobkp

                    self.op.allocarUmPorUm(1, req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                    self.op.allocarUmPorUm(2, str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.timeBkp, req.duracaoBkp, self.topology) #req.timeBkp
                    #self.op.allocar(req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                    #self.op.allocar(str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.timeBkp, req.duracaoBkp, self.topology) #req.timeBkp
                    
                    Simulador.usSlot += req.numSlots
                    Simulador.usBkp += req.numSlotsBkp
                    Simulador.prazomedio += duracao
                    Simulador.numReqAceita += 1
                    #print "Alocado", req

                    Simulador.protegido[str(req.idReq)+"Bkp"] = req.path 

                    holdingTime = duracao
                    holdingTimebkp = duracaobkp
                        
                    if len(req.path) > len(req.pathBkp):
                        #print "opcao 1"
                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        #print "Qtd Slots", num, num2

                        d = Desalocar(duracao)
                        d2 = Desalocar(duracaobkp)
                        SimPy.Simulation.activate(d2, d2.run(req, 2, num2, self.topology))    
                        SimPy.Simulation.activate(d, d.run(req, 1, num, self.topology))    
                                   
                    if len(req.path) < len(req.pathBkp):
                        #print "opcao 2"
                        hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                        htsBkp = (holdingTimebkp/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                        
                        retirar = int(hts/htsBkp)
                        #print "Hold ", holdingTime
                        #print "HoldBKP ", holdingTimebkp
                        #print "params ->", hts, htsBkp, retirar
                        
                        if retirar == 0:
                            hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                            htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                            retirar = int(hts/htsBkp)
                            #print "Novos params ->", hts, htsBkp, retirar
                            
                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        
                        problema = False                        

                        if hts > 0.0 and htsBkp > 0.0:

                            n = 0
                            d2 = Desalocar(duracao)
                            SimPy.Simulation.activate(d2, d2.run(req, 1, num, self.topology))
                            while n < duracao:
                                n += hts
                                d = Desalocar(n)
                                SimPy.Simulation.activate(d, d.run(req, 2, retirar, self.topology))    
                                    
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
                        htsBkp = (holdingTimebkp/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)

                        retirar = int(hts/htsBkp)
                        #print "Hold ", holdingTime
                        #print "HoldBKP ", holdingTimebkp
                        #print "params ->",hts, htsBkp, retirar

                        if retirar == 0:
                            hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                            htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                            retirar = int(hts/htsBkp)
                            #print "Novos params ->", hts, htsBkp, retirar

                        if hts > 0.0 and htsBkp > 0.0:

                            n = 0
                            d = Desalocar(duracao)
                            SimPy.Simulation.activate(d, d.run(req, 1, num, self.topology))
                            while n < duracaobkp:
                                    n += htsBkp
                                    d2 = Desalocar(n)
                                    SimPy.Simulation.activate(d2, d2.run(req, 2, 1, self.topology))    
            
                        else:
                            print "problema"
                            print "params ->",hts, htsBkp, retirar
                            print "Num", num, "NUM2", num2
             
                else:
                    #print "Nao achou BKP", req
                    Simulador.numReqBlocked +=1
        
            else:
                #print "Nao achou espaco", req
                Simulador.numReqBlocked +=1

            #self.op.utilizacaoRedeTempoRealUmPorUm(req.idReq, self.topology)
            #print req

        Simulador.utilizacao = self.op.utilizacaoRedeUmPorUm(self.topology)
        Simulador.fragmentacao = self.op.calcularFragmentacaoUmPorUm(self.topology)
        
        print "Utilizacao ", Simulador.utilizacao
        print "Fragmentacao ", Simulador.fragmentacao
        
        Simulador.bloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        Simulador.usSlotMedia = float(Simulador.usSlot) / float(Simulador.numReqAceita)
        Simulador.usBkpMedia = float(Simulador.usBkp) / float(Simulador.numReqAceita)
        Simulador.MediaPrazo = float(Simulador.prazomedio) / float(Simulador.numReqAceita)
        
        print "Bloqueio ", Simulador.bloqueioTotal
	print "Tempo ", Simulador.MediaPrazo
