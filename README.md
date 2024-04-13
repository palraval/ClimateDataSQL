# ClimateDataSQL


## Analyzing Climate Data 

Firstly, the connection to the SQL database is established. The tables are reflected into classes and saved as objects. After this, the SQLAlchemy session is created for analyzing purposes. 


### Precipitation Table

The first table that is analyzed is regarding precipitation. The most recent date in this dataset is found to calculate the date of previous year. The data is then queried using the previous year information to find information that occurs in the timespan of a year. The data is reduced to only give information regarding the date and the precipitation values and then placed into a dataframe. This dataframe is sorted based on date and plotted on a graph with date on the x-axis and the respective precipitation values on the y-axis. Lastly, the summary statistics for the precipitation data is calculated. 


### Stations Table

The second table is regarding stations. The first thing done is to calculate the number of stations that appear in this data. The most-active station (station that appears the most in the dataset) is calculated by grouping the stations, counting the number of times they each appear, placing the counts in descending order, and noting the first appearance in this order. The name of the station is found for the first appearance. This station name is used to query the dataset so only the values related to this station are noted. The lowest, highest, and average temperatures are calculated from this queried dataset. The most recent date for the "most-active station" queried dataset is found and the date for the year prior to this date is calculated. A query is then conducted according to this 12-month-prior date, so only the data for the past 12 months for the most-active station dataset remains. A 12-bin histogram is created according to this newly-calculated data. The session is then terminated. 


## Climate App


A Flask API is designed based on the queries previously utilized. 6 routes are made created for this:

1. Home Page Route - Lists all the possible routes that can be taken 

2. Precipitation Route - Returns a dictionary with last 12 months of data and the respective precipitation values

3. Stations Route - Shows a JSON list of the stations in the dataset

4. Temperature Route - Gives a JSON list of temperature values in the span of the most recent year for the most-active station

5. Start Route - Provides a JSON list with minimum temperature, average temperature, and maximum temperature based on temperatures in the dataset that are associated with dates greater than or equal to the specified start date 

6. Start-End Route - Returns a JSON list of minimum temperature, average temperature, and maximum temperature based on temperatures in the dataset that are associated with dates greater than or equal to the specified start date and less than or equal to the specified end date.


**NOTE: The start and end dates inputted in the url must be in the format: YYYY-MM-DD. No other characters should be incorporated**
