import requests
from bs4 import BeautifulSoup
from aiounfurl import exceptions
from aiounfurl.headers_utils import generate_headers
from aiounfurl.parsers import oembed, open_graph, meta_tags, twitter_cards


def _fetch_data(url, oembed_url_extractor=None, headers=None):
    result = {}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html5lib')
    if oembed_url_extractor:
        oembed_url = oembed_url_extractor.get_oembed_url_from_html(soup)
        if oembed_url:
            resp = requests.get(oembed_url, headers=headers)
            result['oembed'] = resp.json()
    result['open_graph'] = open_graph.extract_from_html(soup)
    result['twitter_cards'] = twitter_cards.extract_from_html(soup)
    result['meta_tags'] = meta_tags.extract_from_html(soup)
    return result


def fetch_all(url, loop=None, oembed_providers=None,
              oembed_params=None, prefered_languages=None):
    oembed_url_extractor = oembed.OEmbedURLExtractor(
        oembed_providers or [], params=oembed_params)
    oembed_url = oembed_url_extractor.get_oembed_url(url)

    headers = generate_headers(prefered_languages)
    result = {}
    if oembed_url:
        resp = requests.get(oembed_url, headers=headers)
        oembed_result = resp.json()
        if isinstance(oembed_result, dict):
            result['oembed'] = oembed_result
    else:
        other_results = _fetch_data(
            url, oembed_url_extractor=oembed_url_extractor,
            headers=headers)
        result.update(other_results)
    return result


def get_preview_data(url, oembed_providers=None, oembed_params=None, prefered_languages=None):
    data = fetch_all(
        url,
        oembed_providers=oembed_providers,
        oembed_params=oembed_params,
        prefered_languages=prefered_languages)
    result = {'title': None, 'description': None, 'image': None}
    sources = ['oembed', 'open_graph', 'twitter_cards', 'meta_tags']
    for field in ['title', 'description']:
        for source in sources:
            result[field] = data.get(source, {}).get(field)
            if result[field]:
                break
        result[field] = result[field] or None

    # oembed image
    if data.get('oembed'):
        if data['oembed']['type'] == 'photo':
            result['image'] = data['oembed'].get('url')
        elif data['oembed'].get('thumbnail_url'):
            result['image'] = data['oembed']['thumbnail_url']

    # open graph image
    if not result['image'] and data.get('open_graph'):
        image = data['open_graph'].get('image')
        if image and isinstance(image, list):
            result['image'] = image[0]
        elif image:
            result['image'] = image

    # twitter cards image
    if not result['image'] and data.get('twitter_cards'):
        result['image'] = data['twitter_cards'].get('image')

    # from meta tags
    if not result['image'] and data.get('meta_tags'):
        result['image'] = data['meta_tags'].get('image') or None
    return result
