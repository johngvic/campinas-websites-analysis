import re, urllib.request, random, time
from bs4 import BeautifulSoup
from openpyxl import Workbook
from Sheet import Sheet
from Score import Score
from Enhance import Enhance

list_urls      = open('scripts\general-urls.txt')
list_keywords  = open('scripts\keywords.txt', encoding='UTF-8').read().splitlines()
forbidden_file = open('forbidden-urls.txt', 'a')
iterator       = 0
url_number     = 0
max_scrape     = 0
occurrences    = 0
row            = 2

en        = Enhance()
sc        = Score()
obj_sheet = Workbook()
sheet     = obj_sheet.active
ns        = Sheet('Planilha de Ocorrencias', 'sheet', obj_sheet, sheet)
ns.set_header1()
ns.save_sheet()

for url in list_urls:

    # if iterator >= max_scrape:
    #     break

    if en.set_delay(url):
        delay = random.randint(0, 13)
        print('Delay: ' + str(delay))
        time.sleep(delay)

    print('Sheet: {} | N: {} | URL: {}'.format(iterator + 1, url_number + 1, url))
    boolean = False

    try:
        answer      = urllib.request.urlopen(url, timeout=5)
        http_info   = answer.info()
        contenttype = http_info.get_content_type()

        if contenttype == 'text/html':
            html = answer.read()
            soup = BeautifulSoup(html,'html.parser') if url.find('cpat') != -1 else BeautifulSoup(html,'lxml')
            enhanced_soup = en.clear_html(soup)
            string = enhanced_soup.get_text(" ")
            occurrences = 0
            boolean = True
            sc.clear_elements()
            aux_placeholder = re.findall('placeholder', str(soup), re.I)

            for word in list_keywords:
                lista = re.findall(r'\W' + word + r'\W', string, re.IGNORECASE)
                list_placeholder = []

                if len(aux_placeholder) > 0:
                    list_placeholder = re.findall(r'placeholder="[a-zA-Z0-9 -áàâãéèêíóôõúç]*' + r'\W' + word + r'\W', str(soup), re.I)
                
                if len(lista) > 0 or len(list_placeholder) > 0:
                    occurrences = len(lista) + len(list_placeholder)
                    sc.set_dictionary(word, occurrences)

            multiply = sc.calculate_score_list() * sc.calculate_score_dictionary()

            ns.readable_page1(row, url, contenttype, sc.keywords_string_curtailed(), sc.calculate_score_list(), sc.calculate_score_dictionary(), multiply, sc.calculate_by_severity(), sc.calculate_weighted_avg(), sc.calculate_by_simultaneity())

            ns.save_sheet()
    except urllib.error.URLError as e:
        forbidden_file.write(str(e) + ' | ' + url)
    except urllib.error.HTTPError as e:    
        forbidden_file.write(str(e) + ' | ' + url)
    except Exception as e:        
        forbidden_file.write(str(e) + ' | ' + url)
    
    if boolean:
        iterator += 1
        row      += 1
    
    url_number += 1

list_urls.close()
forbidden_file.close()