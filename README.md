# Remote Desktop Shiny App

_Purpose_: This application was created so users would have a way to view the availability of the Remote Desktops within the ERISOne cluster in the Partners HealthCare network. The live data needed by this application is private to the Partners server, but this is a copy of the code I wrote this summer.

_How Does It Work?_: There are three python scripts in this repository. The _rd_caps.py_ script creates a secure shell with every remote desktop and finds the maximum user capacity, then inserts this information into a SQL database. The _rd_usage.py_ script similarly creates a secure shell with every desktop, and it sends a list of all the active users to a SQL database. This script is run in the server every 5 minutes as a cronjob to constantly update the application. Lastly, the _rd_data.py_ takes all the infromation from the SQL database, and exports it into an easily-accessible JSON file for the R application to reference.

The R application is built using the _Shiny_ library, which creates a clean and simple User Interface with a _ui.R_ file that lays out the elements similarly to HTML and a _server.R_ file that handles the transfer of data from the JSON file into the UI.
