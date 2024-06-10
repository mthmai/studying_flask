#!/usr/bin/python3

# Base imports
from typing import Any, Dict, List

# Third imports
import pandas as pd

# Projects imports
from abstract_classes import ReaderFiles


class ReaderCsv(ReaderFiles):
    def validator(self) -> bool:
        try:
            self.dataframe = pd.read_csv(self.file_path)
            return True
        except Exception:
            raise False

    def action(self) -> pd.DataFrame:
        return self.dataframe


class ReaderTsv(ReaderFiles):
    def validator(self) -> bool:
        try:
            self.dataframe = pd.read_csv(self.file_path, sep='\t')
            return True
        except Exception:
            return False

    def action(self) -> pd.DataFrame:
        return self.dataframe


class ReaderExcel(ReaderFiles):
    def validator(self) -> bool:
        try:
            self.dataframe = pd.read_excel(self.file_path)
            return True
        except Exception:
            return False

    def action(self) -> pd.DataFrame:
        return self.dataframe


class IReader:
    def __init__(self, strategies: List[ReaderFiles]) -> None:
        self.strategies = strategies

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs) -> None:
        self._kwargs = kwargs

    @property
    def strategy(self) -> ReaderFiles:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ReaderFiles) -> None:
        self._strategy = strategy

    def _call_next(self) -> Any:
        self.stats_tuples_list = list()
        for strategy in self.strategies:
            self.strategy = strategy(self.kwargs.get('value'))
            if not self.strategy.validator():
                continue
            return self.strategy.action()

    def action_function(self, **kwargs) -> Any:
        self.kwargs = kwargs
        return self._call_next()
    
if __name__ == '__main__':
    file_path = 'C:\\Users\\Pichau\\Desktop\\programacao\\studying_flask\\cbb.csv' 
    df = IReader(
            strategies=[ReaderCsv, ReaderTsv, ReaderExcel]
        ).action_function(value=file_path)
    
    print(df)