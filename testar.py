#import networkx as nx
#from random import randint
#from config import *

l = ['453r', 2334]


'''
topology = nx.read_weighted_edgelist('topology/' + TOPOLOGY, nodetype=int)

c = 10
for u, v in topology.edges():

    topology[u][v]['capacity'] = [0] * 10
    for i in range(10):
        if i % 2 == 0 or i == 1 or i == 9:  
            topology[u][v]['capacity'][i] = 0    
        else:
            topology[u][v]['capacity'][i] = 1


for u, v in topology.edges():
    print u," ", v," ", topology[u][v]['capacity']


path = [[1,2,4,5]] 
#path2 = [5,6,10,14]

#verifca a disponibilidade de um caminho
def buscarCaminho(caminho, numSlots, rede):
    slot = 0
    final = []
    resultado = []
    
    while(slot < 10):
        tam = 0
        for i in range(len(caminho)-1):
            if(rede[caminho[i]][caminho[i+1]]['capacity'][slot] == 0):
                tam+=1
            else:
                if(len(resultado) > 0):
                    final.append(resultado)
                    resultado = []
        #Chegando aki, em todos os enlaces do caminho este slot esta livre    
        if tam+1 == len(caminho):
            resultado.append(slot)
        
        if len(resultado) == numSlots:
            return [True, caminho, resultado]

        slot +=1

    if(len(resultado) > 0):
        final.append(resultado)
                
    #print "resultado", final, "\n"
    return final

# Verifica se algum caminho dentro da lista de caminho pode atendener o numero de slots
# solicitados pelo backup
# Retorna true se a quantidade de slots se encontra disponivel
# Retorna todos os posiveis conjuntos de slots conitiguos que estao livres
def disponibilidade(caminhos, numSlots, topology):
    result = []
    for i in range(len(caminhos)):
        atualPath = buscarCaminho(caminhos[i], numSlots, topology)
        if(atualPath[0] == True):
            #print "Achou caminho ", atualPath
            return atualPath
        else:
            #print "Encontrados ", atualPath, " <- -> ", caminhos[i]
            a = [caminhos[i], atualPath]
            result.append(a)

    return result

result = disponibilidade(path, 5, topology)
print result


def maiorElaticidade(resCaminhos, numSlots):
    for i in range()
'''

'''
def encontrarMaiorElasticidade(resultado, numSlots):
    for i in resultado:
'''

