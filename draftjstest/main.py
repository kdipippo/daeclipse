from html_to_draftjs import html_to_draftjs
import json


json = html_to_draftjs("""
    <h1>My Page</h1>

    <h2>Introduction</h2>

    <p>Some <em>content</em> that is pretty <strong>interesting</strong></p>
    <p>Don't forget to <a href="https://example.com">follow me!</a></p>

    <h2>Illustration</h2>
    <p><img src="https://example.com/image.png" alt="image" /></p>
""")
print(json.dump(html_to_draftjs("Test status post, please ignore.")))
