#!/usr/bin/python3

# Base imports
from abstract_classes import ReaderGen
from pathlib import Path

# Third imports 
import pandas as pd


class Reader:
    def __init__(self, strategy: ReaderGen) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ReaderGen:
       return self._strategy

    @strategy.setter
    def strategy(self, strategy: ReaderGen) -> None:
        self._strategy = strategy

    def run_read_file(self, file_path: Path) -> pd.DataFrame:
        try:
            return self._strategy.read_file(file_path=file_path)
        except NotImplementedError:
            print('Errou na implementação')

class ReaderDataCsv(ReaderGen):
    def read_file(self, file_path: Path) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        return df
    
class ReaderDataTsv(ReaderGen):
    def read_file(self, file_path: Path) -> pd.DataFrame:
        df = pd.read_csv(file_path, sep='\t')
        return df
    
class ReaderDataExcel(ReaderGen):
    def read_file(self, file_path: Path) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        return df
    
class RunReader:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def open_file(self) -> pd.DataFrame:
        try:
            return Reader(strategy=ReaderDataCsv()).run_read_file(self.file_path)
        except Exception as error:
            print(f"Primeiro Erro {error}")
            try:
                return Reader(strategy=ReaderDataTsv()).run_read_file(self.file_path)
            except Exception as error:
                print(f"Segundo erro {error}")
                try:
                    return Reader(strategy=ReaderDataExcel()).run_read_file(self.file_path)
                except Exception as error:
                    print(f'Errou {error}')


if __name__ == '__main__':
    file_path = 'C:\\Users\\Pichau\\Desktop\\programacao\\studying_flask\\cbb.csv'
    instance = RunReader(file_path=file_path)
    df = instance.open_file()
    print(df)