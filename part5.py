import matplotlib.pyplot as plt
import csv
import os

def get_average_price_by_category(csv_directory='csv'):
    """
    Crée un dictionnaire avec les catégories, le nombre de livres par catégorie, 
    et la moyenne des prix des livres présents dans chaque catégorie.
    """
    number_books_by_category = {}
    total_price_by_category = {}

    
    if not os.path.exists(csv_directory):
        print(f"Le répertoire {csv_directory} n'existe pas.")
        return number_books_by_category, total_price_by_category

    
    for file in os.listdir(csv_directory):
        if file.endswith('.csv'):
            category = file.replace('.csv', '')
            total_price = 0
            number_books = 0
            
            try:
                with open(os.path.join(csv_directory, file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    if 'price_including_tax' not in reader.fieldnames:
                        print(f"La colonne 'prince_including_tax' est absente dans le fichier {file}.")
                        continue

                    
                    for row in reader:
                        price = row.get('price_including_tax')
                        if price:
                            try:
                                
                                price = float(price.replace('£', '').strip())
                                total_price += price
                                number_books += 1
                            except ValueError:
                                print(f"Erreur de conversion du prix {price} dans le fichier {file}.")
                                continue  
                
                if number_books > 0:
                    number_books_by_category[category] = number_books
                    total_price_by_category[category] = total_price / number_books

            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file}: {e}")

    return number_books_by_category, total_price_by_category

def plot_combined_charts():
    """
    Crée deux graphiques :
    - Un diagramme circulaire pour la répartition des livres par catégorie.
    - Un diagramme en barres pour la moyenne des prix par catégorie.
    """
    number_books_by_category, average_price_by_category = get_average_price_by_category()

    if not number_books_by_category:
        print("Pas de données pour le nombre de livres.")
        return

    if not average_price_by_category:
        print("Pas de données pour la moyenne des prix.")
        return

    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    
    labels = number_books_by_category.keys()
    sizes = number_books_by_category.values()

    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax1.set_title('Répartition des livres par catégorie')
    ax1.axis('equal')  

    
    categories = list(average_price_by_category.keys())
    average_prices = list(average_price_by_category.values())

    ax2.bar(categories, average_prices, color='skyblue')
    ax2.set_xlabel('Catégories')
    ax2.set_ylabel('Prix moyen (£)')
    ax2.set_title('Prix moyen des livres par catégorie')
    ax2.set_xticklabels(categories, rotation=45, ha='right')

    
    plt.tight_layout()
    plt.show()

plot_combined_charts()
