def img_to_str(image_path):
    import pytesseract
    from PIL import Image

    # open image
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang='chi_sim')
    # return pytesseract.image_to_string(image)
