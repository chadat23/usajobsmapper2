from dataclasses import dataclass
import functools
import json

import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
import folium
import requests

from . import search_utils as su

bp = Blueprint('locations', __name__, url_prefix='/locations')


HOST = 'data.usajobs.gov'
BASE_URL = 'https://data.usajobs.gov/api/search?'

@dataclass
class Location:
    name: str
    lat_long: list


@bp.route("<job_id>")
def locations(job_id):

    print('#'*25, job_id)
    payload, continental_us, searched, page, number_of_pages = su.get_flask_request_args(flask.request.args)

    payload['Page'] = su.set_page(payload, page, number_of_pages)
    url = su.make_url(BASE_URL, payload)
    request = requests.request('GET',
                                url,
                                headers={'Host': HOST,
                                        'User-Agent': current_app.config['USER_AGENT'],
                                        'Authorization-Key': current_app.config['API_KEY']})
    search_results = json.loads(request.content.decode('utf-8'))

    _search_results = search_results['SearchResult']
    _search_result_items = _search_results.get('SearchResultItems')

    for result in _search_result_items:
        _matched_object_descriptor = result['MatchedObjectDescriptor']
        position_id = _matched_object_descriptor['PositionID'] 
        if position_id == job_id:
            locations = []

            for _position_location in _matched_object_descriptor['PositionLocation']:
                location = _position_location['LocationName']
                lat_long = [float(_position_location['Latitude']), float(_position_location['Longitude'])]

                locations.append(Location(location, lat_long))

            break
        
    sw = min([lat.lat_long[0] for lat in locations]), min([lat.lat_long[1] for lat in locations])
    ne = max([long.lat_long[0] for long in locations]), max([long.lat_long[1] for long in locations])

    folium_map = folium.Map()
    folium_map.fit_bounds([sw, ne])
    for location in locations:
        tool_tip = f'''{location.name}
                    '''
        folium.Marker(location.lat_long, tooltip=tool_tip).add_to(folium_map)

    folium.raster_layers.TileLayer(tiles='stamenterrain', name='Stamen Terrain').add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    print(locations)

    payload = {}
    payload['map'] = folium_map._repr_html_()

    return render_template('locations.html', content=payload)
    
