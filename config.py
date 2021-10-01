RANDOM_SEED = 50

MAX_TIME = 10000000  #diminuir 2 zeros

#NUM_OF_REQUESTS = 10 000 
NUM_OF_REQUESTS = 5000


# SIM = 1 -> 100% caminho primario e backup
# SIM = 2 -> 100% caminho primario e backup, usando lista de caminhos
# SIM = 2.1 -> 100% caminho primario e backup, usando lista de caminhos protecao 1:1
# SIM = 3 -> 50% caminho primario e backup, usando lista de caminhos
# SIM = 4 -> 50% caminho primario e backup, usando lista de caminhos, com desalocacao dinamica
# SIM = 5 -> 50% caminho primario e backup, usando lista de caminhos, com desalocacao dinamica reversa
# SIM = 7 -> Aloca igual P2(100% caminho primario e backup) e desaloca igual P4 (desalocao dinamica)
# SIM = 8 -> Aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4, com desalocacao dinamica

# SIM = 8.2 - Protecao Elastica -> Aloca proporcao de 1/2 1/3 1/4 - 1/2 2/3 3/4, com desalocacao dinamica, e expansao de slots

SIM = 8.2

#ERLANG_INC = 50
ERLANG_INC = 5

#ERLANG_MIN = 26
ERLANG_MIN = 55

#ERLANG_MAX = 44
ERLANG_MAX = 95

BANDWIDTH = [5,50,100]
#BANDWIDTH = [5,50,100,150,200]

#DATA = [100,500]
DATA = [100, 500]

#CLASS_TYPE = [1,2]
CLASS_TYPE = [1,2]

#DEADLINE = [0.3,0.5,1] ## Atraso maximo que cada requisicao pode sofrer 
DEADLINE = [0.3,0.5,1]

#DEAD usado na simulacao
DEAD = [5,10,25,50]
#DEAD = [2,4,6,8,10]

#PER = [0.3,0.5,0.7] ## Porcentagem sem QoS
PER = [0.3,0.5,0.7]

TOPOLOGY = 'nsfnet'

HOLDING_TIME = 2.0

#SLOTS = 24
SLOTS = 300

SLOT_SIZE = 12.5

