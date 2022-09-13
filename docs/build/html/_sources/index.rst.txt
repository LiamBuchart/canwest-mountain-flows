.. canwest-mountain-flows master file, created by
   sphinx-quickstart on Sun Sep 11 23:30:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css"
   integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ=="
   crossorigin=""/>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css"
   integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ=="
   crossorigin=""/>

Canwest-Mountain-Flows
==================================================

<div id="map"></div>

map { height: 280px; }

var map = L.map('map').setView([51.505, -120.09], 10)

 L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
   maxZoom: 19,
   attribution: '© OpenStreetMap'
   }).addTo(map);

.. toctree::
   :maxdepth: 2
   :caption: Flows:

   api
   mymarkdown


Search
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
