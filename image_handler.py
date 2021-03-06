from requests import get, ConnectionError

FILENAME = 'medium-cover.jpg'


def retrieve_image_from_url(title, year, path):
    build_title = title.replace(' ', '%20')

    try:
        result = get('https://yts.am/api/v2/list_movies.jsonp?query_term=' + build_title)

        if result.status_code == 200:

            data = result.json()['data']
            movie_details = data['movies']

            slug_data = title.strip().replace(' ', '-').replace('\'', '').replace('.', '').lower() + '-' + year

            for detail in movie_details:
                if slug_data == detail['slug']:
                    print(detail['medium_cover_image'] + ' image downloaded successfully.')
                    r = get(detail['medium_cover_image'])
                    with open(path + FILENAME, 'wb') as new_file:
                        new_file.write(r.content)

            return FILENAME
        else:
            print('Cannot connect to network.')

    except ConnectionError:
        print("No connection... Bypassing image retrieval.")
        return ''


if __name__ == '__main__':
    retrieve_image_from_url('The School of Rock', year=2003, path='')
