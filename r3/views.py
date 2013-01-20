from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from models import Routes
from collections import defaultdict
import MySQLdb as mdb
import sys
from BeautifulSoup import BeautifulSoup
import json as json
import urllib, re, nltk, time
import urllib2
from geopy import geocoders
from math import radians, cos, sin, asin, sqrt
import jsonrpclib

leave_date = ''
return_date = ''
own_car = ''
can_drive = ''
driving_distance = ''
city_or = ''
city_dest = ''
time_weight = ''
cost_weight = ''


northeast = set(["Philadelphia, Pennsylvania (PHL)", "Boston, Massachusetts (BOS)", "Baltimore, Maryland (BWI)", "Hartford, Connecticut (BDL)", "New York, New York (JFK)", "New York, New York (LGA)", "Newark, New Jersey (EWR)", "Washington, D.C. (IAD)", "Washington, D.C. (DCA)"])
texas = set(["San Antonio, Texas (SAT)", "Austin, Texas (AUS)", "Dallas, Texas (DFW)", "Houston, Texas (IAH)", "Houston, Texas (HOU)"])
northwest = set(["Portland, Oregon (PDX)", "Seattle, Washington (SEA)"])
rockies = set(["Salt Lake City, Utah (SLC)", "Denver, Colorado (DEN)"])
california = set(["Los Angeles, California (LAX)", "San Francisco, California (SFO)", "Oakland, California (OAK)", "Sacremento, California (SMF)", "San Diego, California (SAN)", "San Jose, California (SJC)"])
midwest = set(["St Louis, Missouri (STL)", "Louisville, Kentucky (SDF)", "Indianapolis, Indiana (IND)"])
southwest = set(["Las Vegas, Nevada (LAS)", "Phoenix, Arizona (PHX)"])
florida = set(["Fort Lauderdale, Florida (FLL)", "Fort Meyers, Florida (RSW)", "Miami, Florida (MIA)", "Orlando, Florida (MCO)", "Tampa, Florida (TPA)"])
southeast = set(["Atlanta, Georgia (ATL)", "Memphis, Tennessee (MEM)", "Nashville, Tennessee (BNA)", "New Orleans, Louisiana (MSY)"])
greatLakes = set(["Minneapolis, Minnesota (MSP)", "Chicago, Illinois (MDW)", "Chicago, Illinois (ORD)", "Detroit, Michigan (DTW)"])
ohio = set(["Cleveland, Ohio (CLE)", "Cincinnati, Ohio (CVG)", "Columbus, Ohio (CMH)", "Pittsburgh, Pennsylvania (PIT)"])
northCarolina = set(["Charlotte, North Carolina (CLT)", "Raleigh, North Carolina (RDU)"])

total = northeast.union(texas).union(northwest).union(rockies).union(california).union(midwest).union(southwest).union(florida).union(southeast).union(greatLakes).union(ohio).union(northCarolina)


def hello(request):
	return render_to_response('index.html')

def find(request):
	if not request.is_ajax():
		return render_to_response('index.html')
	origin = request.POST['ori']
	destination = request.POST['dest']
	leave_date = request.POST['leave']
	return_date = request.POST['returnd']
	own_car = request.POST['own']
	can_drive = request.POST['can']
	cost_weight = request.POST['cost']
	time_weight = 10 - int(cost_weight)
	origin_point = getLocations(origin)
	destination_point = getLocations(destination)
	distance_driving, duration_driving = getDirectionsDriving(origin, destination)
	#distance_transit, duration_transit = getDirectionsTransit(origin, destination)
	if (own_car == 'true'):
		car_price = gasPrices(origin, destination)
	else:
		taxi_price = taxiPrices(origin, distance_driving)
	flight_call()
	getBusPrices(origin, destination)
	#ALGO HERE YO
	#MAKE THAT SHIT JSON!!!!
	#send it back to js
	message = origin + destination + leave_date + return_date + own_car
	return HttpResponse(json.dumps({"MESSAGE":message}), mimetype="application/json")

#python functions

def getLocations(address):
	origin = address
	g = geocoders.Google('AIzaSyBdM3HJM_ApE4VnOaCyjm4yk5SHAt5K_-k')
	(place, point) = g.geocode(origin)
	(new_place, new_point) = g.reverse(point)
	list1 = new_place.split(",")
	return point

#Google Maps API
def getDirectionsDriving(origin, destination):
	api_driving = 'http://maps.googleapis.com/maps/api/directions/json?'
	origin_api = 'origin=' + urllib2.quote(origin)
	destination_api = 'destination=' + urllib2.quote(destination)
	final_drive = api_driving + origin_api + '&' + destination_api + '&sensor=false'
	response = urllib2.urlopen(final_drive)
	directions_drive = json.loads(response.read())
	distance = int(directions_drive['routes'][0]['legs'][0]['distance']['text'][:2])
	duration = float(directions_drive['routes'][0]['legs'][0]['duration']['value'])/(60)
	return distance, duration

#Google Maps for Transit
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
	return distance, duration

def getBusPrices(city_or, city_dest):
	bus_stop_codes = {'Abilene, TX': '391','Albany, NY': '89','Amherst, MA': '90','Angola, IN': '366','Ann Arbor, MI': '91','Athens, GA': '302','Atlanta, GA': '289','Austin, TX': '320','Baltimore, MD': '143','Big Spring, TX': '393','Binghamton, NY': '93','Birmingham, AL': '292','Boston, MA': '94','Brenham, TX': '335','Buffalo Airport, NY': '273','Buffalo, NY': '95','Burlington, VT': '96','Carthage, TX': '395','Champaign, IL': '98','Charlotte, NC': '99','Chattanooga, TN': '290','Chicago, IL': '100','Christiansburg, VA': '101','Cincinnati, OH': '102','Cleveland, OH': '103','Columbia City, IN': '373','Columbia, MO': '104','Columbus, OH': '105','Dallas/Fort Worth, TX': '317','Dayton-Trotwood, OH': '370','Del Rio, TX': '328','Des Moines, IA': '106','Detroit, MI': '107','Durham, NC': '131','Eagle Pass, TX': '327','East Lansing, MI': '330','El Paso, TX': '397','Elkhart, IN': '367','Fairhaven, MA': '316','Frederick, MD': '109','Ft. Wayne, IN': '365','Gainesville, FL': '296','Galveston, TX': '325','Gary, IN': '369','Giddings, TX': '401','Grand Rapids, MI': '331','Hampton, VA': '110','Harrisburg, PA': '111','Hartford, CT': '112','Houston, TX': '318','Humble, TX': '334','Indianapolis, IN': '115','Iowa City, IA': '116','Jacksonville, FL': '295','Kansas City, MO': '117','Kenton, OH': '362','Knoxville, TN': '118','La Grange, TX': '333','La Marque, TX': '337','Las Vegas, NV': '417','Lima, OH': '363','Little Rock, AR': '324','Livingston, TX': '402','Los Angeles, CA': '390','Louisville, KY': '298','Lubbock, TX': '403','Lufkin, TX': '404','Madison, U of Wisc, WI': '300','Madison, WI': '119','Memphis, TN': '120','Midland, TX': '405','Milwaukee, WI': '121','Minneapolis, MN': '144','Mobile, AL': '294','Montgomery, AL': '293','Morgantown, WV': '299','Muncie, IN': '372','Nacogdoches, TX': '406','Nashville , TN': '291','New Brunswick, NJ': '305','New Haven, CT': '122','New Orleans, LA': '303','New York, NY': '123','Newark, DE': '389','Norman, OK': '322','Oakland, CA': '413','Oklahoma City, OK': '323','Omaha, NE': '126','Orlando, FL': '297','Philadelphia, PA': '127','Pittsburgh, PA': '128','Plymouth, IN': '375','Portland, ME': '129','Prairie View, TX': '336','Princeton, NJ': '304','Providence, RI': '130','Richmond, IN': '371','Richmond, VA': '132','Ridgewood, NJ': '133','Riverside, CA': '416','Rochester, NY': '134','Sacramento, CA': '415','San Angelo, TX': '329','San Antonio, TX': '321','San Francisco, CA': '414','San Jose, CA': '412','Saratoga Springs, NY': '301','Secaucus, NJ': '135','Shreveport, LA': '332','South Bend, IN': '368','Sparks, NV': '419','Springfield, MO': '411','St Louis, MO': '136','State College, PA': '137','Storrs, CT': '138','Syracuse, NY': '139','Texarkana, AR': '407','Toledo, OH': '140','Toronto, ON': '145','Uvalde, TX': '326','Valparaiso, IN': '376','Van Wert, OH': '364','Warsaw, IN': '374','Washington, DC': '142'}
	origin_city = 'New York, NY'
	destination_city = 'Philadelphia, PA'
	url = "http://us.megabus.com/JourneyResults.aspx?originCode=" + bus_stop_codes[origin_city] + "&destinationCode=" + bus_stop_codes[destination_city] + "&outboundDepartureDate=1%2f20%2f2013&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0"
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)
	cleaned_soup = nltk.clean_html(soup.prettify())
	x = False
	tickets = []
	y = cleaned_soup.split("\n")
	for line in y:
		if "Departs" in line:
			ticket = []
			x = True
		if "View" in line:
			try:
				tickets.append(ticket)
				x = False
			except:
				continue
		if x:
			ticket.append(line)
	tickets_dics = []
	current = time.mktime(time.gmtime())
	
	for ticket in tickets:
		ticket_dic = {}
		ticket_dic["origin_time"] = ticket[2]
		ticket_dic["origin_city"] = ticket[3]
		ticket_dic["origin_address"] = ticket[5]
		ticket_dic["destination_time"] = ticket[11]
		ticket_dic["destination_city"] = ticket[12]
		ticket_dic["destination_address"] = ticket[14]
		ticket_dic["duration"] = ticket[19]
		ticket_dic["price"] = ticket[32]
		tickets_dics.append(ticket_dic)
		r = Routes(origin = ticket[3], destination = ticket[12],  origin_address = ticket[5], origin_time = ticket[2], destination_address = ticket[4], \
			destination_time = ticket[11], brand = "Megabus", types="plane", cost = ticket[32], time = ticket[19], current_time = current)
		r.save()
	
	'''	
	for value in tickets_dics:
		for k,v in value.iteritems():
			print k,v
	'''

def gasPrices(origin, destination):
	from_address = origin
	to_address = destination
	new_from_address = from_address.replace(" ", "+")
	new_to_address = to_address.replace(" ", "+")
	url = "http://www.travelmath.com/cost-of-driving/from/" + new_from_address + "/to/" + new_to_address
	html = urllib.urlopen(url)
	for line in html:
		if "costofdriving" and "$" in line:
			one_way_cost = nltk.clean_html(line.split("one-way")[0].replace("$", ""))
			round_trip_cost = nltk.clean_html(line.split("one-way")[1].replace("round trip", "").replace("$", "")).replace('/ ', "")
			break
	fout.close()
	return one_way_cost

def taxiPrices(origin, duration):
	city = origin
	miles = duration
	url = "http://www.taxigrab.com/taxi-fare-calculator.php?city=" + city + "&passengers=1&miles=" + str(miles) + "&done=true&Submit=Calculate+taxi+fare"
	html = urllib.urlopen(url)
	for line in html:
		if "The estimated cost for your ride in" in line:
			cost = nltk.clean_html(line).split("$")[1].split("  ")[0]		
	print cost

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    miles = 0.621371 * km
    return miles

import heapq

def nearest_airports(current_lat, current_lon):
    haversine_values = []
    reverse_dic = {}
    for entry in total:
        dist = haversine_distance(current_lat, current_lon, float(entry.split(":")[1].split(",")[0]), float(entry.split(":")[1].split(",", [1])))
        haversine_values.append(dist)
        reverse_dic[dist] = entry
    three_smallest = heapq.nsmallest(3, haversine_values)
    airports = []
    for items in three_smallest:
        airports.append(reverse_dic[items])
    return airports


def getCity(code):
    for t in total:
        if code in t:
            return t[:-6]

def flight_call():
	service_url = 'https://apps.everbread.com/miniapi' 
	proxy = jsonrpclib.Server(service_url)
	departure_airport_code = ""
	arrival_airport_code = ""
	departure_date = ""
	return_date = ""
	request = {  
	    "user": "scwu",
	    "pass": "skk360Angelus",
	    "departure": "PHL",
	    "arrival": "SFO",
	    "departureDate": "2013-10-10",
	    "returnDate": "2013-10-20",
	    "airline": "",
	    "directFlightsOnly": False,
		"currency": "USD"
	}
	response = proxy.search(request)
	journeys = response['journeys']

	for j in range(3):
	    print "Journey: %s %s" % (j+1, journeys[j])
	    print "these"
	    origCode = journeys[j]['flights'][0]['departure']
	    print "are"
	    destCode = journeys[j]['flights'][0]['arrival']
	    print "the"
	    orig = getCity(origCode)
	    print 'orig ' + orig
	    print "times"
	    dest = getCity(destCode)
	    print "that"
	    deptTime = journeys[j]['flights'][0]['departureDate']
	    print "try"
	    arrivTime = journeys[j]['flights'][0]['arrivalDate']
	    print "men"
	    airline = journeys[j]['flights'][0]['carrier']
	    print "souls"
	    price = journeys[j]['price']
	    print "clara"
	    now = 'lalalala'
	    print "is"
	    duration = (float(journeys[j]['flights'][0]['miles'])/500) * 60
	    print "cool"
	    d = Routes(origin=orig, destination=dest, origin_address=origCode, origin_time=deptTime, destination_address=destCode, destination_time=arrivTime, brand=airline, types='plane', cost=price, time=duration, current_time=now)
	    print "catz"
	    d.save()

