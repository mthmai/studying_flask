#!/usr/bin/python3

# Base imports
from datetime import datetime

# Third imports
import pandas as pd
from peewee import IntegrityError

# Projects imports
from create_database import Teams, Temporada, Staats
from treat_data_chain_of_responsibility import IReader, ReaderCsv, ReaderExcel, ReaderTsv

class PopulateDatabase:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def populate_teams(self) -> None:
        for _, row in self.dataframe.iterrows():
            try:
                teams = Teams.create(
                    team=row['TEAM'], 
                    conference=row['CONF']
                    )
            except IntegrityError:
                continue

    
    def populate_temporada(self) -> None:
        for _, row in self.dataframe.iterrows():
            try:
                temporada = Temporada.create(
                        team=row['TEAM'], 
                        conference=row['CONF'],
                        games_played=row['G'],
                        games_win=row['W'],
                        year=row['YEAR']
                )
            except IntegrityError:
                continue

    def populate_staats(self) -> None:
        for _, row in self.dataframe.iterrows():
            staats = Staats.create(
                team=row['TEAM'], 
                conference=row['CONF'],
                games_played=row['G'],
                games_win=row['W'],
                year=row['YEAR'],
                adjoe=row['ADJOE'],
                adjde=row['ADJDE'],
                barthag=row['BARTHAG'],
                efg_o=row['EFG_O'],
                efg_d=row['EFG_D'],
                tor=row['TOR'],
                tord=row['TORD'],
                orb=row['ORB'],
                drb=row['DRB'],
                ftr=row['FTR'],
                ftrd=row['FTRD'],
                two_point_o=row['2P_O'],
                two_point_d=row['2P_D'],
                three_point_o=row['3P_O'],
                three_point_d=row['3P_D'],
                adj_t=row['ADJ_T'],
                wab=row['WAB'],
                postseason=row['POSTSEASON'],
                seed=row['SEED']
            )

if __name__ == '__main__':
    start = datetime.now()
    file_path = 'C:\\Users\\Pichau\\Desktop\\programacao\\studying_flask\\cbb.csv' 
    df = IReader(
            strategies=[ReaderCsv, ReaderTsv, ReaderExcel]
        ).action_function(value=file_path)
    
    instance = PopulateDatabase(df)
    instance.populate_teams()
    instance.populate_temporada()
    instance.populate_staats()
    elapsed = str(datetime.now() - start).split('.')[0]
    print(f'Finished. Time elapsed: {elapsed}')