from dht.helper import Helper

pos_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/pos.txt", is_readlines=True))
neg_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/neg.txt", is_readlines=True))
neu_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/neutral.txt", is_readlines=True))
not_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/not.txt", is_readlines=True))
degree_list = Helper.duplicate_terms_list(Helper.read_text_file("dataset/sentiment/degree.txt", is_readlines=True))
senti_wordnet = Helper.load_wordnet_by_csv()
vi_wordnet = Helper.load_wordnet_texts()

sentiment_stopwords = ["ufeff", "+", "\"", "", ".", ",", "!", "%", "....", "...", ")", "(", "thì", "là", "và", "bị", "với",
                       "thế_nào", "?", "", "một_số", "mot_so", "thi", "la", "va", "bi", "voi", "trong",
                       "the_nao", " j ", "gì", "có", "pin", "giá", "j7pro", "chứ", "máy", "tôi", "của", "để", "ai",
                       "sản_phẩm", "j7", "thấy", "bản", "vì", "nên", "ace", "pubg", "j5", "ip7", "ip7+", "nhé", "nhe",
                       "nhé'", "như", "từ ", "vậy", "2h", "thui", "thôi", "bin`", "fb", "facebook", "youtube", "pr", "phải"
                       "khi", "triệu", "triệu'", "18tr", "fan", "xài", "lại", "chụp", "camera", "plus", "điện_thoại",
                       "tới", "web", "reset", "nguyên_đán", "s9", "j8", "màn_hình", "64gb", "tết", "nhân_viên"]
