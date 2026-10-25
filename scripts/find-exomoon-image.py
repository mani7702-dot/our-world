#!/usr/bin/env python3
"""Custom Wikimedia Commons search with progressive broadening, rate limiting,
no restrictive modifiers, and proper license/UA handling.
Searches multiple keyword variants and collects all acceptable images.
"""
import urllib.request, urllib.parse, json, re, sys, time, os
import subprocess

UA = "Mozilla/5.0 (OurWorld Site; contact andugulamani722@gmail.com)"

def ok_license(license_str):
    """Check if license is acceptable for reuse."""
    ls = license_str.lower()
    if "public domain" in ls or "cc0" in ls or "no restrictions" in ls:
        return True
    if "cc by" in ls:  # includes cc by-sa
        return True
    return False

def api_get(url, params):
    """Make API GET request with browser UA."""
    full_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"  API error: {e}")
        return {}

def search_files(search_term, limit=10):
    """Search Commons File namespace for images."""
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": "6",
        "srlimit": limit,
    }
    data = api_get("https://commons.wikimedia.org/w/api.php", params)
    titles = []
    for item in data.get("query", {}).get("search", []):
        titles.append(item["title"])
    return titles

def get_image_info(title):
    """Get image info including URL and license."""
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "titles": title,
    }
    data = api_get("https://commons.wikimedia.org/w/api.php", params)
    pages = data.get("query", {}).get("pages", {})
    for pid, page in pages.items():
        ii = page.get("imageinfo", [{}])[0] if page.get("imageinfo") else {}
        ext = ii.get("extmetadata", {})
        license_short = ext.get("LicenseShortName", {}).get("value", "")
        artist = ext.get("Artist", {}).get("value", "")
        # Clean HTML from artist
        artist_clean = re.sub(r"<[^>]+>", "", artist).strip()
        url = ii.get("url", "")
        if url:
            return {
                "title": title,
                "url": url,
                "license": license_short,
                "artist": artist_clean,
                "license_url": ext.get("LicenseUrl", {}).get("value", ""),
            }
    return None

def download_image(url, dest):
    """Download image with browser UA to avoid 403."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        with open(dest, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}, trying curl fallback")
        p = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA,
                            "-o", dest, url], capture_output=True)
        return os.path.exists(dest) and os.path.getsize(dest) > 1000

def search_variant(keywords_str):
    """Search with a single keyword variant, return list of acceptable images."""
    titles = search_files(keywords_str)
    if not titles:
        return []
    results = []
    for t in titles:
        time.sleep(1.5)  # rate limit
        info = get_image_info(t)
        if info and ok_license(info["license"]):
            results.append(info)
    return results

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "test"
    keywords = sys.argv[2:] if len(sys.argv) > 2 else ["exomoon", "brown", "dwarf"]

    all_results = []
    # Progressive broadening: try specific, then broader, then very broad
    variants = [
        " ".join(keywords),
        "exomoon brown dwarf",
        "brown dwarf exoplanet system",
        "extrasolar planet brown dwarf",
        "brown dwarf telescope",
        "exoplanet illustration",
    ]

    for i, variant in enumerate(variants):
        print(f"Trying variant {i+1}: '{variant}'")
        results = search_variant(variant)
        for r in results:
            # Skip duplicates by URL
            if r["url"] not in [x["url"] for x in all_results]:
                all_results.append(r)
        if all_results:
            # Found results, use first acceptable
            break
        time.sleep(2)

    if not all_results:
        print("NO usable image found")
        return

    best = all_results[0]
    print(f"\nBest match: {best['title']}")
    print(f"  License: {best['license']}")
    print(f"  Artist: {best['artist'][:150]}")
    print(f"  URL: {best['url']}")

    # Download to assets/images/<slug>.<ext>
    ext = best["url"].rsplit(".", 1)[-1] if "." in best["url"].rsplit("/", 1)[-1] else "jpg"
    dest = f"assets/images/{slug}.{ext}"
    os.makedirs("assets/images", exist_ok=True)
    if download_image(best["url"], dest):
        print(f"Downloaded to: {dest}")
        # Print clean caption template
        artist = best["artist"].strip() if best["artist"].strip() else "Wikimedia Commons"
        license_name = best["license"] if best["license"] else "CC BY"
        print(f"\nCLEAN CAPTION: Photo: {artist} / {license_name} / Wikimedia Commons")
        print(f"IMAGE_PATH: {dest}")
    else:
        print("Download failed")

if __name__ == "__main__":
    main()
