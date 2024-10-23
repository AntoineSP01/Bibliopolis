from bs4 import BeautifulSoup
from word2number import w2n

import requests, csv, re, os  

def download_image(img_url, titre, categorie_name):
    try :
        response = requests.get(img_url)
        titre =  re.sub(r'[<>:"/\|?*,]', '', titre)

        with open(f'images/{categorie_name}/{titre}.jpg', 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image: {e}")


def scrap_livre(url):
    try :
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        titre = soup.find('h1').text

        product_descritpion = soup.select('article.product_page > p')[0].text


        balise_ul = soup.find('ul', class_='breadcrumb')
        category = balise_ul.find_all('a')[2].text

        review_rating_text = soup.find('p', class_='star-rating')['class'][1]
        review_rating = w2n.word_to_num(review_rating_text)

        image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com') 
        download_image(image_url, titre, categorie_name)

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

    except Exception as e:
        print(f"Erreur : {e}")
    


if not os.path.exists('images'):
    os.makedirs('images')
else:
    for file in os.listdir('images'):
        os.remove(f'images/{file}')

if not os.path.exists('csv'):
    os.makedirs('csv')
else:
    for file in os.listdir('csv'):
        os.remove(f'csv/{file}')

url_main = "https://books.toscrape.com/"
response = requests.get(url_main)
soup = BeautifulSoup(response.content, 'html.parser')

categories = soup.find_all('ul', class_='nav nav-list')


for a in range(1, 51):
    categorie_name = categories[0].find_all('a')[a].text
    categorie_name = ''.join(e for e in categorie_name if e.isalnum())
    print(categorie_name)

    if not os.path.exists(f'images/{categorie_name}'):
        os.makedirs(f'images/{categorie_name}')
    else:
        for file in os.listdir(f'images/{categorie_name}'):
            os.remove(f'images/{categorie_name}{file}')

    with open(f'csv/{categorie_name}.csv', 'w', newline='', encoding='utf8') as fichier_csv:
        writter = csv.writer(fichier_csv)
        writter.writerow(['product_page_url', 'universal_product_code ', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    
        link = categories[0].find_all('a')[a]['href']  
        url_category = link.replace("/index.html", "").replace("catalogue/category/books/", "")
        n = 15
        for i in range(1, n):
            url = f"https://books.toscrape.com/catalogue/category/books/{url_category}/page-{i}.html"
            url_invalid = f"https://books.toscrape.com/catalogue/category/books/{url_category}/page-1.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            page_invalid = soup.find('h1').text
            
            if url == url_invalid and page_invalid == "404 Not Found":
                print(f"Page {i} : en cours de scrapping.")
                url = url.replace(f'page-{i}.html', 'index.html')

                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                url_livre = soup.find_all('h3')
                for livre in url_livre :
                    link = livre.find('a')
                    url = link['href'].replace('../../..', 'https://books.toscrape.com/catalogue')

                    scrap_livre(url)
                break

            elif page_invalid == "404 Not Found":
                break
            
            else :
                print(f"Page {i} : en cours de scrapping.")
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                page_invalid = soup.find('h1').text

                if page_invalid == "404 Not Found":
                    print("Page introuvable")
                else:
                    url_livre = soup.find_all('h3')
                    for livre in url_livre :
                        link = livre.find('a')
                        url = link['href'].replace('../../..', 'https://books.toscrape.com/catalogue')

                        scrap_livre(url) 
                i += 1 
    a += 1
        
    
        

print("Le scrapping est terminé")