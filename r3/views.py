from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from models import Routes
from BeautifulSoup import BeautifulSoup
import json as json
import urllib, re, nltk
import urllib2
from geopy import geocoders

origin = ''
destination = ''
leave_date = ''
return_date = ''
own_car = ''
can_drive = ''
driving_distance = ''
city_or = ''
city_dest = ''

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
	#ALGO HERE YO
	#MAKE THAT SHIT JSON!!!!
	#send it back to js
	message = origin + destination + leave_date + return_date + own_car
	return HttpResponse(json.dumps({"MESSAGE":message}), mimetype="application/json")

#python functions

def getLocations():
	origin = "Buffalo, NY 14226"
	destination = "206 Brownshill Road, Pittsburgh PA"
	g = geocoders.Google('AIzaSyBdM3HJM_ApE4VnOaCyjm4yk5SHAt5K_-k')
	(place, point) = g.geocode(origin)
	(new_place, new_point) = g.reverse(point)
	list1 = new_place.split(",")
	print point

	g2 = geocoders.Google('AIzaSyBdM3HJM_ApE4VnOaCyjm4yk5SHAt5K_-k')
	(place2, point2) = g2.geocode(destination)
	(new_place2, new_point2) = g.reverse(point2)
	list2 = new_place2.split(",")
	print point2

#Google Maps API
def getDirectionsDriving():
	api_driving = 'http://maps.googleapis.com/maps/api/directions/json?'
	origin_api = 'origin=' + urllib2.quote(origin)
	destination_api = 'destination=' + urllib2.quote(destination)
	final_drive = api_driving + origin_api + '&' + destination_api + '&sensor=false'
	response = urllib2.urlopen(final_drive)
	directions_drive = json.loads(response.read())
	distance = int(directions['routes'][0]['legs'][0]['distance']['text'][:2])
	duration = float(directions['routes'][0]['legs'][0]['duration']['value'])/(60)

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

def getBusPrices():
	bus_stop_codes = {'Abilene, TX': '391','Albany, NY': '89','Amherst, MA': '90','Angola, IN': '366','Ann Arbor, MI': '91','Athens, GA': '302','Atlanta, GA': '289','Austin, TX': '320','Baltimore, MD': '143','Big Spring, TX': '393','Binghamton, NY': '93','Birmingham, AL': '292','Boston, MA': '94','Brenham, TX': '335','Buffalo Airport, NY': '273','Buffalo, NY': '95','Burlington, VT': '96','Carthage, TX': '395','Champaign, IL': '98','Charlotte, NC': '99','Chattanooga, TN': '290','Chicago, IL': '100','Christiansburg, VA': '101','Cincinnati, OH': '102','Cleveland, OH': '103','Columbia City, IN': '373','Columbia, MO': '104','Columbus, OH': '105','Dallas/Fort Worth, TX': '317','Dayton-Trotwood, OH': '370','Del Rio, TX': '328','Des Moines, IA': '106','Detroit, MI': '107','Durham, NC': '131','Eagle Pass, TX': '327','East Lansing, MI': '330','El Paso, TX': '397','Elkhart, IN': '367','Fairhaven, MA': '316','Frederick, MD': '109','Ft. Wayne, IN': '365','Gainesville, FL': '296','Galveston, TX': '325','Gary, IN': '369','Giddings, TX': '401','Grand Rapids, MI': '331','Hampton, VA': '110','Harrisburg, PA': '111','Hartford, CT': '112','Houston, TX': '318','Humble, TX': '334','Indianapolis, IN': '115','Iowa City, IA': '116','Jacksonville, FL': '295','Kansas City, MO': '117','Kenton, OH': '362','Knoxville, TN': '118','La Grange, TX': '333','La Marque, TX': '337','Las Vegas, NV': '417','Lima, OH': '363','Little Rock, AR': '324','Livingston, TX': '402','Los Angeles, CA': '390','Louisville, KY': '298','Lubbock, TX': '403','Lufkin, TX': '404','Madison, U of Wisc, WI': '300','Madison, WI': '119','Memphis, TN': '120','Midland, TX': '405','Milwaukee, WI': '121','Minneapolis, MN': '144','Mobile, AL': '294','Montgomery, AL': '293','Morgantown, WV': '299','Muncie, IN': '372','Nacogdoches, TX': '406','Nashville , TN': '291','New Brunswick, NJ': '305','New Haven, CT': '122','New Orleans, LA': '303','New York, NY': '123','Newark, DE': '389','Norman, OK': '322','Oakland, CA': '413','Oklahoma City, OK': '323','Omaha, NE': '126','Orlando, FL': '297','Philadelphia, PA': '127','Pittsburgh, PA': '128','Plymouth, IN': '375','Portland, ME': '129','Prairie View, TX': '336','Princeton, NJ': '304','Providence, RI': '130','Richmond, IN': '371','Richmond, VA': '132','Ridgewood, NJ': '133','Riverside, CA': '416','Rochester, NY': '134','Sacramento, CA': '415','San Angelo, TX': '329','San Antonio, TX': '321','San Francisco, CA': '414','San Jose, CA': '412','Saratoga Springs, NY': '301','Secaucus, NJ': '135','Shreveport, LA': '332','South Bend, IN': '368','Sparks, NV': '419','Springfield, MO': '411','St Louis, MO': '136','State College, PA': '137','Storrs, CT': '138','Syracuse, NY': '139','Texarkana, AR': '407','Toledo, OH': '140','Toronto, ON': '145','Uvalde, TX': '326','Valparaiso, IN': '376','Van Wert, OH': '364','Warsaw, IN': '374','Washington, DC': '142'}
	origin_city = city_or
	destination_city = city_dest
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
	
	'''	
	for value in tickets_dics:
		for k,v in value.iteritems():
			print k,v
	'''
			
			

