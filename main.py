#!/usr/bin/env python

import os
import json
import math
import time
import sys, io
import shutil
import requests

#templates:
import re
from UserDict import UserDict
from urlparse import urlparse
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

# -------------------------------------{O}-------------------------------------#

# Program: My Movie Gallery.
# Author: Gabriel A. Zorrilla. gabriel at zorrilla dot me
# Copyright: GPL 3.0

# -------------------------------------{O}-------------------------------------#

# --------------------------CONFIGURATION PARAMETERS---------------------------#
scriptpath=os.path.dirname(os.path.realpath(__file__))
configfile=os.path.join(scriptpath,"config.py");
if not os.path.isfile(configfile) and not os.path.isfile(configfile+".template"):
	print('Missing template or config file: config.py')
	sys.exit()
		  
if not os.path.isfile(configfile):
	shutil.copyfile(configfile+".template", configfile);
	print('Just created an config file with defaut values, which may not be suitable for you!!');	
	
if not os.path.isfile(configfile):
	print('Failed to create an config file !')
	sys.exit()

execfile(configfile);


if web_dir.strip()=='': 
	web_dir=os.getcwd()

##########################################################################################################################
def query_kodi(url,payload):
    headers = {'content-type': 'application/json'}
   
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        r = r.json()
        return r['result']['movies']
    except:
	#raise
        print('Connection error. Please check host and port.')
        sys.exit()

#-------------------------------------{O}-------------------------------------#
def get_movies_from_kodi(host, port):
    	url = 'http://' + host + ':' + port + '/jsonrpc'
        
	#we will always limit the search result, maybe some browsers will demand a lower settings
    	if limit <= 0:
        	maxlimit=1000
        else:
        	maxlimit=limit

	payload = ({"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", 
         "params": {
             "limits":      { "start" : 0, "end": maxlimit },
             "properties":  ["rating", "imdbnumber", "playcount", "plot", "plotoutline", 
				"votes", "top250", "trailer", "year", "country", "studio", 
				"set", "genre", "mpaa", "tag", "tagline", "writer", 
				"originaltitle" ],  
             "sort":        {"order": "ascending", "method": "label", "ignorearticle": True}},
         "id": "libMovies"
       })

	return query_kodi(url,payload)

#-------------------------------------{O}-------------------------------------#
def get_new_movies_from_kodie(host,port):
    	url = 'http://' + host + ':' + port + '/jsonrpc'
	payload = ({"jsonrpc": "2.0", "method": "VideoLibrary.GetRecentlyAddedMovies", 
         "params": {
             "limits":      { "start" : 0, "end": 50 },
	     "properties":  ["imdbnumber"],
             "sort":        {"order": "ascending", "method": "label", "ignorearticle": True}},
         "id": "libMovies"
       })

	return query_kodi(url,payload)

##########################################################################################################################
def get_poster_image_url(movie, tmdb_key, size, language):
    base_url = 'http://api.themoviedb.org/3/movie/'
    headers = {'content-type': 'application/json'}

    
    if not 'imdbnumber' in movie or len(movie['imdbnumber']) <= 0 :
	print('['+movie['label']+'] Cannot get poster: no imdbnumber found: will use default poster instead')
	return "no-image"

    if len(language)<=0: 
	url = (base_url + str(movie['imdbnumber']) + '/images' + '?api_key=' + tmdb_key + '&language=' + lang)
    else:
	url = (base_url + str(movie['imdbnumber']) + '/images' + '?api_key=' + tmdb_key + '&language=' + str(language[0]))

    r = requests.get(url)
    try:
	# we want aspec ratio 0.66667 but this way we are a bit more flexible, maybe look at the vote count aswell
	i=0
        while r.json()['posters'][i]['aspect_ratio'] > poster_aspect_ratio+poster_aspect_ratio_offset or r.json()['posters'][i]['aspect_ratio'] < poster_aspect_ratio-poster_aspect_ratio_offset:
            i += 1
        image_url = r.json()['posters'][i]['file_path']
        poster_url = 'http://image.tmdb.org/t/p/' + size + image_url
    except LookupError:
	if len(language)>=2:
		#remove first element, and call recursive
		language.pop(0)
		poster_url = get_poster_image_url(movie, tmdb_key, size, language)
	else:
        	print('['+movie['label']+'] No poster exists. Using default no poster image'+ url ) 
        	poster_url = "no-image"

    return poster_url

#-------------------------------------{O}-------------------------------------#
def check_if_poster_exists(imdbid, size, web_dir):
    folder_path = os.path.join(web_dir, 'posters', size)
    if not os.path.exists(folder_path):
	try:
        	os.makedirs(folder_path)
	except  OSError:
		print "Failed to create path, check your permissions or settings: "+folder_path 
    if os.path.isfile(os.path.join(folder_path, imdbid + '.jpeg')):
        return True

#-------------------------------------{O}-------------------------------------#
def save_poster_image(poster_url, imdbid, size, web_dir):
    folder_path = os.path.join(web_dir, 'posters', size)

    if poster_url == 'no-image':
        no_image_path = os.path.join(web_dir, 'assets',
                                     'no-image-' + size + '.jpeg')
        filepath = os.path.join(folder_path, imdbid + '.jpeg')
        shutil.copyfile(no_image_path, filepath)
    else:
        r = requests.get(poster_url)
        filetype = r.headers['content-type'].split('/')[-1]
        filepath = os.path.join(folder_path, imdbid + '.' + filetype)
        f = open(filepath, "wb")
        f.write(r.content)
        f.close()

##########################################################################################################################
def movie_stars(stars=0,votes=0):
    full_stars = int(math.floor(round(stars) / 2))
    remaining_stars = round(stars) / 2 - full_stars;
    full_star_url = os.path.join('assets', 'star-full.svg')
    half_star_url = os.path.join('assets', 'star-half.svg')
    img_full_star_html = "<img src='" + full_star_url + "' alt='star full' title='"+str(round(stars,1))+" rating with "+str(votes)+" votes'>"
    img_half_star_html = "<img src='" + half_star_url + "' alt='star half' title='"+str(round(stars,1))+" rating with "+str(votes)+" votes'>"
    if remaining_stars >= 0.5:
        html_stars = img_full_star_html * full_stars + img_half_star_html
    else:
        html_stars = img_full_star_html * full_stars
    return html_stars


##########################################################################################################################
#extend the userdict for textreplace (replace tekst with a dict of key=value pairs)
class tekstreplace(UserDict):
	def _make_regex(self):
		return re.compile("(%s)" % "|".join(map(re.escape, self.keys())))

	def __call__(self, mo):
		# Count substitutions
		self.count += 1 # Look-up string
		return self[mo.string[mo.start():mo.end()]]

	def substitute (self, text):
		# Reset substitution counter
		self.count = 0
		# Process text
		return self._make_regex().sub(self, text)
		

	#make keys out of the dict, keys are surrounded by % and the values are escaped
	#arrays will become  , seperated stings
	def dict2keys(self, _keys):
		keys={}
		for k,v in _keys.iteritems():
			if str(k)[0] is not '\%':
				#for some silly reason cgi.escape doesn't escape ' 
				if isinstance(v, (list, tuple)):
					keys["%%%s%%"%(k)]=escape(', '.join(v)).replace("'","&apos;")
				elif isinstance(v, (int, long, float, complex)):
					keys["%%%s%%"%(k)]=unicode(v)
				elif isinstance(v, basestring):
					keys["%%%s%%"%(k)]=escape(unicode(v)).replace("'","&apos;")
				else:
					keys["%%%s%%"%(k)]=escape(unicode(v)).replace("'","&apos;")
			else:
				keys[k]=v
		return keys

#-------------------------------------{O}-------------------------------------#
def inlist(mylist,idname ,idvalue):
	if len([element for element in mylist if element[idname] == idvalue]) >=1 : 
		return True
	return False
#-------------------------------------{O}-------------------------------------#
def mycopytree(src, dst, symlinks = False, ignore = None):
	if not os.path.exists(dst):
		os.makedirs(dst)
		shutil.copystat(src, dst)
  	lst = os.listdir(src)

  	if ignore:
		excl = ignore(src, lst)
		lst = [x for x in lst if x not in excl]
	for item in lst:
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if symlinks and os.path.islink(s):
			if os.path.lexists(d):
				os.remove(d)
			os.symlink(os.readlink(s), d)
			try:
				st = os.lstat(s)
				mode = stat.S_IMODE(st.st_mode)
				os.lchmod(d, mode)
			except:
				pass # lchmod not available
		elif os.path.isdir(s):
			mycopytree(s, d, symlinks, ignore)
		else:
			#avoid chmod issues with copy2
			#shutil.copy2(s, d)
			shutil.copyfile(s, d)


##########################################################################################################################
def gettrailerid(params):
	try:
		murl=urlparse(params['trailer'])
		if 'youtube' in murl.netloc:
			for param in murl.query.split('&') : 
				paramlist=param.split('=')
				if paramlist[0]=='videoid':
					return paramlist[1]

	except:
		print "no youtube trailer info found.."
		
	return ""

##########################################################################################################################
def create_movie_html_block(movie):

	if 'votes' not in movie:
		movie['votes']=0
	if 'rating' not in movie:
		movie['rating']=0

        #change movie info to keys
	keys=tekstreplace().dict2keys(movie)
	
	#add extra keys
	if not '%watchedclass%' in keys:
		keys['%watchedclass%'] 		= 'unwatched'
	if movie['playcount'] > 0 :
		keys['%watchedclass%'] 	= 'watched'

	keys['%genreclasses%']		= escape(','.join(movie['genre']))

      	keys['%trailerid%']		= gettrailerid(movie)
	keys['%trailerurl%']		= ''
	if len(keys['%trailerid%']) >0:
		keys['%trailerurl%']	= 'http://www.youtube.com/watch?v='+keys['%trailerid%']
	keys['%trailerhtml%'] 		= ''
	if len(keys['%trailerurl%']) > 0:
		keys['%trailerhtml%'] 	= tekstreplace(keys).substitute(trailer_template)

	keys['%imdbhtml%']		= ''
	if '%imdbnumber%' in keys and len(keys['%imdbnumber%']) > 0:
		keys['%imdburl%']	= 'http://www.imdb.com/title/'+keys['%imdbnumber%']+'/'
		keys['%imdbhtml%'] 	= tekstreplace(keys).substitute(imdb_template)
	else:
		print ('['+movie['label']+'] imdbnumber not found, disable imdb button')

	keys['%starshtml%']		= movie_stars(movie['rating'],keys['%votes%'])

	
	#generate and return the html
	return    unicode(tekstreplace(keys).substitute(movie_template) )



##########################################################################################################################
def write_html(movies, genres, web_dir):
	keys={}
	keys["%cssfile%"]=cssfile	
	keys["%jsfile%"]=jsfile

	if jsinline and os.path.exists(jsfile):
	 	with open(jsfile) as f:
	 		js_data ="<SCRIPT>\n"+f.read()+"</SCRIPT>" 
    		f.close()
	else:
		js_data=tekstreplace(keys).substitute(jsfile_template) 


	if cssinline and os.path.exists(cssfile):
	 	with open(cssfile) as f:
	 		css_data ="<STYLE>\n"+f.read()+"</STYLE>" 
    		f.close()
	else:
		css_data=tekstreplace(keys).substitute(cssfile_template) 

	genres.add("All")
	filter_html=''
	for genre in genres: 
		filter_html += "<div id='"+genre+"' class='filterbutton'><a href='#'>"+genre+"</a></div>"  
	
	watched_html='<input id="watchedbutton" type="checkbox" name="field" value="false"><label for="watchedbutton">Hide Watched</label> '
		

	#String[] allgenres 	= genres.toArray(new String[genres.size()])

	keys['%NAME%']		= gallery_name
	keys['%GENREFILTER%']	= "<div id='genrefilter' active='' decorated=''>"+filter_html+"</div>"
	keys['%WATCHEDFILTER%'] = "<div id='watchedfilter'>"+watched_html+"</div>"
	keys['%GENRES%']	= ','.join(genres)
	keys['%META%']		= meta_template
	keys['%MADEBY%']	= made_template
	keys['%PROJECTURL%']	= projectLink_template
	keys['%TMDBLOGO%']	= tmdblogo_template
	keys['%CSSFILE%']	= css_data
	keys['%JSFILE%']	= js_data
	keys['%MOVIE_HTML%']	= movies
	keys['%CREATED%']	= time.strftime("%Y.%m.%d@%H:%M:%S")
       
	f = io.open(os.path.join(web_dir, web_indexfile), 'w', encoding='utf-8')
	f.write(unicode(tekstreplace(keys).substitute(html_template) ))
	f.close()

##########################################################################################################################
def pushbullet_notification(apikey, movies, gallery, device):
    string_to_push = ''

    for movieid, movie in movies.iteritems():
         string_to_push += movie['label'] + ', '

    string_to_push = 'New movies added: ' + string_to_push[:-2] + '.'
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + apikey}
    payload = {'device_iden': device, 'type': 'note', 'title': gallery,
               'body': string_to_push}
    requests.post(url, data=json.dumps(payload), headers=headers)


##########################################################################################################################
if __name__ == "__main__":
    posters_to_retrieve = {}
    movies_html = ""
    counter = 1
    genres = set()	

    #load/set stuff when we want to verify the result
    if htmllint:
	try: 
    		import tempfile
		from tidylib import tidy_document
	except:
		htmllint=False
		out_dir=web_dir
		print "Failed to load the tempfile and tidylib python module: htmllint is disabled"
	finally:
		out_dir=tempfile.mkdtemp()
		print "htmllint enabled: building in: "+out_dir + " release to: " + web_dir

    else:
    	out_dir=web_dir

    #build a list with new movies
    new_movies={}
    print "Read new movies from KODI: in progress"+"\r",
    for i in get_new_movies_from_kodie(host,port):
	new_movies[i['movieid']]=i
    print "Read new movies from KODI: "+str(len(new_movies))+ " "*15

    #build a list with previous run movies from the cache
    print "Read movies from previous run: in progress"+"\r",
    if not os.path.isfile(moviecache):
	prev_movies={}
    else:
    	prev_movies=eval(open(moviecache, 'r').read())
	if not isinstance(prev_movies, dict): prev_movies={}
    print "Read movies from previous run: "+str(len(prev_movies))+ " "*15

    #query KODI
    print "Read movies from KODI: this can take a while...."+ " "*15+"\r",
    sys.stdout.flush()
    movies=get_movies_from_kodi(host, port)
    print "Read movies from KODI: "+str(len(movies))+ " "*30

    processed_movies={}
    for movie in movies:
	#display progress
	print "Movies processed: "+str(counter)+" / "+str(len(movies)) + " "*15+"\r",
    	sys.stdout.flush()

	#check out_dir and web_dir for posters
        foundposter = check_if_poster_exists(i['imdbnumber'], poster_size, out_dir)
	if not foundposter and htmllint:
        	foundposter = check_if_poster_exists(i['imdbnumber'], poster_size, web_dir)

	#add extra info to the movie for html generation mainly
        movie['counter']=counter;
	movie['poster_url']="posters/"+poster_size+"/"+movie['imdbnumber']+'.jpeg'
	movie['movieclass']	='old'
	if movie['movieid'] in new_movies:
		movie['movieclass']	='new' 	 	#set the background for new movies
		movie['watchedclass']	='newmovie'     #add a new ribbon, overrides by watched

#	elif not inlist(prev_movies,'movieid',movie['movieid']):
	elif not movie['movieid'] in prev_movies:
		movie['movieclass']='added'

	#generate html from the movie and append to the mainlist
        movies_html = (movies_html + create_movie_html_block(movie))
        
	#if in previous run there was no poster: try again
	if foundposter:
		if movie['movieid'] in prev_movies:
			if 'poster_url_source' in prev_movies[movie['movieid']]:
				if prev_movies[movie['movieid']]['poster_url_source'] == 'no-image' :
					foundposter = False

	#generate a list of posters we need to download
        if not foundposter or refreshposters:
            posters_to_retrieve[movie['movieid']]=movie

	#build unique list with genres
	for genre in movie['genre']:
		genres.add(genre)

	#store movie in indexed list
	processed_movies[movie['movieid']]=movie

	#the counter
        counter += 1
    
    #we like to have an indexed list (dict)
    movies=processed_movies	
    print ""


    #retrieve the posters
    counter = 0
    print "Download posters: in progress"+"\r",
    for movieid, movie in posters_to_retrieve.iteritems():
        counter += 1
        print "Download posters: "+ str(counter) + ' / ' + str(len(posters_to_retrieve)) +" "*20+"\r",
    	sys.stdout.flush()
     	url = get_poster_image_url(movie, tmdb_key, poster_size, language)
	movies[movieid]['poster_url_source']=url
        save_poster_image(url, movie['imdbnumber'], poster_size, out_dir)
    print "\nDownload posters: done"

    #write the actual HTML file: the result
    print "Write result to: " + os.path.join(out_dir,web_indexfile)
    write_html("<div id='movies'>"+movies_html+"</div>", genres, out_dir)

    #verify result (if configured) and release to website
    assetsUpdate=True;
    if htmllint: 
	print "Check result (htmllint) .. "
    	with open(os.path.join(out_dir, web_indexfile)) as f:
    		document, errors = tidy_document(f.read(),options={'numeric-entities':1, "show-warnings": htmllint_warnings })
    		f.close()
    		if len(errors) > 0:
                        assetsUpdate=False;
			print "we got some errors and will not release: "
			print error
   
   #update assets
    if assetsUpdate:
	if web_dir=='':
    		web_dir=os.getcwd()
	print "Copy assets to: "+web_dir 
	#copy the assets to the release dir
	mycopytree(os.path.join(scriptpath,"assets")		,os.path.join(web_dir,"assets"))
	
	#in case we use the htmllint we need to copy the result aswell from out_dir to the web_dir
	#todo: when inline=true do not copy css and js files
	if htmllint: 
		print "Copy posters to: "+web_dir 
		mycopytree(os.path.join(out_dir,"posters")		,os.path.join(web_dir,"posters"))
		print "Release result to website: "+web_dir 
		mycopytree(os.path.join(out_dir,web_indexfile)		,os.path.join(web_dir))

    	

    #write the movies to cache file
    target = open(moviecache, 'w')
    target.write(str(movies))


    #send to pushbullet
    if pushbullet_api_key != '':
        if len(posters_to_retrieve) != 0:
            pushbullet_notification(pushbullet_api_key,
                                    posters_to_retrieve, gallery_name,
                                    pushbullet_device_iden)





