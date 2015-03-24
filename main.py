import requests
import json
import math
import os

#-----------------------------------------------------------------------------#
# Program: My Movie Gallery.                                                  #
# Author: Gabriel A. Zorrilla. gabriel at zorrilla dot me                     #
# Copyright: GPL 3.0                                                          #
#-----------------------------------------------------------------------------#
#CONFIGURATION PARAMETERS                                                     #
#-----------------------------------------------------------------------------#

gallery_name = 'My Movie Gallery'
tmdb_key = 'f8860327b25dbbe0d96d9e5d1db91779'
poster_size = 'w185' # 'w92', 'w154', 'w185', 'w342', 'w500', 'original'
language = 'en' #Only english works 100% (I guess). Others may fail.
web_dir = '' #Optional. In case you want to host the script in a different dir.

#-----------------------------------------------------------------------------#

def get_movies_from_kodi():
    host = 'kraken'
    port = '8080'
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
    if os.path.isfile(os.path.join(folder_path,imdbid + '.jpeg')):
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
    full_stars = math.floor(round(stars)/2)
    remaining_stars = round(stars)/2 - full_stars;
    full_star_url = os.path.join(web_dir, 'assets', 'star-full.svg')
    half_star_url = os.path.join(web_dir, 'assets', 'star-half.svg')
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
    block = (row_open + "<td><div class='movie'>" + watched + poster + "<br>" +
             "<div class='star_container'>" + movie_stars(rating) + "</div>" +
             "</div></td>" + row_close)
    return block


def write_html(movies, web_dir):
    projectLink = ("<a href='https://github.com/GAZ082/MyMovieGallery'>" +
                   "Project link.</a>");
    made = 'Made by Gabriel A. Zorrilla.'
    cssfile = ("<link rel='stylesheet' type='text/css' href=" +
    os.path.join(web_dir,'assets','styles.css') + ">")
    tmdblogo = ("<img src='" + os.path.join(web_dir,'assets','tmdb.svg' +
                "' alt='www.themoviedb.org'>"))
    header = ("<!DOCTYPE html><html><head><title>" + gallery_name + "</title>"
              + "<meta charset='UTF-8'>" + cssfile + "</head><body>" +
              "<div id='gallery_name'>" + gallery_name + "</div><table>")
    footer = ("</table><div id='line'></div><div id='footer'>" + made + "<br>"
              + projectLink + "<br>Thanks to:<br><br>" + tmdblogo + "</div>" + 
              "</body></html>")
    html = header + movies + footer
    f = open(os.path.join(web_dir, 'index.html'), 'w', encoding='utf-8')
    f.write(html)
    f.close()



if __name__ == "__main__":
    posters_to_retrieve = []
    movies_html = ""
    counter = 1
    for i in get_movies_from_kodi():
        r = check_if_poster_exists(i['imdbnumber'], poster_size, web_dir)
        poster_url = ("posters/" + poster_size + "/" + i['imdbnumber'] +
                     '.jpeg')
        movies_html = (movies_html + create_movie_html_block(i['label'],
                     i['imdbnumber'], poster_url, counter, i['plot'],
                     i['playcount'],i['rating']))
        if not r:
            posters_to_retrieve.append(i['imdbnumber'])
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
