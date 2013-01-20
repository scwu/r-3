import jsonrpclib

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

def getCity(code):
    for t in total:
        if code in t:
            return t[:-6]

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
        d = Routes(origin=orig,destination=dest,origin_address=deptCode,origin_time=deptTime,destination_address=arrivalCode,destination_time=arrivTime,brand=airline,types='plane',cost=price,time=duration, current_time=now)
        print "catz"
        d.save()
except:
    print "Error connecting to Miniapi service!"