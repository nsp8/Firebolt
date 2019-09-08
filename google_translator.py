"""
@author: Nishant Parmar
@description: Uses Cloud Translate API to translate keywords into queries
"""

import os
try:
    from google.cloud import translate
except (ModuleNotFoundError, ImportError):
    os.system('pip install --upgrade google-cloud-translate')
    from google.cloud import translate

translate_client = translate.Client()


def translate_keyword(keyword, target_lang):
    """Returns a string of the translated response in case of a successful 
        translation, otherwise returns an empty string
    Keyword arguments:
        keyword - string to be translated;
        target_lang - string representing the target's language code
    """
    response = translate_client.translate(keyword, target_language=target_lang)
    if response:
        return response["translatedText"]
    else:
        return ""
