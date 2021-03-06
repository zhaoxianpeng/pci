import time
import random
import math

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]

destination = 'LGA'

flights={}

for line in open('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin, dest), [])
    flights[(origin, dest)].append((depart,arrive,int(price)))

def getminutes(t):
    x=time.strptime(t, '%H:%M')
    return x[3]*60+x[4]

def printschedule(r):
    for d in range(int(len(r)/2)):
        name = people[d][0]
        origin = people[d][1]
        out=flights[(origin, destination)][r[2*d]]
        ret = flights[(destination,origin)][r[2*d + 1]]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' %(name, origin, out[0], out[1], out[2], ret[0], ret[1],ret[2]))

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep=24*60

    for d in range(int(len(sol)/2)):
        origin = people[d][1]
        out=flights[(origin, destination)][sol[2*d]]
        ret = flights[(destination,origin)][sol[2*d + 1]]

        totalprice += out[2]
        totalprice += ret[2]

        if latestarrival < getminutes(out[1]): latestarrival = getminutes(out[1])
        if earliestdep > getminutes(ret[0]): earliestdep = getminutes(ret[0])

    totalwait = 0;

    for d in range(int(len(sol)/2)):
        origin = people[d][1]
        out = flights[(origin, destination)][sol[2 * d]]
        ret = flights[(destination, origin)][sol[2 * d + 1]]
        totalwait += latestarrival - getminutes(out[1])
        totalwait += getminutes(ret[0]) - earliestdep

    if latestarrival > earliestdep: totalprice += 50

    return totalprice + totalwait

def randomoptimize(domain, costf):
    best = 99999999
    bestr = None

    for i in range(1000):
        r = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
        cost = costf(r)

        if cost < best:
            best = cost
            bestr = r
    return bestr


def hillclimb(domain, costf):

    sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while 1:
        neighbors = []

        for j in range(len(domain)):
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
        current = costf(sol)
        best = current

        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best=cost
                sol=neighbors[j]

        if best == current: break

    return sol

def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step = 1):
    vec = [int(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]

    while T>0.1:
        i = random.randint(0, len(domain) -1)
        dir = random.randint(-step, step)
        vecb=vec[:]
        vecb[i]+=dir
        if vecb[i] < domain[i][0]: vecb[i]=domain[i][0]
        elif vecb[i] > domain[i][1]: vecb[i] = domain[i][1]

        ea=costf(vec)
        eb=costf(vecb)

        if (eb < ea or random.random() < pow(math.e, -(eb-ea)/T)):
            vec=vecb
        T=T*cool
    return vec

if __name__ == '__main__':

    domain = [(0,9)]*(len(people) * 2)
    print(domain)
    s=randomoptimize(domain, schedulecost)
    print(schedulecost(s))
    printschedule(s)

    s=hillclimb(domain, schedulecost)
    print(schedulecost(s))
    printschedule(s)

    s=annealingoptimize(domain, schedulecost)
    print(schedulecost(s))
    printschedule(s)