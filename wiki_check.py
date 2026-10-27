import urllib.request, json, urllib.parse

# Wikipedia API for grey-necked picathartes and Mayombe Forest
titles = ["Grey-necked picathartes", "Mayombe Forest", "Picathartes oreas", "Central chimpanzee", "Forest elephant", "Lionel Trill"]
for title in titles:
    params = urllib.parse.urlencode({
        'action': 'query',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': title,
        'format': 'json',
        'redirects': 1
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'OurWorldSite/1.0'})
        resp = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
        data = json.loads(resp)
        pages = data['query']['pages']
        for pid, page in pages.items():
            if 'extract' in page:
                print(f"\n=== {title} ===")
                print(page['extract'][:800])
            else:
                print(f"\n=== {title} === (no extract)")
                if 'title' in page:
                    print(f"  Actual title: {page['title']}")
    except Exception as e:
        print(f"Error for {title}: {e}")
