from Tkinter import *

root = Tk()

root.geometry("235x410+0+0")
root.title("Simulador")
#root.configure(background='green')



#Criando o texto do formulario
Label(root, text="Random Seed: "    ).grid(row=0, column=0)
Label(root, text="Max Time: "       ).grid(row=1, column=0)
Label(root, text="Num of Requests: ").grid(row=2, column=0)
Label(root, text="Sim: "            ).grid(row=3, column=0)
Label(root, text="Earling inc: "    ).grid(row=4, column=0)
Label(root, text="Earlang min: "    ).grid(row=5, column=0)
Label(root, text="Earlang max: "    ).grid(row=6, column=0)
Label(root, text="Bandwidth: "      ).grid(row=7, column=0)
Label(root, text="Data: "           ).grid(row=8, column=0)
Label(root, text="Class type: "     ).grid(row=9, column=0)
Label(root, text="Deadline: "       ).grid(row=10, column=0)
Label(root, text="Dead: "           ).grid(row=11, column=0)
Label(root, text="Per: "            ).grid(row=12, column=0)
Label(root, text="Topology: "       ).grid(row=13, column=0)
Label(root, text="Holding Time: "   ).grid(row=14, column=0)
Label(root, text="Reps: "           ).grid(row=15, column=0)
Label(root, text="Slots: "          ).grid(row=16, column=0)
Label(root, text="Slot size: "      ).grid(row=17, column=0)

#Criando as entradas
RANDOM_SEED     = Entry(root)
MAX_TIME        = Entry(root)
NUM_OF_REQUESTS = Entry(root)
SIM             = Entry(root)
ERLANG_INC      = Entry(root)
ERLANG_MIN      = Entry(root)
ERLANG_MAX      = Entry(root)
BANDWIDTH       = Entry(root)
DATA            = Entry(root)
CLASS_TYPE      = Entry(root)
DEADLINE        = Entry(root)
DEAD            = Entry(root)
PER             = Entry(root)
TOPOLOGY        = Entry(root)
HOLDING_TIME    = Entry(root)
REPS            = Entry(root)
SLOTS           = Entry(root)
SLOT_SIZE       = Entry(root)

#Posicionando as entradas
RANDOM_SEED.grid(row=0, column=1)
MAX_TIME.grid(row=1, column=1)
NUM_OF_REQUESTS.grid(row=2, column=1)
SIM.grid(row=3, column=1)
ERLANG_INC.grid(row=4, column=1)
ERLANG_MIN.grid(row=5, column=1)
ERLANG_MAX.grid(row=6, column=1)
BANDWIDTH.grid(row=7, column=1)
DATA.grid(row=8, column=1)
CLASS_TYPE.grid(row=9, column=1)
DEADLINE.grid(row=10, column=1)
DEAD.grid(row=11, column=1)
PER.grid(row=12, column=1)
TOPOLOGY.grid(row=13, column=1)
HOLDING_TIME.grid(row=14, column=1)
REPS.grid(row=15, column=1)
SLOTS.grid(row=16, column=1)
SLOT_SIZE.grid(row=17, column=1)

#Definindo o evento ao clickar no botao
def run_simulator():
    #criando o txt com os novos parametros
    txt_config = open('config.txt', 'w')
    txt_config.write("RANDOM_SEED = " + RANDOM_SEED.get())
    txt_config.write("\n\nMAX_TIME = " + MAX_TIME.get())
    txt_config.write("\n\nNUM_OF_REQUESTS = " + NUM_OF_REQUESTS.get())
    txt_config.write("\n\nSIM = " + SIM.get())
    txt_config.write("\n\nERLANG_INC = " + ERLANG_INC.get())
    txt_config.write("\n\nERLANG_MIN = " + ERLANG_MIN.get())
    txt_config.write("\n\nERLANG_MAX = " + ERLANG_MAX.get())
    txt_config.write("\n\nBANDWIDTH = " + BANDWIDTH.get())
    txt_config.write("\n\nDATA = " + DATA.get())
    txt_config.write("\n\nCLASS_TYPE = " + CLASS_TYPE.get())
    txt_config.write("\n\nDEADLINE = " + DEADLINE.get())
    txt_config.write("\n\nDEAD = " + DEAD.get())
    txt_config.write("\n\nPER = " + PER.get())
    txt_config.write("\n\nTOPOLOGY = " + TOPOLOGY.get())
    txt_config.write("\n\nHOLDING_TIME = " + HOLDING_TIME.get())
    txt_config.write("\n\nREPS = " + REPS.get())
    txt_config.write("\n\nSLOTS = " + SLOTS.get())
    txt_config.write("\n\nSLOT_SIZE = " + SLOT_SIZE.get() + "\n")
    txt_config.close()
    #Abrindo o simulador
    #import {arquivo do simulador} 
    
    

#Criando botao "run"
runbt = Button(root, text=("Run"), command=run_simulator).grid(row=18, column=0, columnspan=2, sticky=W+E+N+S)


root.mainloop()
