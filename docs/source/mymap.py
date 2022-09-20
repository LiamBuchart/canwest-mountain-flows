# %% [markdown]
# # A Markdown cell
# - You can do all the fun stuff markdown has to offer


#%%
# Imports
import pandas as pd
import geopandas as gpd
import folium
import numpy as np
from shapely.geometry import Polygon
from shapely.wkt import loads

import requests
import json
import geojson

# %% [markdown]
# # Pull Data from the native-land.ca API
# Territory and Name overlays come from Native Land Digital 
# ---
# `native-land.ca <native-land.ca>`_

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

#%%
# load the file into a format for plotting

#print(list(parse_json)[3].items())

# load the json file in a geopandas dataframe thats easier to work with
gdf = gpd.GeoDataFrame(parse_json)
print("The dataframe: ")
#print(type(gdf["geometry"]))
#print(gdf["geometry"].astype("string").iloc[0])
#gdf = gdf["geometry"].apply(loads)
#gdf["geometry"] = gdf["geometry"].astype("string")
gdf = gdf.iloc[0]
print(gdf)
gdf.crs = "epsg:4326"
gdf.to_crs = {'init' :'epsg:4326'}
#geom = np.array(list(gdf["geometry"].values()))
#gdf["geometry"] = geom
#print(gdf)
#gdf["geometry"] = list(gdf["geometry"].values())[0])
#gdf["geometry"] = gdf["geometry"].astype("string") #, dtype="string" #list(gdf["geometry"].values())
#print(gdf["geometry"])
#geom = list(gdf["geometry"].values())
#print("NEXT")
#print(np.array(geom[0]))
#print(type(gdf["geometry"]), type(geom[0]), len(geom)) 
#gdf2 = gdf.set_geometry("geometry")                                             
#gdf = gdf["geometry"].apply(loads)


#print(gdf.columns)
#print(gdf.head())
#poly = Polygon(list(gdf["geometry"]))
#gdf.set_geometry(Polygon(gdf["geometry"]))


#gdf = gpd.GeoDataFrame(data).set_geometry('geometry')

#print(gdf2)

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
#print(type(folium.Popup(list( parse_json[ii].values() )[2]["Name"])))

# data
folium.GeoJson(gdf,
               name="Territories",
               show=False,
               popup="Test",
               zoom_on_click=True).add_to(m)


# loop through the native-land data and load data by creating polygon and popup
#for ii in range(0, len(parse_json)):
#    try:
#      #folium.GeoJson(data, 
#      #               name="Territories").add_to(m)
#      
#      t = folium.GeoJson(list(parse_json[ii].values()))
#      t.add_child(folium.Popup(list( parse_json[ii].values() )[2]["Name"]))
#      t.add_to(m)
#    except:
#      pass

# add the layers to toggle
folium.LayerControl().add_to(m)

# display
m












# %%
# sort out geometry issues
from shapely.geometry import shape

df_m = pd.DataFrame(parse_json)
# initialize a map
m = folium.Map(location=[55, -122], 
               zoom_start=4, 
               tiles="Stamen Terrain",
               name="Terrain")

shapesLayer = folium.FeatureGroup(name="Territories").add_to(m)
popupLayer = folium.FeatureGroup(name="Names").add_to(m)

for ii in range( (len(df_m)-1) ):
  print(ii)
  df = df_m.iloc[ii]
  nn = list(df["properties"].values())[0]

  df["geometry"] = list(df["geometry"].values())[0]

  geo: dict = {"type": "Polygon",
               "coordinates": df["geometry"]}
  try: 
    polygon: Polygon = shape(geo)
    x, y = polygon.exterior.coords.xy

    folium.GeoJson(polygon,
                   zoom_on_click=True).add_to(shapesLayer)

    folium.CircleMarker(location=[np.mean(y), np.mean(x)],
                        zoom_on_click=True,
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