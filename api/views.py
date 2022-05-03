import requests
from bs4 import BeautifulSoup
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_address(request):
    # get name from query string
    name = request.GET.get('name')

    # encode name
    enc_name = requests.utils.quote(name)
    address_list = fetch_address_list(enc_name)

    return Response(address_list)


@api_view(['GET'])
def get_gps(request):
    # get latitude and longitude from query params
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')

    # validate the latitude and longitude variables
    if latitude is None or longitude is None:
        return Response(data={'error': 'Request is missing latitude or longitude query parameters'},
                        status=status.HTTP_400_BAD_REQUEST)

    # check whether latitude and longitude are numbers
    try:
        float(latitude)
        float(longitude)
    except ValueError:
        return Response(data={'error': 'Latitude and longitude must be numbers'},
                        status=status.HTTP_400_BAD_REQUEST)

    address_list = fetch_gps(latitude, longitude)

    if address_list is None or len(address_list) == 0:
        return Response(data={'status': 'No address found'},
                        status=status.HTTP_204_NO_CONTENT)

    return Response(
        data={'status': 'Address found',
              'address': address_list, 'count': len(address_list),
              },
        status=status.HTTP_200_OK)

# get gps from address name
# the address name can be the name or GPS address of the place


def fetch_address_list(name):
    map_url = 'https://ghanapostgps.com/map/'
    action_url = 'https://ghanapostgps.com/jsWebCall.aspx?Action=GetLocation&GPSName=' + name

    session = requests.Session()
    # session.headers.update(headers)

    map_res = session.get(
        map_url, headers=get_normal_headers(), allow_redirects=True)

    # get the value of the ASP.NET_SessionId from the map_res cookies
    # session_id = map_res.cookies.values()[0]

    # find all the scripts under the body tag
    bs_body = BeautifulSoup(map_res.content, 'html.parser').body
    jscripts = bs_body.find_all('script')

    # find the script tag that contains the asaaseOwner token
    third_script = jscripts[2].contents[0]

    asaase_user = "VGgxcyBJcyBvdXIgV2ViIFVzZXI="
    # get the asaaseOwner from the script
    asaase_owner = re.findall("\'([^']+)", third_script)[0]

    # make a post request to get the address
    address_res = session.post(action_url, data={'headers': {
        "AsaaseOwner": asaase_owner,
        "AsaaseUser": asaase_user
    }, }, headers=get_address_headers(asaase_owner, asaase_user))

    address_data = address_res.json()
    address_list = address_data['Table']

    # return the address list as json
    return address_list


# get gps from lat, long
def fetch_gps(latitude, longitude):
    map_url = 'https://ghanapostgps.com/map/'
    action_url = 'https://ghanapostgps.com/jsWebCall.aspx?Action=GetGPSName&Lati={}&Longi={}'.format(
        latitude, longitude)

    session = requests.Session()
    # session.headers.update(headers)

    map_res = session.get(
        map_url, headers=get_normal_headers(), allow_redirects=True)

    # get the value of the ASP.NET_SessionId from the map_res cookies
    # session_id = map_res.cookies.values()[0]

    # find all the scripts under the body tag
    bs_body = BeautifulSoup(map_res.content, 'html.parser').body
    jscripts = bs_body.find_all('script')

    # find the script tag that contains the asaaseOwner token
    third_script = jscripts[2].contents[0]

    # find the last script to extract a useful link
    # last_script = jscripts[-1]['src']

    asaase_user = "VGgxcyBJcyBvdXIgV2ViIFVzZXI="
    # get the asaaseOwner from the script
    asaase_owner = re.findall("\'([^']+)", third_script)[0]

    # make a post request to get the address
    address_res = session.post(action_url, data={'headers': {
        "AsaaseOwner": asaase_owner,
        "AsaaseUser": asaase_user,

    }},
        headers=get_address_headers(asaase_owner, asaase_user)
    )

    address_data = address_res.json()

    try:
        address_list = address_data['Table']
    except Exception:
        return None
    # return the address list as json
    return address_list


# a helper function to get the address headers
def get_address_headers(asaase_owner, asaase_user):
    return {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'Referer': 'https://ghanapostgps.com/map/',
        'Origin': 'https://ghanapostgps.com',
        'AsaaseOwner': asaase_owner,
        'AsaaseUser': asaase_user,

    }


def get_normal_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive'
    }
