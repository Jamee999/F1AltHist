import random, time

print ()

with open('f1data.csv', 'r') as f:
    RawDrivers = [line.strip() for line in f]


Year = 1950

class Driver():
    Name = ''
    Team = ''
    First = 0
    Last = 0
    #Age = Year-DOB
    Pref = ''
    Rating = 0
    Contract = 0
    Points = 0
    Wins = 0
    Podiums = 0
    DNFs = 0
    Rep = 0
    TeamRatio = 0
    TMRating = 0
    TeamRating = 0
    Program = ''
    Power = 0

allDrivers = []

n = 0
for i in RawDrivers:
    i = i.split(',')
    a = Driver()
    a.Name = i[0].strip()
    a.First = int(i[1])
    if a.First == 1950:
        a.Last = int(i[2])
    else:
        a.Last = max(int(i[2]), a.First + random.randrange(13,17))
    a.Rating = float(i[3])
    a.Pref = i[4]
    allDrivers.append(a)
    n = n+1

Drivers = []

for i in allDrivers:
    if i.First <= Year and i.Last >= Year:
        Drivers.append(i)


class Team():
    Name = ''
    Drivers = []
    Rating = 1
    Points = 0
    FutureDrivers = []
    Affiliate = ''

Teams = []
TeamNames = ['Alfa Romeo', 'Ferrari', 'Maserati', 'Cooper']
cardict = {'Alfa Romeo':200,'Ferrari':15,'Maserati':4,'Cooper':3,'Privateer':1}

Races = ['GBR', 'MON', 'SUI', 'BEL', 'FRA', 'ITA']

Champions = []

for i in TeamNames:
    a = Team()
    a.Name = i
    a.Rating = cardict[i]
    Teams.append(a)

def race (Drivers, Teams, n):
    Standings = []

    xDrivers = [i for i in Drivers if i.Team != '' and i not in Standings]

    Chaos = max(1, random.uniform(-18,2))**2
    #Chaos = 3
    #print(Chaos)
    DNFs = []
    if Chaos > 2:
        RetFac = 0.05
    else:
        RetFac = 0.06 + (2020-Year)/1000
    while len(Standings) < n:
        total = 0
        for i in xDrivers:
            for j in Teams:
                if i.Team == j.Name:
                    i.TeamRating = j.Rating
            if i.Rating * i.TeamRating > 1:
                i.Power = (i.Rating * i.TeamRating)**(1/Chaos)
            else:
                i.Power = (i.Rating * i.TeamRating)
            #print (i.Name, i.Power)
            total = total + i.Power

        x = random.uniform(0,total)
        #print (x)
        count = 0
        for i in xDrivers:
            count = count + i.Power
            if x < count:
                if random.random() > RetFac*Chaos**1.5:
                    Standings.append(i)
                    xDrivers.remove(i)
                    #print (len(Standings), i.Name, i.Team, i.Power)
                    break
                elif i not in DNFs:
                    DNFs.append(i)
                    xDrivers.remove(i)
                    break
        if len(xDrivers) == 0:
            xDrivers = [i for i in Drivers if i.Team != '' and i not in Standings]
    for i in xDrivers:
        if random.random() > 2*RetFac*(Chaos+1):
            pass
        elif i not in DNFs:
            DNFs.append(i)
    return Standings, DNFs, Chaos

n = 0
for i in Drivers:
    i.Points = 0
    if n < 3:
        i.Team = 'Alfa Romeo'
    elif n < 6:
        i.Team = 'Ferrari'
    elif n < 9:
        i.Team = 'Maserati'
    elif n < 11:
        i.Team = 'Cooper'
    elif n < 24:
        i.Team = 'Privateer'
    n = n+1


def eval (d, t, y):
    if d.Team != '' or d.Last < y:
        return -1000
    if t.Name in d.Name:
        return (d.Rating**0.5 + d.Rep) * (random.random() + 1)
    elif d.Pref == t.Name:
        return (d.Rating**0.5  + d.Rep) * (random.random() + 0.2)
    else:
        return (d.Rating**0.5 + d.Rep) * random.random()

def teammake (n, r):
    global Teams, Year
    for i in Teams:
        if i.Name == n:
            return False
    if (len(Teams) < 13 and Year > 1975) or len(Teams) < 10:
        a = Team()
        a.Name = n
        a.Rating = r
        Teams.append(a)
        print ('New Team:', a.Name)
        print ()
        return True
    else:
        return False

def season (Drivers, Teams, Year, Races):
    global allDrivers
    print (Year)

    for i in Drivers:
        i.Points = 0
        i.Wins = 0
        i.DNFs = 0
        i.Podiums = 0

    if Year < 1960:
        pointsdict = {1:8,2:6,3:4,4:3,5:2}
    elif Year < 1970:
        pointsdict = {1:8,2:6,3:4,4:3,5:2,6:1}
    elif Year < 1980:
        pointsdict = {1:9,2:6,3:4,4:3,5:2,6:1}
    elif Year < 2000:
        pointsdict = {1:10,2:6,3:4,4:3,5:2,6:1}
    elif Year < 2010:
        pointsdict = {1:10,2:8,3:6,4:5,5:4,6:3,7:2,8:1}
    else:
        pointsdict = {1:25,2:18,3:15,4:12,5:10,6:8,7:6,8:4,9:2,10:1}

    Teams.sort(key = lambda x: x.Rating, reverse = True)

    for i in Teams:
        print (i.Name, i.Rating, end = ', ')
    print()
    
    for j in range (len(Races)):
        #time.sleep(0.01)
        x, y, z = race (Drivers, Teams, len(pointsdict))
        print (Races[j], x[0].Name.ljust(25), x[1].Name.ljust(25), x[2].Name.ljust(25), x[3].Name.ljust(25), x[4].Name.ljust(25), str(round(z,1)).ljust(3), end=' ')
        print ('DNF: ', end='')
        print (len(y), end =' ')
        #for i in y:
            #print (i.Name, end=', ')
        for i in Drivers:
            if x[0].Name == i.Name:
                i.Wins = i.Wins+1
                i.Rep = i.Rep + 0.2
            if i in y:
                i.DNFs = i.DNFs+1
            if x[0].Name == i.Name or x[1].Name== i.Name or x[2].Name == i.Name:
                i.Podiums = i.Podiums+1
                i.Rep = i.Rep + 0.1
        for k in range (len(pointsdict)):
            for i in Drivers:
                if x[k].Name == i.Name:
                    i.Points = i.Points + pointsdict[k+1]
                    if Year < 2010:
                        i.Rep = i.Rep + (pointsdict[k+1])/1000
                    else:
                        i.Rep = i.Rep + (pointsdict[k+1])/5000
        print ()

    Drivers.sort(key = lambda x: x.Points + x.Wins/1000)
    print ()
    print ('Driver'.ljust(25), 'Team'.ljust(15), 'Pts', ' W', ' P', 'DNF')
    for i in Drivers:
        if i.Team != '':
            print (i.Name.ljust(25), i.Team.ljust(15), str(i.Points).rjust(3), str(i.Wins).rjust(2), str(i.Podiums).rjust(2), i.DNFs, '      ',round(i.Rep,1),i.Rating)

    global Champions
    Champions.append([Year, Drivers[-1].Name, Drivers[-1].Team])

    Champion = Drivers[-1]

    for i in Drivers:
        if i.Name == Champion.Name:
            i.Rep = i.Rep + 1

    print()

    for i in Drivers:
        if i.Last == Year:
            Drivers.remove(i)

    for i in allDrivers:
        if i.First == Year+1:
            Drivers.append(i)

    if random.random() < 0.01:
        teammake('BMW',1)
    if random.random() < 0.01:
        teammake('Ford',1)
    if random.random() < 0.01:
        teammake('Nissan',1)
    if random.random() < 0.01:
        teammake('Chevrolet',1)
    if random.random() < 0.01:
        teammake('Volkswagen',1)
    if Year+1 == 1954:
        teammake('Mercedes',70)
    if Year+1 == 1956:
        teammake('B.R.M.',1)
    if Year+1 == 1960:
        teammake('Lotus',1)
    if Year+1 == 1964:
        teammake('Honda',1)
    if Year+1 == 1966:
        v = teammake('Brabham',1)
        if v == True:
            for i in Drivers:
                if i.Name == 'Jack Brabham':
                    i.Team = 'Brabham'
    if Year+1 == 1967:
        v = teammake('McLaren',1)
        if v == True:
            for i in Drivers:
                if i.Name == 'Bruce McLaren':
                    i.Team = 'McLaren'
    if Year+1 == 1970:
        teammake('Tyrell',1)
    if Year+1 == 1976:
        teammake('Ligier',1)
    if Year+1 == 1978:
        teammake('Williams',1)
    if Year+1 == 1977:
        teammake('Renault',1)
    if Year+1 == 1986:
        teammake('Benetton',1)
    if Year+1 == 1991:
        teammake('Jordan',0.1)
    if Year+1 == 1993:
        teammake('Sauber',0.1)
    if Year+1 == 2002:
        teammake('Toyota',0.1)
    if Year+1 == 2005:
        teammake('Red Bull',1)
    if Year+1 == 2016:
        teammake('Haas',0.1)

    for i in Teams:
        if ((i.Rating < 10 and random.random() < 1/100) or (i.Rating < 1 and random.random() < 1/20))  and len(Teams) > 10 and i.Name != 'Ferrari':
            print ()
            print (i.Name, 'leaving F1.')
            print ()
            Teams.remove(i)

    for i in Drivers:
        i.Contract = i.Contract - 1

    print (Year+1, 'Lineups')

    Teams.sort(key= lambda x: x.Rating, reverse = True)
    for i in Teams:
        i.Drivers = []
        for j in Drivers:
            if i.Name == j.Team and j.Last > Year:
                if random.random() < (1/3 + (j.Wins/100)) or j.Contract > 0 or j == Champion or Team.Name in j.Name:
                    i.Drivers.append(j)
                    #print (i.Name.ljust(20), j.Name.ljust(20))
                else:
                    j.Team = ''
            elif j.Last <= Year:
                j.Team = ''

    for i in Teams:
        if Year < 1975:
            while len(i.Drivers) < 3:
                Drivers.sort(key= lambda x: eval (x, i, Year), reverse = True)
                Drivers[0].Team = i.Name
                if i.Rating > 5:
                    Drivers[0].Contract = random.randrange(2,4)
                else:
                    Drivers[0].Contract = random.randrange(1,2)
                i.Drivers.append(Drivers[0])
                #print (i.Name.ljust(20), Drivers[0].Name.ljust(20),round(Drivers[0].Rep,1))
        else:
            while len(i.Drivers) < 2:
                Drivers.sort(key= lambda x: eval (x, i, Year), reverse = True)
                Drivers[0].Team = i.Name
                if i.Rating > 10:
                    Drivers[0].Contract = random.randrange(2,5)
                else:
                    Drivers[0].Contract = random.randrange(1,3)
                i.Drivers.append(Drivers[0])
                #print (i.Name.ljust(20), Drivers[0].Name.ljust(20),round(Drivers[0].Rep,1))

    for i in Teams:
        if random.random() < 1/10 and i.Rating < 250:
            i.Rating == i.Rating * 20 * random.random()
        elif i.Rating < 250:
            if random.random () < 0.5:
                i.Rating = i.Rating*random.uniform(1,2)
            else:
                i.Rating = i.Rating*random.uniform(0.25,1)
        else:
            i.Rating = i.Rating*random.random()*random.random()
        if Year % 7 == 0:
            if random.random() > 1/5:
                i.Rating = max(4*random.random()*random.random()*random.random(), random.random()*i.Rating**(1/2))
            else:
                i.Rating = (random.uniform(0,10)**2)*i.Rating**(1/2)
        if Year % 3 == 0:
            if random.random() > 1/2:
                i.Rating = i.Rating * 20 * random.random()
        else:
            pass
        if i.Rating < 1/2:
            i.Rating = i.Rating*random.uniform(1,4)

        i.Rating = round(i.Rating,1)


    for i in Teams:
        print (i.Name.ljust(20), end = ' ')
        for j in i.Drivers:
            print (j.Name.ljust(20), end = ' ')
        print ()

    return Drivers, Teams


def calendar (r, y):
    print ()
    possibles = ['ESP', 'GER', 'NED', 'ARG', 'MOR', 'POR', 'USA','AUT']

    if y > 1960:
        possibles = possibles + ['MEX', 'CAN', 'RSA', 'BRA', 'JPN']
    if y > 1970:
        possibles = possibles + ['DEN', 'SMR', 'EUR', 'USW', 'SWE']
    if y > 1980:
        possibles = possibles + ['AUS', 'HUN', 'URU', 'DET', 'IRE']
    if y > 1990:
        possibles = possibles + ['MAL', 'PAC', 'CHN', 'FIN', 'RUS']
    if y > 2000:
        possibles = possibles + ['BAH', 'ABU', 'TUR', 'SIN', 'KOR']
    if y > 2010:
        possibles = possibles + ['NYC', 'AZB', 'VIE', 'IND', 'QAT']

    for i in r:
        if i not in ['MON', 'GBR', 'BEL', 'ITA', 'JPN'] and random.random() < 0.01:
            r.remove(i)
            possibles.append(i)
            print ('Grand Prix removed:', i)

    change = False
    fail = False
    while fail == False:
        try:
            if random.random() < 0.25:
                candidates = [i for i in possibles if i not in r]
                x = random.choice(candidates)
                if x == 'USW' and 'USA' not in r:
                    x = 'USA'
                r.append(x)
                print ('New Grand Prix:', x) 
                change = True
            else:
                fail = True
        except:
            break

    summer = ['GBR','MON','BEL','FRA','ITA','GER','SUI','ESP','NED','POR','AUT','CAN',
              'DEN','SMR','EUR','SWE','HUN','POL','DET','IRE','TUR','CZE','AZB','FIN']
    flyaways = [i for i in r if i not in summer]


    def rate (x, s, f):
        timedict = {'MON':-0.75,'ITA':0.9,'BEL':0.89,'GBR':0, 'SMR':-0.9}
        try:
            return timedict[x]
        except:
            if x in f:
                return random.uniform(-100,100)
            else:
                return random.uniform(-1,1)
    if change == True:
        r.sort(key = lambda x: rate(x, summer, flyaways))
    
    return r
        

while Year < 2020:
    print ()
    Drivers, Teams = season (Drivers, Teams, Year, Races)
    Year = Year + 1

    Races = calendar (Races, Year)

print ()
print ('World Champions')

for i in Champions:
    n = 0
    for j in Champions:
        if i[1] == j[1] and i[0] >= j[0]:
            n = n + 1
    print (i[0], i[1].ljust(25), i[2].ljust(15), n)       
