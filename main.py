import json
import math
import time
import os

import requests


# Program: My Movie Gallery.
# Author: Gabriel A. Zorrilla. gabriel at zorrilla dot me
# Copyright: GPL 3.0

# CONFIGURATION PARAMETERS

host = 'localhost'
# KODI host (ip, hostname). Change this to suit your needs.
port = '8080'
# This is the default KODI's port.
gallery_name = 'My Movie Gallery'
tmdb_key = 'f8860327b25dbbe0d96d9e5d1db91779'
poster_size = 'w185'
# 'w92', 'w154', 'w185', 'w342', 'w500'.
language = 'en'
# English language has the largest poster collection on TMDB.
web_dir = ''
# Optional. In case you want to host the script in a different dir.
# So far the directory 'assets' must be in the same dir than main.py
pushbullet_api_key = ''
# Optional. Your PB Access token. If value is other than '', notifications will
# be activated.
pushbullet_device_iden = ''
# Your device iden. Use pb_devices.py script to get your device's iden.


def get_movies_from_kodi(host, port):
    url = 'http://' + host + ':' + port + '/jsonrpc'
    headers = {'content-type': 'application/json'}
    payload = ({"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params":
        {"properties": ["rating", "imdbnumber", "playcount", "plot"], "sort":
            {"order": "ascending", "method": "label", "ignorearticle": True}},
                "id": "libMovies"})
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    r = r.json()
    return r['result']['movies']


def get_poster_image_url(imdbid, tmdb_key, size, language):
    base_url = 'http://api.themoviedb.org/3/movie/'
    headers = {'content-type': 'application/json'}
    url = (base_url + imdbid + '/images' + '?api_key=' + tmdb_key +
           '&language=' + language)
    r = requests.get(url)
    i = 0
    while r.json()['posters'][i]['aspect_ratio'] != 0.666666666666667:
        i += 1
    image_url = r.json()['posters'][i]['file_path']
    poster_url = 'http://image.tmdb.org/t/p/' + size + image_url
    return poster_url


def check_if_poster_exists(imdbid, size, web_dir):
    folder_path = os.path.join(web_dir, 'posters', size)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if os.path.isfile(os.path.join(folder_path, imdbid + '.jpeg')):
        return True


def save_poster_image(poster_url, imdbid, size, web_dir):
    folder_path = os.path.join(web_dir, 'posters', size)
    r = requests.get(poster_url)
    filetype = r.headers['content-type'].split('/')[-1]
    filepath = os.path.join(folder_path, imdbid + '.' + filetype)
    f = open(filepath, "wb")
    f.write(r.content)
    f.close()


def movie_stars(stars):
    full_stars = math.floor(round(stars) / 2)
    remaining_stars = round(stars) / 2 - full_stars;
    full_star_url = os.path.join('assets', 'star-full.svg')
    half_star_url = os.path.join('assets', 'star-half.svg')
    img_full_star_html = "<img src='" + full_star_url + "' alt='star full'>"
    img_half_star_html = "<img src='" + half_star_url + "' alt='star half'>"
    if remaining_stars >= 0.5:
        html_stars = img_full_star_html * full_stars + img_half_star_html
    else:
        html_stars = img_full_star_html * full_stars
    return html_stars


def create_movie_html_block(title, imdbid, poster_url, position, plot, count,
                            rating):
    title = title.replace("'", "")
    plot = plot.replace("'", "")
    poster = ("<img src='" + poster_url + "' alt='" + title + "' title='" +
              plot + "'>")
    row_open = ''
    row_close = ''
    if count > 0:
        watched = "<div class='watched'></div>"
    else:
        watched = ''
    if position == 1:
        row_open = '<tr>'
        row_close = ''
    elif position == 5:
        row_open = ''
        row_close = '</tr>'
    block = ("<div class='movie'>" + watched + poster + "<br>" +
             "<div class='star_container'>" + movie_stars(rating) + "</div>" +
             "</div>")
    return block


def write_html(movies, web_dir):
    projectLink = ("<a href='https://github.com/GAZ082/MyMovieGallery'>" +
                   "Project link.</a>");
    made = 'Made by Gabriel A. Zorrilla'
    cssfile = ("<link rel='stylesheet' type='text/css' href='" +
               os.path.join('assets', 'styles.css') + "'>")
    tmdblogo = ("<img src='" + os.path.join('assets', 'tmdb.svg' +
                                            "' alt='www.themoviedb.org'>"))
    meta = ("<meta name='author' content='Gabriel A. Zorrilla'>" +
            "<meta name='keywords' content='KODI, XBMC, movie, gallery, "
            "HTML5'>" + "<meta name='description' content='My Movie Gallery:"
            + "Python script to show your KODI movies to the world!'>" +
            "<meta charset='UTF-8'>")
    header = ("<!DOCTYPE html><html><head><title>" + gallery_name + "</title>"
              + meta + cssfile +
              "</head><body><div id='container'>" + "<div id='gallery_name'>" +
              gallery_name + "</div>")
    updated = 'Movie list updated on: ' + time.strftime("%Y.%m.%d@%H:%M:%S")
    footer = ("<div id='line'></div><div id='footer'>" + updated +
              '<br>' + made + "<br>" + projectLink + "<br>Thanks to:<br><br>" +
              tmdblogo + "</div>" + "</div></body></html>")
    html = header + movies + footer
    f = open(os.path.join(web_dir, 'index.html'), 'w', encoding='utf-8')
    f.write(html)
    f.close()


def pushbullet_notification(apikey, movies, gallery, device):
    string_to_push = ''
    for i in movies:
        string_to_push += i + ', '
    string_to_push = 'New movies added: ' + string_to_push[:-2] + '.'
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + apikey}
    payload = {'device_iden': device, 'type': 'note', 'title': gallery,
               'body': string_to_push}
    requests.post(url, data=json.dumps(payload), headers=headers)


if __name__ == "__main__":
    posters_to_retrieve = []
    label_posters_to_retrieve = []
    movies_html = ""
    counter = 1
    for i in get_movies_from_kodi(host, port):
        r = check_if_poster_exists(i['imdbnumber'], poster_size, web_dir)
        poster_url = ("posters/" + poster_size + "/" + i['imdbnumber'] +
                     '.jpeg')
        movies_html = (movies_html + create_movie_html_block(i['label'],
                     i['imdbnumber'], poster_url, counter, i['plot'],
                     i['playcount'],i['rating']))
        if not r:
            posters_to_retrieve.append(i['imdbnumber'])
            label_posters_to_retrieve.append(i['label'])
        if counter != 5:
            counter += 1
        else:
            counter = 1
    posters_to_get = str(len(posters_to_retrieve))
    counter = 0
    for i in posters_to_retrieve:
        counter += 1
        url = get_poster_image_url(i, tmdb_key, poster_size, language)
        save_poster_image(url, i, poster_size, web_dir)
        print('Downloaded poster ' + str(counter) + ' / ' + posters_to_get +
              '.')
    write_html(movies_html, web_dir)
    if pushbullet_api_key != '':
        if len(label_posters_to_retrieve) != 0:
            pushbullet_notification(pushbullet_api_key,
            label_posters_to_retrieve, gallery_name, pushbullet_device_iden)