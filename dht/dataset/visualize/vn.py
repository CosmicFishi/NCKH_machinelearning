import matplotlib.pyplot as plt
import numpy as np
import wordcloud


class VisualizeBase:
    def __init__(self, sentences=[]):
        self.sentences = sentences

    def draw(self, width=1000, height=1000, max_words=1000):
        cloud = np.array(self.sentences).flatten()
        plt.figure(figsize=(20, 10))
        word_cloud = wordcloud.WordCloud(max_words=max_words,
                                         background_color="black",
                                         width=width, height=height,
                                         mode="RGB").generate(str(cloud))
        plt.imshow(word_cloud)
        plt.show()

