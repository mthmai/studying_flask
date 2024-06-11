#!/usr/bin/python3

# Base imports
from abc import ABC, abstractmethod
from pathlib import Path

# Third imports
import pandas as pd


class ReaderGen(ABC):
    
    @abstractmethod
    def read_file(self, file_path: Path) -> pd.DataFrame:
        ...

class ReaderFiles(ABC):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.dataframe = None

    @abstractmethod
    def validator(self) -> bool:
        pass

    @abstractmethod
    def action(self) -> pd.DataFrame:
        pass