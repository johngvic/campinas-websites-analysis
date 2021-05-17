class Enhance:

    def clear_html(self, soup):
        if soup.find('div', 'footer') != None:
            soup.find('div', 'footer').clear()

        if soup.find('div', id='copyright2') != None:
            soup.find('div', id='copyright2').clear()
            
        if soup.find('div', 'form-item form-item-email') != None:
            soup.find('div', 'form-item form-item-email').clear()

        if soup.find('section', id='alliedMaterialsArea') != None:
            soup.find('section', id='alliedMaterialsArea').clear()

        if soup.find(style="border-bottom:none; margin-bottom:0;") != None:
            for element in soup.find_all(style="border-bottom:none; margin-bottom:0;"):
                element.replace_with('')

        return soup

    def set_delay(self, url):    
        string = str(url).lower()

        if string.find('arq-camp') != -1:
            return True
        else:
            return False