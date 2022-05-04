# **GH-GPS-DJANGO-REST-API**

*A REST api for Ghana's Global Positioning System (GPS) written with Python Django 🐍🐍*
<br/>

## **API Usage**

<br/>
<details>
<summary>Get GhanaPostGPS Address from PlaceName or GPSName.</summary>
<hr/>

## Request

<b>End Point URL:</b> https://gh-gps.herokuapp.com/api/get-address<br>
<b>Method:</b> GET<br>
<b>Content-Type:</b> application/json<br><br>

### Payload

#### When using with a PlaceName

```json
{
  "name": "KNUST Guesthouse"
}
```

#### When using with a GPSName

```json
{
  "name": "AE-0147-4625"
}
```

## Response

<br>
1. When Address exists, it returns an address field which contains a list of Addresses

```json
{
  "status": "Address found",
  "address": [
    {
      "Place_Name": "KNUST Guesthouse",
      "CenterLatitude": "5.5677456",
      "CenterLongitude": "-0.1863609",
      "Region": "Greater Accra",
      "District": "Korley Klote",
      "Area": "RINGWAY ESTATES",
      "StreetName": "Nuumo Klotey Street",
      "GPSName": "GA0315033",
      "PostCode": "GA031",
      "PlaceName": "KNUST Guesthouse, GA-031-5033, Korley Klote",
      "Street": "KNUST Guesthouse, Nuumo Klotey Street"
    }
  ],
  "count": 1
}
```

2. No Address was found

```json
{
  "status": "No Address found"
}
```

3. Encounter an error

```json
{
  "error": "Request is missing name in the body"
}
```

</details>
<br/>
<details>

<summary>Get GhanaPostGPS Address from Position (Latitude and Longitude) </summary>
<hr/>

## Request

<b>End Point URL:</b> https://gh-gps.herokuapp.com/api/get-gps<br>
<b>Method:</b> POST<br>
<b>Content-Type:</b> application/json<br><br>

### Payload

```json
{
  "lat": "6.1250",
  "long": "-1.94872"
}
```

## Response

<br>
1. When Address exists, it returns an address field which contains a list of Addresses

```json
{
  "status": "Address found",
  "address": [
    {
      "GPSName": "AV31641332",
      "Region": "Ashanti",
      "District": "Amansie Central",
      "PostCode": "AV3164",
      "NLat": 6.12502457351701,
      "SLat": 6.12497965404504,
      "WLong": -1.94876026156099,
      "Elong": -1.94871534579679,
      "Area": ".",
      "Street": ".[Unknown Street]",
      "PlaceName": ""
    }
  ],
  "count": 1
}
```

2. No Address was found

```json
{
  "status": "No Address found"
}
```

3. Encounter an error

```json
{
  "error": "Request is missing latitude or longitude in the body"
}
```
</details>

<br/>

## **API Local Set-Up**
### Technologies
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs
## Installation
* Make sure you've got [Python](https://www.python.org") installed.
* Install virtualenv globally with:
    ```bash
        $ pip install virtualenv
    ```
* Clone this repo
    ```bash
        $ git clone https://github.com/EngineerDanny/GH-GPS-REST-API.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd GH-GPS-API
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ virtualenv  venv -p python3
            $ source venv/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```

* #### Running
   1. Start the server with:
    ```bash
        $ python manage.py runserver
    ```
   2. You can access the local server by sending a GET request to the ENDPOINT:
    ```
        http://localhost:8000/api/
    ``` 
   3. Use the following ENDPOINTS  
     ```
        http://localhost:8000/api/
        http://localhost:8000/api/get-address
        http://localhost:8000/api/get-gps
    ```       
    
<br/>

## **License**
<br/>
This project is under license from MIT. For more details, see the LICENSE file.

Made with :heart: by <a href="https://github.com/EngineerDanny" target="_blank">EngineerDanny</a>

&#xa0;