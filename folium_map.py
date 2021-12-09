import folium
from googlemaps_test import current_location_coord, destination_coord, steps_coord

f_map = folium.Map(location=current_location_coord)

# creates and adds marker on map, could use for start and stop
marker = folium.Marker(destination_coord)
marker.add_to(f_map)

# create line between two points
folium.PolyLine(steps_coord, color="green", weight=2.5, opacity=1).add_to(f_map)

# create empty html file
html_page = 'f_map.html'
# save map to html file
f_map.save(html_page)
