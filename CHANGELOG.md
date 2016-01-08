

1.1 by rnijenhu
	+ changed some pyhton version diffs errors
		+ key not found fixed
		+ encoding error on write fixed
		+ cast for round/float to string
	+ Added these new functions:
		+ removed the config items to seperate file, and created an config.template
		+ made the HTML output strings configurable in config file
		+ added the possibility to use (kodi) keywords in the HTML templates
		+ HTML output shows new items (new for kodi and new for mymoviegallery) by settings a diff movie background
		+ verify result before writing to the website
		+ made the css inline (or not) configurable
		+ support javascript
		+ support more languages
		+ added an filter menu based on genre
		+ added a button for trailers (based on youtube trailers plugin). The button jumps to the site or uses the poster area.
		+ added a button imdb
		+ if case of no poster in previous run: try again
		+ support a range of aspect ratio's
		+ made it 'responsive'
	
	+todo:
		+ test it better!!!
		+ css is not bullet proof nor prefect, when fields are empty the poster is shifting 'off-grid'
		+ iframe youtube in poster should be better
		+ other poster size testing


1.0 initversion
