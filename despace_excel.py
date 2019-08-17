import os
import traceback

import openpyxl
from typing import List

"""
Remove spaces from from the first names of people whose names are written in pinyin. Does not remove the space if it would be ambiguous without spaces (e.g., xi an). Also corrects capitalization of names. Goes through the Excel file in the current directory (.txt) Patient.xlsm, Insurance.xlsx, Checkup.xlsm, and Glasses.xlsx and outputs into _Patient.xlsx, etc.
"""

# Note that this list does not include 'a', 'e', 'o', and 'ei'
syllables = {'a', 'ai', 'an', 'ang', 'ao', 'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi', 'bian', 'biang', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu', 'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cei', 'cen', 'ceng', 'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo', 'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo', 'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng', 'di', 'dian', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo', 'e', 'ei', 'en', 'eng', 'er', 'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang', 'gao', 'ge', 'gei', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo', 'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng', 'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo', 'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun', 'ka', 'kai', 'kan', 'kang', 'kao', 'ke', 'kei', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun', 'kuo', 'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lia', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'lo', 'long', 'lou', 'lu', 'luan', 'lun', 'luo', 'lü', 'lüe', 'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng', 'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu', 'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng', 'ni', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu', 'nong', 'nou', 'nu', 'nuan', 'nuo', 'nü', 'nüe', 'o', 'ou', 'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen', 'peng', 'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu', 'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie', 'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun', 'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou', 'ru', 'rua', 'ruan', 'rui', 'run', 'ruo', 'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sen', 'seng', 'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo', 'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu', 'tuan', 'tui', 'tun', 'tuo', 'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu', 'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun', 'ya', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin', 'ying', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun', 'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng', 'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng', 'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo', 'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo' } | {'lv', 'lve', 'nv', 'nve', 'lyu', 'lyue', 'nyu', 'nyue' } - {'nyu', 'nyue', 'a', 'e', 'o', 'ei'}
syllables2 = syllables | {'a', 'e', 'o', 'ei'}
pinyin_surnames = syllables | {'aixinjueluo', 'ashina', 'baili', 'boerzhijin', 'chunyu', 'diwu', 'dongfang', 'dongge', 'dongguo', 'dongmen', 'duanmu', 'dugu', 'gongsun', 'gongyang', 'gongye', 'gongxi', 'guanqiu', 'guliang', 'helan', 'helian', 'hesheli', 'heruo', 'huangfu', 'huangsi', 'huyan', 'lanxiang', 'linghu', 'lufei', 'luli', 'luqiu', 'lyuqiu', 'lvqiu', 'moqi', 'murong', 'nalan', 'nangong', 'ouyang', 'shazha', 'shangguang', 'shentu', 'sima', 'situ', 'sikong', 'sikou', 'taishi', 'tantai', 'tuoba', 'wanyan', 'wenren', 'wuma', 'xiahou', 'xianyu', 'ximen', 'xuanyuan', 'yangzi', 'yelu', 'yelyu', 'yelv', 'yuezheng', 'yuchi', 'yuwen', 'zhangsun', 'zhongli', 'zhuge', 'zhurong', 'ziju', 'zuoren'}
ambiguous = {
    s1 + s2
    for s1 in syllables2 if s1[-1] in {'n', 'g', 'a', 'e', 'o'} and s1[:-1] in syllables2
    for s2 in syllables2 if s1[-1] + s2 in syllables2
}
# ambiguous = {'bingan', 'xianga', 'chengao', 'panan', 'chenang', 'cengan', 'xiangei', 'mingang', 'jina', 'dengai', 'shuanei', 'panai', 'shuanang', 'wangang', 'zenai', 'mangang', 'renai', 'runyu', 'zenyu', 'anou', 'xingei', 'binou', 'cenan', 'xianang', 'chanang', 'chanyu', 'gengao', 'tangai', 'zhunan', 'canyu', 'qinao', 'tunou', 'kengai', 'sangei', 'chene', 'mingai', 'qunei', 'binge', 'wanang', 'xingang', 'ninang', 'shuange', 'huanei', 'niangei', 'xinang', 'ninan', 'sanou', 'bina', 'shengan', 'kuna', 'kuanang', 'rengei', 'renang', 'mangao', 'manyue', 'shuanga', 'yanai', 'chenge', 'qiane', 'ningou', 'fangan', 'zhunao', 'zenga', 'dene', 'junan', 'xinai', 'kengao', 'mengai', 'xinga', 'junang', 'shenang', 'bangang', 'guane', 'zene', 'guanao', 'ninga', 'jiangang', 'shenan', 'nengou', 'huana', 'kenang', 'shuanan', 'jinai', 'kengou', 'hangai', 'zhuane', 'shana', 'qinang', 'yunao', 'rengang', 'denei', 'yangao', 'chengou', 'qinei', 'sana', 'genei', 'kanyue', 'genao', 'qingou', 'changou', 'kuanei', 'dianai', 'niangou', 'menei', 'fanai', 'qunyue', 'nenai', 'shengai', 'kengang', 'shunyue', 'xiangai', 'pane', 'zhuangao', 'qiangei', 'wangou', 'chuangou', 'rune', 'jingai', 'ange', 'cangao', 'pinou', 'chunai', 'yinou', 'qinyu', 'wengou', 'fana', 'kana', 'qianyu', 'pengao', 'tuna', 'renei', 'bangou', 'zunan', 'bingai', 'guangan', 'huangei', 'zengan', 'xianyue', 'xiane', 'ningei', 'huangao', 'cengang', 'zenan', 'panao', 'langang', 'yane', 'hene', 'nenge', 'yinga', 'binyu', 'denyue', 'liangai', 'jianao', 'gangao', 'liangan', 'shenge', 'huanga', 'qianga', 'chenei', 'nanyue', 'tanang', 'wanou', 'guange', 'pine', 'shuanai', 'shuanou', 'sanyu', 'huange', 'chuangan', 'genga', 'fanyue', 'kuanan', 'chenan', 'henga', 'pengou', 'kuangao', 'lianao', 'xiangao', 'cenyu', 'dengou', 'zhengou', 'gengan', 'dianyu', 'banai', 'denga', 'zhuanyu', 'hangou', 'denang', 'lanao', 'zhanei', 'tanai', 'zenou', 'changao', 'pingai', 'pangai', 'nangang', 'qiangou', 'ranga', 'zhuao', 'hangan', 'dengei', 'henan', 'guana', 'xianyu', 'hanang', 'chuangang', 'mange', 'gunei', 'bine', 'junou', 'panyu', 'fenge', 'fanga', 'xianei', 'dena', 'juna', 'guao', 'zhengang', 'line', 'jianyu', 'kanai', 'pangei', 'zanyue', 'kunai', 'shanyue', 'gangang', 'fengei', 'ningan', 'qina', 'yinyu', 'lunei', 'tangan', 'zunao', 'zhenyu', 'nenao', 'qunou', 'chuanga', 'xuna', 'huanan', 'ganang', 'cangou', 'mingei', 'zhanou', 'lianan', 'dana', 'genang', 'qingai', 'yune', 'kuanao', 'lunai', 'tunyu', 'yunei', 'sunyue', 'menyue', 'lingang', 'zhuanang', 'kuangan', 'kenge', 'xinyu', 'shanei', 'kanao', 'fengan', 'lianyu', 'kange', 'angai', 'cangang', 'nangou', 'xiange', 'zena', 'pana', 'panyue', 'danai', 'dangei', 'shunou', 'manyu', 'fanou', 'zunai', 'kunan', 'manou', 'zhangan', 'lunou', 'kangang', 'chanyue', 'zhanai', 'huanyu', 'gunao', 'zenang', 'qinyue', 'nanang', 'cunan', 'zhenai', 'dange', 'chengan', 'anei', 'lianei', 'pingan', 'manga', 'fangei', 'zangou', 'lianang', 'minyu', 'gengai', 'yunang', 'dune', 'dianei', 'pengang', 'mengan', 'dunyue', 'zhenga', 'wana', 'nenyue', 'kanei', 'ganao', 'zhunang', 'hange', 'hanou', 'shunan', 'xunei', 'genan', 'kangan', 'shanga', 'guanang', 'fangai', 'mene', 'zhangou', 'gengei', 'dunao', 'qiangan', 'bingang', 'xunyue', 'range', 'anyu', 'cengei', 'fengai', 'yinyue', 'dianao', 'nane', 'zhuangou', 'banan', 'pinai', 'qinan', 'qiange', 'bingao', 'kanyu', 'shangou', 'dunang', 'genyu', 'zhuanga', 'xinan', 'pengei', 'tangao', 'chane', 'chena', 'lingei', 'qiangai', 'wangan', 'langao', 'canan', 'wanyu', 'zange', 'rangan', 'chunang', 'zunei', 'angan', 'qunan', 'kuanyue', 'chana', 'guangang', 'lanan', 'zengai', 'zengei', 'guanyu', 'guangei', 'yina', 'guanyue', 'tunang', 'rengou', 'ningang', 'menyu', 'wanyue', 'yinai', 'kuangang', 'minao', 'manan', 'rangai', 'linge', 'lunyu', 'liana', 'jinyue', 'jiange', 'cenang', 'yanang', 'tanan', 'wanei', 'shuangei', 'changei', 'tunai', 'yangei', 'shenao', 'nenga', 'shangang', 'xiangou', 'zhane', 'sunei', 'liane', 'wanan', 'xingai', 'ganou', 'banang', 'zhuanao', 'binan', 'manai', 'jiangai', 'shuangan', 'changan', 'binyue', 'manao', 'cengou', 'jingang', 'mengang', 'fanan', 'angang', 'denou', 'kane', 'kuao', 'cunyue', 'cangei', 'hanei', 'xiao', 'ninou', 'jiangan', 'zangai', 'lana', 'kunyu', 'nangan', 'shunei', 'qinge', 'niangao', 'zhene', 'danang', 'xiangang', 'kunang', 'binai', 'lanyue', 'sunan', 'gunyue', 'mengao', 'guanou', 'danao', 'pina', 'langei', 'tanga', 'chenga', 'pangan', 'hanao', 'pingang', 'xunyu', 'dengang', 'cenai', 'changai', 'shunao', 'mane', 'jiane', 'niangai', 'linang', 'bangai', 'yunou', 'guanei', 'danyu', 'gunou', 'yingai', 'chunyu', 'ana', 'ningao', 'wanao', 'zhenge', 'zengao', 'kunao', 'shune', 'shengou', 'jiao', 'rangao', 'yanga', 'zenei', 'jinang', 'shangao', 'henou', 'anao', 'junyue', 'runan', 'kuana', 'shangai', 'yunyu', 'kengan', 'yinan', 'niangang', 'xianai', 'cunei', 'minang', 'shene', 'lane', 'ganei', 'yangan', 'yinge', 'zhuana', 'zhuanyue', 'qianou', 'hangang', 'tane', 'ningai', 'denao', 'yana', 'zenyue', 'chenao', 'genai', 'liangei', 'shangei', 'shenyue', 'nangei', 'sunang', 'kuangei', 'bangao', 'mangan', 'pinga', 'zuna', 'tunyue', 'kene', 'shuanao', 'zhunei', 'tune', 'zhanao', 'kanou', 'zenge', 'zhuna', 'shenei', 'tanou', 'hane', 'chune', 'chenyue', 'runai', 'shanyu', 'anan', 'wengan', 'genyue', 'runang', 'yanyue', 'menang', 'zhenan', 'lunyue', 'shangan', 'manang', 'zanan', 'xinyue', 'rengao', 'tangei', 'dangai', 'hunei', 'penge', 'denyu', 'guanai', 'fengao', 'lanou', 'cunai', 'pingei', 'zunou', 'pengai', 'hunao', 'nengai', 'guna', 'zhunou', 'pingao', 'dane', 'xinao', 'hanai', 'zanou', 'zhuanan', 'hunou', 'henao', 'jianang', 'henang', 'anyue', 'nanao', 'jiangei', 'xingou', 'binei', 'shuangou', 'menou', 'kenga', 'quna', 'liangou', 'xinou', 'kuange', 'dunei', 'menge', 'huanai', 'guanga', 'huangou', 'huna', 'cenyue', 'henyue', 'chanao', 'xiangan', 'lingou', 'wengai', 'banao', 'zanei', 'ninai', 'denan', 'canang', 'jianei', 'zanang', 'sunou', 'shuanyue', 'danga', 'dunan', 'bane', 'hunai', 'panga', 'dengao', 'dengan', 'canao', 'zhangei', 'chuangao', 'zengou', 'sangang', 'linao', 'yingang', 'linei', 'lianga', 'dangao', 'minou', 'ninao', 'rangei', 'sangan', 'nanyu', 'shengei', 'mangei', 'qinga', 'wangei', 'hengei', 'yanou', 'yingao', 'hunyue', 'gengang', 'cana', 'sangai', 'luna', 'hanan', 'renga', 'qinai', 'pange', 'guangou', 'shuangang', 'bingei', 'liange', 'zhunyu', 'cenao', 'zhenei', 'shunyu', 'chenou', 'dunai', 'zhuangei', 'gena', 'qianei', 'xinge', 'yinang', 'angao', 'anga', 'hena', 'kune', 'cenei', 'hanyue', 'jine', 'gunai', 'nena', 'zhunai', 'qingan', 'dianang', 'kenao', 'pangou', 'kenei', 'lingai', 'kenai', 'rangou', 'mangou', 'xianan', 'zhangang', 'liangao', 'hengang', 'bingou', 'chanan', 'gangou', 'linyue', 'wengei', 'renao', 'ninyue', 'huanao', 'guanan', 'huanou', 'rengai', 'cengao', 'zhenou', 'cune', 'cangan', 'kenan', 'runou', 'zhangai', 'nengei', 'yunai', 'qianao', 'zhuangai', 'zangao', 'nangao', 'shengao', 'binga', 'hengou', 'kanga', 'zangei', 'tana', 'zhuanei', 'zhana', 'nenyu', 'tanyu', 'rene', 'liao', 'cene', 'liangang', 'nine', 'qianan', 'huanang', 'jinga', 'xune', 'shanan', 'danou', 'zhuangan', 'zana', 'xianou', 'tunan', 'zhangao', 'wangao', 'nenang', 'huangan', 'shange', 'panang', 'kuane', 'lianou', 'canou', 'fanyu', 'yangou', 'pinyu', 'lingan', 'hunyu', 'shuna', 'hengai', 'kuanou', 'gene', 'pinan', 'mena', 'binang', 'bange', 'tanei', 'sunai', 'changa', 'yingei', 'sanei', 'pingou', 'wange', 'panou', 'jiangou', 'zhuange', 'banou', 'jinyu', 'banyu', 'ganga', 'qianai', 'qianyue', 'cengai', 'xunou', 'jinei', 'chenai', 'wenge', 'gunan', 'shenyu', 'diana', 'banei', 'mangai', 'mengei', 'huane', 'lanang', 'yine', 'minei', 'menan', 'jingei', 'chunei', 'sunyu', 'nanei', 'lingao', 'pinei', 'nanai', 'jingou', 'gunyu', 'sangao', 'danan', 'zhuanou', 'shenga', 'shenou', 'tanao', 'qunang', 'kangao', 'chunao', 'kuanai', 'pangao', 'kena', 'guangao', 'henai', 'lanyu', 'zunang', 'danyue', 'hunang', 'chenyu', 'chengai', 'sanyue', 'lina', 'menao', 'angei', 'shengang', 'nianga', 'fanang', 'jiangao', 'cange', 'sanan', 'menga', 'panei', 'kanang', 'tanyue', 'huangai', 'zhanyu', 'dunyu', 'qianang', 'yanan', 'ninge', 'fane', 'dianou', 'kuanga', 'chunan', 'chuna', 'dianyue', 'qiangang', 'zhuangang', 'jiana', 'sange', 'fengou', 'yingou', 'qingao', 'shunang', 'kengei', 'dangang', 'sanang', 'gangei', 'zhengao', 'qunai', 'renyu', 'ninei', 'zhanyue', 'mengou', 'denge', 'zanga', 'minga', 'tangang', 'fangao', 'henge', 'nana', 'langan', 'diane', 'pinao', 'ganyu', 'wane', 'bangei', 'xunai', 'zunyu', 'cunou', 'kanan', 'yingan', 'langou', 'nanou', 'junei', 'wengao', 'lunang', 'zhenang', 'banga', 'anang', 'qine', 'changang', 'guangai', 'jinge', 'xinei', 'shuangai', 'xunang', 'kunyue', 'sane', 'linou', 'zanyu', 'qiangao', 'kenou', 'cunao', 'cunang', 'mingan', 'jianan', 'jinan', 'rena', 'zhunyue', 'genge', 'gange', 'duna', 'chuange', 'yinao', 'gengou', 'kangei', 'cangai', 'mingao', 'junyu', 'genou', 'zenao', 'denai', 'dianan', 'minyue', 'zanai', 'kuangai', 'zunyue', 'cane', 'lanai', 'fange', 'qunyu', 'canei', 'pangang', 'mina', 'renyue', 'shanang', 'renge', 'shanao', 'kuangou', 'manei', 'hune', 'hunan', 'minge', 'zane', 'canai', 'pinang', 'zune', 'fangang', 'chengang', 'kunou', 'chanei', 'runao', 'chanai', 'langa', 'huangang', 'jinou', 'diao', 'linyu', 'nina', 'zanao', 'xunan', 'wangai', 'kenyue', 'zhange', 'fanao', 'sanga', 'zhanang', 'kunei', 'gune', 'kangou', 'pinge', 'tange', 'runei', 'rengan', 'qinou', 'xina', 'jingan', 'danei', 'tunei', 'jianai', 'niange', 'dangan', 'tunao', 'kuanyu', 'mana', 'chuangai', 'runa', 'jianou', 'sanao', 'huanyue', 'qune', 'banyue', 'yanei', 'hengao', 'jinao', 'zangang', 'qunao', 'wanga', 'sangou', 'wengang', 'bana', 'linai', 'nange', 'shuane', 'huao', 'yanao', 'qiao', 'angou', 'cena', 'canga', 'hangao', 'zhune', 'fangou', 'mine', 'shanou', 'change', 'xianao', 'junai', 'pinyue', 'sanai', 'june', 'jianyue', 'yunyue', 'binao', 'lune', 'qingang', 'canyue', 'minan', 'jianga', 'qiana', 'minai', 'lianai', 'gangai', 'ganai', 'nenou', 'hangei', 'shanai', 'cenou', 'tangou', 'ganyue', 'dangou', 'zhena', 'zhanan', 'hengan', 'fengang', 'zhanga', 'shena', 'zhenyue', 'runyue', 'nengan', 'suna', 'zhengai', 'zangan', 'yangai', 'bangan', 'ane', 'lange', 'xingan', 'nene', 'shenai', 'yanyu', 'nenan', 'yinei', 'shuanyu', 'linan', 'shuao', 'chengei', 'gangan', 'nengao', 'henei', 'sunao', 'zhuanai', 'rangang', 'pengan', 'xine', 'zhenao', 'chunou', 'nangai', 'anai', 'renan', 'mingou', 'dunou', 'yangang', 'zhengei', 'shane', 'cuna', 'linga', 'nengang', 'yuna', 'chunyue', 'shunai', 'zhengan', 'zengang', 'nanga', 'lianyue', 'xiana', 'menai', 'henyu', 'yange', 'cunyu', 'cenga', 'wenga', 'nenei', 'wanai', 'niangan', 'ninyu', 'chanou', 'fanei', 'hana', 'yunan', 'xunao', 'kangai', 'fenga', 'langai', 'jingao', 'chuangei', 'gana', 'shuangao', 'shuana', 'qingei', 'xingao', 'sune', 'lanei', 'junao', 'renou', 'hanyu', 'cenge', 'lunao', 'kenyu', 'gane', 'nanan', 'hanga', 'penga', 'lunan', 'ganan', 'gunang'}

def title_case(s: str) -> str:
    words = s.split(' ')
    new_words = [word.title() if word.isupper() else word.capitalize() for word in words]
    return ' '.join(new_words)


# Converts a 1-based column number to its letter
def colnum2str(n: int) -> str:
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def despace(filename: str):
    print('\nDespacing ' + filename + '...')
    wb = openpyxl.load_workbook(filename)
    sheet = wb.worksheets[0]
    col_indices = {cell.value: n + 1 for n, cell in enumerate(list(sheet.rows)[0])}
    first_name_col = colnum2str(col_indices['First Name'])
    last_name_col = colnum2str(col_indices['Last Name'])
    pinyin_name_count = 0

    for row in range(2, sheet.max_row + 1):
        row = str(row)
        try:
            last_name: str = sheet[last_name_col + row].value
            last_name_lower = last_name.lower()
            first_name: str = sheet[first_name_col + row].value
            first_name_lower = first_name.lower()
            first_name_words: List[str] = first_name_lower.split(' ')
        except AttributeError:
            print(f'Row {row} skipped due to an exception:')
            traceback.print_exc()
            continue

        if (last_name_lower.replace(' ', '') in pinyin_surnames and
                first_name_lower.replace(' ', '') not in syllables | ambiguous and
                first_name_words[0] in syllables | {'a'} and
                first_name_words[1] in syllables):
            pinyin_name_count += 1
            sheet[first_name_col + row] = title_case(first_name.replace(' ', ''))
        else:
            sheet[first_name_col + row] = title_case(first_name)
        sheet[last_name_col + row] = title_case(last_name)
    print(pinyin_name_count, 'unambiguous pinyin names in this table')
    wb.save(os.path.join(os.getcwd(), 'despaced_' + filename).replace('.xlsm', '.xlsx'))


if __name__ == '__main__':
    files = ['Patient.xlsm', 'Glasses.xlsx', 'Checkups.xlsm', 'Insurance.xlsx']
    for file in files:
        despace(file)
