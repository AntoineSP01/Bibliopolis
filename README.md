*Installer les modules dans requirements.txt :*
pip install -r requirements.txt

**PHASE 1 : Récupération des informations d'un livre**

    Récupération de l'URL d'une page de livre à partir de la page d'accueil.
    Une fois l'URL dédiée obtenue, toutes les informations nécessaires sur le livre sont extraites.
    Toutes les informations sont ensuite ajoutées à un fichier CSV : book.csv.

**PHASE 2 : Refactorisation du code**

    Modifiez le code en créant des fonctions pour éviter la duplication.
    Récupération de l'URL d'une catégorie.
    Une fois l'URL stockée, le code scrappe les données de tous les livres de la catégorie.
    Si plusieurs pages sont présentes dans la catégorie, le script passe à la page suivante après avoir scrappé tous les livres de la page.

**PHASE 3 : Téléchargement des images des livres**

    Ajout des images des livres consultés directement dans le dossier images.
    Les images sont renommées avec le nom des livres pour une identification facile.

**PHASE 4 : Récupération de tous les livres de toutes les catégories**

    Boucle pour récupérer tous les livres de toutes les catégories du site.
    Pour chaque catégorie, un fichier CSV est créé avec le nom de la catégorie, ainsi qu'un dossier pour stocker toutes les images des livres de la catégorie.
    Toutes les données des livres sont stockées dans le fichier CSV correspondant.

**PHASE 5 : Visualisation des données**

    Création d'un diagramme circulaire pour représenter la répartition des livres dans les différentes catégories.
    Création d'un histogramme pour obtenir le prix moyen des livres dans chaque catégorie.