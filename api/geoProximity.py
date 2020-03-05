import csv

from math import sin, cos, sqrt, atan2, radians

from settings import THREAT_RANGE


def getLocationList():
    """
    Reads Merck location file and returns list with the locations and related site code 

    :return: list of Merck sites
    """
    with open('MerckLocations.csv', newline='') as csvfile:
        locations_file = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(locations_file)
        locations = []
        for row in locations_file:
            locations.append(row)
        return locations


def checkRange(site_lat, site_lon, threat_lat, threat_lon):
    """
    Source of math/some codehttps://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

    Checks to see if lat and lon of a threat are within range of a provided site

    :param: site latitude
    :param: site longitude
    :param: threat latitude
    :param: threat longitude 
    :return: boolean if in range
    """

    # approximate radius of earth in miles
    R = 3958.8

    site_lat = radians(site_lat)
    site_lon = radians(site_lon)
    threat_lat = radians(threat_lat)
    threat_lon = radians(threat_lon)

    dist_lon = threat_lon - site_lon
    dist_lat = threat_lat - site_lat

    a = sin(dist_lat / 2)**2 + cos(site_lat) * cos(threat_lat) * sin(dist_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance <= THREAT_RANGE:
        return True
    
    return False


def inRangeOfMerckFacility(threat_lat, threat_lon):
    """
    Checks to see if a threat is in range of a facility

    :param: threat latitude
    :param: threat longitude
    :return: boolean denoting if the threat is in range
    """
    
    # get list of locations
    locations = getLocationList()
    # for each location in list
    for loc in locations:

        # check to see if this site is in range of a threat
        if checkRange(float(loc [1]), float(loc[2]), threat_lat, threat_lon):
            return True
    
    # not in range of any threats
    return False
