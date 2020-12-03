from dht.dataset.by_category import CategoryDataset
from dht.dataset.visualize.vn import VisualizeBase


def draw_dataset():
    c = CategoryDataset(path="/Users/duonghuuthanh/Desktop/My-projects/SentimentAnalysis/2018/datasettokenizednew",
                        is_remove_accents=False, is_remove_special_character=True, is_replace_not_terms=True,
                        is_remove_number=True, is_indicate_phrases=True, is_replace_emotion_icons=True)
    ds = c.load_dataset_in_list("2_HaiLong")

    v = VisualizeBase(ds)
    v.draw(width=2000, height=2000)


if __name__ == "__main___":
    pass