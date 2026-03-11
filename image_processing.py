from PIL import Image, ImageEnhance

def preprocess_image(img):
    # Escala de grises
    img = img.convert("L")

    # Contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Binarización
    img = img.point(lambda x: 0 if x < 140 else 255, '1')
    return img