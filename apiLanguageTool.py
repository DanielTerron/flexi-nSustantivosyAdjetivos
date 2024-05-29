import requests

def check_spelling(word, language='es'):
    url = 'https://api.languagetool.org/v2/check'
    params = {
        'text': word,
        'language': language
    }

    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = response.json()
        matches = result.get('matches', [])
        if not matches:
            return word  # La palabra está bien escrita
        else:
            # Devolver la primera sugerencia de corrección encontrada
            corrections = [match['replacements'][0]['value'] for match in matches if 'replacements' in match and match['replacements']]
            return corrections[0] if corrections else word
    else:
        print(f"Error en la solicitud a LanguageTool: {response.status_code}")
        return word



