from .. import pos_list, neu_list, neg_list, not_list, degree_list
import re

inc_degree_list = ["rất", "quá", "lắm", "cực kỳ", "cực kì", "cực_kỳ", "cực_kì", "dã man", "dã_man", "ghê gớm", "ghê_gớm"]
dec_degree_list = ["hơi",  "tạm", "tương đối", "tương_đối"]

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

emotion_icons = {
    "👹": "negative", "👻": "positive", "💃": "positive",'🤙': ' positive ', '👍': ' positive ',
    "💄": "positive", "💎": "positive", "💩": "positive","😕": "negative", "😱": "negative", "😸": "positive",
    "😾": "negative", "🚫": "negative",  "🤬": "negative","🧚": "positive", "🧡": "positive",'🐶':' positive ',
    '👎': ' negative ', '😣': ' negative ','✨': ' positive ', '❣': ' positive ','☀': ' positive ',
    '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' positive ',
    '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
    '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
    '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
    '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
    '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' positive ',
    '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
    '😒': ' negative ', '🙂': ' positive ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
    '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
    '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
    '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
    '💓': ' positive ', '😐': ' negative ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
    '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
    '😗': ' positive ', '🤔': ' negative ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
    '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
    '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
    '🌝': ' positive ',  '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
    '🌼': ' positive ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
    '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ',
    '💰': ' positive ',  '😇': ' positive ', '😛': ' positive ', '😜': ' positive ',
    '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ',  '💀': ' negative ',
    '😔': ' negative ', '😧': ' negative ', '😩': ' negative ', '😰': ' negative ', '😳': ' negative ',
    '😵': ' negative ', '😶': ' negative ', '🙁': ' negative ', ':))': ' positive ', ':)': ' positive ',
    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ',
    'hjhj': ' positive ', ' lol ': ' negative ', 'huhu': ' negative ', ' 4sao ': ' positive ', ' 5sao ': ' positive ',
    ' 1sao ': ' negative ', ' 2sao ': ' negative ',
    ': ) )': ' positive ', ' : ) ': ' positive '
}

wrong_terms = {
    'ô kêi': ' ok ', 'okie': ' ok ', 'o kê': ' ok ', 'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', 'oke':  ' ok ',
    'okay': ' ok ', 'okê': ' ok ', 'ote': ' ok ',
    'kg ': u' không ', 'not': u' không ', u' kg ': u' không ', '"k ': u' không ', ' kh ': u' không ',
    'kô': u' không ', 'hok': u' không ', ' kp ': u' không phải ', u' kô ': u' không ', '"ko ': u' không ',
    ' ko ': u' không ', u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
    ' cam ': ' camera ', ' cameera ': ' camera ', 'thuết kế': u'thiết_kế', 'ết_kế ': u' thiết_kế ',
    'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ', 'good': u' tốt ', 'gút': u' tốt ',
    'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
    'bt': u' bình thường ',
    ' m ': u' mình ', u' mik ': u' mình ', 'mìn': u'mình', u' mìnhh ': u' mình ', u' mềnh ': ' mình ',
    ' mk ': u' mình ', ' mik ': ' mình ',
    u' wá ': u' quá ', ' wa ': u' quá ', u'qá': u' quá ',
    ' cute ': 'dễ_thương',
    u' tẹc vời ': ' tuyệt_vời ', u'tiệc dời': ' tuyệt_vời ', u'tẹc zời': ' tuyệt_vời ',
    ' dc ': u' được ', u' đc ': u' được ', ' j ': ' gì ',
    ' màn hìn ': ' màn_hình ', u' màng hình ': u' màn_hình ', ' dt ': u' điện_thoại ',
    ' đt ': u' điện_thoại ',
    ' tet ': u' kiểm_tra ', ' test ': u' kiểm_tra ', ' tét ': u' kiểm_tra ',
    u' cẩm ': u' cầm ', u' cấm ': u' cầm ', u' sước ': u' xước ', u' xướt ': u' xước ',
    u'sài ': ' xài ',
    u' mựơt ': u' mượt ',
    u' sức sắc ': u' xuất_sắc ', u' xức sắc ': u' xuất_sắc ',
    ' fai ': u' phải ', u' fải ': u' phải ',
    u' bây_h ': u' bây_giờ ',
    u' mội ': u' mọi ', ' moi ': u' mọi ',
    u'ợc điểm ': u' nhược điểm ',
    u' sámsumg ': ' samsung ', ' sam ': ' samsung ', 'sam_sung ': ' samsung ',
    u' kbiết ': u' không_biết ', u' rất tiết ': u' rất_tiếc ', u' rất_tiết ': u' rất_tiếc ',
    u' rất tiêc ': u' rất_tiếc ',
    u' lát ': ' lag ', u' lác ': ' lag ', ' lat ': ' lag ', ' lac ': ' lag ', u' khựng ': ' lag ', u' giật ': ' lag ',
    u' văng ra ': ' lag ', u' đơ ': ' lag ', u' lắc ': ' lag ',
    u' film ': ' phim ', ' phin ': ' phim ', ' fim ': ' phim ',
    ' nhung ': u' nhưng ', u' ấu hình ': u' cấu_hình ',
    ' sd ': u' sử_dụng ', u' mài ': u' màu ', u' lấm ': u' lắm ',
    u' tôt ': ' tốt ', u' tôn ': u' tốt ', 'aple ': ' apple ', "gja": u" giá ", u"sục": u"sụt",
    u' âm_lượ ': u' âm_lượng ', u' thất_vọ ': u' thất_vọng ', u' dùg ': u' dùng ',
    u' bỗ ': u' bổ ',
    u' sụt ': u' tụt ', u' tuột ': u' tụt ', u' xuống ': u' tụt ',
    u'chíp ': ' chip ',
    ' bin ': ' pin '
}

sentiment_stopwords = ("ufeff", "+", "", ".", ",", "!", "%", "....", "...", ")", "(", "thì", "là", "và", "bị", "với",
                       "thế_nào", "?", "", "một_số", "mot_so", "thi", "la", "va", "bi", "voi", "trong",
                       "the_nao", " j ", "gì", "có", "pin", "giá", "j7pro", "chứ", "máy", "tôi", "của", "để", "ai",
                       "sản_phẩm", "j7", "thấy", "bản", "vì", "nên", "ace", "pubg", "j5", "ip7", "ip7+", "nhé", "nhe",
                       "nhé'", "như", "từ ", "vậy", "2h", "thui", "thôi", "bin`", "fb", "facebook", "youtube", "pr", "phải"
                       "khi", "triệu", "triệu'", "18tr", "fan", "xài", "lại", "chụp", "camera", "plus", "điện_thoại",
                       "tới", "web", "reset", "nguyên_đán", "s9", "j8", "màn_hình", "64gb", "tết")


class VietnameseProcess:
    def __init__(self, sentence):
        self.sentence = sentence

    def remove_stopwords(self):
        for w in sentiment_stopwords:
            self.sentence = self.sentence.replace("%s " % w, " ")
            self.sentence = self.sentence.replace(" %s" % w, " ")

    def indicate_vietnamese_phrases(self):
        text = re.split("\s*[\s,;]\s*", self.sentence)
        length = len(text)
        for idx in range(length):
            if text[idx] in degree_list:
                if idx + 1 < length and (text[idx + 1] in pos_list):
                    # if text[idx] in inc_degree_list:
                    #     text.append("strongpositive")
                    text[idx] = "%s_%s" % (text[idx], text[idx + 1])
                elif idx - 1 >= 0 and (text[idx - 1] in pos_list):
                    text[idx] = "%s_%s" % (text[idx - 1], text[idx])
                    # if text[idx] in inc_degree_list:
                    #     text.append("strongpositive")

        self.sentence = " ".join(text)

    def replace_not_terms(self):
        text = re.split("\s*[\s,;]\s*", self.sentence)
        for idx in range(len(text)):
            if idx < len(text)-1 and text[idx] in not_list:
                if text[idx+1] in pos_list:
                    text[idx] = "notpositive"
                    text[idx+1] = ""
                if text[idx+1] in neg_list:
                    text[idx] = "notnegative"
                    text[idx+1] = ""
            elif text[idx] not in not_list:
                if text[idx] in neu_list:
                    text.append("neutral")
                elif text[idx] in pos_list:
                    text.append("positive")
                elif text[idx] in neg_list:
                    text.append("negative")

        self.sentence = " ".join(text)

    def replace_wrong_terms(self):
        for key, value in wrong_terms.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def replace_emotion_icons(self):
        for key, value in emotion_icons.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def remove_repeated_characters(self):
        self.sentence = re.sub(r'([A-Z])\1+', lambda m: m.group(1), self.sentence, flags=re.IGNORECASE)

    def remove_numbers(self):
        self.sentence = re.sub("[aj]*(ip)*\s*([0-9./])+(trieu)*(tr)*", " ", self.sentence, flags=re.IGNORECASE)

    def remove_special_character(self):
        """
        Remove all of the special characters in the sentence

        :return: the sentence after removing the special characters
        """
        punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~"""
        translator = str.maketrans(punctuation, ' '*len(punctuation))

        self.sentence = self.sentence.translate(translator)

    def remove_vietnamese_accents(self):
        """
        Remove the whole Vietnamese accents of the sentence
        Reference: https://gist.github.com/J2TEAM/9992744f15187ba51d46aecab21fd469

        :param sentence: the sentence need to remove
        :return: the sentence removed accents
        """

        result = ''
        for c in self.sentence:
            result += s0[s1.index(c)] if c in s1 else c

        self.sentence = result

