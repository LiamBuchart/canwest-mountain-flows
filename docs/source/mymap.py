# %% [markdown]
# # A Markdown cell
# - You can do all the fun stuff markdown has to offer


#%%
# Imports
import pandas as pd
import folium
import numpy as np

import requests
import json
import geojson

# %% [markdown]
# # Pull Data from the native-land.ca API
# Territory and Name overlays come from Native Land Digital 
# ---
# [blue_text](native-land.ca)

# %%
url = "https://native-land.ca/wp-json/nativeland/v1/api/index.php"

params = {
    "maps" : "territories",
    "polygon_geojson" : {
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {"Name"},
            "geometry": {
            "type": "Polygon",
            "coordinates": [
            [
                [
                -113.5,
                61.25
                ],
                [
                -160,
                61.25
                ],
                [
                -160,
                47.25
                ],
                [
                -113.5,
                47.25
                ],
          ]
        ]
      }
    }
  ]
}    
}

#%% 
# download and convert to json
response_API = requests.get(url=url, params=params)
data = response_API.text

#print(data)
parse_json = json.loads(data)

# geojson
territory = {
             "type": "FeatureCollection",
             "features": response_API
}

print(territory.items()) 
print(territory)

for ii in range(0, len(parse_json)): 
  try:
    q = 1
    #print(list(parse_json[ii].values())[2]["Name"])
  except:
    pass


#%% [markdown]
# # Make the Map

# %%
# initialize a map
m = folium.Map(location=[55, -122], 
               zoom_start=4, 
               tiles="openstreetmap",
               name="Road Map")

# set map bounds
m.fit_bounds([[47.25, -158], [61.25, -113.5]])

# add terrain layer
tr = folium.TileLayer("Stamen Terrain",
                 name="Terrain").add_to(m)

# add the native-land overlay
folium.GeoJson(territory,
               name="Territories").add_to(m)

# loop through the native-land data and load data by creating polygon and popup
for ii in range(0, len(parse_json)):
    try:
      #folium.GeoJson(data, 
      #               name="Territories").add_to(m)
      
      t = folium.GeoJson(parse_json[ii].values())
      t.add_child(folium.Popup(list( parse_json[ii].values() )[2]["Name"]))
      t.add_to(m)
    except:
      pass

# add the layers to toggle
folium.LayerControl().add_to(m)

# display
m
# %%
# Search GitHub's repositories for requests
response = requests.get(
    'https://native-land.ca/wp-json/nativeland/v1/api/index.php',
    params={'q': 'requests+language:python'},
)

# Inspect some attributes of the `requests` repository
json_response = response.json()
print(json_response)
repository = json_response['items'][0]
print(f'Repository name: {repository["name"]}')  # Python 3.6+
print(f'Repository description: {repository["description"]}')  # Python 3.6+
# %%
