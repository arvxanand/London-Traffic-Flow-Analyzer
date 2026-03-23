from webtris_client import API, SingleSite
from datetime import date

client = API()

certain_date = date(2026, 1, 3)
site = SingleSite(site_id=461, site_name="M25/4432A", traffic_stats=[])
site.load_from_client(client, certain_date)


print(f"--{certain_date}--")
print(f"Total records: {len(site)}")
print(f"Average speed: {site.average_speed()}")
print(f"Total vehicles: {site.total_num_of_vehicles()}")
print(f"Peak hour: {site.peak_hour()}")

for observation in site:
    print(observation)