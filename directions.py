import urllib2
import simplejson as json

def getDirectionsTransit(origin, destination, time):
	api_str = 'http://maps.googleapis.com/maps/api/directions/json?'
	origin_str = 'origin=' + urllib2.quote(origin)
	destination_str = 'destination=' + urllib2.quote(destination)
	time_str = 'departure_time=' + time#will have to convert to epoch 
	final_str = api_str + origin_str + '&' + destination_str + '&sensor=false' + '&' + time_str + '&mode=transit'
	response = urllib2.urlopen(final_str)
	directions = json.loads(response.read())
	distance = int(directions['routes'][0]['legs'][0]['distance']['text'][:2])
	duration = float(directions['routes'][0]['legs'][0]['duration']['value'])/(60)