import pandas
import csv
from typing import List

"""
Remove spaces from from the first names of people whose names are written in pinyin. Does not remove the space if it would be ambiguous without spaces (e.g., xi an). Goes through the TSV files (.txt) Patient.txt, Insurance.txt, Checkup.txt, and Glasses.txt and outputs into _Patient.txt, etc.
"""

# Note that this list does not include 'a', 'e', 'o', and 'ei'
syllables = {'ba', 'pa', 'ma', 'fa', 'da', 'ta', 'na', 'la', 'ga', 'ka', 'ha', 'zha', 'cha', 'sha', 'za', 'ca', 'sa', 'ai', 'bai', 'pai', 'mai', 'dai', 'tai', 'nai', 'lai', 'gai', 'kai', 'hai', 'zhai', 'chai', 'shai', 'zai', 'cai', 'sai', 'an', 'ban', 'pan', 'man', 'fan', 'dan', 'tan', 'nan', 'lan', 'gan', 'kan', 'han', 'zhan', 'chan', 'shan', 'ran', 'zan', 'can', 'san', 'ang', 'bang', 'pang', 'mang', 'fang', 'dang', 'tang', 'nang', 'lang', 'gang', 'kang', 'hang', 'zhang', 'chang', 'shang', 'rang', 'zang', 'cang', 'sang', 'ao', 'bao', 'pao', 'mao', 'dao', 'tao', 'nao', 'lao', 'gao', 'kao', 'hao', 'zhao', 'chao', 'shao', 'rao', 'zao', 'cao', 'sao', 'me', 'de', 'te', 'ne', 'le', 'ge', 'ke', 'he', 'zhe', 'che', 'she', 're', 'ze', 'ce', 'se', 'bei', 'pei', 'mei', 'fei', 'dei', 'nei', 'lei', 'gei', 'hei', 'shei', 'zei', 'beng', 'peng', 'meng', 'feng', 'deng', 'teng', 'neng', 'leng', 'geng', 'keng', 'heng', 'zheng', 'cheng', 'sheng', 'reng', 'zeng', 'ceng', 'seng', 'er', 'yi', 'bi', 'pi', 'mi', 'di', 'ti', 'ni', 'li', 'ji', 'qi', 'xi', 'zhi', 'chi', 'shi', 'ri', 'zi', 'ci', 'si', 'ya', 'dia', 'lia', 'jia', 'qia', 'xia', 'yan', 'bian', 'pian', 'mian', 'dian', 'tian', 'nian', 'lian', 'jian', 'qian', 'xian', 'yang', 'niang', 'liang', 'jiang', 'qiang', 'xiang', 'yao', 'biao', 'piao', 'miao', 'diao', 'tiao', 'niao', 'liao', 'jiao', 'qiao', 'xiao', 'ye', 'bie', 'pie', 'mie', 'die', 'tie', 'nie', 'lie', 'jie', 'qie', 'xie', 'yin', 'bin', 'pin', 'min', 'nin', 'lin', 'jin', 'qin', 'xin', 'ying', 'bing', 'ping', 'ming', 'ding', 'ting', 'ning', 'ling', 'jing', 'qing', 'xing', 'yo', 'yong', 'jiong', 'qiong', 'xiong', 'you', 'miu', 'diu', 'niu', 'liu', 'jiu', 'qiu', 'xiu', 'bo', 'po', 'mo', 'fo', 'lo', 'weng', 'dong', 'tong', 'nong', 'long', 'gong', 'kong', 'hong', 'zhong', 'chong', 'rong', 'zong', 'cong', 'song', 'ou', 'pou', 'mou', 'fou', 'dou', 'tou', 'nou', 'lou', 'gou', 'kou', 'hou', 'zhou', 'chou', 'shou', 'rou', 'zou', 'cou', 'sou', 'wu', 'bu', 'pu', 'mu', 'fu', 'du', 'tu', 'nu', 'lu', 'gu', 'ku', 'hu', 'zhu', 'chu', 'shu', 'ru', 'zu', 'cu', 'su', 'wa', 'gua', 'kua', 'hua', 'zhua', 'shua', 'wai', 'guai', 'kuai', 'huai', 'chuai', 'shuai', 'wan', 'duan', 'tuan', 'nuan', 'luan', 'guan', 'kuan', 'huan', 'zhuan', 'chuan', 'shuan', 'ruan', 'zuan', 'cuan', 'suan', 'wang', 'guang', 'kuang', 'huang', 'zhuang', 'chuang', 'shuang', 'yue', 'nve', 'nyue', 'lve', 'lyue', 'jue', 'que', 'xue', 'wei', 'dui', 'tui', 'gui', 'kui', 'hui', 'zhui', 'chui', 'shui', 'rui', 'zui', 'cui', 'sui', 'wen', 'dun', 'tun', 'lun', 'gun', 'kun', 'hun', 'zhun', 'chun', 'shun', 'run', 'zun', 'cun', 'sun', 'wo', 'duo', 'tuo', 'nuo', 'luo', 'guo', 'kuo', 'huo', 'zhuo', 'chuo', 'shuo', 'ruo', 'zuo', 'cuo', 'suo', 'yu', 'nv', 'nyu', 'lv', 'lyu', 'ju', 'qu', 'xu', 'yuan', 'juan', 'quan', 'xuan', 'yun', 'jun', 'qun', 'xun'}
syllables2 = syllables | {'a', 'e', 'o', 'ei'}
pinyin_surnames = syllables | {'aixinjueluo', 'ashina', 'baili', 'boerzhijin', 'chunyu', 'diwu', 'dongfang', 'dongge', 'dongguo', 'dongmen', 'duanmu', 'dugu', 'gongsun', 'gongyang', 'gongye', 'gongxi', 'guanqiu', 'guliang', 'helan', 'helian', 'hesheli', 'heruo', 'huangfu', 'huangsi', 'huyan', 'lanxiang', 'linghu', 'lufei', 'luli', 'luqiu', 'lyuqiu', 'lvqiu', 'moqi', 'murong', 'nalan', 'nangong', 'ouyang', 'shazha', 'shangguang', 'shentu', 'sima', 'situ', 'sikong', 'sikou', 'taishi', 'tantai', 'tuoba', 'wanyan', 'wenren', 'wuma', 'xiahou', 'xianyu', 'ximen', 'xuanyuan', 'yangzi', 'yelu', 'yelyu', 'yelv', 'yuezheng', 'yuchi', 'yuwen', 'zhangsun', 'zhongli', 'zhuge', 'zhurong', 'ziju', 'zuoren'}
# ambiguous = {
#     s1 + s2
#     for s1 in syllables2 if s1[-1] in { 'n', 'g', 'a', 'e', 'o' } and s1[:-1] in syllables2
#     for s2 in syllables2 if s1[-1] + s2 in syllables2
# }
ambiguous = { 'sangao', 'shuanao', 'xianei', 'wanan', 'zunang', 'mingan', 'cunyue', 'qianou', 'huanei', 'yanao', 'yanei', 'binyue', 'pana', 'huanai', 'fanai', 'rangang', 'xianai', 'binao', 'huangan', 'zane', 'lunai', 'langou', 'pangao', 'lianang', 'dianai', 'pingei', 'jiao', 'zhuanai', 'lunei', 'sunei', 'juna', 'qunai', 'guane', 'mana', 'ranga', 'pine', 'zhuangang', 'kuao', 'hunao', 'sangang', 'bangang', 'wane', 'pangou', 'linga', 'xunei', 'hunai', 'zhanyu', 'niange', 'qinan', 'wengan', 'mangou', 'tangai', 'shunyue', 'tangang', 'anan', 'cane', 'niangang', 'qinai', 'chune', 'minou', 'jiangao', 'gange', 'diana', 'lunyu', 'bangou', 'bane', 'huanou', 'zanai', 'guangei', 'qunang', 'huangang', 'hangan', 'gane', 'cunao', 'wanyu', 'guangai', 'xiangan', 'xiangai', 'nangei', 'angei', 'pangei', 'chunei', 'liangei', 'hunan', 'fangao', 'chuna', 'zunou', 'shanei', 'xianang', 'gunang', 'luna', 'kana', 'gune', 'huna', 'xinga', 'jiana', 'jinan', 'guangao', 'gangai', 'huanao', 'pinge', 'xingang', 'shuangan', 'ganang', 'lanei', 'kuana', 'yingao', 'xinang', 'huange', 'sunyue', 'sanao', 'wangang', 'langao', 'bingai', 'changao', 'banei', 'kuangan', 'yingei', 'ningei', 'angan', 'qinga', 'kuanao', 'dianei', 'pangang', 'pinei', 'dane', 'sanan', 'kangao', 'panyue', 'ninge', 'nangan', 'yangang', 'junai', 'xunan', 'xiangao', 'xinou', 'angao', 'kuangou', 'niangai', 'kunang', 'liangai', 'anyu', 'shanao', 'dianyue', 'wanang', 'tunou', 'sanyu', 'zhane', 'binge', 'zhangang', 'minan', 'canga', 'ganao', 'jianai', 'qunei', 'canang', 'mane', 'zanei', 'xiao', 'wangei', 'mingei', 'danyue', 'changa', 'gana', 'linang', 'zhanan', 'tanga', 'guanyue', 'yunyue', 'junou', 'kuangei', 'yanyu', 'xiane', 'wanai', 'tune', 'diao', 'qinge', 'tana', 'qiangei', 'mangai', 'banai', 'pingou', 'kanyu', 'jiangou', 'nanao', 'mingai', 'xingei', 'xinyue', 'tangan', 'yingai', 'guanai', 'zhanou', 'linyu', 'anyue', 'angou', 'anei', 'gangei', 'banou', 'xiangang', 'danyu', 'langang', 'shuao', 'xinyu', 'fangou', 'manei', 'changai', 'cangao', 'nanai', 'nangou', 'yangao', 'pingan', 'yangai', 'kune', 'wangai', 'mina', 'zhunyu', 'sunou', 'manyue', 'tange', 'qingei', 'changan', 'change', 'zhangei', 'lingang', 'jianyue', 'guangou', 'zhuanyue', 'kunai', 'zhunan', 'xunyue', 'jingou', 'hanyue', 'lanang', 'liana', 'runan', 'suna', 'gangao', 'shanyu', 'huanga', 'junan', 'guanga', 'shangou', 'xingou', 'lanyue', 'nanyu', 'qune', 'chuanga', 'xinge', 'runao', 'pinai', 'lianyue', 'mingang', 'hunyu', 'ana', 'yanga', 'cangang', 'jianang', 'nangai', 'gunan', 'tanou', 'zhuanao', 'xinai', 'huangou', 'lianao', 'zhuanou', 'yune', 'tunai', 'ninou', 'manan', 'yunao', 'yinou', 'nine', 'pinou', 'dangai', 'sangou', 'pinyue', 'jiane', 'mange', 'kuangao', 'lunyue', 'qiangao', 'dunai', 'canai', 'chanei', 'lane', 'tunyu', 'yinao', 'linei', 'mine', 'wangou', 'banao', 'chuange', 'danga', 'banang', 'bingou', 'pinang', 'shuanyue', 'zhuange', 'zangan', 'gangou', 'jingan', 'banyue', 'zhuangei', 'pingai', 'niangao', 'sanga', 'yinang', 'hangou', 'tunao', 'sangan', 'zanyu', 'jinyue', 'qianei', 'lana', 'tunan', 'tunang', 'dangao', 'jinang', 'zhanao', 'xingai', 'tanao', 'canyue', 'lianyu', 'shuanan', 'wangan', 'kuanou', 'sanou', 'zunao', 'jianan', 'zhunou', 'lanou', 'rangao', 'zunei', 'fane', 'lunan', 'niangei', 'mingou', 'gunei', 'angang', 'qunyue', 'guanou', 'guna', 'shunou', 'zunyu', 'ningao', 'minao', 'guanan', 'niangan', 'hanan', 'fanei', 'fanao', 'qingan', 'huanyue', 'huangao', 'lunang', 'panang', 'hanga', 'wengao', 'tanan', 'chanyu', 'lanao', 'qine', 'shunei', 'ningou', 'mingao', 'sanai', 'nangang', 'lange', 'cangan', 'yanou', 'zangai', 'binou', 'shunai', 'chunan', 'zhanyue', 'kuanan', 'chunyu', 'kanou', 'chanai', 'hangang', 'rangei', 'kuanyue', 'jinao', 'bingan', 'fangei', 'xina', 'mangang', 'yinai', 'sunai', 'kanan', 'fangang', 'bangao', 'wenga', 'yinei', 'lunao', 'runei', 'shuangao', 'shuangou', 'dianang', 'hange', 'sana', 'yunan', 'guanao', 'sane', 'ganga', 'pangai', 'nanan', 'shunyu', 'sunao', 'manga', 'sange', 'nanou', 'hanai', 'cange', 'runai', 'nane', 'chuangang', 'xiangou', 'jiange', 'yinan', 'lianou', 'nana', 'jianou', 'qiangang', 'wanga', 'qinyu', 'chuangao', 'dangei', 'zanao', 'yanai', 'quna', 'cangou', 'zangei', 'chuangai', 'chuangei', 'lianei', 'fanang', 'zangang', 'pange', 'zangou', 'jinei', 'hana', 'yunou', 'changei', 'sunang', 'binei', 'zuna', 'yangei', 'chana', 'pinao', 'zhuangai', 'yanan', 'hunyue', 'canei', 'gunyue', 'qianyu', 'kuanai', 'gangang', 'kane', 'qiangai', 'jina', 'tunei', 'ninyu', 'shuangang', 'zange', 'jinai', 'dana', 'yina', 'dange', 'huao', 'zunyue', 'shanga', 'pingang', 'yange', 'linai', 'qiangou', 'xingao', 'qunan', 'cunai', 'guanang', 'wenge', 'binai', 'zhuane', 'qinao', 'ganou', 'ninai', 'zhuangan', 'yana', 'chanao', 'kangou', 'anga', 'fangai', 'qiane', 'manai', 'chuangan', 'dianao', 'kangang', 'qianyue', 'shuana', 'kangai', 'kuangang', 'kunyu', 'dangang', 'hunei', 'jianga', 'hane', 'yinyu', 'nina', 'chanyue', 'jinge', 'runang', 'panou', 'zangao', 'sanang', 'dangan', 'xianyu', 'qunou', 'dianou', 'shanai', 'danang', 'chanan', 'chunou', 'fanga', 'junei', 'yine', 'qianai', 'panei', 'shunang', 'qianang', 'junyue', 'dianan', 'ganan', 'kange', 'tanang', 'binga', 'liangou', 'kunou', 'dunei', 'lingei', 'zhangao', 'yangou', 'ganai', 'minai', 'runa', 'fange', 'bangei', 'zhunao', 'bange', 'qunao', 'pinan', 'shunan', 'shune', 'chuangou', 'xinei', 'jine', 'cangai', 'canyu', 'pina', 'lianan', 'tuna', 'jianyu', 'jingao', 'dunou', 'liangan', 'langei', 'qiange', 'xinao', 'rangou', 'nanei', 'ninga', 'dunao', 'hanang', 'minge', 'dunan', 'pangan', 'tanyue', 'zhunai', 'ninao', 'ninan', 'nianga', 'anao', 'dune', 'xunyu', 'xunao', 'hangao', 'shuange', 'chunai', 'danao', 'bangan', 'kanyue', 'qiangan', 'sanyue', 'ganei', 'xiange', 'qianga', 'zune', 'zhuanan', 'tunyue', 'shuanai', 'qingao', 'tangei', 'qiao', 'rangan', 'fangan', 'yingan', 'cunou', 'xuna', 'ganyu', 'wange', 'wengou', 'fanyu', 'qinang', 'huanang', 'shunao', 'zhuanei', 'qianan', 'kanei', 'minyu', 'pinga', 'kuanyu', 'hanei', 'shuangai', 'panai', 'qingang', 'rangai', 'guangang', 'wengai', 'cunang', 'tane', 'jingai', 'xianyue', 'zhuna', 'nangao', 'huane', 'sangei', 'zhange', 'wangao', 'lianga', 'chunyue', 'dangou', 'zhuangou', 'binyu', 'kunan', 'anang', 'guao', 'yane', 'qinyue', 'kunei', 'hunou', 'zhuanga', 'fanan', 'manyu', 'zanga', 'zanou', 'qiana', 'cunei', 'xunang', 'linou', 'junyu', 'shuane', 'hune', 'runou', 'dunang', 'minang', 'shane', 'huangai', 'yunyu', 'jianao', 'tanai', 'ningai', 'hangai', 'guange', 'ninei', 'shangei', 'kanao', 'xunai', 'lanan', 'lina', 'shanyue', 'bana', 'lingao', 'zhuanyu', 'langan', 'kuanang', 'kunyue', 'xiana', 'manang', 'shanan', 'xianga', 'ange', 'xingan', 'xianan', 'kangan', 'junao', 'zhuao', 'xianou', 'panao', 'yingou', 'linao', 'wengei', 'jinga', 'anai', 'duna', 'nanang', 'qinei', 'chunao', 'chanang', 'xunou', 'pingao', 'canan', 'dianyu', 'nanga', 'xiangei', 'jingei', 'angai', 'lingai', 'jiangai', 'panyu', 'niangou', 'jiangei', 'kuanga', 'guana', 'lunou', 'huangei', 'lingou', 'nanyue', 'canao', 'canou', 'kuanei', 'zunai', 'tangou', 'gunyu', 'line', 'kunao', 'shuanang', 'wanou', 'mangao', 'mangei', 'langa', 'shuangei', 'danan', 'kanang', 'guangan', 'kanai', 'linge', 'huanan', 'rune', 'tanei', 'yinge', 'danou', 'zhanei', 'kanga', 'yinyue', 'yunang', 'shana', 'bina', 'jinyu', 'liane', 'xinan', 'gangan', 'panan', 'ninyue', 'shanang', 'june', 'minei', 'diane', 'bingao', 'shuanyu', 'junang', 'fanyue', 'yangan', 'gunai', 'zhanang', 'huanyu', 'chane', 'jianei', 'wanao', 'sunan', 'lanai', 'qianao', 'shangang', 'fana', 'chunang', 'zanyue', 'runyu', 'qunyu', 'shangan', 'yanyue', 'yunei', 'xine', 'zhangou', 'zunan', 'cune', 'shange', 'zhunang', 'pinyu', 'qingai', 'yingang', 'jinou', 'banyu', 'ninang', 'hangei', 'runyue', 'guanei', 'lingan', 'ningan', 'liange', 'linyue', 'hunang', 'dunyue', 'tangao', 'hanao', 'shuna', 'langai', 'ningang', 'zhunyue', 'zhune', 'wanyue', 'danai', 'anou', 'zana', 'manao', 'zhangan', 'bingei', 'zhuanang', 'zhana', 'mangan', 'zanang', 'minyue', 'cana', 'yinga', 'sunyu', 'yanang', 'wana', 'kangei', 'sune', 'lanyu', 'lune', 'jiangang', 'pane', 'guanyu', 'changang', 'binan', 'kuna', 'sanei', 'lianai', 'shuanei', 'binang', 'range', 'zhuangao', 'fanou', 'jingang', 'bine', 'zhunei', 'cunan', 'liangao', 'shuanou', 'linan', 'shangai', 'wengang', 'cuna', 'kuange', 'kuane', 'xianao', 'tanyu', 'zanan', 'qina', 'panga', 'hanou', 'dunyu', 'nange', 'yunai', 'yuna', 'gunou', 'gunao', 'wanei', 'ane', 'huana', 'bingang', 'liangang', 'shanou', 'liao', 'banan', 'shuanga', 'zhuana', 'chanou', 'ganyue', 'hanyu', 'banga', 'manou', 'zhanai', 'kuangai', 'xune', 'zhanga', 'shangao', 'changou', 'qinou', 'cangei', 'jiangan', 'zhangai', 'bangai', 'qingou', 'cunyu', 'sangai', 'danei', 'minga' }

for filename in ['Checkups.txt', 'Glasses.txt', 'Insurance.txt', 'Patient.txt']:
    print('Currently parsing ' + filename)
    df = pandas.read_csv(filename, sep='\t', header=0)
    for i, row in df.iterrows():
        last_name: str = str(row['Last Name']).lower()
        first_name: str = str(row['First Name']).lower()
        first_name_words: List[str] = first_name.split(' ')

        if (last_name.replace(' ', '') in pinyin_surnames and
                first_name.replace(' ', '') not in (syllables | ambiguous) and
                first_name_words[0] in syllables and
                first_name_words[1] in syllables):
            df.at[i, 'First Name'] = first_name.replace(' ', '')

    df.to_csv('_' + filename, sep='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
