import json, urllib.request, urllib.parse

# Check the metadata of the returned image
title = "Die Vögel Afrikas (1902) Tafel 11 (20326839314).jpg"
encoded_title = urllib.parse.quote("File:" + title)
url = f"https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata|url&format=json&titles={encoded_title}"

try:
    req = urllib.request.Request(url, headers={'User-Agent':'OurWorldSite/1.0'})
    resp = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
    data = json.loads(resp)
    pages = data['query']['pages']
    for pid, page in pages.items():
        if 'imageinfo' in page:
            info = page['imageinfo'][0]
            ext = info.get('extmetadata', {})
            print("ImageDescription:", ext.get('ImageDescription', {}).get('value', 'N/A'))
            print("Artist:", ext.get('Artist', {}).get('value', 'N/A'))
            print("Credit:", ext.get('Credit', {}).get('value', 'N/A'))
            print("LicenseShortName:", ext.get('LicenseShortName', {}).get('value', 'N/A'))
            print("ObjectName:", ext.get('ObjectName', {}).get('value', 'N/A'))
            print("URL:", info.get('url', 'N/A'))
except Exception as e:
    print(f"Error: {e}")
