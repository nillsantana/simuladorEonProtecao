'''
Prop 8 - Elastica
    | - aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4 , usando lista de caminhos, desalocacao dinamica
    o caminho de backup pode ser alocado de forma dinamica
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

import copy 

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
    requisicoes = {}
    protegido = {}
    tempoSim = 0
    reqElastica = []

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
        Simulador.tempoSim = 0
        Simulador.reqElastica = []

        Simulador.protegido = {}
        Simulador.requisicoes = {}

        for count in xrange(1, NUM_OF_REQUESTS+1):
            a = self.random.expovariate(r)
            yield hold, self, a
            
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
            req.timeSimIni = a

            for p in range(0, len(prazos)):
                dmd = int(math.ceil(self.op.calculaTaxaMin(data, prazos[p])))
                req.duracao = prazos[p]
                slots = self.op.buscarPathListUmPorUm(req, dmd, Simulador.protegido,self.topology)

                if slots[0] == True:
                    duracao = prazos[p]
                    duracaobkp = prazosbkp[p]
                    break
                    req.duracao = duracao
            
            #print "Iniciou a busca da req",req.idReq ," ", now(), " " ,req.duracao, " " ,duracaobkp
            req.timeSimulacao = now()
            
            if slots[0] == True:
                req.slotsAlocados = slots[1]
                req.path = slots[2]
                req.numSlots = len(slots[1])
                req.holdingSlotPrim = float(req.duracao) / float(req.numSlots)
                    
                req.timeBkp = req.time+duracao
                req.duracaoBkp = duracaobkp

                if req.path > req.pathBkp:
                    req.casoDes = 1
                elif req.path < req.pathBkp:
                    req.casoDes = 2
                else:
                    req.casoDes = 3
                    
                dmdbkp = int(math.ceil(self.op.calculaTaxaMin(data, duracaobkp)))
                
                pathBkp = self.op.buscarPathBackupList(req, dmdbkp, Simulador.requisicoes, now(), self.topology) 
                
                if pathBkp[0] == True:
                    #print "Retorno PATH BKP ", pathBkp
                           
                    if len(pathBkp) >= 4:
                        #print "Utiliza protecao elastica" 
                        
                        #pathBkp = [True, [path], [bloco de slots livres], [slots que serao alocados futuramente]]    
                        req.pathBkp = pathBkp[1]
                        req.slotsAlocadosBkp = pathBkp[2]
                        req.slotsAdicionaisBkp = pathBkp[3]
                        req.numSlotsBkp = len(pathBkp[2]) + len(pathBkp[3])
                        req.holdingSlotPrim = float(req.duracao) / float(req.numSlots)
                        req.holdingSlotBkp =  float(req.duracaoBkp) / float(req.numSlotsBkp)
                        
                        #print req
                        self.op.allocarUmPorUm(1, req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                        self.op.allocarUmPorUm(2, str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.timeBkp, req.duracaoBkp, self.topology) #req.timeBkp
                        #self.op.printTopology(self.topology)
                        
                        req.casoDes = 1

                        for i in range(len(req.slotsAdicionaisBkp)):
                            req.slotsAlocadosBkp.append(req.slotsAdicionaisBkp[i])
                        
                        Simulador.reqElastica.append(req) # array com todas requisicoes elasticas
                    else:
                    
                        #pathBkp = [True, [path], [bloco de slots livres]]
                        req.pathBkp = pathBkp[1]
                        req.slotsAlocadosBkp = pathBkp[2]
                        req.numSlotsBkp = len(pathBkp[2])
                        req.contSlot = req.numSlots*(len(req.path)-1)
                        req.contSlotBkp = req.numSlotsBkp*(len(req.pathBkp)-1)
                        req.holdingSlotPrim = float(req.duracao) / float(req.numSlots)
                        req.holdingSlotBkp =  float(req.duracaoBkp) / float(req.numSlotsBkp)
                        req.casoDes = 1  
                        self.op.allocarUmPorUm(1, req.idReq, req.path, req.slotsAlocados, req.time, req.duracao, self.topology)
                        self.op.allocarUmPorUm(2, str(req.idReq)+"Bkp", req.pathBkp, req.slotsAlocadosBkp, req.timeBkp, req.duracaoBkp, self.topology) #req.timeBkp
                        #self.op.printTopology(self.topology)            

                    # ------------------------------------------------------------------------------------------------------------
                    #print req
                    Simulador.usSlot += req.numSlots
                    Simulador.usBkp += req.numSlotsBkp
                    Simulador.prazomedio += duracao
                    Simulador.numReqAceita += 1
                    #print "Alocado", req

                    Simulador.requisicoes[req.idReq] = copy.copy(req)
                    Simulador.protegido[str(req.idReq)+"Bkp"] = req.path 
                    holdingTime = duracao
                    holdingTimebkp = duracaobkp

                    #caso 1
                    if req.casoDes == 1:
                        #if len(req.path) > len(req.pathBkp)
                        #print "Caso 1"
                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        d = Desalocar(duracao)
                        d2 = Desalocar(duracaobkp)
                        #print "Opcao 1", duracao, duracaobkp
                        SimPy.Simulation.activate(d2, d2.run(req, 2, num2, self.topology))    
                        SimPy.Simulation.activate(d, d.run(req, 1, num, self.topology))    

                        #print "Removido ", req

                    #caso 2
                    if req.casoDes == 2:
                        #if len(req.path) < len(req.pathBkp)
                        #print "Caso 2"
                        hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                        htsBkp = (holdingTimebkp/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)                        
                        retirar = int(hts/htsBkp)
                        
                        if retirar == 0:
                            hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                            htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                            retirar = int(hts/htsBkp)
                            
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

                        #print "Removido ", req

                    #caso 3
                    if req.casoDes == 3:
                        #if len(req.path) == len(req.pathBkp):
                        #print "Caso 3"

                        num = req.numSlots*(len(req.path)-1)
                        num2 = req.numSlotsBkp*(len(req.pathBkp)-1)
                        hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                        htsBkp = (holdingTimebkp/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                        retirar = int(hts/htsBkp)
                        
                        if retirar == 0:
                            hts = (holdingTime/float(len(req.path)-1))/float(req.numSlots)
                            htsBkp = (holdingTime/float(len(req.pathBkp)-1))/float(req.numSlotsBkp)
                            retirar = int(hts/htsBkp)
                        
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
                    
                        #print "Removido ", req

                else:
                    Simulador.numReqBlocked +=1

            else:
                Simulador.numReqBlocked +=1

            #self.op.utilizacaoRedeTempoRealUmPorUm(req.idReq, self.topology)
            #print req

        #print "final"
        #self.op.printTopology(self.topology)
        Simulador.utilizacao = self.op.utilizacaoRedeUmPorUm(self.topology)
        Simulador.fragmentacao = self.op.calcularFragmentacaoUmPorUm(self.topology)
        
        #print "Utilizacao ", Simulador.utilizacao
        #print "Fragmentacao ", Simulador.fragmentacao
        '''
        for i in Simulador.requisicoes: 
            r = Simulador.requisicoes[i]
            print r
        '''
        Simulador.bloqueioTotal = float(Simulador.numReqBlocked) / float(NUM_OF_REQUESTS)
        Simulador.usSlotMedia = float(Simulador.usSlot) / float(Simulador.numReqAceita)
        Simulador.usBkpMedia = float(Simulador.usBkp) / float(Simulador.numReqAceita)
        Simulador.MediaPrazo = float(Simulador.prazomedio) / float(Simulador.numReqAceita)
        
        print "Bloqueio ", Simulador.bloqueioTotal
        print "ReqElastica ", len(Simulador.reqElastica), " Req normais ", (len(Simulador.requisicoes)-len(Simulador.reqElastica))
	#print "Tempo ", Simulador.MediaPrazo
