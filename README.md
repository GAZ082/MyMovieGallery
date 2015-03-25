# MyMovieGallery
######A Python script for generating a HTML5 valid poster movie gallery from KODI/XBMC and The Movie Database.

<img align='middle' src='https://lh6.googleusercontent.com/-4O55ZZmjQxo/VRG5K3YZssI/AAAAAAAACbw/E8rIH1bHxU4/w804-h549-no/intro.png'>

###Requirements
* Python 2 or 3.
* python2-requests (or python3-requests).

###Configuration
1. You may put the directory assets and main.py anywhere you want.
2. Edit main.py and setup the server host and port if needed.
3. Name your gallery and change poster size if desired.
4. If running on Linux, make sure your destination directory has the proper
permissions to let the user running the script write files.
5. You may host main.py anywhere you want, just set where assets are, posters
and index.html will be written in the parameter web_dir.

###How It Works
1. Pulls all your movies from KODI. Gets IMDB ID, rating, synopsis, playcount
and label. On playcount > 0 the poster is marked with a red ribbon.
2. Checks if the poster is already in the assets/w### directory. If not,
downloads. If no directory is there, it creates. The posters downloaded are 2:3.
3. Once all posters were downloaded, generates index.html.
4. If no new posters are needed, it just recreated index.html but with the
latest information from KODI, ie, updated rating, if watched or not, etc.

###Final Words
This is an early release. Just tested on a Linux machine with python 2 and 3.
Please report any bugs and also do not be shy on suggesting things you would
like to see or corrected. Also, the code is available, so be free to look at it
and suggest corrections based not only on functionality but on good style and
performance.

Thanks for reading.

-Gabriel.
