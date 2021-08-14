import responses
import requests
import daeclipse
import json

class Mock(object):
    def username(self):
        return "ExampleUsername"
    def deviation_url(self):
        return "https://www.deviantart.com/exampleusername/art/example-artwork-12345"
    def body(self, mock_name):
        with open('test/mocks/{0}.json'.format(mock_name)) as json_file:
            return json.load(json_file)


@responses.activate
def test_get_deviation_tags():
    mock = Mock()
    responses.add(
        method=responses.GET,
        url='https://www.deviantart.com/_napi/shared_api/deviation/extended_fetch',
        json=mock.body('extended_fetch'),
        status=200,
        match_querystring=False
    )

    eclipse = daeclipse.Eclipse()
    actual = eclipse.get_deviation_tags(mock.deviation_url())
    expected = ['adopt', 'adoptable', 'ota', 'offertoadopt']
    assert len(actual) == len(expected)
    assert actual == expected
