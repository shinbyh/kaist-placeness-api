import json

district_dict = {}

def loadDistrictDict():
    f = open('districts.csv', 'r')
    for line in f:
        s = line.strip().split(',')
        district_dict[s[0].lower()] = [(float(s[1]), float(s[2])), (float(s[3]), float(s[4]))]

def addDistrictToDict(name, gps_nw, gps_se):
    district_dict[name.lower()] = [(gps_nw[0], gps_nw[1]), (gps_nw[0], gps_nw[1])]
    with open('districts.csv', 'a') as f:
        f.write('{},{},{},{},{}'.format(name, gps_nw[0], gps_nw[1], gps_se[0], gps_se[1]))

def isGPSIncluded(lat, lon, nw, se):
    if(lat < nw[0] and lat > se[0]):
        if(lon > nw[1] and lon < se[1]):
            return True
        return False
    else:
        return False
#
# Return the name of aa district place
# based on the GPS coordinate.
# The list of districts is stored in 'districts.csv'.
#
def getDistrict(lat, lon):
    for key, value in district_dict.items():
        if(isGPSIncluded(lat, lon, value[0], value[1])):
            return key
    return None

#
# Get the center GPS coordinate of a district.
# Since we define a district as a square from
# a northwest point to a southeast point,
# the center point can be calculated.
#
def getCenter(district_name):
    district_name = district_name.lower()
    found = district_dict[district_name]

    if(found is not None):
        gps_nw = found[0]
        gps_se = found[1]
        center_lat = (gps_nw[0] + gps_se[0])/2.0
        center_lon = (gps_se[1] + gps_nw[1])/2.0
        return (center_lat, center_lon)
    else:
        # Return a default GPS coordinate: the center of Seoul
        return (37.550116, 126.989593)

#
# Get a list of hotspots for a specific district.
#
def getHotspots(district_name):
    hotspot_list = []

    json_data = open('data/venue_info_filtered.json').read()
    all_hotspots = json.loads(json_data)
    for hotspot_id in all_hotspots.keys():
        hotspot = all_hotspots[hotspot_id]
        district = getDistrict(hotspot['latitude'], hotspot['longitude'])
        if(district is not None):
            if(district.lower() == district_name.lower()):
                hotspot_list.append(hotspot)
    return hotspot_list


# Load districts from a csv file.
loadDistrictDict()

#
# Test code for testing the functions
#
def main():
    print(district_dict)
#    addDistrictToDict('HongDae', ('127.07','35.32'), ('127.55', '76.55'))
#    print(district_dict)

    up = getDistrict(67.5119, 127.05888)
    print(up)


if __name__ == "__main__":
    main()
