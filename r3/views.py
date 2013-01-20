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
import datetime

leave_date = ''
return_date = ''
own_car = ''
can_drive = ''
driving_distance = ''
city_or = ''
city_dest = ''
time_weight = ''
cost_weight = ''

ddate = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}

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

old_total = northeast.union(texas).union(northwest).union(rockies).union(california).union(midwest).union(southwest).union(florida).union(southeast).union(greatLakes).union(ohio).union(northCarolina)
data = [[ 1077, "DBBDA5AA-2EE6-47FE-98BE-DF3CB104B117", 1077, 1247781711, "278324", 1247781711, "278324", None, "PHX", "33.43416667", "112.0116667" ]
, [ 1418, "4FE7EA2A-5576-4141-8624-AAFFE038D04F", 1418, 1247781711, "278324", 1247781711, "278324", None, "LAX", "33.9425", "118.4072222" ]
, [ 1473, "A7BF2538-20C0-4E4B-BF68-8319C57101FE", 1473, 1247781711, "278324", 1247781711, "278324", None, "OAK", "37.72138889", "122.2208333" ]
, [ 1557, "81262588-4853-41B2-BCB3-BAD40AA9870C", 1557, 1247781711, "278324", 1247781711, "278324", None, "SMF", "38.69555556", "121.5908333" ]
, [ 1570, "C2ABA99C-2D7C-4450-8A37-1E7643C0FA2D", 1570, 1247781711, "278324", 1247781711, "278324", None, "SAN", "32.73361111", "117.1897222" ]
, [ 1572, "EFD7BDD1-8F72-43A3-97D0-2FE925CC463F", 1572, 1247781711, "278324", 1247781711, "278324", None, "SFO", "37.61888889", "122.375" ]
, [ 1574, "91DAC48B-F644-47D2-BA77-FFF709AAD055", 1574, 1247781711, "278324", 1247781711, "278324", None, "SJC", "37.36277778", "121.9291667" ]
, [ 1754, "FDDFAC0D-F3F7-4A41-9FB1-CF9E9F6F959F", 1754, 1247781712, "278324", 1247781712, "278324", None, "DEN", "39.86166667", "104.6730556" ]
, [ 1998, "14840B7E-6A42-4939-A21C-08814B43AA2D", 1998, 1247781712, "278324", 1247781712, "278324", None, "BDL", "41.93888889", "72.68333333" ]
, [ 1999, "F432E60A-F809-4BE9-BA86-D43763F5246F", 1999, 1247781712, "278324", 1247781712, "278324", None, "DCA", "38.85222222", "77.03777778" ]
, [ 2000, "2E501AE3-BA30-4630-9E3E-856B9A47CF89", 2000, 1247781712, "278324", 1247781712, "278324", None, "IAD", "38.9475", "77.46" ]
, [ 2168, "34158DC4-E23F-4536-B937-FE63859CEF64", 2168, 1247781712, "278324", 1247781712, "278324", None, "FLL", "26.07258333", "80.15277778" ]
, [ 2175, "9729F85D-3E82-46A3-87FA-C682EA404C90", 2175, 1247781712, "278324", 1247781712, "278324", None, "RSW", "26.53616667", "81.75527778" ]
, [ 2352, "49677427-6C16-4AB8-9A3E-17290D7207A8", 2352, 1247781712, "278324", 1247781712, "278324", None, "MIA", "25.79325", "80.29055556" ]
, [ 2409, "A22D5203-43A7-453B-BBE1-493F09231BD7", 2409, 1247781712, "278324", 1247781712, "278324", None, "MCO", "28.42944444", "81.30888889" ]
, [ 2489, "875E0B07-053D-4B24-9A0E-D79E6D37EF15", 2489, 1247781712, "278324", 1247781712, "278324", None, "TPA", "27.97555556", "82.53333333" ]
, [ 2551, "C63A7D5E-EF7F-43C1-AA81-06B7E0BEFBB3", 2551, 1247781712, "278324", 1247781712, "278324", None, "ATL", "33.63666667", "84.42805556" ]
, [ 3401, "A301A865-E3A1-4370-9E88-88B54EB7558B", 3401, 1247781713, "278324", 1247781713, "278324", None, "MDW", "41.78611111", "87.7525" ]
, [ 3402, "2D1D5A78-6E35-4E28-991E-3C43594EC66E", 3402, 1247781713, "278324", 1247781713, "278324", None, "ORD", "41.98083333", "87.90666667" ]
, [ 4046, "D59E436E-4332-443B-B870-45389538312E", 4046, 1247781714, "278324", 1247781714, "278324", None, "IND", "39.71722222", "86.29472222" ]
, [ 4686, "44172A7D-52F1-4C89-BF08-4EF1D0DAB482", 4686, 1247781715, "278324", 1247781715, "278324", None, "CVG", "39.04888889", "84.66777778" ]
, [ 4742, "5B01F7C1-E98E-4477-BDCF-1334CF0D81D1", 4742, 1247781715, "278324", 1247781715, "278324", None, "SDF", "38.17416667", "85.73638889" ]
, [ 4961, "5C9A5CE2-70B2-4EF1-BA8C-E84A232693DA", 4961, 1247781715, "278324", 1247781715, "278324", None, "MSY", "29.99333333", "90.25805556" ]
, [ 5042, "91CE1137-C0D9-4697-BD46-F1ED3BD28E3D", 5042, 1247781715, "278324", 1247781715, "278324", None, "BOS", "42.36305556", "71.00638889" ]
, [ 5116, "38B70172-DCF3-4527-98DE-47775AAB8D48", 5116, 1247781715, "278324", 1247781715, "278324", None, "BWI", "39.17527778", "76.66833333" ]
, [ 5456, "C2CCE0B6-DA62-444C-A829-7469DAB8C420", 5456, 1247781716, "278324", 1247781716, "278324", None, "DTW", "42.2125", "83.35333333" ]
, [ 5951, "7DE6D229-0223-424B-9D0C-A5FFCD3A408A", 5951, 1247781717, "278324", 1247781717, "278324", None, "MSP", "44.88194444", "93.22166667" ]
, [ 6412, "31D61A5E-4841-4154-A9F0-26C63AA73269", 6412, 1247781719, "278324", 1247781719, "278324", None, "STL", "38.74861111", "90.37" ]
, [ 6937, "F4ED528A-2050-4217-9B41-1EBFBFB2F29F", 6937, 1247781720, "278324", 1247781720, "278324", None, "CLT", "35.21388889", "80.94305556" ]
, [ 7124, "73E89DC0-B023-4ED0-9402-E533E39464F8", 7124, 1247781720, "278324", 1247781720, "278324", None, "RDU", "35.87777778", "78.7875" ]
, [ 7797, "B2115F13-FD3E-4925-BBBE-050CEB39E950", 7797, 1247781720, "278324", 1247781720, "278324", None, "EWR", "40.6925", "74.16861111" ]
, [ 8026, "8040FF66-50F6-419A-B5E1-94BAEE4583E8", 8026, 1247781720, "278324", 1247781720, "278324", None, "LAS", "36.08", "115.1522222" ]
, [ 8328, "C2C19C37-87BD-4B85-968F-8648B6095E4E", 8328, 1247781720, "278324", 1247781720, "278324", None, "JFK", "40.63972222", "73.77888889" ]
, [ 8329, "CA9F7C64-29EB-4EB9-AD36-480920BB18C5", 8329, 1247781720, "278324", 1247781720, "278324", None, "LGA", "40.77722222", "73.8725" ]
, [ 8582, "439F1A52-0DEB-434B-8B08-D873CD82CDC1", 8582, 1247781721, "278324", 1247781721, "278324", None, "CLE", "41.40944444", "81.855" ]
, [ 8597, "3F0AA6CB-BDF7-43C0-8FF9-F9D7E78554E5", 8597, 1247781721, "278324", 1247781721, "278324", None, "CMH", "39.99805556", "82.89194444" ]
, [ 9516, "A4C4DBE5-A2C0-4BC8-B56D-0A3E20470D1B", 9516, 1247781723, "278324", 1247781723, "278324", None, "PDX", "45.58833333", "122.5975" ]
, [ 9915, "0B4013FF-AFAE-4A0F-82D9-B86D30EF12DB", 9915, 1247781723, "278324", 1247781723, "278324", None, "PHL", "39.87222222", "75.24083333" ]
, [ 9922, "4BCBAD0E-26C1-4299-B11C-239A6E97723B", 9922, 1247781723, "278324", 1247781723, "278324", None, "PIT", "40.49138889", "80.23277778" ]
, [ 10500, "99AB006A-46D3-447C-83F2-4D6B3D9CBB0A", 10500, 1247781723, "278324", 1247781723, "278324", None, "MEM", "35.0425", "89.97666667" ]
, [ 10521, "22F35316-1478-4D13-A959-1C6C2DE2700B", 10521, 1247781723, "278324", 1247781723, "278324", None, "BNA", "36.12444444", "86.67833333" ]
, [ 10653, "260752C9-B451-4F32-AAD8-58D88C446D9B", 10653, 1247781723, "278324", 1247781723, "278324", None, "AUS", "30.19444444", "97.67" ]
, [ 10939, "792305E9-0EF6-42B7-882F-C5D7E2917F86", 10939, 1247781723, "278324", 1247781723, "278324", None, "DFW", "32.89694444", "97.03805556" ]
, [ 11241, "B5245FB3-C8D5-4B70-A6B2-84E972BCB104", 11241, 1247781724, "278324", 1247781724, "278324", None, "IAH", "29.98444444", "95.34138889" ]
, [ 11252, "F2EDD6B3-2BD0-43DF-826C-A07D2C2CEE86", 11252, 1247781724, "278324", 1247781724, "278324", None, "HOU", "29.64555556", "95.27888889" ]
, [ 11747, "9077B71E-73E0-45F2-BF7F-57D1E6DA14FD", 11747, 1247781725, "278324", 1247781725, "278324", None, "SAT", "29.53361111", "98.46972222" ]
, [ 12102, "AFAEEAF9-BFE7-40A7-9619-319DC0023CDD", 12102, 1247781725, "278324", 1247781725, "278324", None, "SLC", "40.78833333", "111.9777778" ]
, [ 12722, "0A79FEDD-35E4-4735-8488-F279C76DCD9C", 12722, 1247781725, "278324", 1247781725, "278324", None, "SEA", "47.45", "122.3116667" ]
 ]
def createsData():
	total = set([])
	for entry in old_total:
		for entry2 in data:
			x = "(" + entry2[8] + ")"
			if x == entry.split(" ")[-1]:
				total.add(entry + ": " + entry2[9] + ", " + entry2[-1])
	return total
	

def hello(request):
	return render_to_response('index.html')

def find(request):
	if not request.is_ajax():
		return render_to_response('index.html')
	origin = request.POST['ori']
	destination = request.POST['dest']
	leave_date = request.POST['leave']
	return_date = request.POST['returnd']
	oday, omonth, oyear = leave_date.split("/")
	leave_month = ddate[omonth]
	rday, rmonth, ryear = return_date.split("/")
	return_month = ddate[rmonth]
	leave_date = oyear + "-" + leave_month + "-" + oday
	return_date = ryear + "-" + return_month + "-" + rday
	own_car = request.POST['own']
	can_drive = request.POST['can']
	cost_weight = request.POST['cost']
	time_weight = 10 - int(cost_weight)
	origin_point = getLocations(origin)
	destination_point = getLocations(destination)
	lat = origin_point[0]
	longi = origin_point[1]
	nearest_ori = nearest_airports(float(lat), float(longi))
	latd= destination_point[0]
	longid = destination_point[1]
	nearest_dest = nearest_airports(float(latd), float(longi))
	count = 1
	while count < 3:
		getBusPrices(nearest_dest[0].split("(")[0], nearest_dest[count].split("(")[0], leave_date)
		count += 1
	for o in nearest_ori:
		airport_code_o = o.split(":")[0].split(" ")[-1]
		for d in nearest_dest:
			airport_code_d = d.split(":")[0].split(" ")[-1]
			flight_call(airport_code_o, airport_code_d, leave_date, return_date)

	distance_driving, duration_driving = getDirectionsDriving(origin, destination)
	#distance_transit, duration_transit = getDirectionsTransit(origin, destination)
	if (own_car == 'true'):
		car_price = gasPrices(origin, destination)
	else:
		taxi_price = taxiPrices(nearest_dest[0].split("(")[0], distance_driving)
	main(nearest_dest[0].split("(")[0], nearest_dest[1].split("(")[0])
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
	try:
		d = Routes.objects.get_or_create(origin=origin, destination=destination, origin_address=origin, origin_time='', destination_address=destination, destination_time='', brand='car', types='car', cost=gasPrices(origin, destination), time=duration, current_time='now')
		d.save()
	except:
		pass
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
	try:
		d = Routes.objects.get_or_create(origin=origin, destination=destination, origin_address=origin, origin_time='', destination_address=destination, destination_time='', brand='transit', types='transit', cost='3.00', time='duration', current_time='now')
		d.save()
	except:
		pass
	return distance, duration

def getBusPrices(city_or, city_dest, date):
	year, month, day = date.split("-")
	bus_stop_codes = {'Albany': '89','State College': '137','Ridgewood': '133','Newark': '389','Toledo': '140','San Francisco': '414','Columbia': '104','Champaign': '98','El Paso': '397','Ann Arbor': '91','Atlanta': '289','Morgantown': '299','Uvalde': '326','Mobile': '294','Storrs': '138','Big Spring': '393','Texarkana': '407','Montgomery': '293','Charlotte': '99','East Lansing': '330','Cincinnati': '102','Washington': '142','Minneapolis': '144','Durham': '131','Gary': '369','Rochester': '134','Sparks': '419','Knoxville': '118','Gainesville': '296','Burlington': '96','Muncie': '372','Nacogdoches': '406','Kenton': '362','Pittsburgh': '128','Giddings': '401','Del Rio': '328','New Orleans': '303','Eagle Pass': '327','Los Angeles': '390','San Antonio': '321','Syracuse': '139','Fairhaven': '316','San Jose': '412','Iowa City': '116','Brenham': '335','Buffalo': '95','Madison': '119','Angola': '366','Boston': '94','Valparaiso': '376','Las Vegas': '417','Amherst': '90','Sacramento': '415','Elkhart': '367','La Grange': '333','Midland': '405','Carthage': '395','Saratoga Springs': '301','Richmond': '132','Providence': '130','Louisville': '298','Riverside': '416','Columbus': '105','Indianapolis': '115','Norman': '322','South Bend': '368','Chicago': '100','Van Wert': '364','Binghamton': '93','Shreveport': '332','Orlando': '297','Dayton-Trotwood': '370','Memphis': '120','Toronto': '145','Princeton': '304','Humble': '334','Little Rock': '324','Detroit': '107','Philadelphia': '127','Dallas/Fort Worth': '317','Livingston': '402','Austin': '320','New Brunswick': '305','Prairie View': '336','New York': '123','Birmingham': '292','Cleveland': '103','Oklahoma City': '323','Lima': '363','Abilene': '391','Lubbock': '403','Athens': '302','Buffalo Airport': '273','St Louis': '136','Springfield': '411','Ft. Wayne': '365','Harrisburg': '111','Grand Rapids': '331','Hartford': '112','La Marque': '337','Columbia City': '373','Jacksonville': '295','San Angelo': '329','Chattanooga': '290','Omaha': '126','Nashville ': '291','Frederick': '109','Kansas City': '117','Plymouth': '375','Lufkin': '404','Baltimore': '143','Galveston': '325','Houston': '318','Hampton': '110','New Haven': '122','Christiansburg': '101','Des Moines': '106','Milwaukee': '121','Portland': '129','Oakland': '413','Secaucus': '135','Warsaw': '374'}
	origin_city = city_or.split(",")[0].strip()
	destination_city = city_dest.split(",")[0].strip()
	url = "http://us.megabus.com/JourneyResults.aspx?originCode=" + bus_stop_codes[origin_city] + "&destinationCode=" + bus_stop_codes[destination_city] + "&outboundDepartureDate=" + month + "%2f" + day + "%2f" + year + "&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0"
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
		try:
			r = Routes.objects.get_or_create(origin = ticket[3], destination = ticket[12],  origin_address = ticket[5], origin_time = ticket[2], destination_address = ticket[4], \
			destination_time = ticket[11], brand = "Megabus", types="bus", cost = ticket[32], time = ticket[19], current_time = current)
			r.save()
		except: 
			pass
	
	'''	
	for value in tickets_dics:
		for k,v in value.iteritems():
			print k,v
	'''

def gasPrices(origin, destination):
	one_way_cost = ''
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
    total = createsData()
    for entry in total:
        dist = haversine(current_lat, current_lon, float(entry.split(":")[1].split(",")[0]), float(entry.split(":")[1].split(",")[1]))
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

def flight_call(origin, destination, rdate, odate):
	print origin
	print destination
	service_url = 'https://apps.everbread.com/miniapi' 
	proxy = jsonrpclib.Server(service_url)
	request = {  
	    "user": "scwu",
	    "pass": "skk360Angelus",
	    "departure": origin[1:4],
	    "arrival": destination[1:4],
	    "departureDate": rdate,
	    "returnDate": odate,
	    "airline": "",
	    "directFlightsOnly": False,
		"currency": "USD"
	}
	try: 
		if not Routes.objects.filter(origin=orig, destination=dest).exists():

			response = proxy.search(request)
			journeys = response['journeys']

			for j in range(3):
			    print "Journey: %s %s" % (j+1, journeys[j])
			    origCode = journeys[j]['flights'][0]['departure']
			    destCode = journeys[j]['flights'][0]['arrival']
			    orig = getCity(origCode)
			    dest = getCity(destCode)
			    deptTime = journeys[j]['flights'][0]['departureDate']
			    arrivTime = journeys[j]['flights'][0]['arrivalDate']
			    airline = journeys[j]['flights'][0]['carrier']
			    price = journeys[j]['price']
			    now = 'lalalala'
			    duration = (float(journeys[j]['flights'][0]['miles'])/500) * 60
			    d = Routes.objects.get_or_create(origin=orig, destination=dest, origin_address=origCode, origin_time=deptTime, destination_address=destCode, destination_time=arrivTime, brand=airline, types='plane', cost=price, time=duration, current_time=now)
			    d.save()
	except:
		pass

def processTime(t):

	if(t == ''):
		return 0;

	#if no minutes
	elif not "min" in t:
		justHours = ""
		for char in t:
			if(char == 'h'):
				break 
			else:
				justHours += char
		return 60*float(justHours)

	else:
		hours = ""
		minutes = ""
		for char in t:
			if(char == 'h'):
				break
			else:
				hours += char

		minutes = t.strip().replace("hrs", "").replace("min", "").replace("s", "").split(" ")[1]

		print minutes
		if minutes.strip() == '0m':
			return 60*int(hours)
		else:
			return 60*int(hours) + int(minutes)


def averageValues(ori, d):
	info = Routes.objects.filter(origin=ori, destination=d)

	sumCost = 0;
	sumTime = 0;

	for i in info:
		try:
			sumCost += float(i.cost.strip()[1:].strip('u'))
			sumTime += processTime(i.time)
		except Exception:
			pass

	return ((sumCost)/len(info)), ((sumTime)/len(info))

def calculateWeight(entry, avgC, avgT):
	#import this somehow
	timeWeight = 0.8
	costWeight = 0.2
	try:
		entryTime = processTime(entry.time)
		entryCost = float(entry.cost.strip()[1:])
	except Exception:
		entryCost = 10.00
		entryTime = 10
		pass

	avgTime = float(avgT)
	avgCost = float(avgC)

	if avgCost == 0 or avgTime == 0:
		return 0
	return (costWeight * (entryCost/avgCost)) + (timeWeight * (entryTime/avgTime))

def generateGraph():
	con = None
	try:
		
		v = defaultdict(lambda : defaultdict(str))
		e = defaultdict(lambda : defaultdict(str))

		for d in Routes.objects.all():
			print d.origin
			print d.destination
			avgC, avgT = averageValues(str(d.origin), str(d.destination))
			if(v[d.origin][d.destination] == ''):
				v[d.origin][d.destination] = calculateWeight(d, avgC, avgT)
				e[d.origin][d.destination] = d.types + " " + str(d.cost)
			elif(v[d.origin][d.destination] > calculateWeight(d, avgC, avgT)):
				e[d.origin][d.destination] = d.types + " " + str(d.cost)
				v[d.origin][d.destination] = calculateWeight(d, avgC, avgT)
			else:	
				continue #dont do anything

		#print v.keys()
		return v, e

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if con:
			con.close()

def initialize(graph, origin):
	d = {} #destination
	p = {} #predecessor
	for node in graph.keys():
		d[node] = 9999
		p[node] = 0
	d[origin] = 0
	return d, p

def relax(node, neighbor, graph, d, p):
	try:
		if (d[neighbor] > d[node] + graph[node][neighbor]) :
			d[neighbor] = d[node] + graph[node][neighbor]
			p[neighbor] = node
	except:
		pass

def bellman_ford(graph, origin):
	d, p = initialize(graph, origin)
	for i in range(len(graph) - 1):
		for u in graph.keys():
			for v in graph[u].keys():
				relax(u, v, graph, d, p)
	return d, p

def getPath(root, leaf, pred):
	if(leaf == root):
		return root
	else:
		try:
			return getPath(root, pred[leaf.strip()], pred) + "-->" + leaf
		except:
			return leaf 

def main(source, destination):
	vertices, edges = generateGraph()
	
	d, p = bellman_ford(vertices, source)

	print edges
	path = getPath(source, destination, p)

	print path
