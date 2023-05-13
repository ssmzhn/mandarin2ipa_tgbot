import json
from pypinyin import pinyin, Style
import re
tone_list = ["˥","˧˥","˨˩˦","˥˩",""]
ipa_table = json.load(open('ipa.json'))
select_table = ['拼音声调','2075北京话音系','UntPhesoca宽','UntPhesoca严','Standard Chinese (Beijing)','Standard Chinese (Beijing)严','胡裕树《现代汉语》','黄伯荣、廖序东《现代汉语》','钱乃荣《现代汉语》','吴宗济','赵元任《汉语口语语法》','《汉语方音字汇》']
def septone(syllable:str) -> tuple:
    tone = syllable[-1]
    return (syllable[:-1],int(syllable[-1]))

def mandarin2ipa(s:str,mode=2): #最好传单个字符
    if mode == 0:
        return pinyin(s,heteronym=True)
    converted = []
    pinyin_list = pinyin(s,heteronym=True,style=Style.TONE3,neutral_tone_with_five=True)
    for x in pinyin_list:
        if not re.match('^[A-Za-z]+[1-5]$',x[0]):
            converted.append(x)
            continue
        char_list = []
        for y in x:
            sep = septone(y)
            #print(sep)
            char_list.append(
                ipa_table[sep[0]][select_table[mode]]+tone_list[sep[1]-1]
            )
        converted.append(char_list)
    return converted
def converted2string(word,mode=2)->str:
    output = ''
    for x in word:
        output += x
        if mandarin2ipa(x)[0][0]==x:
            continue
        output+=' ('
        output += ' '.join(mandarin2ipa(x,mode=mode)[0])
        output +=') '
    return output

if __name__ == '__main__':
    print('欢迎使用普通话转IPA转换器')
    s = '我能吞下玻璃而不伤身体'
    for x,y in enumerate(select_table):
        text = converted2string(s,mode=2)
        print(y,text,'\n')
