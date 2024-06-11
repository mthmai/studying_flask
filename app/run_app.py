#!/usr/bin/python3

# Third imports
from flask import Flask, jsonify, make_response

# Projects imports
from data.create_database import Teams, Temporada, Staats
#app = Flask(__name__)


class Routes:
    def __init__(self):
        self._app = None  # Defina _app como None inicialmente

    @property
    def app(self):
        if self._app is None:
            self._app = Flask(__name__)
        return self._app

    def define_routes(self):
        raise NotImplementedError("Método define_routes deve ser implementado nas subclasses")

class RoutesTeams(Routes):
    
    def define_routes(self):
        @self.app.route('/teams', methods=['GET'])
        def get_all_teams():
            query = Teams.select(Teams.team, Teams.conference).dicts()
            list_dict = list(query)
            return make_response(jsonify(list_dict))
        
        @self.app.route('/teams/<team>', methods=['GET'])
        def get_unique_team(team: str):
            query = Teams.select(Teams.team, Teams.conference).where(Teams.team == team).dicts()
            
            for value in query:
                result = value

            return jsonify(result)
            
if __name__ == '__main__':

    routes_teams = RoutesTeams()
    routes_teams.define_routes()  # Chama o método para definir as rotas
    routes_teams.app.run(debug=True)