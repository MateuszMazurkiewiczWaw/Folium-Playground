import folium
import pandas
import requests


def color_producer(population):
    if population < 100000:
        return 'darkblue'
    elif 100000 <= population < 300000:
        return 'cadetblue'
    elif 300000 <= population < 500000:
        return 'lightblue'
    elif 500000 <= population < 1000000:
        return 'blue'
    elif 1000000 <= population < 1500000:
        return 'lightgreen'
    elif 1500000 <= population < 2000000:
        return 'green'
    elif 2000000 <= population < 3000000:
        return 'darkgreen'
    elif 3000000 <= population < 5000000:
        return 'orange'
    elif 5000000 <= population < 10000000:
        return 'lightred'
    else:
        return 'red'


world_countries_geo = requests.get(
    'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json').json()
countries_fields = ['Country', 'Year_2016']
countries_data = pandas.read_csv('population-figures-by-country.csv', skipinitialspace=True, usecols=countries_fields)
cities_data = pandas.read_csv('MajorCities1.txt')

world_map = folium.Map(location=[52.229675, 21.012230], zoom_start=3, tiles='Stamen Toner')  # tiles='Stamen Terrain')

# list of the threshold population values
threshold_values = list([0, 0.25 * max(countries_data['Year_2016']), 0.5 * max(countries_data['Year_2016']),
                         0.75 * max(countries_data['Year_2016']), max(countries_data['Year_2016'])])

print(threshold_values)

folium.Choropleth(
    geo_data=world_countries_geo,
    name='choropleth',
    data=countries_data,
    columns=['Country', 'Year_2016'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    bins=threshold_values,
    legend_name='World countries by population',
    reset=True
).add_to(world_map)

fgCities = folium.FeatureGroup(name='MajorCities')

for lt, ln, ci, pop in zip(list(cities_data['Latitude']), list(cities_data['Longitude']), list(cities_data['City']),
                           list(cities_data['Population'])):
    fgCities.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(ci) + ' ' + str(pop) + ' inhabitants',
                                           fill_color=color_producer(int(pop)), fill=True, color='grey',
                                           fill_opacity=0.7))

fgPopulation = folium.FeatureGroup(name='Population')

fgPopulation.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                      style_function=lambda x: {
                                          'fillColor': '#fecc5c' if x['properties']['POP2005'] < 10000000
                                          else '#fd8d3c' if 10000000 <= x['properties']['POP2005'] < 20000000
                                          else '#f03b20' if 20000000 <= x['properties']['POP2005'] < 40000000
                                          else '#bd0026'}))

world_map.add_child(fgCities)
world_map.add_child(fgPopulation)
world_map.add_child(folium.LayerControl())

world_map.save('WorldMap.html')
