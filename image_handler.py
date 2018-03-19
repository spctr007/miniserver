from requests import get

FILENAME = 'medium-cover.jpg'


def retrieve_image_from_url(title, year, path):
    build_title = title.replace(' ', '%20')
    result = get('https://yts.am/api/v2/list_movies.jsonp?query_term=' + build_title)
    data = result.json()['data']
    movie_details = data['movies']

    slug_data = title.strip().replace(' ', '-').replace('\'', '').replace('.', '').lower() + '-' + year

    for detail in movie_details:
        if slug_data == detail['slug']:
            print(detail['medium_cover_image'] + ' image downloaded successfully.')
            r = get(detail['medium_cover_image'])
            new_file = open(path + FILENAME, 'wb')
            new_file.write(r.content)
            new_file.close()

    return FILENAME


if __name__ == '__main__':
    retrieve_image_from_url('The Karate Kid', '', '')
