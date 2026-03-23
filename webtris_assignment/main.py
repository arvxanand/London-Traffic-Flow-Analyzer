from webtris_client import API, SingleSite
from datetime import date

#Here we are creating the client class to use
client = API()

#Here we are creating an onbject with the side_id and the site_name we want to get our data for
#The site id and site name I have gotten are examples givin from the assignemnt brief
site = SingleSite(site_id=461, site_name="M25/4432A", traffic_stats=[])
site.load_from_client(client, date(2026, 1, 3))
#Here we are getting the traffic data from a specific day
#From this we get all 96 records from a 15 minute interval of one day

#This is showing many records we got data from 
print(f"Total number of records: {site.__len__()}")

#Here we are finding out rhe average speed of that specific day
#We are also accounting for error handling
if site.average_speed() is not None:
    print(f"Average speed for the day: {site.average_speed()} mph")
else:
    print("No Average speed data found!")

#Here we are finding the total number of vehicles for this specific day
#Again we are accounting for any error handling that we might face
if site.total_num_of_vehicles() is not None:
    print(f"Total number of vehicles for the day: {site.total_num_of_vehicles()}")
else:
    print("No data found for total number of vehicles for this day!")

#Here we a showing the peak hour
#Again we are doing error handling but we also doing "or 0" to account for if the hour 
peak = site.peak_hour() or 0
if site.peak_hour() is not None:
    print(f"Peak Hour: {peak}:00 to {peak+1}:00")
else:
    print("Peak Hour not found")

#Here we are orinting the average speed of the cars during the peak hour we found earlier
if site.average_speed_per_hour(peak) is not None:
    print(f"Average speed during peak hour: {site.average_speed_per_hour(peak)} mph")

#Here we are printing the total num of cars during the peak hour we found earloer
if site.total_num_of_vehicles_per_hour(peak) is not None:
    print(f"Total number of vehicles during peak hour: {site.total_num_of_vehicles_per_hour(peak)}")

#Here we printing out all the records we got for the date we chose
print("\nAll the records for a certain date:")
for a in site:
    print(a)