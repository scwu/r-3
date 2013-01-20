import jsonrpclib

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

try:
    response = proxy.search(request)

    journeys = response['journeys']

    for j in range(len(journeys)):
        print "Journey: %s %s" % (j+1, journeys[j])
except:
    print "Error connecting to Miniapi service!"