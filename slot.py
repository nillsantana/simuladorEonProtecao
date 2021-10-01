
import copy 

class Slot():
    
    def __init__(self):
        self.timeIsAvaible = {}

    # verifica se o slot esta ocupado em um determinado tempo    
    def isAreBusy(self, tempo):
        if self.timeIsAvaible.has_key(tempo) == True:
            return True
            #''' Usado '''
        else:
            return False
    
    def recuperar(self, time):
        if self.isAreBusy(time) == True :
            rec = copy.copy(self.timeIsAvaible[time])
            return rec 
        else:
            return False

    #verifica se um slot esta reservado
    def estaReservado(self, time):
        if type(self.timeIsAvaible[time]) == list:
            return True
        else:
            return False
        
    def getReserva(self, time):
        if self.estaReservado(time):
            reserva = self.timeIsAvaible[time]
            #del(self.timeIsAvaible[time])
            return reserva

        else:
            print "Algo errado"
            return False

    # atribui uma requisicao em um determinado tempo no slot
    def useTimeInSlot(self, time, request):
        if self.isAreBusy(time) == False:
            self.timeIsAvaible[time] = request
        elif type(request) == list:
            self.timeIsAvaible[time] = request
            #print " elif -- "
        else:
            print "Nao disponivel ->>"
    
    # verifica se uma especifica requisicao esta alocado no slot em um determinado instante de tempo
    def verificarSlotReq(self, time, req):
        try:
            #print self.timeIsAvaible[time]
            if self.timeIsAvaible[time] == req:
                return True
            return False
        except:
            return False

    def remove(self, chave):
        del(self.timeIsAvaible[chave])
    
    def removePath(self, time, idReq, req):
        
        if self.timeIsAvaible.has_key(time) == True:
        
            a = self.timeIsAvaible[time]
            if type(a) == list:
                a.remove(idReq)
                
                # Verifica se eh o momento de alocar a reserva
                if len(a) == 2:
                    #print "Antes", a
                    c = a.pop()
                    b = a.pop()
                    if "BkpExt" in c and b == 'r':
                        d = c.split('BkpExt')
                        e = str(d[0])+"Bkp"
                        self.timeIsAvaible[time] = [e]
                        #print "Depois ", self.timeIsAvaible[time]
                    else:
                        print "Erro !", c, b, a
                
                else:
                    #print "Duvida ", a, "Era para desalocar ", idReq 
                    self.timeIsAvaible[time] = a
            
            else:
                del(self.timeIsAvaible[time])

        else:
            print "Esta vazio removePath ? ", time, idReq

    def removeBkp(self, time, idReq):   

        if self.timeIsAvaible.has_key(time) == True:
            a = self.timeIsAvaible[time]
            
            if type(a) == list:
                
                if 'r' in a:
                    try:
                        a.remove(idReq)
                        #self.timeIsAvaible[time] = a 
                        #print "Pular, esta reservado, aqui eh ok"
                        # Verifica se eh o momento de alocar a reserva
                        if len(a) == 2:
                            #print "Antes", a
                            c = a.pop()
                            b = a.pop()
                            if "BkpExt" in c and b == 'r':
                                d = c.split('BkpExt')
                                e = str(d[0])+"Bkp"
                                self.timeIsAvaible[time] = [e]
                                #print "Depois ", self.timeIsAvaible[time]
                            else:
                                print "Erro !", c, b, a
                        
                        else:
                            #print "Duvida ", a, "Era para desalocar ", idReq 
                            self.timeIsAvaible[time] = a
                    except:
                        print "Erro Aqui ", a, idReq
                else:
                    if len(a) == 1:
                        del(self.timeIsAvaible[time])
                    else:
                        b = a[1]
                        self.timeIsAvaible[time] = b
            else:
                print "Existe erro"

        else: 
            print "Esta vazio removeBkp ? ", time, idReq

    # ----------------------------------------------------------------------------------------------- #

    def retornarSlot(self, time):
        if self.isAreBusy(time) == True:
            #esta sendo usado
            return self.timeIsAvaible[time]
        else:
            #esta vazio
            return True

    def reservarSlot(self, time, r):
        self.timeIsAvaible[time] = r

    # ----------------------------------------------------------------------------------------------- #
    def verificarSlotReqUmPorUm(self, time, req):
        try:
            a = self.timeIsAvaible[time]
            
            # Se for um req de bkp
            if type(a) == list:
                for i in range(len(a)):
                    #print a[i], req
                    if a[i] == req:
                        return True

                #print a[i], req
                #print "Noo"
                return False
        
            else:
                #se for um path
                if self.timeIsAvaible[time] == req:
                    #print self.timeIsAvaible[time], req
                    return True
                #print self.timeIsAvaible[time], req
                #print "Nao"
                return False
                
        except:
            #print "Except"
            return False


    def getSlot(self):
        return self.timeIsAvaible
    
    def cleanTimeInSlot(self, time):
        if self.isAreBusy(time) == True:
            del(self.timeIsAvaible[time])

    def livre(self):
        if self.timeIsAvaible.keys() == []:
            return True
        else:
            return False

    def utilizado(self):
        return len(self.timeIsAvaible) 

    def utilizadoUmPorUm(self):
        
        usados = 0

        for i in self.timeIsAvaible.values():
            if type(i) == list:
                if len(i) > 1:
                    usados += 1
            else:
                usados += 1 

            if usados > 0:
                return usados
        
        return usados

    def printTimeSlot(self):

        for tempo in self.timeIsAvaible.keys():
            print "Time ", tempo
            print "Req: ", self.timeIsAvaible[tempo]
            
