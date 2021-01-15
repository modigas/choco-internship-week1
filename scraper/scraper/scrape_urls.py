import re
# Urls of the stores to be scraped
MECHTA_URLS = ['https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&page_num=1&catalog=true&page_element_count=18',
               'https://www.mechta.kz/api/main/catalog_new/index.php?section=smartfony&page_num=1&catalog=true&page_element_count=18',
               'https://www.mechta.kz/api/main/catalog_new/index.php?section=processor&page_num=1&catalog=true&page_element_count=18',
               'https://www.mechta.kz/api/main/catalog_new/index.php?section=videokarta&page_num=1&catalog=true&page_element_count=18']

SHOPWW_URLS = ['https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
               'https://shop.kz/videokarty/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
               'https://shop.kz/noutbuki/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
               'https://shop.kz/protsessory/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/']

TECHNO_URLS = []

SULPAK_URLS = ['https://www.sulpak.kz/f/smartfoniy/nur_sultan',
               'https://www.sulpak.kz/f/noutbuki/nur_sultan',
               'https://www.sulpak.kz/f/videokartiy/nur_sultan',
               'https://www.sulpak.kz/f/processoriy/nur_sultan']

def strPriceToNum(price):
    res = ''
    if type(price) == str:
        for el in re.findall(r'\d+', price):
            res += el
        try:
            num = int(res)
        except:
            num = 0
        return num
    else:
        return 0