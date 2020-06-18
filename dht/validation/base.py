from abc import ABC, abstractmethod
from dht.dataset.by_category import CategoryDataset


class ValidationBase(ABC):
    def __init__(self, train_path, test_path=None):
        c = CategoryDataset(path=train_path,
                            is_remove_special_character=True, is_replace_not_terms=True,
                            is_remove_number=True, is_indicate_phrases=True, is_replace_emotion_icons=True)
        self.train = c.load_dataset()

        if test_path is not None:
            c = CategoryDataset(path=train_path,
                                is_remove_special_character=True, is_replace_not_terms=True,
                                is_remove_number=True, is_indicate_phrases=True, is_replace_emotion_icons=True)
            self.test = c.load_dataset()

    def execute(self):
        pass

    @abstractmethod
    def validate(self):
        pass
