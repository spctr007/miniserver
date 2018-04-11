# Created by: Geoffrey Eslava
import os
from glob import glob

from yattag import Doc

from convert_srt_to_vtt import start_conversion
from image_handler import retrieve_image_from_url
from subtitle_retriever import get_subtitle

ASSETS_FOLDER = ['assets/', 'css/', 'vendor/', '__pycache__/', 'miniserver/']
IMAGE_FILENAME = 'medium-cover.jpg'
VIDEO_LIST = []


class Video(object):

    def __init__(self):
        self.title = ''
        self.video_filename = ''
        self.year = ''
        self.subtitle = ''
        self.video = ''
        self.image = ''
        self.directory = ''
        self.imdb_code = ''

    def get_video_path(self):
        return self.directory + self.video

    def get_image_path(self):
        return self.directory + self.image

    def get_subtitle_path(self):
        return self.directory + self.subtitle

    def get_full_title(self):
        return self.title + ' (' + self.year + ')'


def parse_path(movie_paths):
    for movie in movie_paths:
        new_vid = Video()
        split_data = movie.split('/')
        directory = split_data[0]
        title = split_data[1]
        new_vid.directory = directory + '/'
        new_vid.video_filename = title
        new_vid.title, new_vid.year = parse_title(title)
    
        VIDEO_LIST.append(new_vid)


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


def retrieve_dirs(file_extension=''):
    """
    Navigate to the root directory of all the Movies and
    get the list of movie directories.
    :param file_extension:
    :return: Array of Directory names.
    """
    dirs = []
    os.chdir('../')
    directories = glob('*/' + file_extension)
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
    # video_list = []
    # video_ext = ['.mp4', '.mkv', '.avi']
    # sub_ext = ['.vtt', '.srt']
    # img_ext = ['jpg', '.png', '.tif']

    sub_dirs = retrieve_dirs('*.mp4')
    parse_path(sub_dirs)

    # Loop through each Movie directory
    for video in VIDEO_LIST:
        if not any(fname == 'medium-cover.jpg' for fname in os.listdir(video.directory)):
            print('No image file for ' + video.directory)
            video.image = retrieve_image_from_url(video.title, video.year, video.directory)
        else:
            video.image = 'medium-cover.jpg'

        # Generate VTT file from SRT file.
        os.chdir(video.directory)

        # Check if the folder contains a subtitle. If not,
        # then retrieve the subtitle from yifysubtitles.com
        if not any(fname.endswith('.srt') for fname in os.listdir('.')):
            print("Retrieving subtitle for " + video.title)
            get_subtitle(video.title, video.year)

        for fname in os.listdir('.'):
            if os.path.isfile(fname) and fname.endswith('.srt'):
                video.subtitle = start_conversion(video.directory, fname)

        os.chdir('..')

        # for _, _, dir_file in os.walk(video.directory):
        #     for curr_file in dir_file:    
        #         if not glob(video.directory + '*.jpg'):
        #             print('No image file in ' + video.directory)
        # if not os.path.basename(curr_file) == IMAGE_FILENAME:
        #


def generate_html():
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
                total_count = len(VIDEO_LIST)
                counter = 0
                for video in VIDEO_LIST:
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
    print('Successfully generated INDEX page.')


# generate video player page
def generate_video_player_html(test_list=[]):
    global VIDEO_LIST
    if test_list and VIDEO_LIST:
        VIDEO_LIST = test_list

    for video in VIDEO_LIST:
        print('Start generating html file for ' + video.directory)
        print(video.subtitle)
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
                            with tag('video', src=video.video_filename, controls='', autoplay=''):
                                doc.asis('<track kind="subtitles" label="English" src="' +
                                         video.subtitle + '" srclang="en" default="">')

                with tag('footer', klass='py-5 bg-dark'):
                    with tag('div', klass='container'):
                        with tag('p', klass='m-0 text-center text-white'):
                            text('Copyright (c) 2018 Eslava Movie Database')

                # -- Bootstrap core Javascript -- #
                doc.asis('<script src="../miniserver/vendor/jquery/jquery.min.js"></script>')
                doc.asis('<script src="../miniserver/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>')

        print('Successfully generated PLAYER HTML file for ' + video.directory)

        f = open(video.directory + 'player.html', 'w')

        f.write(doc.getvalue())
        f.close()


if __name__ == '__main__':
    read_dir()
    # vid_list = []
    # new_video = Video()
    # new_video.directory = 'Pixels (2015)/'
    # new_video.video_filename = 'Pixels.2015.720p.BluRay.x264.YIFY.mp4'
    # new_video.subtitle = 'Pixels.2015.1080p.BluRay.x264.YIFY.vtt'
    # vid_list.append(new_video)
    generate_video_player_html()
    generate_html()
    # os.rename('index.html', '../index.html')
