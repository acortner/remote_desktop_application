# Remote Desktop Shiny App

_Purpose_: This application was created so users would have a way to view the availability of the Remote Desktops within ERISOne. 

_How Does It Work?_: The python script within this directory, connects to every remote desktop node, and counts how many users are on each machine. 

## TODO -- There is a lot to be done
1. _Split the App.R file into ui.r and server.r_
Just to better manage the code.
**STATUS: Done**

2. _Finish styling the application_
What I have right now within app.R was just my vision for this application, but to whoever is picking up this project feel free to make it look any way you want.
**STATUS: Done**

3. _Getting Remote Desktop Data_
At the moment, within the python_scripts folder I have a file called rd_data.py. This script connects to the rrd file of all the RGS machines that are presented on https://erisone.partners.org/munin/rdesktop/comparison-day.html#rdesktop, and extracts the recent update (the current number of users who have a session on that remote desktop). For the newer machines, grx0X, I ssh into the machine and use the command _ps auxw | grep nxnode.bin | grep -v grep | grep -v root | cut -d ' ' -f 1 | sort -u_ that returns a list of all the users connected to that desktop. I then record the number. 
I put all of the data into a data table, and then I turn that table into a JSON (this process is at line 49). I chose a JSON because it is a small file that can quickly be updated, rather than sending a real time update to a data base X amount of times during the day. BUT feel free to transfer the data between the script and the application however you want. 

After getting the number of current users on all the machine, you now need to figure out how the capaicty of all the remote desktops. If you need help with this process talk to Rodrigo. 

This is a part of a message Rod sent me describing how to figure out how many licenses a machine has: 

>Here is the command to obtain the NoMachine license type

>" /usr/NX/bin/nxserver --version "

>Which returns one of the following depending on the license applied on server
>
>" NoMachine Terminal Server Subscription - Version 6.2.4 "
Unlimited desktops, but capped at (1) desktop session per user
>
>" NoMachine Workstation "
4 desktops

>" Small Business Server "
>10 desktops

>For more information 
>https://confluence.partners.org/display/HPC/Remote+Desktop+Licensing
>https://confluence.partners.org/display/HPC/Remote+Desktop+Servers


This process doesn't need to be ran often since licences don't change as much. I say create a script that checks the license for all the machines and adds the capacitys to the JSON file as well. 
**STATUS: Done**

4. _Ping Servers_
Sometimes servers are down. Edana came up with the idea to ping each server before running the r_data script to see if a machine is even running. Good idea. If I were to do this, I would create a script thats pings a machine twice and checks the output to decide is the machine is up or not. I somewhat started this process in the rd_ping.py file, but feel free to only use it as reference as I am sure there is a more effiencent way to do this. 

I think this covers the basic functionalty of this applicaiton! If you have any other questions feel free to contact me at madison.b@husky.neu.edu 
- Breanna 