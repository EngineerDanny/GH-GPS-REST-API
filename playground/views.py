from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
import re


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def test(request):
    get_address()
    return render(request, 'index.html')  

# get gps from address name
def get_address():
    base_url = 'https://ghanapostgps.com/'
    map_url = 'https://ghanapostgps.com/map/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive'
    }
    map_res = requests.get(map_url,headers=headers, allow_redirects=True)
    
    # get the value of the ASP.NET_SessionId from the map_res cookies
    session_id = map_res.cookies.values()[0]    
    
    # find all the scripts under the body tag
    bs_body = BeautifulSoup(map_res.content, 'html.parser').body
    jscripts = bs_body.find_all('script')
    
    # find the last but one script tag
    last_script = jscripts[2].contents[0]
    
    # get the asaaseOwner from the script
    asaaseOwner = re.findall("\'([^']+)", last_script)[0]
    
    print(last_script)
    
    
 
# get gps from lat, long

# get addressname from gps