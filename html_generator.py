# Created by: Geoffrey Eslava
import os
from glob import glob

from yattag import Doc

ASSETS_FOLDER = ['assets/', 'css/', 'vendor/']


class Video(object):

    def __init__(self):
        self.title = ''
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


def retrieve_dirs():
    dirs = []
    directories = glob('*/')
    for directory in directories:
        if directory not in ASSETS_FOLDER:
            dirs.append(directory)

    return dirs


def convert_srt(directory, subtitle_file):
    pass


def read_dir():
    video_list = []
    video_ext = ['.mp4', '.mkv', '.avi']
    sub_ext = ['.srt']
    img_ext = ['jpg', '.png', '.tif']

    sub_dirs = retrieve_dirs()
    for sub_dir in sub_dirs:
        new_vid = Video()
        for _, _, files in os.walk(sub_dir):
            # initialize new Video class to hold file details.
            # This would include the title, video file, subtitle and image.
            new_vid.directory = sub_dir
            for curr_file in files:
                if os.path.isfile(sub_dir + '/' + curr_file):
                    if curr_file.endswith(tuple(video_ext)):
                        new_vid.video = curr_file
                        new_vid.title = os.path.splitext(curr_file)[0]
                    elif curr_file.endswith(tuple(img_ext)):
                        new_vid.image = curr_file
                    elif curr_file.endswith(tuple(sub_ext)):
                        new_vid.subtitle = curr_file
                        convert_srt(sub_dir, curr_file)
                    else:
                        pass
        video_list.append(new_vid)
        new_vid = None

    # for obj in video_list:
    #     print(obj.title)
    #     print(obj.subtitle)
    #     print(obj.video)
    #     print(obj.image)

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
            doc.stag('link', rel='stylesheet', href='vendor/bootstrap/css/bootstrap.min.css')
            doc.stag('link', rel='stylesheet', href='css/main.css')
            with tag('title'):
                text('My Movie Player')
        with tag('body'):
            # -- Navigation -- #
            with tag('nav', klass='navbar navbar-expand-lg navbar-dark bg-dark fixed-top'):
                with tag('div', klass='container'):
                    with tag('a', klass='navbar-brand', href='#'):
                        text('Movie Database')
                    doc.asis(
                        '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">')
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
                                with tag('a', klass='nav-link', href='https://yts.am', target='_blank'):
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
                    with tag('h1', klass='display-3'):
                        text('Welcome to Our Movie Collection')
                        with tag('p', klass='lead'):
                            text('This is our latest collection of movies downloaded from YTS.AM')
                        with tag('a', href='https://yts.am/', klass='btn btn-primary btn-lg', target='_blank'):
                            text('Bring me to YIFY')
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
                                            text(video.title)
                                    with tag('div', klass='card-footer'):
                                        with tag('a', href=video.get_video_path(), klass='btn btn-primary'):
                                            text('Play Movie')
                            counter += 1
                        else:
                            with tag('div', klass='col-lg-3 col-md-6 mb-4'):
                                with tag('div', klass='card'):
                                    doc.stag('img', klass='card-img-top', src=video.get_image_path(), alt=video.title)
                                    with tag('div', klass='card-body'):
                                        with tag('h4', klass='card-title'):
                                            text(video.title)
                                    with tag('div', klass='card-footer'):
                                        with tag('a', href=video.get_video_path(), klass='btn btn-primary'):
                                            text('Play Movie')
                            counter += 1
                doc.asis('</div>')

            with tag('footer', klass='py-5 bg-dark'):
                with tag('div', klass='container'):
                    with tag('p', klass='m-0 text-center text-white'):
                        text('Copyright (c) 2018 Eslava Movie Database')

            # -- Bootstrap core Javascript -- #
            doc.asis('<script src="vendor/jquery/jquery.min.js"></script>')
            doc.asis('<script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>')

    print('Successfully generated HTML file.')

    f = open('index.html', 'w')

    f.write(doc.getvalue())
    f.close()


if __name__ == '__main__':
    video_list = read_dir()
    # print(len(video_list))
    # for video in video_list:
    #     print(video.title)
    #     print(video.subtitle)
    generate_html(video_list)
