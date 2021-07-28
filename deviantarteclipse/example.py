import daeclipse
import deviantart
import json

def get_deviation_id(deviation_url):
    """Extract the deviation_id from the full deviantart image URL.

    Args:
        deviation_url (string): deviation URL, i.e. https://da.com/art/Art-12345.
    
    Returns:
        string: Deviation ID.
    """
    url_parts = deviation_url.split("-")
    return url_parts[-1]


eclipse = dAEclipse()

da = deviantart.Api("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET");
popular = da.browse(endpoint="popular", limit=100)
deviations = popular['results']
popular_tags = {}
for deviation in deviations:
    print(f"{get_deviation_id(deviation.url)}\t{deviation.author.username}")
    tags = eclipse.get_deviation_tags(get_deviation_id(deviation.url), deviation.author.username)
    for tag in tags:
        if tag not in popular_tags:
            popular_tags[tag] = 1
        else:
            popular_tags[tag] += 1

with open("popular_tags.json", "w") as outfile: 
    json.dump(popular_tags, outfile)
