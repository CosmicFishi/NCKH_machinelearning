from .by_category import CategoryDataset
from .augmented.sentiment_augmentation import SentimentAugmentation


class AugmentedDataset(CategoryDataset):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)

    def _get_item(self, item, content):
        augmented_contents = [{
            "feature": content,
            "target": item
        }]

        print("=== Original sentence === ", content)

        augmented_contents = augmented_contents + [{
            "feature": sentence,
            "target": item
        } for sentence in SentimentAugmentation(content).execute(num=5)]

        return augmented_contents
