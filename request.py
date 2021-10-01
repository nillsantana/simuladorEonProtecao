
class Request():
    
    def __init__(self, idReq, src, dst, time, data, deadline):
        self.idReq = idReq
        self.src = src
        self.dst = dst
        self.prioridade = -1 
        self.timeSimIni = 0
        self.timeSimulacao = 0
        self.time = time #tempo inicial do caminho principal
        self.timeBkp = 0 #tempo inicial do caminho de bkp
        self.data = data # dados
        self.deadline = deadline #tempo maximo da requisicao
        self.path = []
        self.pathBkp = []
        self.numSlots = 0
        self.numSlotsBkp = 0
        self.slotsAlocados = []
        self.slotsAlocadosBkp = []
        self.slotsAdicionaisBkp = []
        self.duracao = 0
        self.duracaoBkp = 0
        self.holdTimeSlot = 0
        self.holdingSlotPrim = 0
        self.holdingSlotBkp = 0
        self.contSlot = 0
        self.contSlotBkp = 0
        self.casoDes = 0

    def __str__(self):
        return "Id:%s\nSrc,Dst :[%s-%s] - Chegada:%s - Prioridade:%s - Path:%s - PathBkp:%s\nNumSlots:%s - NumSlotsBkp:%s Slots:%s - SlotsBkp:%s - SlotsAdicionaisBkp:%s\nArrival:%s - Tam:%s - Duracao:%s - DuracaoBkp:%s - Deadline:%s - timeIniPrim:%s - timeIniBkp:%s\nHoldingTimeSlot:%s - HoldingTimePrim:%s - HoldingTimeBkp:%s - contSlot:%s - contSlotBkp:%s - contSlotBkp:%s\n"%(self.idReq,self.src, self.dst, self.timeSimIni, self.prioridade,self.path, self.pathBkp, self.numSlots, self.numSlotsBkp, self.slotsAlocados, self.slotsAlocadosBkp, self.slotsAdicionaisBkp, self.time, self.data, self.duracao, self.duracaoBkp, self.deadline, self.time, self.timeBkp, self.holdTimeSlot, self.holdingSlotPrim, self.holdingSlotBkp, self.contSlot, self.contSlotBkp, self.casoDes)