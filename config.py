# --------------------------CONFIGURATION PARAMETERS---------------------------#

host = 'pi:raspberry@192.168.2.3'
# KODI host (ip, hostname). Change this to suit your needs.
	# format (user:pwd@host) or just the host
port = '8080'
# This is the default KODI's port.
gallery_name = 'My Movie Gallery'
tmdb_key = 'f8860327b25dbbe0d96d9e5d1db91779'
poster_size = 'w185'
# 'w92', 'w154', 'w185', 'w342', 'w500'.
language = ['en', 'nl', ''] 
# English language has the largest poster collection on TMDB. 
web_dir = ''
# Optional. In case you want to host the script in a different dir.
# Directory 'assets' must be in the same dir than main.py
pushbullet_api_key = ''
# Optional. Your PB Access token. If value is other than '', notifications will
# be activated.
pushbullet_device_iden = ''
# Your device iden. Use pb_devices.py script to get your device's iden.
limit=2

#get posters once, now it will get new posters each time 
refreshposters=True

#use htmllint, it will check the result before releasing it to web_dir
htmllint=True

cssfile='assets/styles.css'
cssinline=True
#use cssfile inline instead of a cssfile_template reference

projectLink_template ="<a href='https://github.com/GAZ082/MyMovieGallery'>Project link.</a>"
made_template 		='Made by Gabriel A. Zorrilla / rnijenhu'

cssfile_template	="<link rel='stylesheet' type='text/css' href='assets/styles.css'>"

tmdblogo_template 	="<img src='assets/tmdb.svg' alt='www.themoviedb.org'>"

meta_template 		=("<meta name='author' content='Gabriel A. Zorrilla'>" + 
			"<meta name='keywords' content='KODI, XBMC, movie, gallery, HTML5'>" + 
			"<meta name='description' content='My Movie Gallery: Python script to show your KODI movies to the world!'>" +
            		"<meta charset='UTF-8'>")

trailer_template	="<div class='trailer'><a href='%trailerurl%'><img src='assets/youtube.png' alt='youtube'> </a></div>"

html_template =("<!DOCTYPE html><html><head><title>%NAME%</title>%META% %CSSFILE% </head>"+
			       "<body><div id='container'><div id='gallery_name'> %NAME% </div> %MOVIE_HTML% <div id='line'></div>"+
                "<div id='footer'> Movie list updated on: %CREATED% <br> %MADEBY% <br> %PROJECTURL% <br>Thanks to:<br><br> %TMDBLOGO%</div></div></body></html>")
              
              
movie_template=("\n<div class='movie'><div class='%watchedclass%'></div><img src='%poster_url%' alt='%label%' title='%plot%'><br>"+ 
					"<div class='star_container'>%starshtml% </div><div class='movietext'>"+
					"<div class='originaltitle'>%originaltitle%</div>"+
					"<div class='genre'>%genre%</div>"+
					"<div class='year'>%year%</div>%trailerhtml%"+
					"</div></div>")
