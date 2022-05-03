from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def test(request):

    # get name from query string
    name = request.GET.get('name')

    # encode name
    enc_name = requests.utils.quote(name)

    address_list = get_address_list(enc_name)

    print(type(address_list))

    return Response(address_list)


# get gps from address name
def get_address_list(name):
    base_url = 'https://ghanapostgps.com/'
    map_url = 'https://ghanapostgps.com/map/'
    action_url = 'https://ghanapostgps.com/jsWebCall.aspx?Action=GetLocation&GPSName=' + name

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive'
    }
    session = requests.Session()
    # session.headers.update(headers)

    map_res = session.get(map_url, headers=headers, allow_redirects=True)

    # get the value of the ASP.NET_SessionId from the map_res cookies
    session_id = map_res.cookies.values()[0]

    # find all the scripts under the body tag
    bs_body = BeautifulSoup(map_res.content, 'html.parser').body
    jscripts = bs_body.find_all('script')

    # find the script tag that contains the asaaseOwner token
    third_script = jscripts[2].contents[0]

    # find the last script to extract a useful link
    last_script = jscripts[-1]['src']

    # append the last script to the base url
    last_script_url = base_url + last_script

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

# get addressname from gps


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
        'AsaaseUser': asaase_user
    }
