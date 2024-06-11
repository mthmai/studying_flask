#!/usr/bin/python3

# Base imports
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Third imports
from flask import Flask, jsonify, make_response, render_template

# Projects imports
from data.create_database import Teams, Temporada, Staats

class Routes(ABC):
    def __init__(self):
        self._app = None  # Inicializa _app como None
        self.return_query = None

    @property
    def app(self):
        if self._app is None:
            self._app = Flask(__name__)
        return self._app

    @abstractmethod
    def validator(self) -> bool:
        pass

    @abstractmethod
    def action(self):
        pass

# Classe para as rotas de times
class RoutesHomepage(Routes):
    def validator(self) -> bool:
        try:
            @self.app.route('/', methods=['GET'])
            def get_homepage():
                print("Rota / chamada")
                #query = Teams.select(Teams.team, Teams.conference).dicts()
                self.return_query = render_template("index.html")
                return self.return_query
            return True
        except Exception as e:
            print(f"Exception in RoutesHomepage: {e}")
            return False

    def action(self):
        return self.app

# Classe para as rotas de times
class RoutesTeams(Routes):
    def validator(self) -> bool:
        try:
            @self.app.route('/teams', methods=['GET'])
            def get_all_teams():
                print("Rota /teams chamada")
                query = Teams.select(Teams.team, Teams.conference).dicts()
                self.return_query = make_response(jsonify(list(query)))
                return self.return_query

            @self.app.route('/teams/<team>', methods=['GET'])
            def get_unique_team(team: str):
                print(f"Rota /teams/{team} chamada")
                query = Teams.select(Teams.team, Teams.conference).where(Teams.team == team).dicts()
                result = None
                for value in query:
                    result = value
                self.return_query = jsonify(result) if result else jsonify({"error": "Team not found"}), 404
                return self.return_query

            print("Rotas de Teams registradas com sucesso")
            return True
        except Exception as e:
            print(f"Exception in RoutesTeams: {e}")
            return False

    def action(self):
        return self.app

# Classe para as rotas de temporada
class RoutesTemporada(Routes):
    def validator(self) -> bool:
        try:
            @self.app.route('/temporada', methods=['GET'])
            def get_all_temporada():
                print("Rota /temporada chamada")
                query = Temporada.select(Temporada.team, 
                                         Temporada.conference,
                                         Temporada.games_played,
                                         Temporada.games_win,
                                         Temporada.year).dicts()
                self.return_query = make_response(jsonify(list(query)))
                return self.return_query

            @self.app.route('/temporada/<int:temp>', methods=['GET'])
            def get_unique_temporada(temp: int):
                print(f"Rota /temporada/{temp} chamada")
                query = Temporada.select(Temporada.team, 
                                         Temporada.conference,
                                         Temporada.games_played,
                                         Temporada.games_win,
                                         Temporada.year).where(Temporada.year == temp).dicts()
                result = list()
                for value in query:
                    result.append(value)
                self.return_query = make_response(jsonify(result)) if result else jsonify({"error": "Season not found"}), 404
                return self.return_query

            print("Rotas de Temporada registradas com sucesso")
            return True
        except Exception as e:
            print(f"Exception in RoutesTemporada: {e}")
            return False

    def action(self):
        return self.app
    
class RoutesStaats(Routes):
    def validator(self) -> bool:
        try:
            @self.app.route('/staats', methods=['GET'])
            def get_all_staats():
                print("Rota /staats chamada")
                query = Staats.select().dicts()
                self.return_query = make_response(jsonify(list(query)))
                return self.return_query

            @self.app.route('/staats/<team>', methods=['GET'])
            def get_unique_team_staats(team: str):
                print(f"Rota /staats/{team} chamada")
                query = Staats.select(Staats.team, 
                                         Staats.conference,
                                         Staats.games_played,
                                         Staats.games_win,
                                         Staats.year).where(Staats.team == team).dicts()
                result = list()
                for value in query:
                    result.append(value)
                self.return_query = make_response(jsonify(result)) if result else jsonify({"error": "Season not found"}), 404
                return self.return_query

            print("Rotas de Staats registradas com sucesso")
            return True
        except Exception as e:
            print(f"Exception in RoutesStaats: {e}")
            return False

    def action(self):
        return self.app

# Classe para gerenciamento das rotas
class IRoutes:
    def __init__(self, strategies: List[Routes]) -> None:
        self.strategies = strategies
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        for strategy_cls in self.strategies:
            strategy = strategy_cls()
            strategy._app = self.app  # Usa o mesmo aplicativo Flask para todas as estratégias
            if strategy.validator():
                print(f"Estratégia {strategy_cls.__name__} validada e rotas registradas com sucesso")
            else:
                print(f"Estratégia {strategy_cls.__name__} falhou na validação")

    def action_function(self) -> Any:
        return self.app
    
if __name__ == '__main__':
    #routes_teams = RoutesTeams()
    #routes_temporada = RoutesTemporada()

    #routes_teams.define_routes()  # Chama o método para definir as rotas
    #routes_temporada.define_routes()
    app_instance = IRoutes(
        strategies=[RoutesHomepage, RoutesTeams, RoutesTemporada, RoutesStaats]
    ).action_function()
    
    if app_instance:
        app_instance.run(debug=True)
    else:
        print("No valid strategy found")
    #instance.app.run(debug=True)
    #instance.app.run(debug=True)
    #routes_teams.app.run(debug=True)
    #routes_temporada.app.run(debug=True)
