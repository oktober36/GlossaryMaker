import requests
from bs4 import BeautifulSoup


def cambridge_dictionary(input_word) -> dict[str, str]:
    base_url = 'https://dictionary.cambridge.org/dictionary/english-russian/'
    url = base_url + input_word + '/'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/51.0.2704.103 "
                             "Safari/537.36 "
               }
    response = requests.get(url=url, headers=headers)
    if response.url == base_url:
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')
    transcription = soup.find(attrs={'class': 'pron dpron'}).text.replace('/', '|')
    meaning = soup.find(attrs={'class': 'def ddef_d db'}).text
    translation = soup.find(attrs={'class': 'trans dtrans dtrans-se'}).text
    return {'transcription': transcription,
            'meaning': meaning,
            'translation': translation}


def synonyms_thesaurus(input_word) -> dict[str, str]:
    base_url = 'https://www.synonyms-thesaurus.com/synonyms-'
    url = base_url + input_word
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/51.0.2704.103 "
                             "Safari/537.36 "
               }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    strong = soup.find('strong')
    if strong is not None:
        if 'no synonym available' in strong.text:
            return {}

    synonyms = []
    synonyms_rows = soup.find(attrs={'class': 'synonym'}).findAll(attrs={'class': 'twelve columns first'})
    if len(synonyms_rows) == 0:
        synonyms_rows = soup.find(attrs={'class': 'synonym'}).find(attrs={'class': 'twelve columns listDetails'}) \
            .findChildren()
    for row in synonyms_rows[:min(3, len(synonyms_rows))]:
        synonyms.append(row.text.replace(' ', ''))
    try:
        example = soup.find(attrs={'class': 'definition'}).find('span').findNext('li').text
    except AttributeError:
        example = ''

    antonyms = []
    antonyms_container = soup.find(attrs={'class': 'row antonym'})
    if antonyms_container is not None:
        antonyms_row = antonyms_container.findAll('a')
        if len(antonyms_row) != 0:
            for row in antonyms_row[:min(3, len(antonyms_row))]:
                antonyms.append(row.text.replace(' ', ''))
    return {'example': example,
            'synonyms': synonyms,
            'antonyms': antonyms}


def get_word(word: str) -> dict[str, str]:
    cambridge = cambridge_dictionary(word)
    if len(cambridge) == 0:
        return {}
    out = dict(cambridge, **synonyms_thesaurus(word))
    out['word'] = word
    return out


if __name__ == '__main__':
    print(get_word('white'))
