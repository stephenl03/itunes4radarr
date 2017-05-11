# itunes4radarr
`python itunes4radarr.py`

Pulls the [iTunes Top 100 Movies](https://itunes.apple.com/us/rss/topmovies/limit=100/json) for Apple rss feed. Then pulls the title, hits the [OMDb API](http://www.omdbapi.com/) to get the IMDB ID, last, uses [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html) to put it all together in a file called 'topmovies.xml'

The file 'topmovies.xml' is then put up on the web to be utilized by [Radarr](https://radarr.video/)

**Requires**
* sys
* json
* datetime
* PyRSS2Gen
* requests
* urllib
* re

