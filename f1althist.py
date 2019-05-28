import random, time

print ()

with open('f1data.csv', 'r') as f:
    RawDrivers = [line.strip() for line in f]

with open('f1circuits.csv', 'r') as f:
    RawCircuits = [line.strip() for line in f]

Year = 1950

randomdebut = 'n'

class Driver():
    Name = ''
    ln = ''
    iln = ''
    Team = ''
    First = 0
    Last = 0
    #Age = Year-DOB
    Nat = ''
    Rating = 0
    Peak = 0
    Contract = 0
    Injury = 0
    Sub = ''
    rangz = 0
    Points = 0
    Wins = 0
    CWins = 0
    Podiums = 0
    CPodiums = 0
    DNFs = 0
    Races = 0
    YRaces = 0
    Best = 1000
    Moves = 0
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

    ln = a.Name.split(' ')[-1]
    if ln == ('Jr.' or 'Sr.' or "Jr" or "Sr") or ' de ' in a.Name or ' da ' in a.Name or ' di ' in a.Name or ' von ' in a.Name or ' van ' in a.Name:
        ln = a.Name.split(' ')[-2] + ' ' + ln

    a.ln = ln
    a.iln = a.Name[0] + '. ' + ln
    
    while len(a.Name) > 20:
        if "-" in a.Name:
            a.Name = a.Name.replace("-"," ")
        names = a.Name.split(' ')
        a.Name = ''
        if len (names) > 2 and 'Sr' not in names and 'Jr' not in names:
            names[1] = names[1][0] + "'" + names[1][3:]
        for k in names:
            if len(k) > 15:
                k = k[0] + '.'
            if len(k) == 2 and k[1] == "'":
                k[1] == '.'
            a.Name = a.Name + k + ' '
        a.Name = a.Name[:-1]
        if len(a.Name) > 20 and a.Name[3] != '':
            a.Name = a.Name[0] + "'" + a.Name[3:]
            continue
        elif len(a.Name) > 20:
            a.Name = a.Name[0] + "." + a.Name[3:]
            continue
        
    a.First = int(i[1])
    real = int(i[2])
    if a.First <= 1952:
        a.Last = int(i[2])
    else:
        a.Last = a.First + random.randrange(8,12)
        a.Last = a.Last + round((a.First-1950)/15)
        if a.First >= 1955:
            a.First = a.First + random.randrange(-1,1)
    if a.Last != 2019:
        a.Last = a.Last + random.randrange(-2,2)
    if real > a.Last and (a.Last - a.First < 16 or random.random() < 0.5):
        a.Last = real

    if a.Last == 2019:
        a.Last = a.Last + random.randrange(0, 4)
        
    a.Rating = float(i[3])
    if a.Rating < 1 and a.Last < 2019:
        a.Rating = a.Rating * random.random()
    
    a.Peak = a.Rating ** random.uniform(2/3,4/3)
    a.Nat = i[4]
    allDrivers.append(a)
    n = n+1

if randomdebut == 'y':
    years = [[x.First,x.Last] for x in allDrivers]
    years.sort(key = lambda x: random.random())

    for i in range(len(allDrivers)):
        allDrivers[i].First = years[i][0]
        allDrivers[i].Last = years[i][1]

class Circuit():
    Name = ''
    Race = ''
    First = 0
    Last = 0
    Total = 0

Circuits = []

for i in RawCircuits:
    i = i.split(',')
    a = Circuit()
    a.Name = i[0]
    a.Race = i[1]
    a.First = int(i[2])
    a.Last = int(i[3])
    a.Total = int(i[4])
    Circuits.append(a)

Drivers = []

for i in allDrivers:
    if i.First <= Year and i.Last >= Year:
        Drivers.append(i)


class Team():
    Name = ''
    Drivers = []
    Rating = 1
    Points = 0
    Wins = 0
    Races = 0
    First = 0
    Last = '    '
    rangz = 0
    FutureDrivers = []
    Affiliate = ''
    Owner = ''
    Nat = ''

Teams = []
TeamNames = ['Alfa Romeo', 'Ferrari', 'Maserati', 'Cooper','Privateer']
cardict = {'Alfa Romeo':600,'Ferrari':200,'Maserati':160,'Cooper':40,'Privateer':1}
formers = []
formerTeams = []

Races = ['GBR', 'MON', 'SUI', 'BEL', 'FRA', 'ITA']

Champions = []

for i in TeamNames:
    a = Team()
    a.Name = i
    a.Rating = cardict[i]
    a.First = 1950
    if i == 'Alfa Romeo' or i == 'Ferrari' or i == 'Maserati':
        a.Nat = "Italy"
    elif i == 'Cooper':
        a.Nat = 'United Kingdom'
    Teams.append(a)

def teamfind (x, t):
    for i in t:
        if i.Name == x:
            return i

def race (Drivers, Teams, n, c):
    Standings = []

    xDrivers = [i for i in Drivers if i.Team != '' and i not in Standings]

    for i in xDrivers:
        if i.Team == 'Privateer' and random.random() < 0.5*i.Rating:
            xDrivers.remove(i)
        elif i.Sub != '':
            for j in Drivers:
                if i.Sub == j:
                    j.Team = i.Team
                    j.Injury = -1
                    xDrivers.append(j)
                    xDrivers.remove(i)

    t = len(xDrivers)

    Chaos = max(1, random.uniform(-17,3)+c)**1.5
    #Chaos = 3
    #print(Chaos)
    DNFs = []
    if Chaos > 4:
        print ('Chaotic race!!!')
    elif Chaos > 3:
        print ('Chaotic race!!')
    elif Chaos > 2:
        print ('Chaotic race!')

    RetFac = random.random()/8 + (2020-Year)/350 + (Chaos**2)/100

    Pole = ''

    y = 27 + ((2020-Year)/7)*random.random()

    if Year > 1985:
        y = 26

    if y > t+1:
        y = t+1
        
    while y > len(Standings) + len(DNFs) < t:
        total = 0
        for i in xDrivers:
            if i.Rating * i.Team.Rating > 1:
                i.Power = (i.Rating * i.Team.Rating)**(1/Chaos)
            else:
                i.Power = (i.Rating * i.Team.Rating)
            #print (i.Name, i.Power)
            total = total + i.Power

        if Pole == '':
            xDrivers.sort(key = lambda x:( 100*random.random()* + 2*random.random()*x.Power ), reverse = True)
            Pole = xDrivers[0]
            xDrivers[0].Power = 50 + xDrivers[0].Power * 1.25
            xDrivers[0].Rep = xDrivers[0].Rep + 0.1

        x = random.uniform(0,total)
        #print (x)
        count = 0
        for i in xDrivers:
            #print (i.Name, i.Team.Name, i.Power)
            count = count + i.Power
            if x < count:
                if len(Standings) + len(DNFs) < t:
                    z = RetFac + max(0, (6-i.Rating)**2/500)
                    if len(Standings) > n:
                        z = z+0.1

                    if z > 0.8:
                        z = 0.8
                    if random.random() > z:
                        Standings.append(i)
                        xDrivers.remove(i)
                        break
                    elif i not in DNFs:
                        DNFs.append(i)
                        xDrivers.remove(i)
                        break


    DNFs.sort(key= lambda x: random.random())


    Standings = Standings + DNFs

    DNQs = [x for x in xDrivers if x not in Standings]

    xDrivers = [i for i in Drivers]

    PodTeams = []

    n = 0
    while len(PodTeams) < 3:
        for i in xDrivers:
            if Standings[n] == i.Sub or Standings[n] == i:
                PodTeams.append(i.Team)
                n = n + 1
                break

    for i in Standings:
        if i.Sub != '':
            Standings.remove(i)

    for i in Drivers:
        if i.Injury == -1:
            i.Team = ''

    return Standings, DNFs, Chaos, PodTeams, Pole, DNQs


n = 0
for i in Drivers:
    i.Points = 0
    if n < 3:
        i.Team = teamfind('Alfa Romeo', Teams)
    elif n < 6:
        i.Team = teamfind('Ferrari', Teams)
    elif n < 9:
        i.Team = teamfind('Maserati', Teams)
    elif n < 11:
        i.Team = teamfind('Cooper', Teams)
    elif n < 20:
        i.Team = teamfind('Privateer', Teams)
    n = n+1
    for j in Teams:
        if i.Team == j:
            j.Drivers.append(i)



def eval (d, t, y, m):
    for i in Teams:
        if i.Owner == d and d != i:
            return - 1000
    if d.Last <= y or d.First > y+1 or (d.Team != '' and m != 'mid') or (m == 'mid' and d.First == y+1 and y != 1950) or (m == 'mid' and Champion == d):
        return -1000
    if t.Owner == d.Name and d.Last <= y:
        return 1000

    twdc = sum([x.rangz for x in t.Drivers])
    
    x = d.Rating + d.Peak + d.Rep + d.Wins + d.Podiums/5 - max(2.5,d.Races**(1/3)) - 25*twdc*d.rangz*random.random() #- min(20, (1+y-d.First)**1.25)
    
    if d.Nat == t.Nat:
        return x * (random.random() + 1/5)
    else:
        return x * random.random()

def teammake (n, r, o, nat):
    global Teams, Year, Drivers
    for i in Teams:
        if i.Name == n:
            return False
    if ( (len(Teams) < 15 and Year > 1975) or (len(Teams) < 10 and Year > 1975) or (len(Teams) < 7) ) and n != 'Privateer':
        a = Team()
        a.Name = n
        a.Rating = random.random()*100*r
        a.Owner = o
        a.First = Year + 1
        a.Nat = nat
        Teams.append(a)
        print ('New Team:', a.Name)
        if o != '':
            for j in Drivers:
                if j.Name == o:
                    j.Team = a
                    j.Contract = 10
                    a.Drivers.append(j)
        return True
    else:
        return False

def pick(ts, k, ad, i, ds): #teams, team, allDrivers, driver, drivers
    global Year
    worseteam = False
    oldteam = ''
    tried = []
    aa = []

    for j in ad:
        if j.First > Year or j.Last < Year:
            continue
        else:
            aa.append(j)
        
    while worseteam == False:
        aa.sort(key = lambda x: eval (x, k, Year, 'mid') + random.random() - x.Moves, reverse = True)
        pick = aa[0]
        if pick.Team == '':
            worseteam = True
        elif pick.Team.Points*1.5 < k.Points and pick.Contract <= 1 and pick.Team.Name != k.Name and pick != i and pick.Team.Rating*3 < k.Rating and pick.Team.Rating < 100 and pick.Team.Owner != pick:
            worseteam = True
        else:
            aa.remove(pick)
            
    #print ()
            
    return pick, ts, ds, ad, pick.Team #new driver, teams, drivers, allDrivers, new driver's previous team

def resolve (t2, d1, d2, t, d, ad):
    global Year
    d1.Rep = d1.Rep/2
    t1 = d1.Team

    if d1 not in d1.Team.Drivers:
        t2, d1, d2, t, d, ad

    for i in d:
        if i.Team == '':
            continue
        if i.Team.Name == '':
            continue
            #print (i.Name)

    if t2 == '':
        if Year >= 1975 or (t1.Rating > 100 or d1.Points > 0):
            if i.Name not in ['Privateer', 'Backmarker']:
                print ('DRIVER CHANGE: ' + d1.Name + ' (' + t1.Name + ') replaced by ' + d2.Name, end = ' ')
                if d2.Races == 0:
                    print ('(rookie)', end = ' ')
                print ()
        d1.Team = ''
        t1.Drivers.remove(d1)
        t1.Drivers.append(d2)
        d2.Team = t1
        d1.Moves = d1.Moves+1
        d2.Moves = d2.Moves+1
        
    else:
        #print (d1.Name, d2.Name, t1.Drivers, t2.Drivers)
        d1.Moves = d1.Moves+1
        d2.Moves = d2.Moves+1
        if d1.Team.Name in ['Privateer', 'Backmarker']:
            pass
        elif Year >= 1975 or t1.Rating > 100 or d1.Points > 0 or d2.Points > 0 or t2.Rating > 100 :
            print ('DRIVER CHANGE: ' + d1.Name + ' (' + t1.Name + ') replaced by ' + d2.Name + ' (' + t2.Name + ')', end = ' ')
            if d2.Races == 0:
                print ('(rookie)', end = ' ')
        if random.random() > 0.5 + d1.Rep/10:
            print ()
            t1.Drivers.remove(d1)
            t2.Drivers.remove(d2)
            t2.Drivers.append(d1)
            t1.Drivers.append(d2)
            
            d1.Team = t2
            d2.Team = t1
            d3, t, d, ad, t3 = pick (t, t2, allDrivers, d1, d)
            resolve (t3, d1, d3, t, d, ad)
        else:
            if d1.Team.Name in ['Privateer', 'Backmarker']:
                pass
            if d2.Team.Name in ['Privateer', 'Backmarker']:
                print ()
            elif Year >= 1975 or t1.Rating > 100 or t2.Rating > 100 or d1.Points > 0 or d2.Points > 0:
                print ("Drivers swapped.")
            t1.Drivers.remove(d1)
            t2.Drivers.remove(d2)
            t1.Drivers.append(d2)
            t2.Drivers.append(d1)
            d1.Rep = d1.Rep*1.5
            d1.Team = t2
            d2.Team = t1

    #print (d1.Team)
            
    return t2, d1, d2, t, d, ad
        


def driverswap (d, t, y, n, c):
    global allDrivers
    change = False

    p = teamfind ('Privateer', t)
    
    if random.random() < 0 or n == c-1 or (n<5 and Year >= 1980) or ( (n/c < 0 or n < 1) and Year < 1980):
        return d, t

    else:
        for i in d:
            if i.Wins > 0 or d[0].Points*0.5 < i.Points or i.Team == '' or i.Team == p or 0.75*(i.Team.Points-i.Points) <= i.Points > 0 or i.Races < c/2 or i == i.Team.Owner:
                continue
            elif random.random() > (5 + i.Rep + i.Peak**3 + i.Rating + i.Points/8 - i.Team.Points/20 + i.Podiums - i.DNFs*0.1 + (n+1-i.YRaces) #+ (c-n)/5
                                    - (2020-Year)/4 + 5*i.Moves) / 10 and random.random() < 1/10:
                if i.Team.Name == '' or i not in i.Team.Drivers:
                    continue
                change = True
                ot = ''
                #new driver, teams, drivers, allDrivers, new driver's previous team
                #print (i.Name, i.Team.Name)
                d2, t, d, allDrivers, ot = pick (t, i.Team, allDrivers, i, d)
                ot, i, d2, t, d, allDrivers = resolve (ot, i, d2, t, d, allDrivers)

    return d, t


def injuries (d, ad, t, y):
    global Year

    for i in d:
        x = 0
        if i.Team == '':
            continue
        if random.random() <  1/(1000-(2020-Year)*2):
            if random.random() < 1/5:
                x = random.random() * (random.random()*random.random()*5)**2
            else:
                x = random.random()*2
        elif i in y and random.random() < 1/(200-(2020-Year)*2):
            if random.random() < 1/5:
                x = random.random() * (random.random()*random.random()*5)**2
            else:
                x = random.random()*2

        if Year > 1995:
            x = x * random.uniform(0, 2)
        elif Year > 1980:
            x = x * random.uniform(0, 3)

        x = round (x)
        if x > 0:
            i.Injury = i.Injury + x + 1
            d.sort(key = lambda x: random.random() + eval (x, i.Team, Year, ''))
            
            for j in d:
                no = False
                for k in ad:
                    if k.Sub == j:
                        no = True
                if j != i and j.Team == '' and no == False and j.Last >= Year and j.First <= Year:
                    if i.Team.Name not in ['Privateer', 'Backmarker']:
                        print (i.Name + ' ('+i.Team.Name+')' + ' is injured. He will miss the next ' + str(i.Injury) + ' races. To be replaced by ' + j.Name)          
                    i.Sub = j
                    break

    return d, ad, t











def season (Drivers, Teams, Year, Races):
    global allDrivers, space, formers
    print (Year, end = ' - ')
    print (len(Races), 'Races')

    space = 0
    for i in Drivers:
        if len(i.Name) > space:
            space = len(i.Name)

    Teams.sort(key = lambda x: x.Rating, reverse = True)

    teamspace = 0
    for i in Teams:
        i.Points = 0
        if len(i.Name) > teamspace:
            teamspace = len(i.Name)
        print (i.Name, i.Rating, end = ", ")
    print()

    for i in Drivers:
        i.Points = 0
        i.Wins = 0
        i.DNFs = 0
        i.Podiums = 0
        i.YRaces = 0
        i.Moves = 0
        i.Best = 1000
        i.Rating = i.Rating + 0.5*(i.Peak-i.Rating)
        if i.Races == 0 and Year != 1950:
            i.Rating = i.Rating * random.uniform(1/4,3/4)
        if (Year >= i.Last - 2 or Year - i.First > 15) and i.Last < 2019:
            i.Peak = i.Peak * random.uniform(2/3,1)
        i.Rating = round(i.Rating,1)

        if Year < 1970:
            i.Rating = i.Rating ** 1.5
        elif Year < 1990:
            i.Rating = i.Rating ** 1.25

        i.Rating = round(i.Rating, 1)
        
        if i.Rating <= 0:
            i.Rating = 0.1
        if i.Injury > 0:
            i.Injury = i.Injury - 5
            if i.Injury < 0:
                i.Injury = 0
                i.Sub.Injury = 0
                i.Sub = '' 

    if Year < 1960:
        pointsdict = {1:8,2:6,3:4,4:3,5:2}
    elif Year < 1970:
        pointsdict = {1:8,2:6,3:4,4:3,5:2,6:1}
    elif Year < 1990:
        pointsdict = {1:9,2:6,3:4,4:3,5:2,6:1}
    elif Year < 2000:
        pointsdict = {1:10,2:6,3:4,4:3,5:2,6:1}
    elif Year < 2010:
        pointsdict = {1:10,2:8,3:6,4:5,5:4,6:3,7:2,8:1}
    else:
        pointsdict = {1:25,2:18,3:15,4:12,5:10,6:8,7:6,8:4,9:2,10:1}

    HighV = ['Monte-Carlo', 'Marina Bay', 'Baku', 'Interlagos', 'Sepang', 'Spa-Francorchamps', 'Detroit', 'Phoenix', 'Montréal'
        ]

    LowV = ['Yas Marina', 'Sochi', 'Magny-Cours', 'Doha'
        ]

    ChampionDecided = False

    Drivers, allDrivers, Teams = injuries (Drivers, allDrivers, Teams, [])
    
    for n in range (len(Races)):
        #print ()
        #time.sleep(0.1)

        if racedict[Races[n]] in HighV:
            ChaosMod = 1
        elif racedict[Races[n]] in LowV:
            ChaosMod = -1
        else:
            ChaosMod = 0
        
        x, y, z, PodTeams, Pole, DNQs = race (Drivers, Teams, len(pointsdict), ChaosMod)
        for i in Drivers:
            if i.Injury == -1:
                i.Team = ''
            if i.Injury > 0:
                i.Injury = i.Injury - 1
            if i.Injury == 0 and i.Sub != '':
                for j in Drivers:
                    if j == i.Sub:
                        j.Injury = 0
                i.Sub = ''
            
        print (str(str(n+1).rjust(2)+'/'+ str(len(Races)))   , Races[n], racedict[Races[n]].center(15), str(x[0].Name + ' ('+ PodTeams[0].Name +')').center(space+teamspace+5),
               str(x[1].Name + ' ('+ PodTeams[1].Name +')').center(space+teamspace+5),
               str(x[2].Name + ' ('+ PodTeams[2].Name +')').center(space+teamspace+5),
               #x[0].Name.center(space),WinningTeam.Name.ljust(teamspace),
               #x[1].Name.center(space+5), x[2].Name.center(space+5)) #end ='|') #str(round(z,1)).ljust(3), end=' '
               )
        
        #print()
        for i in Drivers:
            if i in x:
                i.Races = i.Races + 1
                i.YRaces = i.YRaces + 1
                for j in Teams:
                    if i.Team == j:
                        j.Races = j.Races + 1
            if x[0].Name == i.Name:
                i.Wins = i.Wins+1
                i.CWins = i.CWins+1
                i.Rep = i.Rep + 1/3
                for j in Teams:
                    if i.Team == j.Name:
                        j.Wins = j.Wins + 1
                        WinNo = j.Wins
            if i in y:
                i.DNFs = i.DNFs+1
            if x[0].Name == i.Name or x[1].Name== i.Name or x[2].Name == i.Name:
                i.Podiums = i.Podiums+1
                i.CPodiums = i.CPodiums+1
                i.Rep = i.Rep + 0.1
        for j in Teams:
            #j.Rating = round ( j.Rating * random.uniform(0.9,1.1), 1)
            if PodTeams[0] == j:
                j.Wins = j.Wins + 1
        for k in range (len(pointsdict)):
            for i in Drivers:
                if x[k].Name == i.Name:
                    i.Points = i.Points + pointsdict[k+1]
                    if i.Team != '':
                        i.Team.Points = i.Team.Points + pointsdict[k+1]
                    if Year < 2010:
                        i.Rep = i.Rep + (pointsdict[k+1])/50
                    else:
                        i.Rep = i.Rep + (pointsdict[k+1])/150

        for i in range(len(x)):
            try:
                for j in Drivers:
                    if x[i] == j:
                        if i < j.Best:
                            i = j.Best
            except:
                pass
        #print ()
        Drivers.sort(key = lambda x: x.Points + x.Wins/1000, reverse = True)


        #print()

        print ('Pole:', Pole.iln, end = ' - ' )
        
        print('Points:', end = ' ')
        for q in range(3,len(pointsdict)):
            print(x[q].iln + ',', end =' ')
        print()

        print(x[0].ln, 'Career Win #', x[0].CWins, '-', PodTeams[0].Name, "Team Win #", PodTeams[0].Wins, '-',
              x[0].ln, 'Career Podium #', x[0].CPodiums, '-', x[1].ln, 'Career Podium #', x[1].CPodiums, '-', x[2].ln, 'Career Podium #', x[2].CPodiums)


        print ('DNF:', end='')
        print (str(len(y)).rjust(2), end =' ')
        for i in y:
            print (i.iln, end=', ')

        if len (DNQs) > 0:
            print ('DNQ:', end='')
            print (str(len(DNQs)).rjust(2), end =' ')
            for i in DNQs:
                print (i.iln, end=', ')

        print ()
        
        if (Drivers[0].Points - Drivers[1].Points) > (pointsdict[1] * (len(Races)-n-1) ) and ChampionDecided == False:
            #print ()
            print ("WORLD DRIVERS' CHAMPION:", Drivers[0].Name + ' (' + Drivers[0].Team.Name +')')
            ChampionDecided = True
            



        t = 0

        namelist = []
        for j in Drivers:
            if j.Points >= 5:
                namelist.append(j.ln)
        
        while t < 5 or (Drivers[0].Points*0.5 < Drivers[t].Points):
            if namelist.count(Drivers[t].ln) > 1:
                print (Drivers[t].iln.center(14), str(Drivers[t].Points).rjust(3), end = ' ')
            else:
                print (Drivers[t].ln.center(14), str(Drivers[t].Points).rjust(3), end = ' ')
            t = t+1
        print()
            
        
        if n < len(Races)-1:
            Drivers, allDrivers, Teams = injuries (Drivers, allDrivers, Teams, y)
            Drivers, Teams = driverswap(Drivers, Teams, Year, n, len(Races))
        print()

    Drivers.sort(key = lambda x: x.Points + x.Wins/1000 - x.Best/1000, reverse = True)
    Teams.sort (key = lambda x: x.Points, reverse = True)

    global Champions
    Champions.append([Year, Drivers[0].Name, Drivers[0].Team.Name, Teams[0].Name])

    Champion = Drivers[0]
    Champion.Rep = Champion.Rep + 10
    Champion.rangz = Champion.rangz + 1

    for i in Drivers:
        if i.Name == Champion.Name:
            if i.Last == Year and i.Last - i.First < 15 and random.random() < 0.5:
                i.Last = i.Last + 1
            if i.Rating < 3:
                i.Rating = i.Rating*1.5
            
            i.Rating = round(i.Rating,1)
                
        if i.Team == '':
            continue
                
        if i.Team.Points > 0:
            i.Rep = i.Rep + (i.Points/i.Team.Points)*len(i.Team.Drivers)




    print ('Driver'.ljust(space), 'Team'.ljust(teamspace), 'Pts', ' W', ' P', ' R', 'DNF')
    for i in Drivers:
        i.Rating = round(i.Rating,1)
        if i.Points >= 1: #or (i.YRaces > 0 and i.Team != "Privateer"):
            if i.Team != '':
                print (i.Name.ljust(space), i.Team.Name.ljust(teamspace), str(i.Points).rjust(3), str(i.Wins).rjust(2),
                       str(i.Podiums).rjust(2), str(i.YRaces).rjust(2), str(i.DNFs).rjust(2), str(round(i.Rep,1)).rjust(5),i.Rating, end =' ')
            else:
                print (i.Name.ljust(space), ''.ljust(teamspace), str(i.Points).rjust(3), str(i.Wins).rjust(2),
                       str(i.Podiums).rjust(2), str(i.YRaces).rjust(2), str(i.DNFs).rjust(2), str(round(i.Rep,1)).rjust(5),i.Rating, end =' ')
            
            for j in Champions:
                if j[1] == i.Name:
                    print (j[0], end=' ')
            print()
    print ('0 points: ',end ='')
    for i in Drivers:
        if i.YRaces > 0 and i.Points == 0:
            if i.Team != '':
                if i.Team.Name in ['Privateer']:#, 'Backmarker']:
                    continue
                print (i.Name + ' ('+ i.Team.Name +'), ', end =  '')
            else:
                print (i.Name, end =  ', ')

    for i in Drivers:
        if Year < 1970:
            i.Rating = i.Rating ** (2/3)
        elif Year < 1990:
            i.Rating = i.Rating ** (4/5)
    print ()


    
    Teams[0].rangz = Teams[0].rangz + 1
    print ('Team Points: ', end = ' ')
    for i in Teams:
        print (i.Name, str(i.Points).rjust(5), end = ', ')
    print ()
    print ('Team Ratings:', end = ' ')
    for i in Teams:
        print (i.Name, str(i.Rating).rjust(5), end = ', ')
    print ()

    if Champion.rangz > 1:
        print (Champion.Name, '-', Champion.rangz, "World Drivers' Championships", end = ' - ')
    else:
        print (Champion.Name, '-', "First World Drivers' Championship", end = ' - ')

    if Teams[0].rangz > 1:
        print (Teams[0].Name, '-', Teams[0].rangz, "World Constructors' Championships")
    else:
        print (Teams[0].Name, '-', "First World Constructors' Championship")

    print()
    print()













    

    DriverLog = []

    for i in Teams:
        for j in i.Drivers:
            while i.Drivers.count(j) > 1:
                i.Drivers.remove(j)
                print (i.Name, j.Name)

    for i in Teams:
        x = i.Name
        y = []
        for j in i.Drivers:
            if j not in y:
                y.append(j)
        DriverLog.append([x, y])

    for i in Drivers:
        if (i.First + 5 == Year and i.Races == 0) or (Year - i.First > 15 and random.random() < 0.2):
            i.Last = Year
        if i.Last == Year:
            if i.Last-i.First < 12 and i.rangz > 0 and i.First != 1950 and i.Last >= Year:
                i.Last = i.Last + 1

    for i in allDrivers:
        if i.First == Year+1:
            Drivers.append(i)
            #print (i.Name)

    global formerTeams

    for i in Teams:
        if i.Name == 'Privateer' and Year > 1965 and random.random() < 0.1:
            i.Name = 'Backmarker'
            print ('Privateers eliminated.')
        if i.Name in ['Ferrari', 'Privateer', 'Backmarker']:
            continue
        if (      ((i.Rating < (50-(i.rangz)) and random.random() < 1/5)
                   or (i.Rating < (10-(i.rangz/5))  and random.random() < 1/5)
             or (i.Rating < 10 and i.Wins < 1  and (0 < (Year - i.First) < 5) and random.random() < 1/5 )
                   or (i.Rating < 10 and Year - i.First < 2 and random.random() < 1/4 and i.Wins < 1 )
                  or ( Year < 1960 and random.random() < 1/25)
                   )
            and ( len(Teams) > 10 or (Year < 1975 and len(Teams) > 7) )): 
        #or (Year > 1970 and random.random() < 1/10 and i.Name == 'Privateer')):
            
            print (i.Name, 'leaving F1 -', i.rangz, 'Championships -', i.Wins, 'Wins')
            if i.Name not in formers and i.Wins > 9:
                formers.append(i.Name)
            i.Last = Year
            formerTeams.append(i)
            Teams.remove(i)
            for j in Drivers:
                if j.Team == i:
                    j.Team = ''
            for j in Teams:
                if i.Name == 'Red Bull' and j.Name == 'Toro Rosso':
                    j.Name = 'Red Bull'
                    print ('Toro Rosso is now now Red Bull.')

    possteams = ['BMW', 'Ford', 'Volkswagen','Aston Martin','Porsche','Bentley','Peugeot', 'Jaguar', 'Dallara','Bugatti', 'Lancia','Citroën','Lamborghini']

    if 1970 > Year > 1956:
        possteams.append('B.R.M.')
    if Year > 1980:
        possteams.append('Penske')
        possteams.append('Audi')
    if 1970 > Year > 1960:
        possteams.append('Lotus')
    if Year > 1960:
        possteams.append('Chrysler')
        possteams.append('Chevrolet')
        possteams.append('Lola')
    if Year > 1966:
        possteams.append('Honda')
        possteams.append('Toyota')
        possteams.append('Nissan')
        possteams.append('Mazda')
        possteams.append('Yamaha')
    if 1990 > Year > 1967:
        possteams.append('McLaren')
    if 1990 > Year > 1966:
        possteams.append('Brabham')
    if Year > 1970:
        possteams.append('March')
    if 1990 > Year > 1978:
        possteams.append('Williams')
    if Year > 2005:
        possteams.append('Red Bull')
        possteams.append('Carlin')
    if Year > 2010:
        possteams.append('Monster Energy')

    natdict = { 'BMW':'Germany', 'Ford':'United States', 'Volkswagen':'Germany', 'Aston Martin':'United Kingdom','Porsche':'Germany','Bentley':'United Kingdom','Peugeot':'France',
                'Jaguar':'United Kingdom', 'Dallara':'Italy', 'Bugatti':'Italy', 'Lancia':'Italy', 'Citroën':'France', 'Lamborghini':'Italy', 'B.R.M.':'United Kingdom',
                'Penske':'United States', 'Audi':'Germany', 'Lotus':'United Kingdom','Chrysler':'United States', 'Chevrolet':'United States', 'Honda':'Japan','Toyota':'Japan','Nissan':'Japan',
                'Mazda':'Japan', 'McLaren':'United Kingdom', 'Brabham':'Australia', 'March':'United Kingdom', 'Williams':"United Kingdom", 'Carlin':'United Kingdom', 'Yamaha':'Japan'
        }


    possteams = possteams + [i for i in formers if i not in possteams]

    names = [i for i in allDrivers if (i.Rep > (30 + 20*random.random() + max (0, Year-1990) ) and (i.Last < Year - 3 and i.First + 15 < Year and i. First > Year - 30) )
             or (i.Rep > 1 and Year < 1975 and (i.First + 7 < Year < i.Last + 10 or i.First == 1950)) ]
    possdrivers = []

    for i in names:
        possdrivers.append([i.Name,i.ln, i.Nat])
    for i in possteams:
        for j in Teams:
            if i == j.Name:
                possteams.remove(i)

    for i in names:
        if random.random() < 1:
            new = random.choice(possdrivers)
            possdrivers.remove(new)
            possteams.append(new)

    for i in Teams:
        for j in possteams:
            if i.Name == j or i.Name == j[1]:
                possteams.remove(j)

    #print(possteams)

    if (random.random() < 1/5 and Year >=1965) or (Year < 1965 and random.random() < 1/5) and Year > 1952:
        x = random.choice(possteams)
        if type(x) == list:
            teammake(x[1], 1, x[0], x[2])
        else:
            teammake(x, 1, '', natdict.get(x, ''))
        
    if Year+1 == 1954:
        teammake('Mercedes',70,'',"Germany")
    if Year+1 == 1954 and random.random() < 1/10:
        teammake('Vanwall',1,'',"United Kingdom")
    if Year+1 == 1956 and random.random() < 1/2:
        teammake('B.R.M.',1,'',"United Kingdom")
    if Year+1 == 1960:
        teammake('Lotus',1,'',"United Kingdom")
    if Year+1 == 1964 and random.random () <1/2:
        teammake('Honda',1,"",'Japan')
    if Year+1 == 1962:
        teammake('Brabham',1,'Jack Brabham','Australia')
    if Year + 1 == 1966 and random.random() < 1/10:
        teammake('Eagle',1,'','United States')
    if Year+1 == 1967:
        teammake('McLaren',1,'Bruce McLaren',"United Kingdom")
    if Year+1 == 1967 and random.random() < 1/10:
        teammake('Matra',1,'','France')
    if Year+1 == 1970 and random.random() < 1/5:
        teammake('Tyrell',1,'',"United Kingdom")
    if Year+1 == 1976 and random.random() < 1/5:
        teammake('Ligier',1,'','France')
    if Year+1 == 1978:
        teammake('Williams',1,'',"United Kingdom")
    if Year+1 == 1977:
        teammake('Renault',1,'','France')
    if Year+1 == 1978 and random.random() < 1/10:
        teammake('Arrows',1,'',"United Kingdom")
    if Year+1 == 1985 and random.random() < 1/10:
        teammake('Minardi',1,'',"Italy")
    if Year+1 == 1986 and random.random() < 1/5:
        teammake('Benetton',1,'',"Italy")
    if Year+1 == 1991 and random.random() < 1/5:
        teammake('Jordan',1,'',"United Kingdom")
    if Year+1 == 1993 and random.random() < 1/5:
        teammake('Sauber',1,'','')
    if Year+1 == 1999 and random.random() < 1/10:
        teammake('B.A.R.',1,'',"Canada")
    if Year+1 == 2002 and random.random() < 1/5:
        teammake('Toyota',1,'',"Japan")
    if Year+1 == 2005:
        teammake('Red Bull',1,'','')
    if Year+1 > 2005 and random.random() < 1/50 and 'Red Bull' not in possteams:
        teammake('Toro Rosso',1,'','')
    if Year+1 == 2008 and random.random() < 1/10:
        teammake('Force India',1,'',"India")
    if Year+1 == 2009 and random.random() < 1/10:
        teammake('Brawn GP',1,'','')
    if Year+1 == 2016 and random.random() < 1/5:
        teammake('Haas',1,'',"United States")





    for i in Teams:
        for j in i.Drivers:
            while i.Drivers.count(j) > 1:
                i.Drivers.remove(j)

    
    Retiring = []
    print ('Retiring:')
    allDrivers.sort(key = lambda x: x.rangz + x.CWins/1000 + x.Races/1000000, reverse = True)
    for i in allDrivers:
        if i.Last == Year and (i.Races > 0):# or Year > 1975):
            if i.Team != '':
                print (i.Name.ljust(space), i.Team.Name.ljust(teamspace), str(i.Races).rjust(3), 'Races', str(i.CWins).rjust(3), 'Wins', str(i.CPodiums).rjust(3),
                       'Podiums', str(i.rangz).rjust(2), 'Championships',  end =' ')
            else:
                print (i.Name.ljust(space), ''.ljust(teamspace), str(i.Races).rjust(3), 'Races', str(i.CWins).rjust(3), 'Wins', str(i.CPodiums).rjust(3),
                'Podiums', str(i.rangz).rjust(2), 'Championships',  end =' ')
                try:
                    i.Contract = 0
                    i.Team.Drivers.remove(i)
                    i.Team = ''
                    Drivers.remove(i)
                except:
                    pass

            for j in Champions:
                if j[1] == i.Name:
                    print (j[0], end = ' ')

            print ()

        elif i.Last == Year:
            Drivers.remove(i)
            i.Team = ''

    print ()
    for i in Drivers:
        i.Contract = i.Contract - 1

    Teams.sort(key= lambda x: x.Points, reverse = True)
    for i in Teams:
        if i.Name in ['Privateer', 'Backmarker']:
            pass
        i.Drivers = []
        for j in Drivers:
            if i == j.Team and j.Last > Year:
                if random.random() < (1/2 + 0.05*j.Wins + 0.03*j.rangz) or j.Contract > 0 or j == Champion or i.Owner == j.Name:
                    if j.Rep > 40 and j.Contract == 0 and i.Rating > 100:
                        j.Contract = random.randrange(2,5)
                    elif j.Rep > 20 and j.Contract == 0 and i.Rating > 10:
                        j.Contract = random.randrange(2,3)
                    elif j.Rep > 10 and j.Contract == 0:
                        j.Contract = random.randrange(1,2)
                    elif j.Contract == 0:
                        j.Contract = 1
                    if j not in i.Drivers:
                        i.Drivers.append(j)
                        j.Team = i
                    if j.Contract > 1 and i.Name in ['Privateer', 'Backmarker']:
                        j.Contract = 1
                    #print (i.Name.ljust(space), j.Name.ljust(space))
                else:
                    j.Team = ''
            elif j.Last <= Year:
                try:
                    j.Team.Drivers.remove(j)
                    j.Team = ''
                except:
                    j.Team = ''
                j.Team = ''
                Drivers.remove(j)

    for i in Drivers:
        if i.Team == '':
            continue
        if i not in i.Team.Drivers:
            i.Team =''

    for i in Teams:


        n = 0
        if Year < 1960 and ( (i.Rating > 500 or (i.Rating > 100 and random.random() < 0.5) or random.random() < 0.1) ):
            m = 4
        elif Year < 1975 and (i.Rating > 25 or random.random() > 0.2):
            m = 3
        else:
            m = 2
        if i.Name in ['Privateer', 'Backmarker']:
            m = 0
        

        while len(i.Drivers) < m:
            Drivers.sort(key= lambda x: eval (x, i, Year, ''), reverse = True)
            
            if Drivers[0].Rep > 40:
                Drivers[0].Contract = random.randrange(3,6)
            elif Drivers[0].Rep > 20 or i.Rating > 200:
                Drivers[0].Contract = random.randrange(2,4)
            elif Drivers[0].Rep > 10 or i.Rating > 50:
                Drivers[0].Contract = random.randrange(1,3)
            else:
                Drivers[0].Contract = random.randrange(1,2)

            Drivers[0].Team = i
            
            if Drivers[0] not in i.Drivers:
                i.Drivers.append(Drivers[0])
            #print (i.Name.ljust(space), Drivers[0].Name.ljust(space),round(Drivers[0].Rep,1))


    for i in Teams:
        if i.Name in ['Privateer', 'Backmarker']:
            for j in i.Drivers:
                j.Team = ''
            i.Drivers = []
            if i.Name == 'Privateer':
                Drivers.sort(key= lambda x: ((Year-x.First) + eval (x, i, Year, '')*random.random()), reverse = True)
                n = round ( random.randrange(0,10) + max(0, (2020-Year)*0.2) - len(Teams))
            else:
                Drivers.sort(key= lambda x: random.random() * eval (x, i, Year, ''), reverse = True)
                n = round ( random.randrange(12,16) + max(0, (2020-Year)*0.1) - len(Teams))
            if i.Name == 'Backmarker' and n%2 == 1:
                n = n-1
            for j in range(n):
                Drivers[j].Team = i
                Drivers[j].Contract = 1
                i.Drivers.append(Drivers[j])


    if random.random() < 1/5:
        newreg = True
        if random.random() < 0.5:
            print ('Regulations overhaul for ' + str(Year+1)  + '!')
        else:
            print ('New technologies introduced for ' + str(Year+1) + '!')
    else:
        newreg = False


    for i in Teams:

        if newreg == True:
            i.Rating = 10*i.Rating** (1/3) + 100*random.random() 

        #i.Rating = i.Rating**random.uniform(2/3,1/3)

        if random.random () < 0.5:
            i.Rating = i.Rating*random.uniform(1,5)
        else:
            i.Rating = i.Rating*random.uniform(1/5,1)

        if i.Rating < 1:
            i.Rating = i.Rating*5*random.random()

        if Year - i.First < 5:
            i.Rating = i.Rating * random.uniform(0.2,1)

        if Year + 1 == i.First:
            i.Rating = i.Rating/5

        if i.Name in ['Ferrari', 'Mercedes', 'Renault', 'McLaren', 'Lotus', 'Williams'] and random.random() < 2/7:
            i.Rating = i.Rating * random.uniform(1,5)

        i.Rating = i.Rating + random.uniform(0,10)

        if i.Rating > 900 and newreg == False:
            i.Rating = max(200,i.Rating**((1+random.random()+random.random())/3))

        #print (i.Name, i.Rating)


    fastest = 0
    loop = 0

    while fastest < 250:
        for i in Teams:
            if loop > 0:
                i.Rating = 1 + i.Rating**2 + 10*random.random()
        
        factor = 1000/sum([i.Rating for i in Teams])

        for i in Teams:
            i.Rating = i.Rating * factor
            i.Rating = round(i.Rating,1)
        loop = loop + 1

        fastest = max([i.Rating for i in Teams])
                
    privrating = 0
    
    for i in Teams:
        if i.Rating == 0:
            i.Rating = 0.1

        if i.Name == 'Privateer':
            i.Rating = round(0.1+10*random.random(),1)
            privrating = i.Rating
        if i.Name == "Backmarker":
            i.Rating = round(0.1+2*random.random(),1)

        for j in Teams:
            if i.Rating > j.Rating and i.Name == 'Toro Rosso' and j.Name == 'Red Bull':
                i.Rating, j.Rating = j.Rating, i.Rating

    for i in Teams:
        if i.Rating < privrating:
            i.Rating = privrating










    Drivers.sort(key = lambda x: x.Rep, reverse = True)

    for i in Drivers:
        if Year == 1950:
            continue
        ot = ''
        for k in DriverLog:
            if i in k[1]:
                ot = k[0]
                break
        if ot == '' or i.Team == '':
            continue
        if ot != i.Team.Name and i.Team.Name != 'Privateer':
            print (i.Name.ljust(space), k[0].center(teamspace), 'to', i.Team.Name.center(teamspace))

    print ('No ' + str(Year+1) + ' Seat: ', end ='')
    for k in DriverLog:
        for l in k[1]:
            for m in Drivers:
                if l.Name == m.Name and m.Team == '' and l.Last > Year and k[0] != 'Privateer' and Year != 1950:
                    print (l.Name + " (" + k[0] +'), ', end ='')
                    m.Rep = m.Rep/2
    print()

    print ('Returning:', end = ' ')
    for i in Drivers:
        tick = False
        for k in DriverLog:
            #print (i.Name, k[1])
            if i in k[1]:
                tick = True
        if i.Team != '' and i.Races > 0 and tick == False:
            if i.Name in ['Privateer']:
                continue
            print (i.Name + " (" + i.Team.Name + ")", end = ', ')

    print ()
    print ('Rookies:', end = ' ')
    for i in Drivers:
        if i.Team != '' and i.Races == 0:
            if i.Team.Name == 'Privateer':
                continue
            print (i.Name + " (" + i.Team.Name + ")", end = ', ')

    print ()
    for i in Teams:
        if i.Name in ['Privateer', 'Backmarker']:
            print (i.Name, end= ': ')
            for j in i.Drivers:
                print (j.iln, end = ', ')
            

    print ()
    print()

    for i in Teams:
        if i.Name in ['Privateer', 'Backmarker'] or Year == 1950:
            continue
        check = False
        print (i.Name.ljust(teamspace), end = ' ')
        i.Drivers.sort(key = lambda x: x.ln)
        print (Year, end = ' - ')
        for k in DriverLog:    
            if k[0] == i.Name:
                check = True
                for j in k[1]:
                    k[1].sort(key = lambda x: x.ln)
                    print (j.Name.ljust(space), end= ' ')
                if (len(k[1]) < 4 and Year <= 1960) or (len(k[1]) < 3 and Year <= 1980):
                    print (''.ljust(space+1), end = '')
                if (len(k[1]) == 2 and Year <= 1960):
                    print (''.ljust(space+1), end = '')
        if check == False:
            if Year > 1980:
                print (' '.ljust(2+2*space), end = '')
            elif Year >= 1960:
                print (' '.ljust(3+3*space), end = '')
            else:
                print (' '.ljust(4+4*space), end = '')
        print (Year+1, end = ' - ')
        for j in i.Drivers:
            print (j.Name.ljust(space), end = ' ')

                        
        print ()

    return Drivers, Teams


def calendar (r, y):
    print ()
    possibles = ['ESP', 'GER', 'NED', 'ARG', 'MOR', 'POR', 'USA','AUT','EUR']

    if y > 1960:
        possibles = possibles + ['MEX', 'CAN', 'RSA', 'BRA']
    if y > 1970:
        possibles = possibles + ['SMR', 'JPN', 'USW', 'SWE']
    if y > 1980:
        possibles = possibles + ['AUS', 'HUN', 'DET', 'other']
    if y > 1990:
        possibles = possibles + ['MAL', 'PAC', 'CHN', 'RUS']
    if y > 2000:
        possibles = possibles + ['BAH', 'ABU', 'TUR', 'SIN']
    if y > 2010:
        possibles = possibles + ['KOR', 'AZB', 'VNM', 'IND']

#FIN URU NZL QAT NYC

    for i in r:
        if i not in ['MON', 'GBR', 'BEL', 'ITA', 'JPN'] and random.random() < 1/2*len(r) and ( (Year < 1960 and len(r)>6) or
                                                                                             (Year < 1970 and len(r)>8) or (Year < 1980 and len(r)>10)
                                                                                  or    (Year < 1990 and len(r)>12) or (Year < 2000 and len(r)>14) or (Year < 2000 and len(r)>16)
                                                                                     or (Year < 2010 and len(r)>18) or len(r)>20):
            r.remove(i)
            possibles.append(i)
            print ('Grand Prix removed:', i, '-', racedict[i], end = ' - ')
            racedict.pop(i)

    change = False
    fail = False
    while fail == False:
        try:
            if ( (random.random() < 1/3 ) ) and ( (Year > 1950 and len(r) < 10) or (Year > 1970 and len(r) < 18) or (Year > 2005 and len(r) < 26)  ):
                candidates = [i for i in possibles if i not in r]
                x = random.choice(candidates)
                if x in ['USW', 'DET', 'NYC', 'DET', 'DAL','LVG','TEX'] and 'USA' not in r:
                    x = 'USA'
                if x == ('PAC') and 'JPN' not in r:
                    x = 'JPN'
                r.append(x)
                #print ()
                #print ('New Grand Prix:', x, end = ' - ') 
                change = True
            else:
                fail = True
        except:
            break

    summer = ['GBR','MON','BEL','FRA','ITA','GER','SUI','ESP','NED','POR','AUT','CAN','QBC','EGR','YUG','SOV','SIC',
              'RUS','SMR','EUR','SWE','HUN','POL','DET','IRE','TUR','CZE','AZB','FIN','NYC']

    additionals = [ ['AUS','Mount Panorama'], ['AUS','Surfers Paradise'], ['AUT','Vienna'], ['CAN','Vancouver'], ['CHI', 'Macau'], ['ITA','Imola'], ['RUS','Moscow'], ['SUI','Dijon'],['GBR','Goodwood'],
                    ['AUT','Salzburgring'], ['AUS', 'Phillip Island'], ['AUS', 'Eastern Creek'], ['GER','Sachsenring'], ['SUI','Geneva'],['FIN','Tampere'],['SMR','Mugello'],['MOR','Marrakech'],
                    ['DNK','Copenhagen'],['SWE','Karlskoga'],['CAN','Edmonton'],['NED','Assen'],['MEX','Monterrey'],['POR','Algarve'],['RSA','Cape Town'],['GBR','Oulton Park'],
                    ['GER','Solitudering'], ['VNM','Hanoi'],['MAL','Putrajaya'],['AUS','Sandown'],
                    ['PAC','Laguna Seca'],['PAC','Long Beach'], ['PAC','Tsukuba'], ['PAC', 'Vancouver'],['PAC','Surfers Paradise'],['PAC','Suzuka'],
                    ['USA', 'Laguna Seca'], ['USW', 'Laguna Seca'], ['USA', 'Road America'], ['USA', 'Omaha'],
                    ['USA','Daytona'], ['USA','Virginia Intl.'], ['USA','Miami'], ['USA','Chicago'], ['USW','Portland'],['USW','Sonoma'],['USA','Road Atlanta'],                    
                    
        ]


    unusuals = [ ['CZE','Brno'], ['CZE','Prague'], ['DNK','Copenhagen'], ['DNK', 'Jyllandsringen'], ['ROM', 'Bucharest'], ['POL', 'Warsaw'],['IRE', 'Mondello Park'],["SCO",'Knockhill'],
                 ['LUX','Nürburgring'],  ['ENG','Brands Hatch'], ['QBC','Montréal'],['BER','Berlin'],['FLN','Zolder'],['WLN','Spa-Francorchamps'],['ENG','Silverstone'],['CAT','Barcelona'],
                 ['FIN','Ahvenisto'], ['DNK','Jyllandsringen'], ['NZL','Wellington'],['NYC','Brooklyn'], ['NYC','Port Imperial'],['NYC','New York City'],['PES','Pescara'],['LEM','Le Mans'],
                 ['FIN','Keimola']
                 
                 ]

    if y < 1995:
        unusuals = unusuals + [ ['YUG','Grobnik'], ['SIC','Siracusa'], ['SOV','Moscow'], ['EGR','Sachsenring'], ['SIC', 'Targa Florio']
                                ]
    else:
        unusuals.append(['SVK','Slovakiaring'])
        unusuals.append(['GEO','Tblisi'])
        unusuals.append(['NOR','Rakkestad'])
        unusuals.append(['CRO','Grobnik'])
        unusuals.append(['IDO','Sentul'])
        unusuals.append(['LAT','Biķernieki'])
        unusuals.append(['EST','Auto24Ring'])
        unusuals.append(['EGR','EuroSpeedway Lausitz'])


    for x in unusuals:
        summer.append(x[0])


    unusuals = unusuals + [['DUB','Dubai'],['KSA','Riyadh'],['THA','Buriram'],['CHL','Codegua'],['TEX','Austin'],['IRN','Tehran'], ['KEN','Nairobi'], ['EGY','Cairo'],['LVG','Las Vegas'],
                           ['ISR','Tel-Aviv'],['ZIM','Donnybrook'],['DAL','Dallas'],['TEX','Austin'],['TEX','Dallas'],['SUZ','Suzuka'],['URU','Montevideo'], ['NZL','Pukekohe'],['QAT','Doha'],
                           ['VEN','Caracas'],['CUB','Havana']

                           ]
                           

    if y > 2000:
        additionals.append(['GBR','Rockingham'])
        additionals.append(['FIN','Kymiring'])
        additionals.append(['ARG','Rio Hondo'])
        additionals.append(['RSA','Phakisa'])
        additionals.append(['NZL','Hampton Downs'])
        additionals.append(['JPN','Motegi'])
        additionals.append(['GER','Lausitzring'])



    flyaways = [i for i in r if i not in summer]


    global Circuits

    for i in r:
        #print (i)
        if i in racedict:
            ov = racedict[i]
        else:
            ov = ''
            
        if i in racedict and  (random.random() > 1.5/len(r) or (Year < 1975 and random.random() < 3/len(r)) or (Year < 1960 and random.random() < 0.5)):
            continue
        elif i in racedict:
            racedict.pop(i)
            pass
            
        race = ''
                                                                                                     
        if i == 'other':
            x = ['','Monte-Carlo']
            while x[1] in racedict.values():
                x = random.choice(unusuals)
            unudict = {x[0]:x[1]}
            racedict.update(unudict)
            summer.append(x[0])
            r.append(x[0])
            print ('New Race:', x[0], "at", x[1])
            continue
                                                                                                     

        cands = []

        for j in Circuits:
            if (j.Race == i and j.First <= Year + 15 and j.Last >= Year - 10 and j.Name not in racedict.values() ):
                cands.extend([j.Name]*j.Total)
            if i == 'EUR' and j.Race in summer and j.Race in r and j.Race in racedict and j.Name not in racedict.values() and j.Race not in ['CAN', 'DET', 'NYC'] and j.First <= Year and j.Last >= Year - 10:
                cands.extend([j.Name]*j.Total)

        
        #cands = [x for x in Circuits if x.Race == i and x.First <= Year]
            
        n = 0
        while len(cands) == 0 and n < 100:
            cands = [x.Name for x in Circuits if x.Race == i and x.First <= Year+n and x.Last >= Year-n and x.Name not in racedict.values()]
            n = n+5

        for j in additionals:
            if j[0] == i and j[1] not in racedict.values() and y > 1955:
                cands.append(j[1])
            if i == 'EUR' and j[0] in summer and j[0] in r and j[1] not in racedict.values() and j[0] not in ['CAN', 'DET', 'NYC']:
                cands.append(j[1])

        if i == 'USA' and 'USW' not in r:
            cands = cands + [x.Name for x in Circuits if x.Race == 'USW' and x.First <= Year and x.Last >= Year - 10 and x.Name not in racedict.values()]

        if ov != '':
            cands.append(ov)
                
        if race == '':
            #print (i)
            cands.sort(key= lambda x: random.random())
            if len (cands) > 0:
                race = cands[0]
            #print (cands)
            try:
                race = race.Name
            except:
                pass

        if i not in racedict:
            racedict[i] = race
                         
        if racedict[i] != ov:
            if ov != '':
                print (i, 'from', ov, 'to', racedict[i], end = ' - ')
            else:
                print ('New Race:', i, 'at', racedict[i], end = ' - ')

        #print (i, racedict[i])

    def rate (x, s, f):
        
        timedict = {'MON':-0.75,'ITA':0.9,'BEL':0.8,'HUN':0.5,'GBR':0, 'SMR':-0.9,'JPN':50,'MEX':50,'BAH':-50,'ARG':-80,'PAC':-65,'ABU':80,'SIN':65}
        try:
            return timedict[x]
        except:
            if x in ['EUR', 'MOR', 'TUR' ]:
                return random.uniform(-2,2)
            if x in f:
                return random.uniform(-100,100)
            else:
                return random.uniform(-1,1)

    if 'other' in r:
        r.remove('other')

    if change == True:
        r.sort(key = lambda x: rate(x, summer, flyaways))
        print ()
    
    return r, racedict
        
Champion = ''
racedict = {}
while Year < 2020:
    Races, racedict = calendar (Races, Year)
    Drivers, Teams = season (Drivers, Teams, Year, Races)
    Year = Year + 1
    
print ()
print ('World Champions')

for i in Champions:
    n = 0
    for j in Champions:
        if i[1] == j[1] and i[0] >= j[0]:
            n = n + 1
    print (i[0], i[1].ljust(25), str(n).rjust(2), i[2].ljust(15), i[3])       

print ()

Teams = Teams + formerTeams

Teams.sort(key = lambda x: x.Wins, reverse = True)
Teams.sort(key = lambda x: x.First)
Teams.sort(key = lambda x: x.Name)
print ('Team'.ljust(14), 'First', 'Last', 'Wins', 'Races', 'Championships')
for i in Teams:
    if i.First != i.Last and i.Races > 0:
        print (i.Name.ljust(15), i.First, i.Last, str(i.Wins).rjust(4), str(i.Races).rjust(5), str(i.rangz).rjust(2))

print()
allDrivers.sort(key = lambda x: x.rangz + x.CWins/100 - x.Races/100000000000000, reverse = True)
print ('Driver'.ljust(25), 'Wins', 'Pods', ' Races', ' WP%', '  First', 'Last', '                 Championships')
x = 0
for i in allDrivers:
    if i.CWins >= 10 or i.rangz > 0 or (i.CWins/(i.Races+0.01) > 0.1 and i.CWins > 1):
        if x > i.rangz:
            print()
        x = i.rangz
        per = '{0:.1f}'.format(round((100*i.CWins/(i.Races+0.0000000000000001)),2))
        print (i.Name.ljust(25), str(i.CWins).rjust(4), str(i.CPodiums).rjust(4), str(i.Races).rjust(5), str(per).rjust(5) + '%', i.rangz, i.First, i.Last, end ='                  ')
        for j in Champions:
            if j[1] == i.Name:
                print (j[0], end=' ')
        print ()
#print ('5+ Wins: ', end = '')
print ()
allDrivers.sort(key = lambda x: x.ln)
for j in range (9, 0, -1):
    if j > 1:
        print (j, 'Wins:', end = '')
    else:
        print ('1 Win:', end = '')
    for i in allDrivers:
        if i.rangz == 0 and i.CWins == j:
            print (' '+i.Name, end = ',')
    print()
print ()
