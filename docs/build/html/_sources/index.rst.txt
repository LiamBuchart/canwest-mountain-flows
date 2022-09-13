.. canwest-mountain-flows documentation master file, created by
   sphinx-quickstart on Sun Sep 11 23:30:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Canwest-Mountain-Flows!
==================================================

.. raw:: html

   <div id="mapdiv" style="height: 200px; width: 100%"></div>
   <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
   <script>
   map = new OpenLayers.Map("mapdiv")
   map.addLayer(new OpenLayers.Layer.OSM());

   var lonlat = new OpenLayers.LonLat( -120 ,51 )
      .transform(
         new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
         map.getProjectionObject()  // to spherical Mercartor Projection
      );
   
   var zoom=16;

   var markers = new OpenLayers.Layer.Markers( "Markers");
   map.addLayer("markers")

   markers.addMarker(new OpenLayers.Marker(lonlat));

   map.setCenter (lonlat, zoom);
   </script>

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   mymarkdown
   mathmd


Flows
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
