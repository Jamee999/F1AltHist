import random, time


####THIS FILE IS BEING CONVERTED TO MAKE DRIVER.TEAM OBJECTS INSTEAD OF STRINGS

print ()

with open('f1data.csv', 'r') as f:
    RawDrivers = [line.strip() for line in f]

with open('f1circuits.csv', 'r') as f:
    RawCircuits = [line.strip() for line in f]

Year = 1950

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
    try:
        ln = lndict[ln]
    except:
        pass
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
    if a.First <= 1950:
        a.Last = int(i[2])
    else:
        a.Last = a.First + random.randrange(8,12)
        a.Last = a.Last + round((Year-1950)/15)
        if a.First >= 1955:
            a.First = a.First + random.randrange(-1,1)
    a.Last = a.Last + random.randrange(-2,2)
    if real > a.Last:
        a.Last = real

    if a.Last == 2019:
        a.Last = a.Last + random.randrange(0, 4)
        
    a.Rating = float(i[3])
    a.Peak = a.Rating
    a.Peak = a.Peak
    a.Nat = i[4]
    allDrivers.append(a)
    n = n+1

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
cardict = {'Alfa Romeo':800,'Ferrari':100,'Maserati':60,'Cooper':40,'Privateer':1}
formers = []
formerTeams = []

Races = ['GBR', 'MON', 'SUI', 'BEL', 'FRA', 'ITA']

Champions = []

for i in TeamNames:
    a = Team()
    a.Name = i
    a.Rating = cardict[i]
    a.First = 1950
    if i == ('Alfa Romeo' or 'Ferrari' or 'Maserati'):
        a.Nat = "Italy"
    elif i == 'Cooper':
        a.Nat = 'United Kingdom'
    Teams.append(a)

def teamfind (x, t):
    for i in t:
        if i.Name == x:
            return i

def race (Drivers, Teams, n):
    Standings = []

    xDrivers = [i for i in Drivers if i.Team != '' and i not in Standings]

    for i in xDrivers:
        if i.Team.Name == 'Privateer' and random.random() < 0.1:
            xDrivers.remove(i)
        elif i.Sub != '':
            for j in Drivers:
                if i.Sub == j:
                    j.Team = i.Team
                    j.Injury = -1
                    xDrivers.append(j)
                    xDrivers.remove(i)

    t = len(xDrivers)

    Chaos = max(1, random.uniform(-18,2))**2
    #Chaos = 3
    #print(Chaos)
    DNFs = []
    if Chaos > 2:
        RetFac = 0.06
    else:
        RetFac = 0.06 + (2020-Year)/1000

    Pole = ''
        
    while 27 > len(Standings) + len(DNFs) < t:
        total = 0
        for i in xDrivers:
            if i.Rating * i.Team.Rating > 1:
                i.Power = (i.Rating * i.Team.Rating)**(1/Chaos)
            else:
                i.Power = (i.Rating * i.Team.Rating)
            #print (i.Name, i.Power)
            total = total + i.Power

        if Pole == '':
            xDrivers.sort(key = lambda x:( 5*random.random()* + 2*random.random()*x.Power + (Chaos+1)**(random.uniform(1,4))), reverse = True)
            Pole = xDrivers[0]
            xDrivers[0].Power = xDrivers[0].Power + 100

        x = random.uniform(0,total)
        #print (x)
        count = 0
        for i in xDrivers:
            #print (i.Name, i.Team.Name, i.Power)
            count = count + i.Power
            if x < count:
                if len(Standings) + len(DNFs) < t:
                    if len (Standings) < n:
                        if random.random() > RetFac*Chaos**1.5 - i.Rating/1000:
                            Standings.append(i)
                            xDrivers.remove(i)
                            break
                        elif i not in DNFs:
                            DNFs.append(i)
                            xDrivers.remove(i)
                            break
                    else:
                        if random.random() > 2*RetFac*(Chaos+1) - i.Rating/1000:
                            Standings.append(i)
                            xDrivers.remove(i)
                            break
                        elif i not in DNFs:
                            DNFs.append(i)
                            xDrivers.remove(i)
                            break

    if len(Standings) < n:

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
    if d.Last < y or d.First > y or (d.Team != '' and m != 'mid'):
        return -1000
    if t.Owner == d.Name and d.Last <= y:
        return 1000
    x = d.Rating + d.Rep

    if t.Rating < 3:
        if i.First == y:
            x = x*2
        elif y - i.First < 5:
            x = x*(2-(y-i.First)*(1/5))
        #if i.Races == 0:
            #x = x*1.5
    
    if d.Nat == t.Nat:
        return x * (random.random() + 1/5)
    else:
        return x * random.random()

def teammake (n, r, o, nat):
    global Teams, Year, Drivers
    for i in Teams:
        if i.Name == n:
            return False
    if ( (len(Teams) < 15 and Year > 1975) or (len(Teams) < 10 and Year > 1975) or len(Teams) < 8 ) and n != 'Privateer':
        a = Team()
        a.Name = n
        a.Rating = r
        a.Owner = o
        a.First = Year + 1
        a.Nat = nat
        Teams.append(a)
        print ('New Team:', a.Name)
        if o != '':
            for j in Drivers:
                if j.Name == o:
                    j.Team = a
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
        elif pick.Team.Points*1.5 < k.Points and pick.Contract <= 1 and pick.Team.Name != k.Name and pick != i and pick.Team.Rating*3 < k.Rating and pick.Team.Rating < 100:
            worseteam = True
        else:
            aa.remove(pick)
            
    #print ()
            
    return pick, ts, ds, ad, pick.Team #new driver, teams, drivers, allDrivers, new driver's previous team

def resolve (t2, d1, d2, t, d, ad):
    global Year
    d1.Rep = d1.Rep/2
    t1 = d1.Team

    for i in d:
        if i.Team == '':
            continue
        if i.Team.Name == '':
            continue
            #print (i.Name)

    if t2 == '':
        if Year >= 1975 or (t1.Rating > 25 or d1.Points > 0):
            print ('DRIVER CHANGE: ' + d1.Name + ' (' + t1.Name + ') replaced by ' + d2.Name)
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
        if d1.Team.Name == 'Privateer':
            pass
        elif Year >= 1975 or t1.Rating > 25 or d1.Points > 0 or d2.Points > 0 or t2.Rating > 25 :
            print ('DRIVER CHANGE: ' + d1.Name + ' (' + t1.Name + ') replaced by ' + d2.Name + ' (' + t2.Name + ')', end = ' ')
        if random.random() > 0.5 + d1.Rep/10:
            print ()
            t1.Drivers.remove(d1)
            t2.Drivers.remove(d2)
            t1.Drivers.append(d2)
            t2.Drivers.append(d1)
            d1.Team = t2
            d2.Team = t1
            d3, t, d, ad, t3 = pick (t, t2, allDrivers, d1, d)
            resolve (t3, d1, d3, t, d, ad)
        else:
            if d1.Team.Name == 'Privateer':
                pass
            elif Year >= 1975 or t1.Rating > 25 or t2.Rating > 25 or d1.Points > 0 or d2.Points > 0:
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
            if i.Wins > 0 or d[0].Points*0.5 < i.Points or i.Team == '' or i.Team == p or 0.75*(i.Team.Points-i.Points) <= i.Points > 0 or i.Races < c/2:
                continue
            elif random.random() > (5 + i.Rep + i.Peak**3 + i.Rating + i.Points/8 - i.Team.Points/20 + i.Podiums - i.DNFs*0.1 + (n+1-i.YRaces) #+ (c-n)/5
                                    - (2020-Year)/4 + 5*i.Moves) / 10 and random.random() < 1/10:
                if i.Team.Name == '':
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
        if random.random() <  1/(500-(2020-Year)*2):
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
                    if i.Team.Name != 'Privateer':
                        print (i.Name + ' ('+i.Team.Name+')' + ' is injured. He will miss the next ' + str(i.Injury) + ' races. To be replaced by ' + j.Name)          
                    i.Sub = j
                    break

    return d, ad, t











def season (Drivers, Teams, Year, Races):
    global allDrivers, space, formers
    print (Year, end = ' - ')
    print (len(Teams), 'Teams,', len(Races), 'Races')

    space = 0
    for i in Drivers:
        if len(i.Name) > space:
            space = len(i.Name)

    teamspace = 0
    for i in Teams:
        i.Points = 0
        if len(i.Name) > teamspace:
            teamspace = len(i.Name)

    for i in Drivers:
        i.Points = 0
        i.Wins = 0
        i.DNFs = 0
        i.Podiums = 0
        i.YRaces = 0
        i.Moves = 0
        i.Best = 1000
        if Year == i.First and Year != 1950:
            i.Rating = i.Rating * random.uniform(1/4,2/3)
        else:
            i.Rating = i.Rating + 0.5*(i.Peak-i.Rating)
        if (Year >= i.Last - 2 or Year - i.First > 15) and i.Last < 2019:
            i.Rating = i.Rating * random.uniform(0.5,1)
        i.Rating = round(i.Rating,1)
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

    Teams.sort(key = lambda x: x.Rating, reverse = True)

    ChampionDecided = False

    Drivers, allDrivers, Teams = injuries (Drivers, allDrivers, Teams, [])
    
    for n in range (len(Races)):
        #print ()
        #time.sleep(0.01)
        x, y, z, PodTeams, Pole, DNQs = race (Drivers, Teams, len(pointsdict))
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
            if i.Last == Year and i.Last - i.First < 15:
                i.Last = i.Last + 1
            if i.Rating < 3:
                i.Rating = i.Rating*2
            
            i.Rating = round(i.Rating,1)
                
        if i.Team == '':
            continue
                
        if i.Team.Points > 0:
            i.Rep = i.Rep + (i.Points/i.Team.Points)


                


    


    print ('Driver'.ljust(space), 'Team'.ljust(teamspace), 'Pts', ' W', ' P', ' R', 'DNF')
    for i in Drivers:
        if i.Points > 1: #or (i.YRaces > 0 and i.Team != "Privateer"):
            if i.Team != '':
                print (i.Name.ljust(space), i.Team.Name.ljust(teamspace), str(i.Points).rjust(3), str(i.Wins).rjust(2),
                       str(i.Podiums).rjust(2), str(i.YRaces).rjust(2), str(i.DNFs).rjust(2), end = '   ')#str(round(i.Rep,1)).rjust(5),i.Rating, end =' ')
            else:
                print (i.Name.ljust(space), ''.ljust(teamspace), str(i.Points).rjust(3), str(i.Wins).rjust(2),
                       str(i.Podiums).rjust(2), str(i.YRaces).rjust(2), str(i.DNFs).rjust(2), end = '   ')#str(round(i.Rep,1)).rjust(5),i.Rating, end =' ')
            
            for j in Champions:
                if j[1] == i.Name:
                    print (j[0], end=' ')
            print()
    print ('0 points: ',end ='')
    for i in Drivers:
        if i.YRaces > 0 and i.Points == 0:
            if i.Team != '':
                print (i.Name + ' (' + i.Team.Name +'), ', end =  '')
            else:
                print (i.Name, end =  ', ')
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

    for i in Teams:
        DriverLog.append([i.Name,i.Drivers])

    for i in Drivers:
        if i.First + 5 == Year and i.Races == 0:
            i.Last = Year
        if i.Last == Year:
            if i.Last-i.First < 12 and i.rangz > 0 and i.First != 1950 and i.Last >= Year:
                i.Last = i.Last + 1
            else:
                Drivers.remove(i)

    for i in allDrivers:
        if i.First == Year+1:
            Drivers.append(i)

    global formerTeams

    for i in Teams:
        if i.Name == 'Ferrari' or (i.Name == 'Privateer' and Year < 1965):
            continue
        if (      ((i.Rating < (30-(i.rangz)) and random.random() < 1/5)
                   or (i.Rating < (2-(i.rangz/40))  and random.random() < 1/5)
             or (i.Rating < 5 and i.Wins < 1  and (0 < (Year - i.First) < 5) and random.random() < 1/5 )
                   or (i.Rating < 1 and Year - i.First < 2 and random.random() < 1/3 and i.Wins < 1 )
                  or ( Year < 1960 and random.random() < 1/25)
                   )
            and ( len(Teams) > 10 or (Year < 1975 and len(Teams) > 7) ) 
        or (Year > 1970 and random.random() < 1/10 and i.Name == 'Privateer')):
            
            print (i.Name, 'leaving F1.')
            if i.Name not in formers and i.Wins > 1:
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
    if Year > 1960:
        possteams.append('Lotus')
        possteams.append('Chrysler')
        possteams.append('Chevrolet')
        possteams.append('Lola')
    if Year > 1966:
        possteams.append('Honda')
        possteams.append('Toyota')
        possteams.append('Nissan')
        possteams.append('Mazda')
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
                'Mazda':'Japan', 'McLaren':'United Kingdom', 'Brabham':'Australia', 'March':'United Kingdom', 'Williams':"United Kingdom", 'Carlin':'United Kingdom'
        }


    possteams = possteams + [i for i in formers if i not in possteams]

    names = [i for i in allDrivers if (i.Rep > (30 + 20*random.random() + max (0, Year-1990) ) and i.Last < Year - 3 and i.First + 15 < Year and i. First > Year - 30)
             or (i.Rep > 10 and Year < 1975 and i.First + 7 < Year) ]
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


    if random.random() < 1/3:
        x = random.choice(possteams)
        if type(x) == list:
            teammake(x[1], 1, x[0], x[2])
        else:
            teammake(x, 1, '', natdict.get(x, ''))
        
    if Year+1 == 1954:
        teammake('Mercedes',70,'',"Germany")
    if Year+1 == 1954 and random.random() < 1/10:
        teammake('Vanwall',0.1,'',"United Kingdom")
    if Year+1 == 1956 and random.random() < 1/2:
        teammake('B.R.M.',1,'',"United Kingdom")
    if Year+1 == 1960:
        teammake('Lotus',1,'',"United Kingdom")
    if Year+1 == 1964 and random.random () <1/2:
        teammake('Honda',1,"",'Japan')
    if Year+1 == 1966:
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
        teammake('Arrows',0.1,'',"United Kingdom")
    if Year+1 == 1985 and random.random() < 1/10:
        teammake('Minardi',0.1,'',"Italy")
    if Year+1 == 1986 and random.random() < 1/5:
        teammake('Benetton',1,'',"Italy")
    if Year+1 == 1991 and random.random() < 1/5:
        teammake('Jordan',0.1,'',"United Kingdom")
    if Year+1 == 1993 and random.random() < 1/5:
        teammake('Sauber',0.1,'','')
    if Year+1 == 1999 and random.random() < 1/10:
        teammake('B.A.R.',0.1,'',"Canada")
    if Year+1 == 2002 and random.random() < 1/5:
        teammake('Toyota',1,'',"Japan")
    if Year+1 == 2005:
        teammake('Red Bull',1,'','')
    if Year+1 > 2005 and random.random() < 1/50 and 'Red Bull' not in possteams:
        teammake('Toro Rosso',0.1,'','')
    if Year+1 == 2008 and random.random() < 1/10:
        teammake('Force India',0.1,'',"India")
    if Year+1 == 2009 and random.random() < 1/10:
        teammake('Brawn GP',1,'','')
    if Year+1 == 2016 and random.random() < 1/5:
        teammake('Haas',0.1,'',"United States")
    
    Retiring = []
    print ('Retiring:')
    allDrivers.sort(key = lambda x: x.rangz + x.CWins/1000 + x.Races/1000000, reverse = True)
    for i in allDrivers:
        if i.Last == Year and i.Races > 0:
            if i.Team != '':
                print (i.Name.ljust(space), i.Team.Name.ljust(teamspace), str(i.Races).rjust(3), 'Races', str(i.CWins).rjust(3), 'Wins', str(i.CPodiums).rjust(3),
                       'Podiums', str(i.rangz).rjust(2), 'Championships',  end =' ')
            else:
                print (i.Name.ljust(space), ''.ljust(teamspace), str(i.Races).rjust(3), 'Races', str(i.CWins).rjust(3), 'Wins', str(i.CPodiums).rjust(3),
                'Podiums', str(i.rangz).rjust(2), 'Championships',  end =' ')

            for j in Champions:
                if j[1] == i.Name:
                    print (j[0], end = ' ')
            print ()
    print ()
    for i in Drivers:
        i.Contract = i.Contract - 1

    Teams.sort(key= lambda x: x.Points, reverse = True)
    for i in Teams:
        if i.Name == 'Privateer':
            pass
        i.Drivers = []
        for j in Drivers:
            if i == j.Team and j.Last > Year:
                if random.random() < (1/3 + 0.1*j.Wins + 0.05*j.rangz) or j.Contract > 0 or j == Champion or i.Owner == j.Name:
                    if j.Rep > 30 and j.Contract == 0:
                        j.Contract = random.randrange(3,6)
                    elif j.Rep > 10 and j.Contract == 0:
                        j.Contract = random.randrange(2,4)
                    elif j.Rep > 5 and j.Contract == 0:
                        j.Contract = random.randrange(1,3)
                    elif j.Contract == 0:
                        j.Contract = 1
                    if j not in i.Drivers:
                        i.Drivers.append(j)
                        j.Team = i
                    #print (i.Name.ljust(space), j.Name.ljust(space))
                else:
                    j.Team = ''
            elif j.Last <= Year:
                j.Team = ''

    n = 0
    if Year < 1975:
        m = 3
    else:
        m = 2
        
    for i in Teams:
        while len(i.Drivers) < m:
            Drivers.sort(key= lambda x: eval (x, i, Year, ''), reverse = True)
            if Drivers[0].Rep > 30:
                Drivers[0].Contract = random.randrange(3,6)
            elif Drivers[0].Rep > 10:
                Drivers[0].Contract = random.randrange(2,4)
            elif Drivers[0].Rep > 5:
                Drivers[0].Contract = random.randrange(1,3)
            else:
                Drivers[0].Contract = random.randrange(1,2)
            if Drivers[0] not in i.Drivers:
                Drivers[0].Team = i
                i.Drivers.append(Drivers[0])
            #print (i.Name.ljust(space), Drivers[0].Name.ljust(space),round(Drivers[0].Rep,1))


    for i in Teams:
        if Year < 1975 and i.Name == 'Privateer':
            Drivers.sort(key= lambda x: (Year-x.First) + eval (x, i, Year, ''), reverse = True)
            n =( (random.randrange(0,10) - (Year-1980)) - len(Teams) ) / 4
            
            for j in range(round(n)):
                Drivers[j].Team = i
                Drivers[j].Contract = 1
                i.Drivers.append(Drivers[j])


    for i in Teams:
        if i.Rating > 500:
            i.Rating = i.Rating**random.uniform(0.5,1)
        if i.Rating > 500:
            i.Rating = i.Rating/random.uniform(1,10)
        elif random.random() < 1/10:
            i.Rating == i.Rating * 25 * random.random()
        elif i.Rating < 100:
            if random.random () < 0.5:
                i.Rating = i.Rating*random.uniform(1,10)
            else:
                i.Rating = i.Rating*random.uniform(0.1,1)
        else:
            i.Rating = i.Rating*random.uniform(0.25,1.25)
            
        if Year % 7 == 0:
            prev = i.Rating
            i.Rating = 10**(random.uniform(-8,2)) + i.Rating**(1/3)
            if i.Rating < 1:
                i.Rating = random.uniform(0, 3) + prev**(1/3)

        if Year % 3 == 0 and random.random() < 0.2:
            i.Rating = i.Rating**(1/2) + i.Rating * 2**((random.uniform (0, 2))**3)

        if i.Rating < 1:
            i.Rating = i.Rating**random.uniform(0.5,2)

        if Year - i.First < 5:
            i.Rating = i.Rating *random.uniform(0.2,1)


        if i.Name in ['Ferrari', 'Mercedes', 'Alfa Romeo', 'Renault', 'McLaren', 'Lotus', 'Williams'] and random.random() < 1/7:
            i.Rating = i.Rating * random.uniform(1,5)


    fastest = 0

    while fastest < 10:
        total = 0
        for i in Teams:
            total = total + i.Rating
            if i.Rating > fastest:
                fastest = i.Rating
        if fastest > 10:
            continue
        else:
            total = 0
            for i in Teams:
                i.Rating = 1 + i.Rating**2
                total = total + i.Rating
        
    factor = 1000/total

    for i in Teams:
        i.Rating = i.Rating * factor
        i.Rating = round(i.Rating,1)
        if i.Rating == 0:
            i.Rating = 0.1

        if i.Name == 'Privateer':
            i.Rating = 1

        for j in Teams:
            if i.Rating > j.Rating and i.Name == 'Toro Rosso' and j.Name == 'Red Bull':
                i.Rating, j.Rating = j.Rating, i.Rating

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
        if ot != i.Team.Name:
            print (i.Name.ljust(space), k[0].center(teamspace), 'to', i.Team.Name.center(teamspace))

    print ('No ' + str(Year+1) + ' Seat: ', end ='')
    for k in DriverLog:
        for l in k[1]:
            for m in Drivers:
                if l.Name == m.Name and m.Team == '' and l.Last > Year and k[0] != 'Privateer' and Year != 1950:
                    print (l.Name + " (" + k[0] +'), ', end ='')
    print()

    print ('Returning:', end = ' ')
    for i in Drivers:
        tick = False
        for k in DriverLog:
            #print (i.Name, k[1])
            if i in k[1]:
                tick = True
        if i.Team != '' and i.Races > 0 and tick == False:
            print (i.Name + " (" + i.Team.Name + ")", end = ', ')

    print ()
    print ('Rookies:', end = ' ')
    for i in Drivers:
        if i.Team != '' and i.Races == 0:
            print (i.Name + " (" + i.Team.Name + ")", end = ', ')

    print ()
    print()

    for i in Teams:
        if i.Name == 'Privateer' or Year == 1950:
            continue
        check = False
        print (i.Name.ljust(teamspace), end = ' ')
        i.Drivers.sort(key = lambda x: x.Name)
        print (Year, end = ' - ')
        for k in DriverLog:    
            if k[0] == i.Name:
                check = True
                for j in k[1]:
                    k[1].sort(key = lambda x: x.Name)
                    print (j.Name.ljust(space), end= ' ')
        if check == False:
            if Year > 1975:
                print (' '.ljust(2+2*space), end = '')
            else:
                print (' '.ljust(3+3*space), end = '')
        print (Year+1, end = ' - ')
        for j in i.Drivers:
            print (j.Name.ljust(space), end = ' ')

                        
        print ()

    for i in Teams:
        if i.Name == 'Privateer':
            print ('Privateers: ', end = '')
            for j in i.Drivers:
                print (j.iln, end =', ')
            print()


    return Drivers, Teams


def calendar (r, y):
    print ()
    possibles = ['ESP', 'GER', 'NED', 'ARG', 'MOR', 'POR', 'USA','AUT']

    if y > 1960:
        possibles = possibles + ['MEX', 'CAN', 'RSA', 'BRA', 'JPN']
    if y > 1970:
        possibles = possibles + ['FIN', 'SMR', 'EUR', 'USW', 'SWE']
    if y > 1980:
        possibles = possibles + ['AUS', 'HUN', 'URU', 'DET', 'other']
    if y > 1990:
        possibles = possibles + ['MAL', 'PAC', 'CHN', 'NZL', 'RUS']
    if y > 2000:
        possibles = possibles + ['BAH', 'ABU', 'TUR', 'SIN', 'KOR']
    if y > 2010:
        possibles = possibles + ['NYC', 'AZB', 'VNM', 'IND', 'QAT']


    for i in r:
        if i not in ['MON', 'GBR', 'BEL', 'ITA', 'JPN'] and ( random.random() < 0.03 or
                                                              (Year < 1960 and random.random() < 1/10)) and ( (Year < 1960 and len(r)>6) or (Year < 1970 and len(r)>8) or (Year < 1980 and len(r)>10)
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
            if ( (random.random() < 1/3 and len(r) < 20) or (random.random() < 1/4 and len(r) >= 20 ) ) and ( (Year > 1950 and len(r) < 10) or (Year > 1970 and len(r) < 18) or (Year > 2010)  ):
                candidates = [i for i in possibles if i not in r]
                x = random.choice(candidates)
                if x == ('USW' or 'DET' or 'NYC' or 'PAC') and 'USA' not in r:
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

    summer = ['GBR','MON','BEL','FRA','ITA','GER','SUI','ESP','NED','POR','AUT','CAN','QBC',
              'RUS','SMR','EUR','SWE','HUN','POL','DET','IRE','TUR','CZE','AZB','FIN','NYC']

    additionals = [ ['AUS','Mount Panorama'], ['AUS','Surfers Paradise'], ['AUT','Vienna'], ['CAN','Vancouver'], ['CHI', 'Macau'], ['ITA','Imola'], ['RUS','Moscow'], ['SUI','Dijon'],
                    ['AUT','Salzburgring'], ['AUS', 'Phillip Island'], ['AUS', 'Eastern Creek'], ['GER','Sachsenring'], ['SUI','Geneva'],['FIN','Tampere'],['SMR','Mugello'],['MOR','Marrakech'],
                    ['DNK','Copenhagen'],['JPN','Motegi'],['SWE','Karlskoga'],['CAN','Edmonton'],['NED','Assen'],['MEX','Monterrey'],['POR','Algarve'],['RSA','Cape Town'],['EUR', 'Rome'],
                    ['URU','Montevideo'], ['NZL','Pukekohe'], ['FIN','Ahvenisto'], ['DNK','Jyllandsringen'], ['QAT','Doha'], ['NYC','New York City'], ['VNM','Hanoi'],['NZL','Wellington'],
                    ['PAC','Laguna Seca'],['PAC','Long Beach'], ['PAC','Tsukuba'], ['PAC', 'Vancouver'],['PAC','Surfers Paradise'],
                    ['USA', 'Laguna Seca'], ['USW', 'Laguna Seca'], ['USA', 'Road America'], ['USA', 'Omaha'],
                    ['USA','Daytona'], ['USA','Virginia Intl.'], ['USA','Miami'], ['USA','Chicago'], ['USW','Portland'],['USW','Sonoma'],['USA','Road Atlanta'],                    
                    ['NYC','Brooklyn'], ['NYC','Port Imperial']
        ]


    unusuals = [ ['CZE','Brno'], ['CZE','Prague'], ['DNK','Copenhagen'], ['DNK', 'Jyllandsringen'], ['ROM', 'Bucharest'], ['POL', 'Warsaw'],['IRE', 'Mondello Park'],["SCO",'Knockhill'],
                 ['LUX','Nürburgring'], ['IRN','Tehran'], ['KEN','Nairobi'], ['EGY','Cairo'], ['LDN','Brands Hatch'], ['QBC','Montréal'],['LVG','Las Vegas'],['BER','Berlin'],['ISR','Tel-Aviv'],
                 ['FLN','Zolder']
                 
                 
                 ]


    if y < 1995:
        unusuals.append(['YUG','Grobnik'])
        unusuals.append(['SIC','Siracusa'])
        unusuals.append(['SOV','Moscow'])
    else:
        unusuals.append(['SVK','Slovakiaring'])
        unusuals.append(['GEO','Tblisi'])
        unusuals.append(['NOR','Rakkestad'])
        unusuals.append(['CRO','Grobnik'])
        unusuals.append(['IDO','Sentul'])
        unusuals.append(['LAT','Biķernieki'])
        unusuals.append(['EST','Auto24Ring'])


    for x in unusuals:
        summer.append(x[0])


    unusuals.append(['DUB','Dubai'])
    unusuals.append(['KSA','Riyadh'])
    unusuals.append(['THA','Buriram'])
    unusuals.append(['CHL','Codegua'])
    unusuals.append(['TEX','Austin'])
    unusuals.append(['COL','Tocancipá'])

    if y > 2000:
        additionals.append(['GBR','Rockingham'])
        additionals.append(['FIN','Kymiring'])
        additionals.append(['ARG','Rio Hondo'])
        additionals.append(['RSA','Phakisa'])
        additionals.append(['NZL','Hampton Downs'])



    flyaways = [i for i in r if i not in summer]


    global Circuits

    for i in r:
        #print (i)
        if i in racedict:
            ov = racedict[i]
        else:
            ov = ''
            
        if i in racedict and (random.random() < 0.9 or (Year < 1975 and random.random() < 0.8) or (Year < 1960 and random.random() < 0.5)):
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
            if (j.Race == i and j.First <= Year and j.Last >= Year - 10 and j.Name not in racedict.values()  or
                (i == 'EUR' and j.Race in summer and j.Race in r and j.Name not in racedict.values() and j.First <= Year and j.Last >= Year - 10 and j.Race != ('CAN' or 'DET' or 'NYC'))):
                cands.extend([j.Name]*j.Total)

        
        #cands = [x for x in Circuits if x.Race == i and x.First <= Year]
            
        n = 0
        while len(cands) == 0 and n < 100:
            n = n+1
            cands = [x.Name for x in Circuits if x.Race == i and x.First <= Year+n and x.Last >= Year-n and x.Name not in racedict.values()]

        for j in additionals:
            if j[0] == i and j[1] not in racedict.values() and y > 1955:
                cands.append(j[1])

        if i == 'USA' and 'USW' not in r:
            cands = cands + [x.Name for x in Circuits if x.Race == 'USW' and x.First <= Year and x.Last >= Year - 10 and x.Name not in racedict.values()]

        if ov != '':
            cands.append(ov)

        if len(cands) == 0:
            r.remove(i)
            i = 'HKG'
            race = 'Hong Kong'
            racedict[i] = race
            r.append(i)
                
        if race == '':
            #print (i)
            cands.sort(key= lambda x: random.random())
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
        
        timedict = {'MON':-0.75,'ITA':0.9,'BEL':0.89,'HUN':0.5,'GBR':0, 'SMR':-0.9,'JPN':50,'MEX':50,'BAH':-50,'ARG':-80,'ABU':80}
        try:
            return timedict[x]
        except:
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
allDrivers.sort(key = lambda x: x.rangz + x.CWins/100 + x.Races/100000000000000, reverse = True)
print ('Driver'.ljust(25), 'Wins', 'Pods', ' Races', ' WP%', '  Championships')
x = 0
for i in allDrivers:
    if i.CWins >= 5 or i.rangz > 0 or i.CWins/(i.Races+0.01) > 0.1:
        if x > i.rangz:
            print()
        x = i.rangz
        per = '{0:.1f}'.format(round((100*i.CWins/(i.Races+0.0000000000000001)),2))
        print (i.Name.ljust(25), str(i.CWins).rjust(4), str(i.CPodiums).rjust(4), str(i.Races).rjust(5), str(per).rjust(5) + '%', i.rangz, end =' ')
        for j in Champions:
            if j[1] == i.Name:
                print (j[0], end=' ')
        print ()
