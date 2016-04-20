# MyMovieGallery
######A Python script for generating a HTML5 valid poster movie gallery from KODI/XBMC and The Movie Database.

<img align='middle' src='https://lh6.googleusercontent.com/-4O55ZZmjQxo/VRG5K3YZssI/AAAAAAAACbw/E8rIH1bHxU4/w804-h549-no/intro.png'>

###Features
* HTML5 valid code, so it renders fine in a myriad of devices such as phones,
tablets and browsers.
* Watched movie ribbon.
* Reference to imdb and trailers
* Filter by genre and hide watched
* 5 stars ratings.
* Customizable layout 
* Able to download several poster sizes.
* PushBullet notification to a device.
* Movie synopsis when you roll over the poster.
* Eye candy ;-).

###Requirements
* Python 2 or 3.
* python2-requests (or python3-requests).

###Configuration
1. Make sure you put the directory 'assets' in the 'web_server' you specified. main.py may be everywhere (your home dir for example, away from the public server directory, for better security).
2. Edit main.py and setup the server host and port if needed.
3. Name your gallery and change poster size if desired.
4. If running on Linux, make sure your destination directory has the proper
permissions to let the user running the script write files.
5. You may host main.py anywhere you want, just set where assets are, posters
and index.html will be written in the parameter web_dir.
6. If you want to know when new movies are added, you may configure PushBullet.
Use the provided pb_devices.py script to get your devices iden (first you need a
pushbullet Access Token https://www.pushbullet.com/account).

###How It Works
1. Pulls all your movies from KODI. Gets IMDB ID, rating, synopsis, playcount
and label. On playcount > 0 the poster is marked with a red ribbon.
2. Checks if the poster is already in the assets/w### directory. If not,
downloads. If no directory is there, it creates. The posters downloaded are 2:3.
3. Once all posters were downloaded, generates index.html.
4. If no new posters are needed, it just recreated index.html but with the
latest information from KODI, ie, updated rating, if watched or not, etc.

###Liked it? Tip me!: http://gaz082.tip.me/

###Final Words
This is an early release. Just tested on a Linux machine with python 2 and 3.
Please report any bugs and also do not be shy on suggesting things you would
like to see or corrected. Also, the code is available, so be free to look at it
and suggest corrections based not only on functionality but on good style and
performance.

Thanks for reading.

-Gabriel.
