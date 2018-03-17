# Created by: Geoffrey Eslava
import os
from glob import glob
from pathlib import Path

from yattag import Doc
from convert_srt_to_vtt import start_conversion
from image_handler import retrieve_image_from_url

ASSETS_FOLDER = ['assets/', 'css/', 'vendor/', '__pycache__/', 'miniserver/']
IMAGE_FILENAME = 'medium-cover.jpg'


class Video(object):

    def __init__(self):
        self.title = ''
        self.video_filename = ''
        self.year = ''
        self.subtitle = ''
        self.video = ''
        self.image = ''
        self.directory = ''

    def get_video_path(self):
        return self.directory + self.video

    def get_image_path(self):
        return self.directory + self.image

    def get_subtitle_path(self):
        return self.directory + self.subtitle

    def get_full_title(self):
        return self.title + ' (' + self.year + ')'


def parse_title(movie_filename):
    """
    Parsing of the title and year based on the Movie's filename.
    :param movie_filename:
    :return: title, year
    """
    title = movie_filename.split('.')
    actual_title = ''
    year = 0
    for word in title:
        if word.isdigit() and len(word) == 4:
            year = word
            break
        else:
            actual_title = actual_title + ' ' + word

    return actual_title, year


def retrieve_dirs():
    """
    Navigate to the root directory of all the Movies and
    get the list of movie directories.
    :return: Array of Directory names.
    """
    dirs = []
    os.chdir('../')
    directories = glob('*/')
    for directory in directories:
        if directory not in ASSETS_FOLDER:
            dirs.append(directory)

    return dirs


def read_dir():
    """
    Traverse through each of the movie directories and
    retrieve all the movie details.
    These include the following:
        -> title
        -> year
        -> path
        -> video filename and path
        -> subtitle filename and path
        -> image filename and path

    :return:
    """
    video_list = []
    video_ext = ['.mp4', '.mkv', '.avi']
    sub_ext = ['.vtt']
    img_ext = ['jpg', '.png', '.tif']

    sub_dirs = retrieve_dirs()

    # Loop through each Movie directory
    for sub_dir in sub_dirs:

        # initialize new Video class to hold file details.
        # This would include the title, video file, subtitle and image.
        new_vid = Video()
        new_vid.directory = sub_dir

        for _, _, files in os.walk(sub_dir):
            for curr_file in files:
                full_file_path = sub_dir + curr_file
                if os.path.isfile(full_file_path):

                    # set the video filename
                    if curr_file.endswith(tuple(video_ext)):
                        new_vid.video = curr_file
                        new_vid.title, new_vid.year = parse_title(curr_file)
                        image_file = Path(sub_dir + IMAGE_FILENAME)

                        if not image_file.exists():
                            retrieve_image_from_url(new_vid.title, new_vid.year, new_vid.directory)
                    # set the image
                    elif curr_file.endswith(tuple(img_ext)):
                        # Check if the image name == 'medium_cover.jpg'
                        if curr_file.split('.')[0] == IMAGE_FILENAME.split('.')[0]:
                            new_vid.image = curr_file
                        else:
                            new_vid.image = retrieve_image_from_url(new_vid.title, new_vid.year, new_vid.directory)

                    # set the subtitle
                    elif curr_file.endswith('vtt'):
                        new_vid.subtitle = curr_file
                    elif curr_file.endswith('srt'):
                        # check if the vtt file exists
                        vtt_file = os.path.splitext(curr_file)[0]
                        vtt_path = sub_dir + '/' + vtt_file + '.vtt'
                        if not os.path.isfile(vtt_path):
                            subtitle = start_conversion(full_file_path, vtt_path)
                            print('Successfully created vtt file: ' + str(subtitle))
                            new_vid.subtitle = str(subtitle)
                    else:
                        pass
        video_list.append(new_vid)
        new_vid = None

    return video_list


def generate_html(this_videos_list):
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html', lang='en'):
        with tag('head'):
            doc.stag('meta', charset='utf-8')
            doc.stag('meta', name='viewport', content='width=device-width initial-scale=1, shrink-to-fit=no')
            doc.stag('meta', name='description', content='')
            doc.stag('meta', name='author', content='')
            doc.stag('link', rel='stylesheet', href='miniserver/vendor/bootstrap/css/bootstrap.min.css')
            doc.stag('link', rel='stylesheet', href='miniserver/css/main.css')
            with tag('title'):
                text('Director\'s Seat')
        with tag('body'):
            # -- Navigation -- #
            with tag('nav', klass='navbar navbar-expand-lg navbar-dark bg-dark fixed-top'):
                with tag('div', klass='container'):
                    with tag('a', klass='navbar-brand', href='#'):
                        text('Director\'s Seat')
                    doc.asis(
                        '<button class="navbar-toggler" type="button" data-toggle="collapse" ' +
                        'data-target="#navbarResponsive" aria-controls="navbarResponsive" ' +
                        'aria-expanded="false" aria-label="Toggle navigation">')
                    doc.asis('<span class="navbar-toggler-icon"></span>')
                    doc.asis('</button>')
                    with tag('div', klass='collapse navbar-collapse', id='navbarResponsive'):
                        with tag('ul', klass='navbar-nav ml-auto'):
                            with tag('li', klass='nav-item active'):
                                with tag('a', klass='nav-link', href='#'):
                                    text('Home')
                                    with tag('span', klass='sr-only'):
                                        text('(current)')
                            with tag('li', klass='nav-item'):
                                with tag('a', klass='nav-link', href='https://yts.am/yify', target='_blank'):
                                    text('YTS.AM')
                            with tag('li', klass='nav-item'):
                                with tag('a', klass='nav-link', href='#'):
                                    text('Services')
                            with tag('li', klass='nav-item'):
                                with tag('a', klass='nav-link', href='#'):
                                    text('Contact')
            # -- Page Content -- #
            with tag('div', klass='container'):
                # -- Jumbotron Header -- #
                with tag('header', klass='jumbotron my-4'):
                    with tag('h1', klass='display-4'):
                        text('Welcome to Our Movie Collection')
                        with tag('p', klass='lead'):
                            text('This is our latest collection of movies downloaded from YIFY (YTS.AM)')
                        with tag('a', href='https://yts.am/yify', klass='btn btn-primary btn-lg', target='_blank'):
                            text('Take me to YIFY')
                # -- Page Features -- #
                total_count = len(this_videos_list)
                counter = 0
                for video in this_videos_list:
                    if counter <= total_count:
                        if counter == 0:
                            doc.asis('<div class="row text-center">')
                            with tag('div', klass='col-lg-3 col-md-6 mb-4'):
                                with tag('div', klass='card'):
                                    doc.stag('img', klass='card-img-top', src=video.get_image_path(), alt=video.title)
                                    with tag('div', klass='card-body'):
                                        with tag('h4', klass='card-title'):
                                            text(video.get_full_title())
                                    with tag('div', klass='card-footer'):
                                        with tag('a', href=video.directory + 'player.html', klass='btn btn-primary'):
                                            text('Play Movie')
                            counter += 1
                        else:
                            with tag('div', klass='col-lg-3 col-md-6 mb-4'):
                                with tag('div', klass='card'):
                                    doc.stag('img', klass='card-img-top', src=video.get_image_path(), alt=video.title)
                                    with tag('div', klass='card-body'):
                                        with tag('h4', klass='card-title'):
                                            text(video.get_full_title())
                                    with tag('div', klass='card-footer'):
                                        with tag('a', href=video.directory + 'player.html', klass='btn btn-primary'):
                                            text('Play Movie')
                            counter += 1
                doc.asis('</div>')

            with tag('footer', klass='py-5 bg-dark'):
                with tag('div', klass='container'):
                    with tag('p', klass='m-0 text-center text-white'):
                        text('Copyright (c) 2018 Eslava Movie Database')

            # -- Bootstrap core Javascript -- #
            doc.asis('<script src="miniserver/vendor/jquery/jquery.min.js"></script>')
            doc.asis('<script src="miniserver/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>')

    f = open('index.html', 'w')

    f.write(doc.getvalue())
    f.close()
    print('Successfully generated HTML file.')


# generate video player page
def generate_video_player_html(movie_list):
    for video in movie_list:
        doc, tag, text, line = Doc().ttl()
        doc.asis('<!DOCTYPE html>')
        with tag('html', lang='en'):
            with tag('head'):
                doc.stag('meta', charset='utf-8')
                doc.stag('meta', name='viewport', content='width=device-width initial-scale=1, shrink-to-fit=no')
                doc.stag('meta', name='description', content='')
                doc.stag('meta', name='author', content='')
                doc.stag('link', rel='stylesheet', href='../miniserver/vendor/bootstrap/css/bootstrap.min.css')
                doc.stag('link', rel='stylesheet', href='../miniserver/css/main.css')
                with tag('title'):
                    text('Director\'s Seat')
            with tag('body'):
                # -- Navigation -- #
                with tag('nav', klass='navbar navbar-expand-lg navbar-dark bg-dark fixed-top'):
                    with tag('div', klass='container'):
                        with tag('a', klass='navbar-brand', href='../index.html'):
                            text('Director\'s Seat')
                        doc.asis(
                            '<button class="navbar-toggler" type="button" data-toggle="collapse"' +
                            ' data-target="#navbarResponsive" aria-controls="navbarResponsive"' +
                            ' aria-expanded="false" aria-label="Toggle navigation">')
                        doc.asis('<span class="navbar-toggler-icon"></span>')
                        doc.asis('</button>')
                        with tag('div', klass='collapse navbar-collapse', id='navbarResponsive'):
                            with tag('ul', klass='navbar-nav ml-auto'):
                                with tag('li', klass='nav-item active'):
                                    with tag('a', klass='nav-link', href='../index.html'):
                                        text('Home')
                                        with tag('span', klass='sr-only'):
                                            text('(current)')
                                with tag('li', klass='nav-item'):
                                    with tag('a', klass='nav-link', href='https://yts.am/yify', target='_blank'):
                                        text('YTS.AM')
                                with tag('li', klass='nav-item'):
                                    with tag('a', klass='nav-link', href='#'):
                                        text('Services')
                                with tag('li', klass='nav-item'):
                                    with tag('a', klass='nav-link', href='#'):
                                        text('Contact')
                # -- Page Content -- #
                with tag('div', klass='container'):
                    with tag('div', klass='card'):
                        with tag('div', klass='header'):
                            text(video.get_full_title())
                        with tag('div', klass='card-body'):
                            with tag('video', src=video.video, controls='', autoplay=''):
                                doc.asis('<track kind="subtitles" label="English" src="' +
                                         video.subtitle + '" srclang="en" default="">')

                with tag('footer', klass='py-5 bg-dark'):
                    with tag('div', klass='container'):
                        with tag('p', klass='m-0 text-center text-white'):
                            text('Copyright (c) 2018 Eslava Movie Database')

                # -- Bootstrap core Javascript -- #
                doc.asis('<script src="../miniserver/vendor/jquery/jquery.min.js"></script>')
                doc.asis('<script src="../miniserver/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>')

        print('Successfully generated player HTML file to ' + video.directory)

        f = open(video.directory + 'player.html', 'w')

        f.write(doc.getvalue())
        f.close()


if __name__ == '__main__':
    video_list = read_dir()
    generate_html(video_list)
    generate_video_player_html(video_list)
    # os.rename('index.html', '../index.html')
