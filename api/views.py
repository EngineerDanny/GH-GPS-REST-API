import requests
from bs4 import BeautifulSoup
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def get_address(request):
    # get name from query string
    # name = request.GET.get('name')

    # get name from request body
    name = request.data.get('name')

    # validate the name variable
    if name is None:
        return Response(data={'error': 'Request is missing name in the body'},
                        status=status.HTTP_400_BAD_REQUEST)

    # type check the name variable
    try:
        str(name)
    except ValueError:
        return Response(data={'error': 'name must be string'},
                        status=status.HTTP_400_BAD_REQUEST)

    # encode name
    enc_name = requests.utils.quote(name)
    action_url = 'https://ghanapostgps.com/jsWebCall.aspx?Action=GetLocation&GPSName=' + enc_name

    # get gps from address name
    address_list = fetch_address(action_url)
    return normal_response(address_list)


@api_view(['POST'])
def get_gps(request):
    # get latitude and longitude from query params
    latitude = request.data.get('lat')
    longitude = request.data.get('long')

    # validate the latitude and longitude variables
    if latitude is None or longitude is None:
        return Response(data={'error': 'Request is missing latitude or longitude in the body'},
                        status=status.HTTP_400_BAD_REQUEST)

    # check whether latitude and longitude are numbers
    try:
        float(latitude)
        float(longitude)
    except ValueError:
        return Response(data={'error': 'Latitude and longitude must be numbers'},
                        status=status.HTTP_400_BAD_REQUEST)

    action_url = 'https://ghanapostgps.com/jsWebCall.aspx?Action=GetGPSName&Lati={}&Longi={}'.format(
        latitude, longitude)

    # the address name can be the name or GPS address of the place
    address_list = fetch_address(action_url)
    return normal_response(address_list)


def fetch_address(action_url):
    map_url = 'https://ghanapostgps.com/map/'

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

    address_txt = address_res.text
    if len(address_txt) == 0:
        return None
    address_data = address_res.json()

    try:
        address_list = address_data['Table']
    except Exception:
        return None
    # return the address list as json
    return address_list


def normal_response(address_list):
    if address_list is None or len(address_list) == 0:
        return Response(data={'status': 'No address found'},
                        status=status.HTTP_204_NO_CONTENT)
    return Response(
        data={'status': 'Address found',
              'address': address_list, 'count': len(address_list),
              },
        status=status.HTTP_200_OK)

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
