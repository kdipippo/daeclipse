import json
import re

# "This is an <b>example</b> <i>journal</i> <u>main</u> content."
def convert_html_to_editorraw(input_html):
    # ['This is an ', '<b>example</b>', ' ', '<i>journal</i>', ' ', '<u>main</u>', ' content.']
    clean = re.compile('<.*?>')
    split_html = re.findall(r'<[^>]*>.*?</[^>]*>(?:<[^>]*/>)?|[^<>]+', input_html)
    inlineStyleRanges = []
    offset = 0
    for entry in split_html:
        if entry[:3] not in ["<b>", "<i>", "<u>"]:
            offset += len(entry)
            continue
        inlineStyleRange = {
            "offset": offset,
            "length": len(entry) - 7
        }
        if entry[:3] == "<b>":
            inlineStyleRange["style"] = "BOLD"
        elif entry[:3] == "<i>":
            inlineStyleRange["style"] = "ITALIC"
        elif entry[:3] == "<u>":
            inlineStyleRange["style"] = "UNDERLINE"
        inlineStyleRanges.append(inlineStyleRange)
        offset += len(entry) - 7
    return {
        "blocks": [
            {
                "key": "foo",
                "text": re.sub(clean, '', input_html),
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": inlineStyleRanges,
                "entityRanges": [],
                "data": {}
            }
        ],
        "entityMap": {}
    }

'''
This can't support the Wix .gif plugin, as there are too many fields we can't infer from the code conversion:
"entityMap": {
    "0": {
        "type": "wix-draft-plugin-giphy",
        "mutability": "IMMUTABLE",
        "data": {
            "config": {
                "size": "small",
                "alignment": "center"
            },
            "gif": {
                "originalUrl": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy.gif",
                "originalMp4": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy.mp4",
                "stillUrl": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy_s.gif",
                "downsizedUrl": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy.gif",
                "downsizedStillUrl": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy_s.gif",
                "downsizedSmallMp4": "https://media4.giphy.com/media/y4PQTcLTYJwOI/giphy-downsized-small.mp4",
                "height": 320,
                "width": 240
            }
        }
    }
}
'''
