# %% [markdown]
# # A Markdown cell
# - You can do all the fun stuff markdown has to offer


#%%
# Imports
import pandas as pd
import folium

import requests
import json

# %% [markdown]
# # Pull Data from the native-land.ca API
# Territory and Treaty overlays come from Native Land Digital
# native-land.ca

#%%
response_API = requests.get("https://native-land.ca/api/index.php?maps=territories,treaties")
print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)

#%%
m = folium.Map(location=[49.5236, -122.6750], zoom_start=8)
m

