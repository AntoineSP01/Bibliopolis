from bs4 import BeautifulSoup
from word2number import w2n

import requests, csv, re

url = "https://books.toscrape.com/catalogue/soumission_998/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

with open('Python_Scrapping/information.csv', 'w', newline='', encoding='utf8') as fichier_csv:
    writter = csv.writer(fichier_csv)
    writter.writerow(['product_page_url', 'universal_product_code ', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    titre = soup.find('h1').text

    product_descritpion = soup.select('article.product_page > p')[0].text


    balise_ul = soup.find('ul', class_='breadcrumb')
    category = balise_ul.find_all('a')[2].text

    review_rating_text = soup.find('p', class_='star-rating')['class'][1]
    review_rating = w2n.word_to_num(review_rating_text)

    image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com') 

    print(titre, product_descritpion, category, review_rating, image_url)

    balise_table = soup.find('table')
    balise_tr = balise_table.find_all('tr')
    tableau_info = []

    for ligne in balise_tr:
        balise_th = ligne.find('th').text
        balise_td = ligne.find('td').text
        
        if balise_th == "UPC" or balise_th == "Price (incl. tax)" or balise_th == "Price (excl. tax)":
            tableau_info.append(balise_td)
        elif balise_th == "Availability":
            availability = re.search(r"\d+", balise_td).group()
            tableau_info.append(availability)
        else:
            pass  

    upc = tableau_info[0]
    price_incl_tax = tableau_info[1]
    price_excl_tax = tableau_info[2]
    availability = tableau_info[3]

    writter.writerow([url, upc, titre, price_incl_tax, price_excl_tax, availability, product_descritpion, category, review_rating, image_url])

