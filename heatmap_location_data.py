from selenium import webdriver
import geckodriver_autoinstaller
from glob import glob
import numpy as np
import folium
from folium.map import *
from folium import plugins
from folium.plugins import HeatMap
import pandas as pd
import os
import time
import matplotlib

geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                     # and if it doesn't exist, download it automatically,
                                     # then add geckodriver to path

title = "Plots & Heatmap"
m = folium.Map([41, -87], tiles=None, zoom_start=4)
folium.raster_layers.TileLayer(tiles='openstreetmap', control=False).add_to(m)
# This centers map on Chicago with a focus of the United States
# change the "[41, -87] to the center of where you want to map to be located, changing zoom_start to a larger number 
# will zoom the map in.

currentDirectory = os.getcwd()
csv_directory = currentDirectory + "/csv_folder/"
csv_array = list(filter(lambda x: '.csv' in x, os.listdir(csv_directory)))
matplotlib_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#000000']


# function will be utilized to create a color coded legend for the map
def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f'<li><span style="background-color: {color}"></span>{label}</li>'
        
    legend_html = f"""
    <div id='maplegend' class="maplegend">
      <div class="legend-title">{title}</div>
      <div class="legend-scale">
        <ul class="legend-labels">
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type="text/css">
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

data_to_be_heatmapped = []
colors = []
labels = []

#creates matrix of data to be plotted
for each in csv_array:
    name = each.rstrip(".csv")
    df = pd.read_csv(csv_directory + each)
    index_location = csv_array.index(each)
    colors.append(matplotlib_colors[index_location])
    labels.append(name)
    data_to_be_heatmapped.append([name, df, matplotlib_colors[index_location]])

#plots points
for each in data_to_be_heatmapped:
    color = each[2]
    for index, row in each[1].iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=2,
                            popup=row["Location Name"],
                            fill_color=color, weight = 0, fill_opacity=1).add_to(m)
        


#creates heatmap overlays
for each in data_to_be_heatmapped:
    dataArr = each[1][['latitude', 'longitude']].values
    feature_group = folium.FeatureGroup(each[0] + "Heatmap", show=False)
    HeatMap(dataArr).add_to(feature_group)
    feature_group.add_to(m)

folium.LayerControl(position='bottomright').add_to(m)



m = add_categorical_legend(m, title,
                             colors = colors,
                           labels = labels)

m.save('map.html')
delay=10
fn='map.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
m.save(fn)

browser = webdriver.Firefox()
browser.get(tmpurl)
#Give the map tiles some time to load
time.sleep(delay)
browser.save_screenshot('map.png')
browser.quit()