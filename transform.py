teams = ['ATL- Atlanta Hawks',
'BOS- Boston Celtics',
'CHA- Charlotte Hornets',
'CHI- Chicago Bulls',
'CLE- Cleveland Cavaliers',
'DAL- Dallas Mavericks',
'DEN- Denver Nuggets',
'DET- Detroit Pistons',
'GSW- Golden State Warriors',
'HOU -Houston Rockets',
'IND- Indiana Pacers',
'LAC -Los Angeles Clippers',
'LAL- Los Angeles Lakers',
'MEM- Memphis Grizzlies',
'MIA- Miami Heat',
'MIL- Milwaukee Bucks',
'MIN- Minnesota Timberwolves',
'NOH- New Orleans Pelicans',
'NYK- New York Knicks',
'BKN- Brooklyn Nets',
'OKC- Oklahoma City Thunder',
'ORL- Orlando Magic',
'PHI- Philadelphia 76ers',
'PHO- Phoenix Suns',
'POR- Portland Trail Blazers',
'SAC- Sacramento Kings',
'TOR- Toronto Raptors',
'UTH- Utah Jazz',
'WAS- Washington Wizards']

codes = []
map = {}
teamsArr = []
for team in teams:
    splitter = team.split('-')
    teamsArr.append(splitter[1].strip())

    # map[splitter[0]] = splitter[1].strip()

print(teamsArr)
# print(map)
    
