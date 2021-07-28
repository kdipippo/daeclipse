from daeclipse import *
import json
import pathlib
import logging

def test_convert_html_to_editorraw__simple():
    input = "This is an <b>example</b> <i>journal</i> <u>main</u> content."
    with open('tests/expected/simple.json') as json_file:
        expected = json.load(json_file)
    actual = convert_html_to_editorraw(input)
    assert actual == expected

def test_convert_html_to_editorraw__complex():
    input = """
<h2>Subtitle Text</h2>
<p>This is an <u><i>example</i></u> <b><i>first</i></b> <b><u>paragraph</u></b> <b>that</b> <i>has</i> <u>overlapping</u> styles. This is the second sentence of this paragraph.</p>
<p>This is another line right afterward.</p>
<h2>Second Subtitle Text</h2>
<p>Below is us adding an ordered list:
<ul>
    <li>Ordered list item 1</li>
    <li>Ordered list item 2</li>
    <li>Ordered list item 3</li>
</ul>
<p>Below is us adding an unordered list:
<ol>
    <li>Unordered list item 1</li>
    <li>Unordered list item 2</li>
    <li>Unordered list item 3</li>
</ol>
<blockquote>"This is an example blockquote. To err is to human. Time to go to Taco Bell." - Karl Marx</blockquote>
<p>End of journal entry.</p>
"""
    with open('tests/expected/complex.json') as json_file:
        expected = json.load(json_file)
    actual = convert_html_to_editorraw(input)
    assert actual == expected
