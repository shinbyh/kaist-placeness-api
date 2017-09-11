import json

json_data = open('data/venue_info_filtered.json').read()
all_hotspots = json.loads(json_data)

new_hotspots = {}

f = open('data/place_filtered_name.csv', 'r')
for line in f:
    s = line.strip().split(',')
    hotspot_id = s[0]
    new_hotspots[hotspot_id] = all_hotspots[hotspot_id]

with open('data/venue_info_filtered2.json', 'w') as fp:
    json.dump(new_hotspots, fp)
#print(new_hotspots)
