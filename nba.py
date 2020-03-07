from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats

player_dict = players.get_players()
team_dict = teams.get_teams()



def nba_player(player_name):
    for player in player_dict:
        if player["full_name"] == player_name:
            print (player)
            print (type(player))
            nba_list = []
            for value in player.values():
                nba_list.append(value)
            print(nba_list)

def nba_team(team_name):
    for team in team_dict:
        if team["full_name"] == team_name:
            return team
