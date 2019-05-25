from pprint import pprint

import requests

GRAPHQL_URL = 'https://silverscreen.by/graphql/'
HEADERS = {
    "Content-Type": "application/json",
}

REQUEST = '''{
    "query":"{
        shows {
            code
            name
            showtimes {
                date
            }
        }
    }"
}'''.replace('\n', '')


def query_dates():
    response = requests.post(GRAPHQL_URL, headers=HEADERS, data=REQUEST)
    json_response = response.json()
    for movie in json_response['data']['shows']:
        dates = [x['date'] for x in movie["showtimes"]]
        yield movie["code"], movie["name"], list(sorted(set(dates)))


if __name__ == '__main__':
    pprint(list(query_dates()))
