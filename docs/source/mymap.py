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
import matplotlib.pyplot as plt
from shapely.geometry import shape, GeometryCollection

#with open(data) as f:
#  features = json.load(f)["features"]
num = 1
print(num)
df = pd.DataFrame(parse_json)
df = df.iloc[num]

#print(df.columns)
#print(df.dtypes)
df["geometry"] = list(df["geometry"].values())[0]
#print(df["geometry"])
#df["geometry"] = list(df["geometry"].values())[0]
#df["geometry"] = df["geometry"].astype("float")
#df.crs = "epsg:4326"
#df.to_crs = {'init' :'epsg:4326'}
#print(df.head())
#print(df.dtypes)

geo: dict = {"type": "Polygon",
             "coordinates": df["geometry"]}

print(list(geo.values())[1])
polygon: Polygon = shape(geo)

C = polygon.exterior.coords.xy

#print(C)

# initialize a map
m = folium.Map(location=[55, -122], 
               zoom_start=4, 
               tiles="openstreetmap",
               name="Road Map")

shapesLayer = folium.FeatureGroup(name="Territories").add_to(m)

folium.PolyLine(list(geo.values())[1],
                color="red",
                weight=5).add_to(shapesLayer)

folium.Polygon(list(geo.values())[1],
               color="orange",
               weight=5,
               fill=True,
               fill_color="orange",
               fill_opacity=0.4).add_to(shapesLayer)

# display the layer switcher widget
folium.LayerControl().add_to(m)

m

# save the map object to be displayed on the home page
m.save('canwest_flows.html')
# %%
