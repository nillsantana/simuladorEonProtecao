from config import *
from slot import *
from request import *
import networkx as nx
import math
from estatistica import *
import random

class Operacoes():
    
    def __init__(self):
        pass
    
    # verifica se caminho esta disponivel -> para a tematica 1:1
    def verificarPathPrimarioUmPorUm(self, path, numSlots, time, duracao, protegidos, prioridade, topology):    
        slotsAptos = []
        inicio = time
        total = time+duracao
        s = 0

        while s < SLOTS:
            disponivel = True
            
            for p in range(len(path)-1):
                for t in range(inicio, total):
                    if topology[path[p]][path[p+1]]['capacity'][s].isAreBusy(t) == True:
                        # verifica se prioridade for baixa 
                        if prioridade == 0:
                            #verifica se o slot esta reservado
                            if topology[path[p]][path[p+1]]['capacity'][s].estaReservado(t):
                                #recupera qual bkp reservou o caminho
                                reserva = topology[path[p]][path[p+1]]['capacity'][s].getReserva(t)
                                # se o len(reserva) > 1 implica que ja tem algum pathPrincipal  
                                if len(reserva) == 1 and ('r' not in reserva):
                                    if 'r' in reserva:
                                        print "Res com r", reserva
                                    protegido = protegidos[reserva[0]]
                                    #verifica se sao disjunto
                                    if self.saoDisjuntos(path, protegido) == False:
                                        disponivel = False
                                        break
                                    else:
                                        #print "Disjuntos", reserva[0]
                                        pass
                                else:
                                    #print "Slot de reserva ja ocupado"
                                    disponivel = False
                                    break

                            else:
                                disponivel = False
                                break

                        else:
                            #print "Prioridade Alta, nao pode ocupar reserva"
                            disponivel = False
                            break
                        
                        
                if disponivel == False:
                    break
    
            if disponivel == True:
                slotsAptos.append(s)
                if len(slotsAptos) == numSlots:
                    return [True, slotsAptos]
            else:
                slotsAptos = []
    
            s += 1
        
        return [False]
    
    # Usado na protecao 1:1
    def buscarPathListUmPorUm(self, req, dmd, protegidos, topology):
        
        #buscarPathList(self, src, dst, data, dmd, time, duracao ,topology)
        #req.src, req.dst, req.data req.data, req.time, req.duracao

        try:
            p = list(nx.all_shortest_paths(topology, req.src, req.dst, weight='weight'))
        except:
            return [False]

        random.shuffle(p)

        for i in range(0, len(p)):            
            path = p[i]
            distance = int(self.distance(path, topology))
            numSlots = int(math.ceil(self.modulation(distance, dmd))) 
            
            pathFinal = self.verificarPathPrimarioUmPorUm(path, numSlots, req.time, req.duracao, protegidos, req.prioridade, topology)
                
            if pathFinal[0] == True:
                pathFinal.append(path)
                pathFinal.append(numSlots)
                
                return pathFinal
            
        return [False]

    def verificarPathPrimario(self, path, numSlots, time, duracao, topology):    
        slotsAptos = []
        inicio = time
        total = time+duracao
        s = 0

        while s < SLOTS:
            disponivel = True
            
            for p in range(len(path)-1):
                for t in range(inicio, total):
                    if topology[path[p]][path[p+1]]['capacity'][s].isAreBusy(t) == True:
                        # Esta sendo usado
                        disponivel = False
                        break

                if disponivel == False:
                    break
    
            if disponivel == True:
                slotsAptos.append(s)
                if len(slotsAptos) == numSlots:
                    return [True, slotsAptos]
            else:
                slotsAptos = []
    
            s += 1
        
        return [False]
    # usada na proposta 8.2 -> elastica

    # Busca um caminho de bkp e caso nao possui slots livres de imediato, caso nao sejam suficientes de imediato, 
    # eh verificado se existem slots que ficarao em breve livres podendo ser utilizados
    #def buscarPathBackupList(self, path, time, dmd ,duracao, requisicoes,topology):
    def buscarPathBackupList(self, req, dmd, requisicoes, timeSimAtual, topology):
        p = req.path
        duracao = req.duracaoBkp
        time = req.timeBkp
        
        src = p[0]
        dst = p[len(p)-1]

        if len(p) == 2:

            topologyAux = topology.copy() 
            topologyAux.remove_edge(src,dst)        
            try:
                bkp = list(nx.all_shortest_paths(topologyAux, src, dst, weight='weight'))
            except:
                return [False]
            
            random.shuffle(bkp)
            result = []

            for i in range(0, len(bkp)):
                path = bkp[i]
                distance = int(self.distance(path, topology))
                numSlots = int(math.ceil(self.modulation(distance, dmd))) 
                
                #print "Path ", path, "Slots ", numSlots
                result.append([path, numSlots])
                pathBkp = self.buscarCaminhoBkp(path, numSlots, time, duracao, topology)
                #return = [true, path, slots]
                
                if pathBkp[0] == True:
                    return pathBkp            
                else:
                    result[i].append(pathBkp[1])

            #usando o calculo de elasticidade
            #res = self.verificarElasticidade(req, result, time, duracao, requisicoes, timeSimAtual, topology)
            #usando o tempo de simulacao
            res = self.verificarElasticidadeAlt(req, result, time, duracao, requisicoes, timeSimAtual, topology)            
            
            if res[0] == True:
                return res
            else:
                return [False]
            
        else:
            topologyAux = topology.copy()
            for i in range(0, len(p)-1):
                topologyAux.remove_edge(p[i], p[i+1])
            
            try:
                bkp = list(nx.all_shortest_paths(topologyAux, src, dst, weight='weight'))
            except:
                return [False]

            random.shuffle(bkp)
            
            result = []

            for i in range(0, len(bkp)):
                Path = bkp[i]
                #print "Path ", path
                distance = int(self.distance(Path, topology))
                numSlots = int(math.ceil(self.modulation(distance, dmd))) 
                
                result.append([Path, numSlots])
                pathBkp = self.buscarCaminhoBkp(Path, numSlots, time, duracao, topology)
                #return = [true, path, slots]

                #print "Path bkp ", pathBkp
                if pathBkp[0] == True:
                    return pathBkp            
                else:
                    #print "False ", pathBkp
                    result[i].append(pathBkp[1])
            
            #usando o calculo de elasticidade
            #res = self.verificarElasticidade(req, result, time, duracao, requisicoes, timeSimAtual, topology)
            #usando o tempo de simulacao
            res = self.verificarElasticidadeAlt(req, result, time, duracao, requisicoes, timeSimAtual, topology)
            
            if res[0] == True:
                return res    
            else:
                return [False]
 
    # Recebe todos os possiveis slots livres e verifica suas possibilidades de expadir-se
    # Retorna o bloco que pode ser expandido || Retorna que nao eh possivel 
    # [True, [path], [bloco incialmente livre], [bloco de slots que podem ser expandidos futuramente ]]
    def verificarElasticidade(self, req, resultado, time, duracao, requisicoes, timeSimAtual, rede):
        
        for i in range(len(resultado)):
            path = resultado[i][0] 
            slots = resultado[i][1] 
            blocos = resultado[i][2]
            #print "Escolha ", path, slots, blocos
            elastAtual = 0
            atual = []

            # pega um bloco de slots livres por vez, para verificar se ele pode ser expandido
            # permitido apenas blocos com tamanho maior que 1
            for k in range(len(blocos)):
                if len(blocos) > 1:   
                    resposta = self.encontrarBloco(req, path, slots, blocos[k], time, duracao, requisicoes, rede)               
                    
                    if resposta[0] == True:
                        if resposta[2] > elastAtual:
                            elastAtual = resposta[2] 
                            resposta.append(blocos[k])
                            atual = resposta

        if len(atual) > 0:
            if atual[0] == True:
                self.allocarReserva(req.idReq, path, atual[1], time, duracao, rede)
                #print "TAM bl ", len(blocos[k]), " Tam bl En ", len(resposta[1])
                return [True, path, atual[3], atual[1]]
        else:
            pass
            
        return [False]
    
    #usando tempo de simulacao
    def verificarElasticidadeAlt(self, req, resultado, time, duracao, requisicoes, timeSimAtual, rede):
        #print "Verificando Elaticidade ....."
      
        for i in range(len(resultado)):
            path = resultado[i][0] 
            slots = resultado[i][1] 
            blocos = resultado[i][2]
            
            # pega um bloco de slots livres por vez, para verificar se ele pode ser expandido
            # permitido apenas blocos com tamanho maior que 1
            for k in range(len(blocos)):
                if len(blocos) > 1:   
                    resposta = self.encontrarBlocoTimeSim(req, path, slots, blocos[k], time, duracao, requisicoes, timeSimAtual, rede)               
                    
                    if resposta[0] == True:
                        resposta.append(blocos[k])
                        atual = resposta

                        self.allocarReserva(req.idReq, path, atual[1], time, duracao, rede)
                        return [True, path, atual[2], atual[1]]

        return [False]

    #Pega cada bloco individualmente e calcula a elasticidade
    # retorna o caminho e o valor da elasticidade
    def encontrarBloco(self, req, path, qtdSlots, bloco, time, duracao, requisicoes, topology):
        
        inicio = time
        total = time + duracao
        slotsAdd = [] # slot adicionais que serao usados futuramente
        htpbk = float(duracao)/float(qtdSlots) 
        #print htpbk, duracao, qtdSlots           
        elasticidade = 0    

        qtd = qtdSlots - len(bloco)
        #print qtd, qtdSlots, len(bloco)
        #print "Ini  -- - - - - --  --"
          
        if ((bloco[len(bloco)-1] + qtd) < SLOTS) and len(bloco) >= 2:
            y = 1    
            while y <= qtd and y < SLOTS:
                for p in range(len(path)-1):
                    for t in range(inicio, total):
                        reserva = topology[path[p]][path[p+1]]['capacity'][y+bloco[len(bloco)-1]].recuperar(t) 
                        r = reserva
                        
                        if reserva == False:
                            #slot esta vazio, nao contem alocacao
                            #print 'Slot[',y+bloco[len(bloco)-1],'] = Livre'
                            pass

                        else:
                            # primeiro caso ex [2], contem apenas uma req no slot
                            if type(reserva) == int:
                                prox = requisicoes[int(reserva)]
                                #calcula elaticidade
                                elas  = (float(prox.holdingSlotPrim) * float(prox.numSlotsBkp))/float(len(bloco))
                                elasticidade += elas
                                #print "Elas ", elas, len(bloco), prox
                            
                            else:
                                # verificar se o slot ja esta reservado futuramente
                                if type(reserva) == list and ('r' in reserva):
                                    #quando possui uma reserva de um outro caminho elastico
                                    return [False]
                                    
                                #segundo caso ex: ['bkp', 1], bkp e uma req
                                if(len(reserva) == 2):
                                    r = reserva
                                    a = r.pop()
                                    b = r.pop()                                          
                                    c = b.split('Bkp')
                                    c = int(c[0])                                               
                                    prox = requisicoes[int(a)]
                                    proxBkp = requisicoes[int(c)]
                                    
                                    #calcula elaticidade
                                    elas1  = (float(prox.holdingSlotPrim) * float(prox.numSlotsBkp))/float(len(bloco))
                                    elas2  = (float(proxBkp.holdingSlotPrim) * float(proxBkp.numSlotsBkp))/float(len(bloco))
                                    if elas1 <= elas2:
                                        elasticidade += elas2
                                    else:
                                        elasticidade += elas1
                            
                                # terceiro caso ex: ['2bkp'] , slot contem apenas bkp 
                                if len(reserva) == 1:
                                    #print "Len 1", reserva
                                    r = reserva
                                    a = r.pop()
                                    c = a.split('Bkp')
                                    c = int(c[0])
                                   
                                    proxBkp = requisicoes[c] 
                                    #calcula elaticidade
                                    elas  = (float(proxBkp.holdingSlotPrim) * float(proxBkp.numSlotsBkp))/float(len(bloco))
                                    elasticidade += elas
                                    #print "Elas ", elas, len(bloco),proxBkp       
                    
                slotsAdd.append(y+bloco[len(bloco)-1])
                
                if len(slotsAdd) == qtd:
                    return [True, slotsAdd, elasticidade]
                    #break
                else:
                    pass
                    #print "Slot Add", slotsAdd, len(slotsAdd), qtd
                y += 1
            
            return [False]
            # se tiver cara livre, o correto eh alocar logo, 

        else:
            #print "Excede limite"
            return [False]
   
    # Busca com criterio diferente
    # Recebe um bloco de slots livres de imediato, verifica quando os slots vizinhos a este bloco irao ficar livres,
    # se o tempo for aceitavel este slot sera usado em um tempo futuro como expansao do bloco de slots inicial 
    # Retorna um bloco contendo os slots que completa a quantidade desejada
    # return = [ [bloco de slots que podem ser expandidos futuramente], [slots incialmente livres]]
    def encontrarBlocoAlt(self, req, path, qtdSlots, bloco, time, duracao, requisicoes, topology):
        
        inicio = time
        total = time + duracao
        slotsAdd = [] # slot addionais que serao usados futuramente
        htpbk = float(duracao)/float(qtdSlots) 
        #print htpbk, duracao, qtdSlots           
        qtd = qtdSlots - len(bloco)
        #print qtd, qtdSlots, len(bloco)
        
        if ((bloco[len(bloco)-1] + qtd) < SLOTS) and len(bloco) >= 2:
            y = 1    
            while y <= qtd and y < SLOTS:
                #tempoAtual = (req.timeSimIni+req.timeBkp+((len(bloco)-1)*htpbk))-htpbk
                tempoAtual = req.timeBkp
                #print "tempo Atual Inic ", tempoAtual, req.timeSimIni, req.timeBkp, len(bloco), htpbk
                for p in range(len(path)-1):
                    # tempo limite para alocar um novo slot, trabalhando com bloco inicial de tamanho 2
                    tempoAtual += len(bloco)*htpbk # Falta Adicionar ainda o tempo correspondente ao bloco atual
                    #print "tempo Atual Increm ", tempoAtual
                    okPode = True # flag para verificar se pode usar futuramente esse slot
                    for t in range(inicio, total):
                        reserva = topology[path[p]][path[p+1]]['capacity'][y+bloco[len(bloco)-1]].recuperar(t) 
                        r = reserva
                        # tem de verificar em qual caso de desalocacao a req do atual slot vai estar
                        # caso 1 prim > bkp, o bkp eh desalocado ao final da duracaoBkp e prim eh desalocados ao final da duracaoPrim
                        # caso 2 prim < bkp, prim desalocado apos duracaoPrim e bkp eh retirado incrementalmente
                        # caso 3 prim == bkp, o bkp sai um por 1 e o principal so sai ao final da duracaoPrim
                        
                        if reserva == False:
                            #print 'Slot[',y+bloco[len(bloco)-1],'] = Livre'
                            pass

                        else:
                            # primeiro caso ex [2], contem apenas uma req no slot
                            if type(reserva) == int:
                                prox = requisicoes[int(reserva)]
                                if (prox.timeSimIni + prox.duracao) < tempoAtual:
                                    #print "Pode - Comparar Atual ", prox.timeSimIni + prox.duracao, "Seguinte ", tempoAtual, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                    okPode = True
                                else:
                                    okPode = False
                                    #print "Pode - Comparar Atual ", prox.timeSimIni + prox.duracao, "Seguinte ", tempoAtual, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                    break

                            else:
                                # verificar se o slot ja esta reservado futuramente
                                if type(reserva) == list and ('r' in reserva):
                                    #print "Res ", reserva, [y+bloco[len(bloco)-1]], req.idReq
                                    okPode = False  
                                    break

                                #segundo caso ex: ['bkp', 1], bkp e uma req
                                if(len(reserva) == 2):
                                    r = reserva
                                    a = r.pop()
                                    b = r.pop()                                          
                                    c = b.split('Bkp')
                                    c = int(c[0])                                               
                                    #print "Alocado ", 'Slot[',s+soma,'] = ', a, b, c
                                    prox = requisicoes[int(a)]
                                    proxBkp = requisicoes[int(c)]
                                    
                                    if len(proxBkp.path) > len(proxBkp.pathBkp):
                                        #bkp e prim so sao desalocados quando espirar sua duracao

                                        if (prox.timeSimIni + prox.duracao) < tempoAtual and (proxBkp.timeSimIni + proxBkp.timeBkp + proxBkp.duracaoBkp) < tempoAtual:
                                            okPode = True
                                        else:
                                            okPode = False
                                            break
                                    
                                    else:
                                        #bkp dinamicamente e prim eh desalocados quando espirar sua duracao
                                        prim = prox.timeSimIni + prox.duracao
                                        prot = proxBkp.timeSimIni + proxBkp.timeBkp + ((p+1)*proxBkp.holdingSlotBkp)
                                        
                                        if prim < tempoAtual and prot < tempoAtual:
                                            #print "Pode -  Comparar Atuall ", htpbk, "Seguinte req", prox.holdingSlotPrim, " Bkp ", proxBkp.holdingSlotBkp, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                            okPode = True
                                        else:
                                            okPode = False
                                            #print "Nao pode - Comparar Atuall ", htpbk, "Seguinte req", prox.holdingSlotPrim, " Bkp ", proxBkp.holdingSlotBkp, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                            break
                                
                                # terceiro caso ex: ['2bkp'] , slot contem apenas bkp 
                                if len(reserva) == 1:
                                    r = reserva
                                    a = r.pop()
                                    c = a.split('Bkp')
                                    c = int(c[0])
                                    #print "Request ", 'Slot[',s+soma,'] = ', c, 'Bkp'
                                    #print "Apenas um bkp reservado ", c,'Bkp'
                                    proxBkp = requisicoes[c] 
                                    prot = proxBkp.timeSimIni + proxBkp.timeBkp + ((p+1)*proxBkp.holdingSlotBkp)
                                        
                                    if prot < tempoAtual:
                                        #print "Pode - Comparar Atuall ", htpbk, "Seguinte Bkp ", proxBkp.holdingSlotBkp, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                        okPode = True
                                    else:
                                        okPode = False
                                        #print "Nao pode - Comparar Atual ", htpbk, "Seguinte Bkp ", proxBkp.holdingSlotBkp, 'Slot[',y+bloco[len(bloco)-1],'] = ', r
                                        break
                            
                    if okPode == False:
                        break

                # Chegando aki e okPode = True, entao este slot esta livre e pode ser alocado
                if okPode == True:
                    slotsAdd.append(y+bloco[len(bloco)-1])
                else:
                    return [False]
                
                y += 1

            return [True, slotsAdd]
            # se tiver cara livre, o correto eh alocar logo, 

        else:
            #print "Excede limite"
            return [False]
        #'''
    
    def encontrarBlocoTimeSim(self, req, path, qtdSlots, bloco, time, duracao, requisicoes, timeSimAtual, topology):
        
        #ir verificando a cada slot
        #pega o tempo de simulacao atual soma com o valor de tempo nescessario para o slot
        #pega o tempo de simulacao no momento em que a requisicao foi criada e soma com o tempo nescessario para 
        # transmitir pelo slot
        #verifica se o tempo permite que possa existir a esperar para alocar futuramente 

        inicio = time
        total = time + duracao
        slotsAdd = [] # slot addionais que serao usados futuramente
        htpbk = float(duracao)/float(qtdSlots) 
        #print htpbk, duracao, qtdSlots           
        qtd = qtdSlots - len(bloco)
        #print qtd, qtdSlots, len(bloco)
        
        if ((bloco[len(bloco)-1] + qtd) < SLOTS) and len(bloco) >= 2:
            y = 1    
            while y <= qtd and y < SLOTS:
                
                for p in range(len(path)-1):
                    
                    okPode = True # flag para verificar se pode usar futuramente esse slot
                    for t in range(inicio, total):
                        reserva = topology[path[p]][path[p+1]]['capacity'][y+bloco[len(bloco)-1]].recuperar(t) 
                        r = reserva
                        # tem de verificar em qual caso de desalocacao a req do atual slot vai estar
                        # caso 1 prim > bkp, o bkp eh desalocado ao final da duracaoBkp e prim eh desalocados ao final da duracaoPrim
                        # caso 2 prim < bkp, prim desalocado apos duracaoPrim e bkp eh retirado incrementalmente
                        # caso 3 prim == bkp, o bkp sai um por 1 e o principal so sai ao final da duracaoPrim
                        
                        if reserva == False:
                            #print 'Slot[',y+bloco[len(bloco)-1],'] = Livre'
                            pass

                        else:
                            # primeiro caso ex [2], contem apenas uma req no slot
                            if type(reserva) == int:
                                prox = requisicoes[int(reserva)]
                                tprox = prox.timeSimulacao + prox.duracao 
                                tAtual = req.duracaoBkp + timeSimAtual
                                #print "tAtual ", tAtual, " tprox ", tprox
                                if (tAtual+1.0) < tprox:
                                    okPode = True
                                else:
                                    okPode = False
                                    break

                            else:
                                # verificar se o slot ja esta reservado futuramente
                                if type(reserva) == list and ('r' in reserva):
                                    #print "Res ", reserva, [y+bloco[len(bloco)-1]], req.idReq
                                    okPode = False  
                                    break

                                #segundo caso ex: ['bkp', 1], bkp e uma req
                                if(len(reserva) == 2):
                                    r = reserva
                                    a = r.pop()
                                    b = r.pop()                                          
                                    c = b.split('Bkp')
                                    c = int(c[0])                                               
                                    #print "Alocado ", 'Slot[',s+soma,'] = ', a, b, c
                                    prox = requisicoes[int(a)]
                                    proxBkp = requisicoes[int(c)]
                                    
                                    tprox = prox.timeSimulacao + prox.duracao 
                                    tproxBkp = proxBkp.timeSimulacao + proxBkp.duracao 
                                    tAtual = req.duracaoBkp + timeSimAtual
                                    #print "tAtual ", tAtual, " tprox ", tprox, " tproxBkp ", tproxBkp 
                                    if ((tAtual+1.0) < tprox) and ((tAtual+1.0) < tproxBkp):
                                        okPode = True
                                    else:
                                        okPode = False
                                        break


                                # terceiro caso ex: ['2bkp'] , slot contem apenas bkp 
                                if len(reserva) == 1:
                                    r = reserva
                                    a = r.pop()
                                    c = a.split('Bkp')
                                    c = int(c[0])
                                    #print "Request ", 'Slot[',s+soma,'] = ', c, 'Bkp'
                                    #print "Apenas um bkp reservado ", c,'Bkp'
                                    proxBkp = requisicoes[c] 
                                    #prot = proxBkp.timeSimIni + proxBkp.timeBkp + ((p+1)*proxBkp.holdingSlotBkp)
                                    tprox = proxBkp.timeSimulacao + proxBkp.duracao 
                                    tAtual = req.duracaoBkp + timeSimAtual
                                    #print "tAtual ", tAtual, " tproxBkp ", tprox
                                    if tAtual+1.0 < tprox:
                                        okPode = True
                                    else:
                                        okPode = False
                                        break
                                    
                    if okPode == False:
                        break

                # Chegando aki e okPode = True, entao este slot esta livre e pode ser alocado
                if okPode == True:
                    slotsAdd.append(y+bloco[len(bloco)-1])
                else:
                    return [False]
                
                y += 1

            return [True, slotsAdd]
            # se tiver cara livre, o correto eh alocar logo, 

        else:
            #print "Excede limite"
            return [False]
        #'''

    # Busca blocos de slots livres para serem alocados
    # Retorna um conjunto de slots aptos com a quantidade desejada pronta para alocacao 
    # ou
    # Retorna todos os conjuntos de slots livres ao logo do caminho
    # return = [True, path, slots] || return = [False, todos os blocos disponiveis ao longo do caminho]

    def buscarCaminhoBkp(self, caminho, numSlots, time, duracao, rede):
        slot = 0
        final = []
        resultado = []

        inicio = time
        total = time + duracao
    
        while(slot < SLOTS):
            vazio = True
            tam = 0
            for i in range(len(caminho)-1):
                for t in range(inicio, total):
                    #print "TIme ", t
                    if rede[caminho[i]][caminho[i+1]]['capacity'][slot].isAreBusy(t) == False:
                        #print "Ok"
                        pass
                    else:
                        #print "Ok False"
                        vazio = False;
                        if(len(resultado) > 0):
                            final.append(resultado)
                            #print "Add final", final
                            resultado = []
                        break          
                if vazio == False:
                    break

            #Chegando aki, em todos os enlaces do caminho este slot esta livre    
            if vazio == True:
                resultado.append(slot)
                #print "Res ", resultado
 
            if len(resultado) == numSlots:
                return [True, caminho, resultado]

            slot +=1

        if(len(resultado) > 0):
            final.append(resultado)
            #print "Append ", resultado
        
        #print "Final -> ", final
        #print "resultado", final, "\n"
        return [False, final]

    # Usado para marcar os slots que irao ficar livres futuramente e que ja foram previamente solitados por requisicoes existentes 
    # na simulacao
    # 
    # Simplemeste adiciona um 'r' no slot de tempo que ira ficar livre 
    def allocarReserva(self, idReq, path, listSlots, timeInicial, duracao, topology):
        
        final = timeInicial + duracao
        for p in range(len(path)-1):
            for slot in range(len(listSlots)):
                for t in range(timeInicial, final):
                    s = topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t) 
                    #obs cuidado aki
                    if s == True:
                        # esta vazio
                        #l = ['r', str(idReq)+"BkpExt"]
                        l = [str(idReq)+"Bkp"]
                        topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].reservarSlot(t, ['r', str(idReq)+"Bkp"])
                        #print "Apos Reserva", topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t), listSlots[slot] 
                    elif type(s) == int:
                        l = [s, 'r', str(idReq)+"BkpExt"]
                        topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].reservarSlot(t, [s, 'r', str(idReq)+"BkpExt"])
                        #print "Apos Reserva", topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t), listSlots[slot] 
                    elif type(s) == list:
                        s.append('r')
                        s.append(str(idReq)+"BkpExt")
                        topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].reservarSlot(t, s)
                        #print "Apos Reserva", topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t), listSlots[slot] 
                    else:
                        print "Tem problema"

                    #print "Apos Reserva", topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t)
    
    
    # Usado para a tematica 1:1
    def allocarUmPorUm(self, tipoReq, idReq, path, listSlots, timeInicial, duracao, topology):
        #print "Chamou "
        final = timeInicial + duracao
        # Alocar pathPrincipal
        if tipoReq == 1 : 

            for p in range(len(path)-1):
                for slot in range(len(listSlots)):
                    for t in range(timeInicial, final):
                        s = topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t)
                        if topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].isAreBusy(t) == False:
                            topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].useTimeInSlot(t, idReq)
                        
                        elif topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].estaReservado(t):
                            reserva = topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].getReserva(t)
                            reserva.append(idReq)
                            topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].useTimeInSlot(t, reserva)

                        else:
                            print "**-- Nao foi possivel alocar", idReq
                            print "Conteudo ", s, slot
                            break
        # Alocar bkp
        if tipoReq == 2:
            #print "Bkp"
            for p in range(len(path)-1):
                for slot in range(len(listSlots)):
                    for t in range(timeInicial, final):
                        s = topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].retornarSlot(t)
                        if topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].isAreBusy(t) == False:
                            topology[path[p]][path[p+1]]['capacity'][listSlots[slot]].useTimeInSlot(t, [idReq])
                        else:
                            print "**-- Nao foi possivel alocar", [idReq]
                            print "Conteudo bkp ", s, listSlots[slot]
                            break
            #print "Alocado "

    def saoDisjuntos(self, a, b):
        
        for i in range(0, len(a)-1):
            for j in range(0, len(b)-1):
                #print "Verifi ", i, j
                if ((a[i] == b[j]) and (a[i+1] == b[j+1])) or ((a[i] == b[j+1]) and (a[i+1] == b[j])):
                    #print "Enlace Igual, Path1 [",palavra1[i],palavra1[i+1],"] Path2 [",palavra2[j],palavra2[j+1],"]"  
                    return False
        
        return True

    def calculaTaxaMin(self, data, deadline):
        dmd = data/float(deadline)
        return dmd

    def calculaTempoTrans(self, data, dmd):
        tempo = data/float(dmd)
        #print "result", tempo
        return tempo

    def printTopology(self, topology = None):
        for u, v in topology.edges():
            print "Enlace ||-- ",u, v," --||"
            listaEnl = []
            for i in range(SLOTS):
                #print i
                listaEnl.append(['Slot',i, topology[u][v]['capacity'][i].getSlot()])
            print listaEnl
        
    def distance(self, path, topology):
        soma = 0
        for i in range(0, (len(path)-1)):
            soma += topology[path[i]][path[i+1]]['weight']
        return soma
    
    def modulation(self, dist, demand):
        if dist <= 500:
    		return (float(demand) / float(4 * SLOT_SIZE))
        elif 500 < dist <= 1000:
    		return (float(demand) / float(3 * SLOT_SIZE))
        elif 1000 < dist <= 2000:
    		return (float(demand) / float(2 * SLOT_SIZE)) 
        else:
    		return (float(demand) / float(1 * SLOT_SIZE))

    # Para verificar a utilizacao da rede ao final da simulacao
    def utilizacaoRede(self, topology):
        
        result = []
        slotsUsados = 0
        edges = 0

        for u, v in topology.edges():
            edges += 1
            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizado() > 0:
                    slotsUsados += 1

        #print slotsUsados, "slots - ", ((slotsUsados*100)/(edges*SLOTS)),"%"
        
        
        return (slotsUsados*100)/(edges*SLOTS)

        # utilizado para protecao 1:1
    
    def utilizacaoRedeUmPorUm(self, topology):
        
        result = []
        slotsUzados = 0
        edges = 0

        for u, v in topology.edges():
            edges += 1
            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizadoUmPorUm() > 0:
                    slotsUzados += 1
        
        #print "\n", slotsUzados, "slots - ", ((slotsUzados*100)/(edges*SLOTS)),"% \n"
        
        #result.append([slotsUzados, ((slotsUzados*100)/(edges*SLOTS))])
        return (slotsUzados*100)/(edges*SLOTS)

    # Verifica a utilizacao da rede em tempo real
    def utilizacaoRedeTempoReal(self, idReq, topology):
        result = []
        slotsUzados = 0
        edges = 0

        for u, v in topology.edges():
            edges += 1
            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizado() > 0:
                    slotsUzados += 1

        print "Id ", idReq, " ", slotsUzados, "slots - ", ((slotsUzados*100)/(edges*SLOTS)),"%"
        result.append([u,v, idReq,slotsUzados, ((slotsUzados*100)/(edges*SLOTS))])
        return result

        # utilizado para protecao 1:1
    
    def utilizacaoRedeTempoRealUmPorUm(self, idReq, topology):
        result = []
        slotsUzados = 0
        edges = 0

        for u, v in topology.edges():
            edges += 1
            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizadoUmPorUm() > 0:
                    slotsUzados += 1

        #print "Id ", idReq, " ", slotsUzados, "slots - ", ((slotsUzados*100)/(edges*SLOTS)),"%"
        #result.append([u,v, idReq,slotsUzados, ((slotsUzados*100)/(edges*SLOTS))])
        return (slotsUzados*100)/(edges*SLOTS)
   
    def calcularFragmentacao(self, topology):
        fragmentacao = self.veriFragmentacao(topology)
        
        frag = []
        meanfrag = 0
        for i in range(0, len(fragmentacao)):
            if (fragmentacao[i][2] == 0) or (fragmentacao[i][3] == 0): 
                frag.append([fragmentacao[i][0], fragmentacao[i][1], 1])
            else:
                calc = 1-(float(fragmentacao[i][2])/float(fragmentacao[i][3]))
                #print "1 -", (float(fragmentacao[i][2])/float(fragmentacao[i][3]))
                frag.append([fragmentacao[i][0], fragmentacao[i][1], calc])
                meanfrag += calc

        #for i in frag:
            #print i
        #print frag
        return meanfrag/len(frag)

        # utilizado para protecao 1:1
    
    def calcularFragmentacaoUmPorUm(self, topology):
        fragmentacao = self.veriFragmentacaoUmPorUm(topology)
        
        frag = []
        meanfrag = 0
        for i in range(0, len(fragmentacao)):
            if (fragmentacao[i][2] == 0) or (fragmentacao[i][3] == 0): 
                frag.append([fragmentacao[i][0], fragmentacao[i][1], 1])
            else:
                calc = 1-(float(fragmentacao[i][2])/float(fragmentacao[i][3]))
                #print "1 -", (float(fragmentacao[i][2])/float(fragmentacao[i][3]))
                frag.append([fragmentacao[i][0], fragmentacao[i][1], calc])
                meanfrag += calc
        #for i in frag:
            #print i
        #print frag
        return meanfrag/len(frag) 
    
    #usando lista
    def veriFragmentacao(self, topology):
        
        list = []  
        #ind = 1
        for u, v in topology.edges():
            seqList = []
            seq = 0
            maiorSeq = 0
            totalLivre = 0

            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizado() == 0:
                    totalLivre += 1
                    seq += 1
                else:
                    if seq > maiorSeq:
                        maiorSeq = seq
                        seqList.append(seq)
                        seq = 0
                    else:
                        if seq > 0:
                            seqList.append(seq)
                        seq = 0

            if seq > 0:
                if seq > maiorSeq:
                        maiorSeq = seq
                        seqList.append(seq)
                        seq = 0

            list.append([u,v, maiorSeq, totalLivre, seqList]) 

        #for i in list:
        #    print i 
        #print list
        
        return list

        # utilizado para protecao 1:1
    
    def veriFragmentacaoUmPorUm(self, topology):
        
        list = []  
        #ind = 1
        for u, v in topology.edges():
            seqList = []
            seq = 0
            maiorSeq = 0
            totalLivre = 0

            for i in range(SLOTS):
                if topology[u][v]['capacity'][i].utilizadoUmPorUm() == 0:
                    totalLivre += 1
                    seq += 1
                else:
                    if seq > maiorSeq:
                        maiorSeq = seq
                        seqList.append(seq)
                        seq = 0
                    else:
                        if seq > 0:
                            seqList.append(seq)
                        seq = 0

            if seq > 0:
                if seq > maiorSeq:
                        maiorSeq = seq
                        seqList.append(seq)
                        seq = 0

            list.append([u,v, maiorSeq, totalLivre, seqList]) 

        #for i in list:
        #    print i 
        #print list
        
        return list
    
    def filtrarCaminhos(self, listaReq):
        caminhos = []

        for i in range(0, len(listaReq)):
            if listaReq[i].path not in caminhos:
                caminhos.append(listaReq[i].path)
            if listaReq[i].pathBkp not in caminhos:
                caminhos.append(listaReq[i].pathBkp)
        return caminhos
    
    def escreverResultados(self, rate, Bloqueio, slot, slotbkp, time, util, frag):

        arquivoB = open('output2/bp_dpp2x_2'+'.dat', 'a')
    	arquivoS = open('output2/slot_dpp2x_2'+'.dat', 'a')
        arquivoBkp = open('output2/slotBkp_dpp2x_2'+'.dat', 'a')
    	arquivoTime = open('output2/holdingtime_dpp2x_2'+'.dat', 'a')
    	arquivoUtil = open('output2/util_dpp2x_2'+'.dat', 'a')
    	arquivoFrag = open('output2/frag_dpp2x_2'+'.dat', 'a')
    	
        result = CalculaMediaDesvio(Bloqueio)
        arquivoB.write(str(rate))
    	arquivoB.write("\t")
    	arquivoB.write(str(result[0]))
        arquivoB.write("\t")
        arquivoB.write(str(result[0]-(2.093*(result[1]/math.sqrt(len(Bloqueio))))))
        arquivoB.write("\t")
        arquivoB.write(str(result[0]+(2.093*(result[1]/math.sqrt(len(Bloqueio))))))
        arquivoB.write("\n")

        result2 = CalculaMediaDesvio(slot)
        arquivoS.write(str(rate))
    	arquivoS.write("\t")
    	arquivoS.write(str(result2[0]))
    	arquivoS.write("\t")
    	arquivoS.write(str(result2[0]-(2.093*(result2[1]/math.sqrt(len(slot))))))
    	arquivoS.write("\t")
    	arquivoS.write(str(result2[0]+(2.093*(result2[1]/math.sqrt(len(slot))))))
        arquivoS.write("\n")

        result3 = CalculaMediaDesvio(slotbkp)
        arquivoBkp.write(str(rate))
    	arquivoBkp.write("\t")
    	arquivoBkp.write(str(result3[0]))
    	arquivoBkp.write("\t")
    	arquivoBkp.write(str(result3[0]-(2.093*(result3[1]/math.sqrt(len(slotbkp))))))
    	arquivoBkp.write("\t")
    	arquivoBkp.write(str(result3[0]+(2.093*(result3[1]/math.sqrt(len(slotbkp))))))
        arquivoBkp.write("\n")
    	
    	result4 = CalculaMediaDesvio(time)
        arquivoTime.write(str(rate))
        arquivoTime.write("\t")
        arquivoTime.write(str(result4[0]))
        arquivoTime.write("\t")
        arquivoTime.write(str(result4[0]-(2.093*(result4[1]/math.sqrt(len(time))))))
        arquivoTime.write("\t")
        arquivoTime.write(str(result4[0]+(2.093*(result4[1]/math.sqrt(len(time))))))
        arquivoTime.write("\n")

        result5 = CalculaMediaDesvio(util)
        arquivoUtil.write(str(rate))
        arquivoUtil.write("\t")
        arquivoUtil.write(str(result5[0]))
        arquivoUtil.write("\t")
        arquivoUtil.write(str(result5[0]-(2.093*(result5[1]/math.sqrt(len(util))))))
        arquivoUtil.write("\t")
        arquivoUtil.write(str(result5[0]+(2.093*(result5[1]/math.sqrt(len(util))))))
        arquivoUtil.write("\n")

        result6 = CalculaMediaDesvio(frag)
        arquivoFrag.write(str(rate))
        arquivoFrag.write("\t")
        arquivoFrag.write(str(result6[0]))
        arquivoFrag.write("\t")
        arquivoFrag.write(str(result6[0]-(2.093*(result6[1]/math.sqrt(len(frag))))))
        arquivoFrag.write("\t")
        arquivoFrag.write(str(result6[0]+(2.093*(result6[1]/math.sqrt(len(frag))))))
        arquivoFrag.write("\n")
        
        arquivoB.close() 
        arquivoS.close()
    	arquivoBkp.close()
    	arquivoTime.close()
        arquivoUtil.close()
    	arquivoFrag.close()
    	
# Nao usadas -----------------------------------------------------------------------------------------------------------

    def buscarBackup(self, path, time, dmd ,duracao ,topology):
        src = path[0]
        dst = path[len(path)-1]

        if len(path) == 2:

            topologyAux = topology.copy() 
            topologyAux.remove_edge(src,dst)
            
            try:
                bkp = list(nx.all_shortest_paths(topologyAux, src, dst, weight='weight'))
            except:
                return [False]
                
            random.shuffle(bkp)
            # Econtou o caminho

            for i in range(0, len(bkp)):
                path = bkp[i]
                distance = int(self.distance(path, topology))
                numSlots = int(math.ceil(self.modulation(distance, dmd))) 
                
                #substituir
                pathBkp = self.verificarPathPrimario(path, numSlots, time, duracao, topology)
                
                if pathBkp[0] == True:
                    pathBkp.append(path)
                    pathBkp.append(numSlots)
                    return pathBkp            
            return [False]
            
        else:
            topologyAux = topology.copy()
            for i in range(0, len(path)-1):
                topologyAux.remove_edge(path[i], path[i+1])
            
            try:
                bkp = list(nx.all_shortest_paths(topologyAux, src, dst, weight='weight'))
            except:
                return [False]

            random.shuffle(bkp)

            for i in range(len(bkp)):
                Path = bkp[i]
                distance = int(self.distance(Path, topology))
                numSlots = int(math.ceil(self.modulation(distance, dmd))) 
                
                #substituir
                pathBkp = self.verificarPathPrimario(Path, numSlots, time, duracao, topology)
                
                if pathBkp[0] == True:
                    pathBkp.append(Path)
                    pathBkp.append(numSlots)
                    return pathBkp
            
            return [False]
    
    # Verifica se algum caminho dentro da lista de caminho pode atendener o numero de slots solicitados pelo backup
    # Chama a funcao buscarCaminhoBkp, para verificar se algum caminho da lista atende a requisicao
    # Retorna true se um caminho atende quantidade de slots se encontra disponivel
    # Se nao achar slots disponiveis, retorna os blocos de slots livres nos caminhos em uma lista
    def disponibilidade(caminhos, numSlots, tempoInicial, tempoFinal, topology):
        
        result = []
        for i in range(len(caminhos)):
            atualPath = buscarCaminhoBkp(caminhos[i], numSlots, tempoInicial, tempoFinal, topology)
            if(atualPath[0] == True):
                #print "Achou caminho ", atualPath
                return atualPath
            else:
                #print "Encontrados ", atualPath, " <- -> ", caminhos[i]
                a = [caminhos[i], atualPath]
                result.append(a)

        return result
