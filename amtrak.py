import urllib2
import urllib
import simplejson
import pprint

def hi():
	api_driving = 'http://maps.googleapis.com/maps/api/directions/json?'
	origin_api = 'origin=' + urllib2.quote("32 Endicott Drive, Amherst New York")
	destination_api = 'destination=' + urllib2.quote("206 Brownshill Road, Pittsburgh Pennsylvania")
	final_drive = api_driving + origin_api + '&' + destination_api + '&sensor=false'
	response = urllib2.urlopen(final_drive)
	directions_drive = simplejson.loads(response.read())
	print directions_drive
hi()