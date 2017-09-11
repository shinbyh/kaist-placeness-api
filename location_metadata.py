import sys
import json

locMetaData = []

def getLocationMetaData(metadataFile):
    with open(metadataFile, 'r') as content_file:
        content = content_file.read()

    locations = json.loads(content)
    return locations

# get all location metadata from file
locMetaData = getLocationMetaData('CoexIpark.json')

def getLocationName(locationId):
    locIdStr = '{}'.format(locationId)
    try:
        if ('name' in locMetaData[locIdStr]):
            return locMetaData[locIdStr]['name']
        else:
            return None
    except:
        return None

def getGPS(locationId):
    locIdStr = '{}'.format(locationId)
    try:
        if ('name' in locMetaData[locIdStr]):
            return (locMetaData[locIdStr]['latitude'], locMetaData[locIdStr]['longitude'])
        else:
            return None
    except:
        return None

#
# Test code for checking location ids
#
def main(argv):
    testLocs = getLocationMetaData('CoexIpark.json')
    for each in testLocs:
        try:
            if ('name' in testLocs[each]):
                print (testLocs[each]['name'])
                print ('({}, {})'.format(testLocs[each]['latitude'], testLocs[each]['longitude']))
        except:
            pass

if __name__ == "__main__":
   main(sys.argv[1:])
