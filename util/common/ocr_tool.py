from aip import AipOcr

config = {
    'appId': '17820395',
    'apiKey': 'tK7IpNHIFQldfwvvvpwY75Px',
    'secretKey': 'FU0ob0bfUmkXAqG6qYizR62v8tfGGE4t'
}

client = AipOcr(**config)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_ocr1(image_path):
    import pytesseract
    from PIL import Image

    # open image
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang='chi_sim')


def img_ocr(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])
