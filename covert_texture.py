import cairosvg
from PIL import Image

# Chemin du fichier SVG d'entrée
chemin_svg = "texture/the core charger v4.svg"

# Chemin du fichier PNG de sortie
chemin_png = "texture/the core charger v4.png"

# Conversion SVG vers PNG avec cairosvg
cairosvg.svg2png(url=chemin_svg, write_to=chemin_png)

# Ouverture de l'image PNG avec PIL pour effectuer d'autres opérations si nécessaire
image_png = Image.open(chemin_png)

# Exemple : Redimensionnement de l'image PNG
nouvelle_largeur = 300
nouvelle_hauteur = 200
image_redimensionnee = image_png.resize((nouvelle_largeur, nouvelle_hauteur))

# Sauvegarde de l'image redimensionnée
chemin_png_redimensionne = "chemin/vers/votre/image_redimensionnee.png"
image_redimensionnee.save(chemin_png_redimensionne)

# Fermeture de l'image PNG
image_png.close()
