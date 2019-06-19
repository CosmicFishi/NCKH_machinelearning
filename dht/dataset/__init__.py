from dht.helper import Helper

pos_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/pos.txt", is_readlines=True))
neg_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/neg.txt", is_readlines=True))
neu_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/neutral.txt", is_readlines=True))
not_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/not.txt", is_readlines=True))
degree_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/degree.txt", is_readlines=True))
senti_wordnet = Helper.load_wordnet_by_csv()
vi_wordnet = Helper.load_wordnet_texts()
