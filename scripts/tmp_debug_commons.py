import urllib.request, urllib.parse, json, time

url = 'https://commons.wikimedia.org/w/api.php'

# First, do a simple search
params = urllib.parse.urlencode({
    'action': 'query',
    'format': 'json',
    'list': 'search',
    'srsearch': 'Clusia plant leaves',
    'srnamespace': '6',
    'srlimit': '10',
})
req = urllib.request.Request(url + '?' + params, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
try:
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode('utf-8'))
    print("RAW RESPONSE:")
    print(json.dumps(data, indent=2)[:3000])
except Exception as e:
    print(f"ERROR: {e}")
