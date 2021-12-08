import gmplot # Need this to be pip installed for into work

lat = [53.8711] # need variables to plot this on map
longitude = [2.3931] # need variables to plot this on map

map1=gmplot.GoogleMapPlotter(53.8711, 2.3931,15)# give latitude, longitiude values - the number relates to zoom level
map1.scatter(lat,longitude, 'red', size=50,marker=True)
map1.plot(lat,longitude,'blue', edge_width=2.5)
map1.draw("map.html") #this actually creates the map