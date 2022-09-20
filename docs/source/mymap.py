# %% [markdown]
# # Pull Data from the native-land.ca API
# Territory and Name overlays come from Native Land Digital 
# ---
# `native-land.ca <native-land.ca>`_

#%%
# Imports
import pandas as pd
import geopandas as gpd
import folium
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import shape

import requests
import json

#%%
# api URL
url = "https://native-land.ca/wp-json/nativeland/v1/api/index.php"

# parameters of the download
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

#convert to json
parse_json = json.loads(data)

# make a geojson (not used currently)
territory = {
             "type": "FeatureCollection",
             "features": response_API
}


#%% [markdown]
# # Make the Map

# %%
# dataframe of the json
df_m = pd.DataFrame(parse_json)

# initialize a map
m = folium.Map(location=[55, -122], 
               zoom_start=4, 
               tiles="Stamen Terrain",
               name="Terrain")

# set map bounds
m.fit_bounds([[47.25, -158], [61.25, -113.5]])

shapesLayer = folium.FeatureGroup(name="Territories",
                                  show=False).add_to(m)
popupLayer = folium.FeatureGroup(name="Names",
                                 show=False,).add_to(m)

for ii in range( (len(df_m)-1) ):
  df = df_m.iloc[ii]
  nn = list(df["properties"].values())[0]

  df["geometry"] = list(df["geometry"].values())[0]

  geo: dict = {"type": "Polygon",
               "coordinates": df["geometry"]}
  try: 
    polygon: Polygon = shape(geo)
    x, y = polygon.exterior.coords.xy

    folium.GeoJson(polygon,
                   zoom_on_click=True,
                   show=False,).add_to(shapesLayer)

    folium.CircleMarker(location=[np.mean(y), np.mean(x)],
                        zoom_on_click=True,
                        show=False,
                        radius=2,
                        color="orange", 
                        fill_color="orange",
                        popup=str(nn)).add_to(popupLayer)
    
  except:
    pass

# display the layer switcher widget
folium.LayerControl().add_to(m)

m

# %%
# save the map object to be displayed on the home page
m.save('canwest_flows.html')
