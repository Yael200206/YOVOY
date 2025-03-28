import cv2
import numpy as np
import fitz  # PyMuPDF
import matplotlib.pyplot as plt

def extract_first_page_as_image(pdf_path, zoom_factor=1.0):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # No aplicar zoom para mantener el tamaño original de la imagen
    matrix = fitz.Matrix(zoom_factor+10, zoom_factor+10)  # El zoom_factor es 1.0 para mantener el tamaño original
    pix = page.get_pixmap(matrix=matrix)
    
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if img.shape[2] == 4:  # Convertir RGBA a RGB para correcta visualización
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


def filter_red_blue(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Ampliar el rango de color para rojo
    lower_red1, upper_red1 = np.array([0, 100, 100]), np.array([20, 255, 255])  # Rango rojo 1
    lower_red2, upper_red2 = np.array([160, 100, 100]), np.array([200, 255, 255])  # Rango rojo 2
    lower_blue, upper_blue = np.array([100, 100, 100]), np.array([140, 255, 255])
    
    # Crear máscaras para rojo y azul
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Crear una imagen negra
    filtered_image = np.zeros_like(image)
    
    # Aplicar las máscaras al fondo negro
    filtered_image[mask_red > 0] = [255, 0, 0]  # Rojo
    filtered_image[mask_blue > 0] = [0, 0, 255]  # Azul
    
    return filtered_image

def main():
    pdf_path = "01.pdf"  # Cambia esto por tu archivo PDF
    image = extract_first_page_as_image(pdf_path, zoom_factor=2.0)  # Aumenta la calidad con un zoom de 2
    filtered_image = filter_red_blue(image)
    
    # Mostrar la imagen filtrada con matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(filtered_image)
    plt.axis("off")  # Ocultar los ejes
    plt.title("Filtro Rojo y Azul")
    plt.show()

if __name__ == "__main__":
    main()
