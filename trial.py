from geopy import geocoders



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

getLocations()