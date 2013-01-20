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
