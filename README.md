# **GH-GPS-DJANGO-REST-API**

*A REST api for Ghana's Global Positioning System (GPS) written with Python Django 🐍🐍*
<br/>

## **API Usage**

<br/>
<details>
<!-- http://127.0.0.1:9000/api/get-address?name=KNUST Guesthouse -->
<!-- http://127.0.0.1:9000/api/get-gps?lat=6.6500&long=-1.64878 -->
<summary>Get GhanaPostGPS Address from PlaceName or GPSName.</summary>
<hr/>

## Request

<b>End Point URL:</b> http://127.0.0.1:9000/api/get-address<br>
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
<!-- http://127.0.0.1:9000/api/get-address?name=KNUST Guesthouse -->
<!-- http://127.0.0.1:9000/api/get-gps?lat=6.6500&long=-1.64878 -->
<summary>Get GhanaPostGPS Address from Position (Latitude and Longitude) </summary>
<hr/>

## Request

<b>End Point URL:</b> http://127.0.0.1:9000/api/get-gps<br>
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
