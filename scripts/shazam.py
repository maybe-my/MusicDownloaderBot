import config
import requests


def shazam_voice(file):
    """
    По ссылке определяет название и много другой информации
    :param file: Путь к файлу
    :return: возвращает json формат
    """
    data = {
        'api_token': config.API,
        'url': f'https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file}',
        'return': 'lyrics,napster,youtube',
    }
    file = requests.post('https://api.audd.io/', data=data)  # recognizeWithOffset/
    music = file.json()
    print(music)
    return music