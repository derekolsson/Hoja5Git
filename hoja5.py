import simpy
import random

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# env: environment de simpy
# name: identificacion del task
# memory:  cola para RAM (container)
# cpu: cola para procesador
# creation_time: tiempo para esperar antes de crear Task
# needed: cantidad de operaaciones requeridas



#STATES:
#       1= ready
#       2= waiting
def task(env, name, memory, cpu , creation_time, needed):
    global avgTime     
    # Creation of the process
    yield env.timeout(creation_time)
    created= env.now         #Arrival time
    print "Task ",name,"Created at ",created
    #now in NEW
    state = 1    
    while (needed!=0):
        if state==1:
            print "Task ",name,"Getting memory"
            requesting = random.randint(1,needed)
            print "Task ",name,"needs ",requesting
            yield memory.get(requesting)
            print "Task ",name,"Got memory"
            with cpu.request() as req:  #pedimos atención del cpu
                yield req
            if (needed>3):
                needed = needed-3
                state = random.randint(1,2)
            else:
                needed = 0
            memory.put(requesting)
        if state==2:
            waitTime = random.randint(1,5)
            yield env.timeout(waitTime)

            
                
            
            #yield env.timeout(charge_duration)
    print "Task ",name,"Done at ",env.now        
    total = env.now - created
    avgTime += total   #Put this in a list or something instead to get standard deviation
    #print('%s took %s at the gas station' % (name, total))
    

#
env = simpy.Environment()  #crear ambiente de simulacion
processor = simpy.Resource(env) #cola para cpu
ram = simpy.Container(env,init=100, capacity=100) #RAM tiene 100 unidades de memoria

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

interval = 10
nTasks = 3
avgTime =  0.0
# crear los tasks
for i in range(nTasks):
    t = random.expovariate(1.0 / interval)
    processesNeeded= random.randint(1,10)
    env.process(task(env, 'Task %d' % i, ram, processor, t,processesNeeded))

# correr la simulacion
env.run()

avgTime = avgTime/nTasks
print "Average Time: ", avgTime
    
