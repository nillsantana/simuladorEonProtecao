import SimPy
from SimPy.Simulation import *
from request import *
from slot import *
from operacoes import *

op = Operacoes()

class Desalocar(SimPy.Simulation.Process):
    
    def __init__(self, holdTime):
        SimPy.Simulation.Process.__init__(self)
        self.holdTime = holdTime

    def desalocar(self, idReq, src, dst, slot, inicial, final, topology, req):
        
        for t in range(inicial, final):
            # tratar caso para quanto tiver uma reserva
            s = topology[src][dst]['capacity'][slot].retornarSlot(t)
            if type(s) == list:
                if 'r' in s:
                    # tem que desalocar e colocar a reserva
                    #print "Reservado ", topology[src][dst]['capacity'][slot].retornarSlot(t), slot
                    # -> imprimir o tempo atual de desalocacao
                    #print "Slot: ", s, " -> time: ", self.holdTime, " timeSim: ", now()
                    topology[src][dst]['capacity'][slot].removePath(t, idReq, req)   
                else:
                    #print "Tem problema para verificar"
                    #print "Cont em desalocar req uniq ", s
                    #print "Altern ", topology[src][dst]['capacity'][slot].retornarSlot(t), slot
                    topology[src][dst]['capacity'][slot].removePath(t, idReq, req)   
                    #print "Tem problema para verificar"
                    #s = topology[src][dst]['capacity'][slot].retornarSlot(t)
                    #print "Cont em desalocar req uniq ", s
                    
            else:     
                topology[src][dst]['capacity'][slot].removePath(t, idReq, req)
        #print "Desalocou ", idReq 
        return True
        #return False

    def verDesalocar(self, idReq, src, dst, slot, inicial, final, topology, req):
        #print ">>> Req ",idReq," Slot ",slot
        if topology[src][dst]['capacity'][slot].verificarSlotReqUmPorUm(inicial, idReq) == True:
            veri = self.desalocar(idReq, dst, src, slot, inicial, final, topology, req)
            #print "Veri ", veri
            if veri == True:
                #print idReq, slot
                return True
            return False
        else:
           return False 


    def run(self, req, tipoReq, qtdRetirar, topology):
        yield hold, self, self.holdTime
        
        '''
        if tipoReq == 1:
            print "time de desalocao req",req.idReq, " ", now(), req.duracao, self.holdTime
        if tipoReq == 2:
            print "time de desalocao req",req.idReq,"Bkp ", now(), req.duracaoBkp, self.holdTime
        '''
        #print ">>>>>>>>>>>>>>>>>>>>...", tipoReq
        if tipoReq == 1:
            inicial = req.time
            final = req.time + req.duracao             
            #print "Prim", req.contSlot

            ini = 0

            for i in range(0, len(req.path)-1):
                for slot in range(0, len(req.slotsAlocados)):
                    if self.verDesalocar(req.idReq, req.path[i], req.path[i+1], req.slotsAlocados[slot], inicial, final, topology, req) == True:
                        ini += 1
                        '''
                        if req.contSlot == 0:
                            print "Problema slots estrapolou"
                            #pass
                        else:
                            print "Prim ! ", req.contSlot, req.idReq
                            req.contSlot -= 1
                            print "Prim ", req.contSlot, req.idReq#'''
                        #print "Retirou"
                        #op.printTopology(topology)
                        #print "\n"
                        if ini == qtdRetirar:
                            #print "Fim Int"
                            #op.printTopology(topology)        
                            #print "\n"
                            return
                       
        if tipoReq == 2:
            
            #print "Escolha 2"
            inicial = req.timeBkp
            final = req.timeBkp + req.duracaoBkp             
            ini = 0
            #print "BKP ", req.contSlotBkp

            for i in range(0, len(req.pathBkp)-1):
                for slot in range(0, len(req.slotsAlocadosBkp)):
                    if self.verDesalocarBkp(str(req.idReq)+"Bkp", req.pathBkp[i], req.pathBkp[i+1], req.slotsAlocadosBkp[slot], inicial, final, topology, req) == True:
                        ini += 1
                        '''
                        if req.contSlotBkp == 0:
                            print "problema slots estrapolou bkp"  
                            #pass
                        else:
                            print "BKP * ", req.contSlotBkp, req.idReq
                            req.contSlotBkp -= 1
                            print "BKP ", req.contSlotBkp, req.idReq#'''
                        #print "Retirou"
                        #op.printTopology(topology)
                        #print "\n"
                        if ini == qtdRetirar:
                            #print "Fim Int"
                            #op.printTopology(topology)        
                            #print "\n"
                            return               

        #op.printTopology(topology)

    def verDesalocarBkp(self, idReq, src, dst, slot, inicial, final, topology, req):
        #print ">>>",idReq
        #print ">>> Req ",idReq," Slot ",slot
        '''if len(req.slotsAdicionaisBkp) > 0:
            if slot in req.slotsAdicionaisBkp:
                print "Excluind slot adiconal ", slot, idReq'''
        #req.slotsAlocadosBkp.remove(slot)
        if topology[src][dst]['capacity'][slot].verificarSlotReqUmPorUm(inicial, idReq) == True:
            '''if len(req.slotsAdicionaisBkp) > 0:
                print "Adicionais ", req.slotsAdicionaisBkp, req.slotsAlocadosBkp 
            if slot in req.slotsAdicionaisBkp:
                print "Excluind slot adiconal ", slot, idReq'''
            #else:
            #    print "Excluido slot ", slot, idReq
            veri = self.desalocarBkp(idReq, dst, src, slot, inicial, final, topology)
            #print "Veri ", veri
            #veri = True
            if veri == True:
                #print idReq, slot
                return True
            return False
        else:
           return False 

    def desalocarBkp(self, idReq, src, dst, slot, inicial, final, topology):
        for t in range(inicial, final):
            #print ">>> Req ",idReq," Slot ",slot
            topology[src][dst]['capacity'][slot].removeBkp(t, idReq)
        #print "Desalocou ", idReq 
        return True
        #return False
