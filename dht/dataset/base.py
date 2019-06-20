from abc import ABC, abstractmethod
import pandas as pd
import os


class BaseDataset(ABC):
    def __init__(self, path):
        self.path = path

    def load_dataset(self, ignore_categories=[".DS_Store"]):
        ds = []

        items = os.listdir(self.path)
        for item in items:
            if item not in ignore_categories:
                ds = ds + self._read(item=item)

        df_train = pd.DataFrame(ds)

        return df_train

    @abstractmethod
    def _read(self, item):
        pass

    @abstractmethod
    def _pre_process(self, sentence):
        pass

