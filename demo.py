import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re
import warnings
warnings.filterwarnings('ignore')
sb.set_style("darkgrid")
from underthesea import word_tokenize, pos_tag, sent_tokenize # sent_tokenize tách ra từ 1 văn bản thành nhiều câu
import regex
import demoji
from pyvi import ViPosTagger, ViTokenizer
import string
from sklearn.model_selection import KFold, train_test_split, cross_validate
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.preprocessing import FunctionTransformer
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.semi_supervised import LabelSpreading
from sklearn.metrics import f1_score
from imblearn.pipeline import Pipeline
import os
from imblearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB,ComplementNB, GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time

import joblib
import streamlit  as st


data = pd.read_csv('crawl_data/Foody.csv')



############
def replace_word(text):
    text = text.lower()  #chuyển kí tự in hoa sang chữ thường
    
    text = text.replace('\.',' ') #bỏ một số kí tự đặc biệt ngăn cách câu
    text = text.replace(',',' ') #bỏ một số kí tự đặc biệt ngăn cách câu
    text = text.replace('[0-9]+k|[0-9]+đ|[0-9]+vnd||[0-9]+vnđ','') #bỏ các cụm về giá 
    text = text.replace( ':)','')
    text = text.replace( '🥰',' yêu ')
    text = text.replace( '😘',' yêu ')
    text = text.replace( 'app','')
    text = text.replace( ' add ',' thêm ')
    text = text.replace( 'tuyệt vơi','tuyệt vời')
    text = text.replace( 'tuyêth vời','tuyệt vời')
    text = text.replace( 'soang chảnh','sang chảnh')
    text = text.replace( 'chình ình','chình_ình')
    text = text.replace( ' ình ',' mình ')
    text = text.replace( ' tuyệ ',' tuyệt ')
    text = text.replace(' kb ',' không biết ')
    text = text.replace('báh','bánh')
    text = text.replace(' k hề ',' không hề ')
    text = text.replace('đưpj','đẹp')
    text = text.replace('rẻe','rẻ')
    text = text.replace(' siu ',' siêu ')
    text = text.replace(' ưg ',' ưng ')
    text = text.replace(' bôg ',' bông ')
    text = text.replace(' uốg ',' uống ')
    text = text.replace(' mìh ',' mình ')
    text = text.replace(' rat ',' rất ')
    text = text.replace('râdt','rất')
    text = text.replace('rata','rất')
    text = text.replace('dimớium','mới')
    text = text.replace(' nhuet65 ',' nhiệt ')
    text = text.replace(' mỳ ',' mì ')
    text = text.replace(' cmt ',' bình luận ')
    text = text.replace(' rv ',' nhận xét ')
    text = text.replace(' t ',' tao ')
    text = text.replace(' chea ',' chưa ')
    text = text.replace(' ngonn ',' ngon ')
    text = text.replace(' qay ',' quay ')
    text = text.replace(' faỉ ',' phải ')
    text = text.replace(' it ',' ít ')
    text = text.replace(' thàh ',' thành ')
    text = text.replace(' nnhaf ',' nhà ')
    text = text.replace(' nhiêud ',' nhiều ')
    text = text.replace('vọmg','vọng')
    text = text.replace(' nc ',' nước ')
    text = text.replace(' nuoc ',' nước ')
    text = text.replace(' nươc ',' nước ')
    text = text.replace(' ma91m ',' mắm ')
    text = text.replace(' muon1 ',' muốn ')
    text = text.replace(' muóin ',' muốn ')
    text = text.replace('deliverynow','')
    text = text.replace(' foody ',' ')
    text = text.replace(' grab ',' ')  
    text = text.replace(' baemin ',' ')    
    text = text.replace(' gojek ',' ')
    text = text.replace(' sale ',' ')
    text = text.replace(' fresh ',' sạch ')
    text = text.replace('tđộ','thái độ')
    text = text.replace('thái đô','thái độ')
    text = text.replace(' ún ',' uống ')
    text = text.replace(' ăm ',' ăn ')
    text = text.replace(' roàii ',' rồi ')
    text = text.replace(' đôg ',' đông ')
    text = text.replace(' cũg ',' cũng ')
    text = text.replace(' tơi ',' hơi ')
    text = text.replace(' mụt ',' một ')
    text = text.replace(' ok.',' được.')
    text = text.replace(' chut ',' chút ')
    text = text.replace('thíc hợp','thích hợp')
    text = text.replace('dêc thương','dễ thương')
    text = text.replace(' ai nă ',' ai ăn ')
    text = text.replace(' an vào lai ',' ăn vào lại ')
    text = text.replace(' an ngon ',' ăn ngon ')
    text = text.replace(' mọi nguoi ',' mọi người ')
    text = text.replace(' mieng thit ',' miếng thịt ')
    text = text.replace(' tranht hủ ',' tranh thủ ')
    text = text.replace(' mã km ',' mã khuyến mãi ')
    text = text.replace(' ơi kì ',' hơi kì ')
    text = text.replace(' nhà hàg ',' nhà hàng ')
    text = text.replace(' hợp lú ',' hợp lý ')
    text = text.replace(' lầm li ',' lầm lì ')
    text = text.replace(' fai bàn ',' phải bàn ')
    text = text.replace(' decor ',' trang trí ')
    text = text.replace(' decoration ',' trang trí ')
    text = text.replace(' lân chào ',' lần nào ')
    text = text.replace('thân thiệ','thân thiện')
    text = text.replace('delivery','')
    text = text.replace('amateur','nghiệp dư')
    text = text.replace('must try','phải thử')
    text = text.replace('must-try','phải thử')
    text = text.replace('gònnếu',' gòn nếu')
    text = text.replace('tíh $','tính tiền')
    text = text.replace('1 đi','một đi')
    text = text.replace(' món an ',' món ăn ')
    text = text.replace(' quá tặng ',' quán tặng ')
    text = text.replace('hợp lí','hợp lý')
    text = text.replace('phục vụ tê','phục vụ tệ')
    text = text.replace('k nhớ','không nhớ')
    text = text.replace('ko gian','không gian')
    text = text.replace('không gián','không gian')
    text = text.replace('chất lương','chất lượng')
    text = text.replace(' soeeu ngon ',' siêu ngon ')
    text = text.replace('tôn tiền','tốn tiền')
    text = text.replace('bé chỗ này','né chỗ này')
    text = text.replace('giá phải chăng','giá hợp lý')
    text = text.replace('giá cả phải chăng','giá cả hợp lý')
    text = text.replace('ngọn đẹp mắt','ngon đẹp mắt')
    text = text.replace('ko bao h','không bao giờ')
    text = text.replace(' kbây giờ ',' không bao giờ ')
    text = text.replace('#khôngbaogioquaylai','không bao giờ quay lại')
    text = text.replace('khongbaogioquaylai','không bao giờ quay lại')

    
    text = text.replace(r'(\w)\1*',r'\1') #thay thế những từ lặp đi lặp lại như wowwwww => wow
    text = text.replace(r'\b[kk]+\b',' tốt ') # ít nhất 2 chữ kk liên tục đổi thành tốt
    text = text.replace('[^a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]',' ')
    text = text.replace(' [a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]{1} ',' ')
    khong = [' khg ', ' k ',' ko ', ' k0 ', ' kog ', ' đéo ', ' đếch ', ' nỏ ', ' not ', ' kg ', ' khôg ' , ' hok ', ' hông ', ' kô ', ' chẳng ', ' chẳg ', ' khỏi ', ' kh ', ' hong ', ' doesn t ', ' don t ', ' khong ']
    for c in khong:
        text = text.replace(c,' không ')
    
    tot = [' gút ', ' good ', ' gud ', ' nice ', ' nicely ', ' perfect ', ' perfectly ']
    for c in tot:
        text = text.replace(c,' tốt ')
    
    dc = [' đc ', ' dc ', ' dk ', ' đk ', ' dx ', ' đx ',  ' duoc ',' okie ', ' okey ', ' ô kê ', ' oke ', ' okay ', 'ok', ' oki ']
    for c in dc:
        text = text.replace(c,' được ')
    
    thich = ['like', ' thik ', ' thix ', ' thjk ', ' thich ']
    for c in thich:
        text = text.replace(c,' thích ')
    
    bthg = [' bt ', ' bth ', ' bthg ']
    for c in bthg:
        text = text.replace(c,' bình thường ')
    
    ngon = [' mlem ', ' yummy ', ' nhon ', ' ngol ', ' delicious ', ' tasty ', ' wao ', ' wào ', ' wow ']
    for c in ngon:
        text = text.replace(c,' ngon ')
    
    order = [' book ', 'order', ' ord ', ' od ' , ' oder ']
    for c in order:
        text = text.replace(c,' đặt ')
    
    roi = [' r ', ' roi ', ' roài ', ' ròi ']
    for c in roi:
        text = text.replace(c,' rồi ')
    
    thanks = [' tks ', ' thanks ', ' thank ', ' tanks ', ' tk ']
    for c in thanks:
        text = text.replace(c,' cảm ơn ')
    
    biet = [' bik ', ' bík ', ' pjk ', ' pik ']
    for c in biet:
        text = text.replace(c,' biết ')
    
    minh = [' m ', ' mik ']
    for  c in minh:
        text = text.replace(c,' mình ')
    
    qua = [' qá ', ' wá ']
    for  c in qua:
        text = text.replace(c,' quá ')
    
    cuoi = [' ha ha ', ' haha ', ' he he ', ' hehe ', ' hi hi ', ' hihi ', ' hj hj ', ' hjhj ', ' hêh ', ' cười ', ' cheers ', ' hihi ']
    for  c in cuoi:
        text = text.replace(c,' cười ')
    
    te = [' shit ', ' cc ', ' sad ', ' poor ', ' worst ', ' disapointed ', ' tasteless ', ' disgusted ', ' bad ', ' fucking ']
    for  c in te:
        text = text.replace(c,' tệ ')
    
    dat = [' expensive ', ' mắc ', ' overpriced ', ' overpirced ']
    for  c in dat:
        text = text.replace(c,' đắt ')
    
    nv = [' nv ', ' nvien ', ' n.viên ']
    for c in nv:
        text = text.replace(c,' nhân viên ')
    
    cheap = [' cheap ', ' gẻ ', ' ghẻ ']
    for c in cheap:
        text = text.replace(c,' rẻ ')
    
    xs = [' fantastic ', ' excelent ', ' xúc xắc ', ' xuất sắccc ']
    for c in xs:
        text = text.replace(c,' xuất_sắc ')
    
    rude = [' impolite ', ' rude ', ' láo ', ' mất dạy ', ' hỗn xược ', ' thô lỗ ']
    for c in rude:
        text = text.replace(c,' bất lịch sự ')
    
    pv = [' pv ', ' pvu ']
    for c in pv:
        text = text.replace(c,' phục vụ ')
    
    cmt = [' cmmt ', ' cmt ', ' comment ']
    for c in cmt:
        text = text.replace(c,' bình luận ')
    
    truoc_day = [' trước kia ', ' trước đó ']
    for c in truoc_day:
        text = text.replace(c,' trước đây ')
        
    
    
    ### --- Đổi 15k, 75k,... thành 15000, 75000,....
    # Hàm thay thế để chuyển "k" thành "000" và chuyển chuỗi thành số nguyên
    def replace_with_thousands(match):
        return str(int(match.group(1)) * 1000)
    
    # Thay thế "k" bằng "000" và chuyển chuỗi thành số nguyên
    text = re.sub(r'(\d+)k', replace_with_thousands, text)
    
    
    
    # Biểu thức chính quy để bỏ các chữ cái kéo dài
    # Hàm thay thế để giữ lại chữ cái đầu tiên và loại bỏ các chữ cái kéo dài
    def remove_repeated_letters(match):
        return match.group(1)
    
    # Thay thế các chữ cái kéo dài bằng các chữ cái duy nhất
    text = re.sub(r'(\w)(\1{2,})', remove_repeated_letters, text)
    
    
    replace_list = {' ship ': ' giao hàng ', ' fody ': ' ứng dụng ',' tl ':' trả lời ',' r ':' rồi ','vs':'với','trể':'trễ','bh':'bây giờ',' ntn ':' như thế này ',
                     'ms':'mới', ' hnay ':' hôm nay ', 'mn':'mọi người', 'dậy':'vậy',' dzay ':' vậy ',' wa ':' qua ', ' zui ':' vui ',' kbh ':' không bao giờ ',
                     'nx':'nhận xét', ' dj ':' đi ', ' rùi ':' rồi ',' view ':' phong cảnh ','cx':'cũng',' kbiet ':' không biết ', ' review ':' nhận xét',
                    ' trc ':' trước ', ' bil ': ' hóa đơn', ' shiper ' : ' người vận chuyển ', 'shipper': 'người vận chuyển'  ,'check in': '', 'checkin':'',
                   'chick in':'', ' c ': ' chị ', ' t ': ' tôi ', ' a ':' anh ', ' j ': ' gì ', ' mún ': ' muốn ', ' ngag ': ' ngang ', ' ak ': ' à ',
                   ' complain ': ' phàn nàn ', ' free ': ' miễn phí ', ' free.': ' miễn phí.', ' phờ ri ': ' miễn phí ' ,' recommend ': ' đề xuất ', 
                    ' cùg ': ' cùng ', ' nhưg ': ' nhưng ', 'qua loa': 'sơ sài', 'xơ sài': 'sơ sài','sơ xài': 'sơ sài', ' never ': ' không bao giờ ',
                    ' service ': ' phục vụ ', 'vui vẽ': 'vui vẻ', ' <3 ': ' yêu ', 'nghĩ dưỡng': 'nghỉ dưỡng', 'trung bìng': 'trung bình', 
                    'bỗ duong': 'bổ dưỡng', 'đất mất': 'đẹp mắt', 'nice': 'tốt', ' soeeu đỉnh ': ' siêu đỉnh ', 'thân thiệnn': 'thân thiện',
                    'quay lại': 'trở lại', 'ghé lại': 'trở lại', 'thắc đắt': 'thắc mắc', ' củg ': ' củng ', ' take care ' : ' chăm sóc ',
                    'rất là': 'rất', 'quá là': 'quá', ' ròn ' : ' giòn ', 'welcome': 'chào đón', 'tiet kiem': 'tiết kiệm', ' siêu ': ' rất ',
                    ' cốc ': ' ly ', 'tí hon': 'nhỏ', ' kute ': ' dễ thương ', ' cute ': ' dễ thương ', ' best ': ' tuyệt vời ', 'very bad' : 'rất tệ',
                    'come back': 'trở lại', 'sang chảnh': 'sang trọng', 'không quá': 'bình thường', 'rất chất lượng': 'rất ngon', 'quá chất lượng': 'quá ngon',
                    'nogn': 'ngon', 'thạm tệ': 'thậm tệ', 'công túa': 'công chúa', 'không bị': 'không', 'không được': 'không', 'service': 'phục vụ', 'xức xắc': 'xuất sắc',
                    'super': 'rất', 'không thấy chán': 'không chán', 'không thấy ngon': 'không ngon', 'không thấy no': 'không no', 'không thấy ngán': 'không ngán',
                    'ngon cực kì': 'rất ngon', 'cực kì ngon': 'rất ngon', 'siêu ngon': 'rất ngon', 'cực dở': 'rất dở', 'siêu dở': 'rất dở', 'dở cực kì': 'rất dở',
                    'siêu chán': 'rất chán', 'cực chán': 'rất chán', 'ngon cực': 'rất ngon', 'cực kì tệ': 'rất tệ', 'cực tệ': 'rất tệ', 'cực ngon': 'rất ngon',
                    'không bao giờ': 'không', 'thiếu chuyên nghiệp': 'không chuyên nghiệp',
                    }
    
    for word, rep_word in replace_list.items():
      text = text.replace(word,rep_word)
    
    
    text = text.replace(r'(\s)\1*',r'\1') #thay thế những khoảng trắng lặp lại
    return text

#add columns review_class:
data['review_class'] = ['positive' if a >= 8 else 'negative' if a < 5 else 'neural' for a in data.ratings]
#label encoder:
data['review_class_num'] = [0 if x == 'positive'  else 1 if x == 'neural' else 2 for x in data.review_class]

##LOAD EMOJICON
file = open('data/files/emojicon.txt', 'r', encoding="utf8")
emoji_lst = file.read().split('\n')
emoji_dict = {}
for line in emoji_lst:
    key, value = line.split('\t')
    emoji_dict[key] = str(" "+value)
file.close()
#################
#LOAD TEENCODE
file = open('data/files/teencode.txt', 'r', encoding="utf8")
teen_lst = file.read().split('\n')
teen_dict = {}
for line in teen_lst:
    key, value = line.split('\t')
    teen_dict[key] = str(value)
file.close()
###############
#LOAD TRANSLATE ENGLISH -> VNMESE
file = open('data/files/english-vnmese.txt', 'r', encoding="utf8")
english_lst = file.read().split('\n')
english_dict = {}
for line in english_lst:
    key, value = line.split('\t')
    english_dict[key] = str(value)
file.close()
################
#LOAD wrong words
file = open('data/files/wrong-word.txt', 'r', encoding="utf8")
wrong_lst = file.read().split('\n')
file.close()
#################
#LOAD STOPWORDS
file = open('data/files/vietnamese-stopwords.txt', 'r', encoding="utf8")
stopwords_lst = file.read().split('\n')
file.close()

def process_text(text, emoji_dict, teen_dict, wrong_lst):
# def process_text(text, emoji_dict, teen_dict):
    document = text.lower()
    document = document.replace("’",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence =''
    for sentence in sent_tokenize(document):
        # if not(sentence.isascii()):
        ###### CONVERT EMOJICON
        sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))
        ###### CONVERT TEENCODE
        sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())
        ###### DEL Punctuation & Numbers
        pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
        sentence = ' '.join(regex.findall(pattern,sentence))
        ###### DEL wrong words   
        sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())
        ###### english words  
        # sentence = ' '.join(word if word not in dict_eng_vn.keys() else dict_eng_vn[word] for word in sentence.split())
        new_sentence = new_sentence+ sentence + '. '                    
    document = new_sentence  
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document

# Chuẩn hóa unicode tiếng việt
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
 
# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
def convert_unicode(txt):
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

# có thể bổ sung thêm các từ: chẳng, chả...
def process_special_word(text):
    new_text = ''
    text_lst = text.split()
    i= 0
    if 'không' in text_lst or 'rất' in text_lst or 'quá' in text_lst:
        while i <= len(text_lst) - 1:
            word = text_lst[i]
            #print(word)
            #print(i)
            if  word == 'không' or word == 'rất' or  word == 'quá':
                next_idx = i+1
                if next_idx <= len(text_lst) -1:
                    word = word +'_'+ text_lst[next_idx]
                i= next_idx + 1
            else:
                i = i+1
            new_text = new_text + word + ' '
    else:
        new_text = text
    return new_text.strip()

def process_postag_thesea(text):
    new_document = ''
    for sentence in sent_tokenize(text):
        sentence = sentence.replace('.','')
        ###### POS tag
        lst_word_type = ['A','AB','V','VB','VY','R', 'M', 'N', 'C']
        sentence = ' '.join( word[0] if word[1].upper() in lst_word_type else '' for word in pos_tag(process_special_word(word_tokenize(sentence, format="text"))))
        new_document = new_document + sentence + ' '
    ###### DEL excess blank space
    new_document = regex.sub(r'\s+', ' ', new_document).strip()
    return new_document

def remove_stopword(text, stopwords):

    ###### REMOVE stop words
    document = ' '.join('' if word in stopwords else word for word in text.split())
    #print(document)
    ###### DEL excess blank space
    document = re.sub(r'\s+', ' ', document).strip()
    return document

from sql_utils import save_to_database
df_new = pd.read_csv("Labeled_Foody_Review_from_model.csv")
df_new = df_new.dropna()

X_train, X_test, Y_train, Y_test = train_test_split(df_new['processed_comments'], df_new['review_class_num'], test_size=0.2)

model = joblib.load('model.joblib')
Y_pred = model.predict(X_test)

### Show kết quả lên Streamlit
menu = ["Giới thiệu"]
choice = st.sidebar.selectbox('Menu', menu)


st.subheader("Giới thiệu")
st.write("""
    Hệ thống phân loại các phản hồi của khách hàng thành 3 nhóm: tích cực, tiêu cực và trung lập. Dựa trên dữ liệu dạng văn bản.
    Xây dựng hệ thống dựa trên lịch sử những đánh giá của các khách hàng đã có trước đó, dữ liệu được thu thập từ phần bình luận và đánh giá của khách hàng ở trang Foody…
""")


with st.form("my_form"):
    st.write("""
    Mô hình hiện tại vẫn còn chưa thực sự hoàn thiện. Những bình luận của bạn sẽ là nguồn dữ liệu quý giá giúp cải thiện khả năng dự đoán.
    Cảm ơn rất nhiều!!!
""")
    st.write('#### Nhập bình luận của bạn')
    comment = st.text_input("Nhập bình luận: ")
    # review = st.selectbox("Bạn muốn: ", options = ["Bình luận tích cực", "Bình luận trung lập", "Bình luận tiêu cực"])
    submit = st.form_submit_button(label='Submit')

    if submit:  # Xử lý khi nhấn nút "Submit"
        # Thực hiện xử lý khi nhấn "Submit"
        if comment:
            text = comment
            document = replace_word(text)
            document = process_text(document, emoji_dict, teen_dict, wrong_lst)
            document = convert_unicode(document)
            document = process_postag_thesea(document)
            # document
            document = remove_stopword(document,stopwords_lst)
            
            yhat = model.predict([document])[0]
            if yhat== 0:
                label = "bình luận tích cực"
            elif yhat== 1:
                label = "bình luận trung tính"
            else:
                label = "bình luận tiêu cực"
            st.text("Kết quả: " + label)
            save_to_database(comment)
            # review = st.selectbox("Bạn muốn: ", options = ["Bình luận tích cực", "Bình luận trung lập", "Bình luận tiêu cực"])

        else:
            st.error("Vui lòng nhập bình luận để có thể dự đoán")



                
       
                