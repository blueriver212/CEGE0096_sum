CEGE0096_sum
This is Indigo Brownhall's Assignment 1 for CEGE0096 Summative (Grade = 94%). 

This software was written in Python 3.7.6 and will be compatible with anything above Python 3. It requires the sys, os and matplotlib packages to be already installed. 
After cloning the project from github (blueriver212/CEGE0096_sum), the tasks can be run from the cmd line. Everything is required to be in the same directory. The user will need to paste in a chosen polygon and point csv files here.

Points from File
$ python main_from_file.py
- Type the filename of your polygon (include .csv):
- Type the filename of your testing points (include .csv):
- Type the name of your output file (include .csv):

The user will see a plot of the points and a new .csv of the point ‘id’ and ‘classification’ will be created in the project directory. 

Points from User
$ python main_from_user.py
- Input the name of the relative path of your polygon (include .csv):
- Enter your coordinates (x, y format):
The software will return a terminal statement of where the user’s point is located, and a plot of the point and polygon.

Creative Task
For the creative task the user will need, pandas, geopandas, shapely, contextily all installed (see Task 10 for further details). Then run:
$ python creative_task.py
- Outputs a simple plot of points inside or outside a polygon
- Once the first plot is closed, a map of these points georeferenced will show.
