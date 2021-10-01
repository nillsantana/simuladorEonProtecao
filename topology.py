import imp
import SimPy
from SimPy.Simulation import *
from config import *
import networkx as nx
from slot import Slot
from operacoes import *


topology = nx.read_weighted_edgelist('topology/' + TOPOLOGY, nodetype=int)
op = Operacoes()

def escolherSimulacao(opc, topology, actions):
    '''
    if opc == 1:
        print "P1 - 100% caminho primario e backup"
        from proposta1 import Simulador        
        return Simulador(topology, actions)
    
    if opc == 2:
        print "P2 - 100% caminho primario e backup, usando lista de caminhos - 1+1"
        from proposta2 import Simulador
        return Simulador(topology, actions)
    
    if opc == 2.1:
        print "P2 - 100% caminho primario e backup, usando lista de caminhos - 1:1"
        from util.proposta2_Mod import Simulador
        return Simulador(topology, actions)
    

    if opc == 3:
        print "P3 - 50% caminho primario e backup"
        from proposta3 import Simulador        
        return Simulador(topology, actions)

    if opc == 4:
        print "P4 - 50% caminho primario e backup, desalocacao dinamica"
        from proposta4 import Simulador        
        return Simulador(topology, actions)
    if opc == 5:
        print "P4-Rev - 50% caminho primario e backup, desalocacao dinamica reversa"
        from propostasAnteriores.roposta4Rev import Simulador        
        return Simulador(topology, actions)

    if opc == 6:
        print "P6 - Selecionada - Proposta 6"
        from proposta6 import Simulador        
        return Simulador(topology, actions)
    if opc == 7:
        print "P7 - Aloca igual P2 e desaloca igual P4"
        from proposta7 import Simulador        
        return Simulador(topology, actions)
    if opc == 8:
        print "P8 - Aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4, com desalocacao dinamica"
        from proposta8 import Simulador        
        return Simulador(topology, actions)
    '''
    if opc == 8.1:
        print "P8 - Aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4, com desalocacao dinamica, protecao 1:1"
        from proposta8_mod import Simulador        
        return Simulador(topology, actions)

    if opc == 8.2:
        print "P8 Elastica - Aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4, com desalocacao dinamica, protecao 1:1"
        from proposta8_Elastica import Simulador        
        return Simulador(topology, actions)
    
    

    else:
        print "Opcao Errada"


for e in xrange(ERLANG_MIN,  ERLANG_MAX + 1 , ERLANG_INC):
    
    bloqueio = []
    usSlot = []
    usBkp = []
    holdingTime = []
    util = []
    frag = []
    
    reps = 1
    for rep in xrange(reps):
        print "\n"
        print "Simulating for {} Erlangs ({})".format(e,rep)
        rate = e/HOLDING_TIME
    
        for u, v in topology.edges():
            topology[u][v]['capacity'] = [0] * SLOTS
            for i in range(SLOTS):
                topology[u][v]['capacity'][i] = Slot()
        
        s = escolherSimulacao(SIM, topology, Operacoes())
        SimPy.Simulation.initialize()
        SimPy.Simulation.activate(s, s.execut(rate))
        SimPy.Simulation.simulate(until=MAX_TIME)
        #op.printTopology(topology)
        bloqueio.append(s.bloqueioTotal)
        usSlot.append(s.usSlotMedia)
        usBkp.append(s.usBkpMedia)
        holdingTime.append(s.MediaPrazo)
        util.append(s.utilizacao)
        frag.append(s.fragmentacao)
    
    #print "->", bloqueio, usSlot, usBkp, "<-" 
    #op.escreverResultados(e, bloqueio, usSlot, usBkp, holdingTime, util, frag)
