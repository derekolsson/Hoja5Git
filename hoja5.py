import simpy
import random

# env: environment de simpy
# name: identificacion del task
# memory:  cola para RAM (container)
# cpu: cola para procesador(Resource)
# creation_time: tiempo para esperar antes de crear Task
# needed: cantidad de operaciones requeridas



#STATES:
#       1= ready
#       2= waiting
def task(env, name, memory, cpu , creation_time, needed):
    global avgTime     
    # Creation of the process
    yield env.timeout(creation_time)
    created= env.now         #Arrival time
    print "Task ",name,"Created at ",created,"with ",needed,"processes"
    #now in NEW
    print "Task ",name,"Getting memory"
    requesting = random.randint(1,needed)
    print "Task ",name,"needs ",requesting
    if requesting>memory.level:
        print "\nWaiting on ram....."
    yield memory.get(requesting)
    print "Task ",name,"Got memory"    
    state = 1    
    while (needed!=0):
        if state==1:
#            print "Task ",name,"Getting memory"
#            requesting = random.randint(1,needed)
#            print "Task ",name,"needs ",requesting
#            yield memory.get(requesting)
#            print "Task ",name,"Got memory"
            with cpu.request() as req:  #pedimos atención del cpu
                yield req
                yield env.timeout(1)
            print "Task ",name,"Was Attended to"
            if (needed>speed):
                needed = needed-speed
                state = random.randint(1,2)
                print "Task ",name,"processed, still has",needed
                print "Sent to state ",state
            else:
                needed = 0
                print "Task ",name,"finished"
                memory.put(requesting)
                print "Task ",name,"Gave back ram"
        if state==2:
            waitTime = random.randint(1,10)
            print "Task ",name,"will wait",waitTime
            yield env.timeout(waitTime)
            state = 1

            
                
            
            #yield env.timeout(charge_duration)
    print "Task ",name,"Done at ",env.now        
    total = env.now - created
    avgTime += total   #Put this in a list or something instead to get standard deviation
    

#CONFIGURACION DE PROCESOS
interval = 5
nTasks = 25

#CONFIGURACION DEL RAM
availableRAM= 100

#CONFIGURACION DEL PROCESADOR
speed = 3   #procesos que se puede realizar en 1 
cores = 1


#
env = simpy.Environment()  #crear ambiente de simulacion
processor = simpy.Resource(env, capacity = cores) #cola para cpu
ram = simpy.Container(env,init=availableRAM, capacity=availableRAM) #RAM tiene 100 unidades de memoria

RANDOM_SEED = 42
random.seed(RANDOM_SEED)



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
    
