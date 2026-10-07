import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    # 1. Enlever le fond
    input_img = Image.open(input_path)
    subject_only = remove(input_img)
    
    # Convertir pour OpenCV
    img_arr = np.array(subject_only)
    alpha = img_arr[:, :, 3]
    bgr = img_arr[:, :, 0:3]
    
    # 2. Passer en niveaux de gris et forcer le contraste (CLAHE)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrasted = clahe.apply(gray)
    
    # 3. Placer sur un fond blanc pur (le blanc sera vide en ASCII)
    white_bg = np.ones_like(contrasted) * 255
    alpha_norm = alpha / 255.0
    final_img = (contrasted * alpha_norm + white_bg * (1 - alpha_norm)).astype(np.uint8)
    
    cv2.imwrite(output_path, final_img)

if __name__ == "__main__":
    # Si aucun argument n'est passé, on cherche une image par défaut
    img_name = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
    prep_photo(img_name)
