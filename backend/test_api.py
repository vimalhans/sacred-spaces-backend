import urllib.request
import json

# Test countries
r = urllib.request.urlopen("http://localhost:8000/api/countries")
countries = json.loads(r.read())
print(f"Countries: {len(countries)}")

# Test places
r = urllib.request.urlopen("http://localhost:8000/api/places")
places = json.loads(r.read())
print(f"Places: {len(places)}")

# Test place detail
r = urllib.request.urlopen("http://localhost:8000/api/places/1")
p = json.loads(r.read())
print(f"Place: {p['name']} | Events: {len(p['events'])} | PrayerTimes: {len(p['prayer_times'])}")

# Test search
r = urllib.request.urlopen("http://localhost:8000/api/places?religion=Islam")
islamic = json.loads(r.read())
print(f"Islamic places: {len(islamic)}")

# Test place detail serialization
for place in places[:2]:
    print(f"  {place['name']} - {place.get('country_name','?')}")
