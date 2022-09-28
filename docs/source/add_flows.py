#%%
# script to add each of the flows location to the map
# flows locations are specified in the flows.json file
# in the json directory

#%%
# imports
import numpy as np
import pandas as pd
import folium
from shapely.geometry import Polygon
import json

#%%
# open the json and load as an easy to use dataframe
path = "/Users/lbuchart/Documents/canwest-mountain-flows/docs/source/json/"
file = "flows.json"

df = pd.read_json(path + file, orient="columns")
df.head()

# %%
# now make an easier to work with dataframe for plotting polygons
pldf = pd.DataFrame(columns=["Name", "type", "Longitude", "Latitude", "polygon"],
                    index=range(0, len(df)))
for ii in range(len(df)):
    points = df.iloc[ii]["flows"]["shape"]
    poly = Polygon(points)

    name = df.iloc[ii].name
    type = df.iloc[ii]["flows"]["type"]
    point = df.iloc[ii]["flows"]["point"]

    # maybe redundant but I like to see it right there in front of me
    d = {"Name": name, 
         "type": type,
         "Longitude": point[1],
         "Latitude": point[0],
         "polygon": poly
        }

    pldf.iloc[ii] = pd.Series(d)

#print(pldf)
