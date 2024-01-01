#cv2 est largement utilisée pour le traitement d'images. Elle vous permet de charger, manipuler, afficher et effectuer des opérations sur des images.
import cv2
#numpy est une bibliothèque pour le calcul scientifique en Python.
import numpy as np
#pour la gestion des images stockées dans un répertoire.
import os
import tkinter as tk
from tkinter import filedialog, CENTER
from PIL import Image, ImageTk  # Assurez-vous d'avoir la bibliothèque Pillow (PIL) installée


# Fonction pour extraire les coins à l'aide du détecteur de Harris
def extract_harris_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    # Détection des coins à l'aide du détecteur de Harris
    #blockSize=2 : La taille de la fenêtre voisine pour le calcul du vecteur propre (plus grande que 2 signifie une détection plus globale).
    #ksize=3 : La taille du noyau utilisé pour le lissage (filtrage Gaussien) avant de calculer les dérivées.
    #k=0.04 : Paramètre de sensibilité du détecteur de Harris. Une valeur plus élevée donnera moins de coins.
    dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    #retourne une carte de points de coin de Harris.
    return dst


# Fonction pour calculer la similarité en pourcentage
#Cette fonction calculate_similarity est utilisée pour calculer la similarité en pourcentage entre deux ensembles de coins (points de coin) en utilisant la méthode de la somme des carrés des différences (SSD).
def calculate_similarity(query_corners, indexed_corners):
    query_corners = cv2.resize(query_corners, (indexed_corners.shape[1], indexed_corners.shape[0]))

    # Calcul de la somme des carrés des différences (SSD)
    #(SSD)la somme des carrés des différences .
    ssd = np.sum(np.square(query_corners - indexed_corners))

    # Normalisation de la similarité (plus proche de zéro signifie plus similaire)
    similarity = 1.0 / (1.0 + ssd)
    #La fonction retournera un score de similarité en pourcentage entre les deux ensembles de coins.
    return similarity * 100


# Fonction pour charger l'image requête depuis un fichier
def load_query_image():
    file_path = filedialog.askopenfilename(title="Sélectionner l'image requête")
    if file_path:
        return cv2.imread(file_path)
    return None


# Fonction pour rechercher et afficher les images similaires
def search_similar_images():
    query_image = load_query_image()
    if query_image is None:
        return

    query_corners = extract_harris_corners(query_image)
    similarities = []

    for filename in os.listdir(indexed_image_folder):
        indexed_image_path = os.path.join(indexed_image_folder, filename)
        indexed_image = cv2.imread(indexed_image_path)
        indexed_corners = extract_harris_corners(indexed_image)
        similarity = calculate_similarity(query_corners, indexed_corners)
        similarities.append((filename, similarity))
        print(f"Similarity with {filename}: {similarity:.2f}%")

    if similarities:
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similarities = similarities[:5]  # Afficher les 5 images les plus similaires

        display_similar_images(top_similarities)

        # Mise à jour du Label avec les résultats de similarité
        result_text = "Résultats de similarité :\n\n"
        for filename, similarity in top_similarities:
            result_text += f"{filename}: {similarity:.2f}%\n"
        result_label.config(text=result_text)
    else:
        result_label.config(text="Aucune image similaire trouvée.")

# Fonction pour afficher les images similaires dans une nouvelle fenêtre
def display_similar_images(similarities):
    similar_window = tk.Toplevel(root)
    similar_window.title("Images Similaires")

    for i, (filename, similarity) in enumerate(similarities):
        if similarity > 0:
            img = Image.open(os.path.join(indexed_image_folder, filename))
            img = img.resize((200, 200), Image.LANCZOS)  # Redimensionner l'image
            img = ImageTk.PhotoImage(img)

            label = tk.Label(similar_window, text=f"Similarité: {similarity:.2f}%")
            label.pack()

            canvas = tk.Canvas(similar_window, width=200, height=200)
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.image = img
            canvas.pack()



# Fonction pour effectuer la détection de coins de Harris
def harris_corner_detection():
    file_path = filedialog.askopenfilename(title="Sélectionner l'image pour la détection de Harris")
    if not file_path:
        print("Aucune image sélectionnée.")
        return

    # Chargez l'image sélectionnée
    query_image = cv2.imread(file_path)
    if query_image is None:
        print("Erreur : Chargement de l'image requête échoué")
        return

    # Effectuez la détection de coins de Harris sur l'image requête
    query_corners = extract_harris_corners(query_image)

    # Affichez l'image des coins de Harris avec les coins en rouge
    red_color = (0, 0, 255)
    query_image[query_corners > 0.01 * query_corners.max()] = red_color

    cv2.imshow("Coins de Harris", query_image)

    # Attendre que l'utilisateur appuie sur une touche (0 signifie attendre indéfiniment)
    cv2.waitKey(0)


# Crée la fenêtre principale de l'application
root = tk.Tk()
root.title("Recherche d'Images Similaires")
root.geometry("1000x600")  # Définit la taille de la fenêtre

# Chargez l'image de fond
background_image = Image.open("C:/Users/hp/Desktop/profile.jpg")  # Remplacez "background.jpg" par le chemin de votre image de fond
# Redimensionnez l'image à la largeur et la hauteur souhaitées
new_width = 1000  # Remplacez par la largeur souhaitée en pixels
new_height = 600  # Remplacez par la hauteur souhaitée en pixels
background_image = background_image.resize((new_width, new_height), Image.LANCZOS)

# Créez un PhotoImage depuis l'image redimensionnée
background_photo = ImageTk.PhotoImage(background_image)

# Créez un Label pour afficher l'image de fond
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0)
photo = ImageTk.PhotoImage(background_image)


# création d'une étiquette pour afficher l'image en arrière-plan
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0)

indexed_image_folder = 'C:/Users/hp/Desktop/imagesMur'

# Label pour afficher les résultats de similarité
result_label = tk.Label(root, text="")
result_label.pack()


# Bouton pour rechercher des images similaires
tk.Button(root, text="Rechercher Images Similaires", font=('Helvetin 16 bold'), bg='azure', width=25, command=search_similar_images).place(relx=.3, rely=.5, anchor=CENTER)
tk.Button(root, text="Détection de Coins de Harris", font=('Helvetin 16 bold'), bg='azure', width=25, command=harris_corner_detection).place(relx=.7, rely=.5, anchor=CENTER)



root.mainloop()









