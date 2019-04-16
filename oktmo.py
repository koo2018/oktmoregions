from urllib.request import urlopen
import re, json
from bs4 import BeautifulSoup


def getGeo(urlIn,fileOut):

    link_list = list()
    reg_dict = dict()

    with urlopen(urlIn) as connect:

        html = connect.read().decode('windows-1251') # да, этот сайт на windows-1251
    
    print('ULR:',urlIn)

    links = re.findall('"((http|ftp)s?://.*?)"', html)

    for link in links:

        if 'municipality_registry' in link[0] or 'locality_registry' in link[0]:
    
            link_list.append(link[0])
        
    print('Найдено мест:',len(link_list))

    for link in link_list:

        with urlopen(link) as connect:

            html = connect.read().decode('windows-1251')

        print('Просмотр:',link)
    
        soup = BeautifulSoup(html,'html.parser')
    
        p_list = soup.select('p')
    
        for p in p_list:
        
            if re.search('\d{8,}',p.decode()):
        
                reg = re.split('\.', p.text,1)
            
                reg_dict[reg[0]]=reg[1].strip()

    print('Всего муниципалитетов:', len(reg_dict))

    with open(mreg, "w", encoding='utf8') as f:

            f.write(json.dumps(reg_dict, ensure_ascii=False, indent=4))
        
    print('Сфоримирован файл', mreg)


url = 'http://www.oktmo.ru/municipality_registry/'
mreg = "mreg.json"

getGeo(url,mreg)


url = 'http://www.oktmo.ru/locality_registry/'
mreg = "stlmts.json"

getGeo(url,mreg)
