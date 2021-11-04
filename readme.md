<h1>Utilizing Folium and Pandas for Creating Heatmaps</h2>
<br>
<p>Recently a member of a Google Group I'm subscribed to asked about software to create heat maps of data which contained geocoordinates.  I did my best to direct her to some Python libraries to handle this, but I realized that I'd like to put something together to empower people to quickly make heat maps.
<br>
<h2>Ensure Python 3 is Installed</h2>
<p>Before we begin, make sure you have a version of Python 3 installed and pip.  
Open a terminal window: 
    Linux:  Ctrl-Alt-T, Ctrl-Alt-F2
    Windows:  Win+R > type powershell > Enter/OK
    MacOS:  Finder > Applications > Utilities > Terminal

Then enter:
``` 
python --version
```
and
```  
pip --version
```
<h2>Install Requirements</h2>
<br>
Your version of Python should begin with a 3, if it does not please go to https://www.python.org/downloads/ and install a release of Python which is version 3.8 or greater.

If pip is not a recognized command, please go to https://pip.pypa.io/en/stable/installation/ and follow the instructions for installation, however pip should already be included if you have Python 3.4 or greater.
<br>
Now back into the terminal window, change to the directory where the files from this repository are stored, and type:
```
pip install -r requirements.txt
```
This will install the python libraries listed in the requirements.txt file.

<h2>Create Your Heatmap</h2>
<br>
<p>For this example we will be using csv's of the locations of White Castles and Waffle Houses in North America (datasets thanks to http://www.poi-factory.com/). You could substitute any data sets of points you would like to compare by removing the files in "csv_folder" and substituting your own. For each categorical group to be mapped, you would need to place a csv file in the "csv_folder."  Each csv file needs to have columns with the headings: 'latitude', 'longitude', and 'Location Name'.  This program will then go line by line through each csv, plot the given geocoordinates and label the plotted dot with the location name.  It will then create a heat map overlay for each categorical group which you can toggle on and off at the bottom right of the map, and finally a categorical legend for the individual dots so you can differentiate the data points easily.
<br>
<p>This program will be looking at the *.csv files stored in the subfolder named "csv_folder" it will utilize the names of the individidual csv files to create the categorical legend for the map and assign a varying color for each csv's plotted points. At the bottom right of the map, there will be layers button.  Clicking on this button will allow you to bring up a heat map display for each data category.



