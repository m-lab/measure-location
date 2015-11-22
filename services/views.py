import json
import pygeoip
import os

from django import http

def home(request):
  lookup_response = {
      'ip': os.environ["REMOTE_ADDR"]
  }

  geoip_asn_lookup = pygeoip.GeoIP('resources/GeoIPASNum-2015-09-15.dat',
      flags=pygeoip.const.MEMORY_CACHE)
  geoip_location_lookup = pygeoip.GeoIP('resources/GeoLiteCity-2015-09-15.dat',
      flags=pygeoip.const.MEMORY_CACHE)

  geoip_location = geoip_location_lookup.record_by_addr(lookup_response['ip'])
  if geoip_location:
    lookup_response.update(geoip_location)

  geoip_asn = geoip_asn_lookup.org_by_addr(lookup_response['ip'])
  if geoip_asn:
    lookup_response['asn'], lookup_response['isp'] = geoip_asn.split(' ', 1)

  lookup_response_json = json.dumps(lookup_response)

  response = http.HttpResponse(lookup_response_json, mimetype='application/json')
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"
  return response


#
#
#ip (Visitor IP address, or IP address specified as parameter)
#country_code (Two-letter ISO 3166-1 alpha-2 country code)
#country_code3 (Three-letter ISO 3166-1 alpha-3 country code)
#country (Name of the country)
#region_code (Two-letter ISO-3166-2 state / region code)
#region (Name of the region)
#city (Name of the city)
#postal_code (Postal code / Zip code)
#continent_code (Two-letter continent code)
#latitude (Latitude)
#longitude (Longitude)
#dma_code (DMA Code)
#area_code (Area Code)
#asn (Autonomous System Number)
#isp (Internet service provider)
#timezone (Time Zone)
#Output example :
#
#The following example use Telize server IP : city, region, and postal code information is not available and thus not present in the output JSON object :
#
