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

def task(env, name, memory, cpu , creation_time, needed):
    global avgTime     
    # Creation of the process
    yield env.timeout(creation_time)
    while (needed > 0):
        
        #print('%s arriving at %d' % (name, env.now))
        arrive= env.now         #Arrival time
        with cpu.request() as req:  #pedimos atención del cpu
            yield req
            
            
            #yield env.timeout(charge_duration)
            
        total = env.now - arrive
        avgTime += total   #Put this in a list or something instead to get standard deviation
        print('%s took %s at the gas station' % (name, total))
    

#
env = simpy.Environment()  #crear ambiente de simulacion
waiting = simpy.Resource(env) #cola para cpu
ready = simpy.Container(env, capacity=100) #RAM tiene 100 unidades de memoria

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

interval = 10
nTasks = 25
avgTime =  0.0
# crear los tasks
for i in range(nTasks):
    t = random.expovariate(1.0 / interval)
    env.process(task(env, 'Task %d' % i, ready, waiting, t, 10))

# correr la simulacion
env.run()

avgTime = avgTime/nTasks
print "Average Time: ", avgTime
    
