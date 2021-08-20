import functools
import json

import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
import requests

from . import search_utils as su

bp = Blueprint('search', __name__, url_prefix='/')


HOST = 'data.usajobs.gov'
BASE_URL = 'https://data.usajobs.gov/api/search?'

@bp.route("/")
def search():
    # https://developer.usajobs.gov/API-Reference/GET-api-Search

    payload, continental_us, searched, page, number_of_pages = su.get_flask_request_args(flask.request.args)

    if searched:
        payload['Page'] = su.set_page(payload, page, number_of_pages)
        url = su.make_url(BASE_URL, payload)
        request = requests.request('GET',
                                   url,
                                   headers={'Host': HOST,
                                            'User-Agent': current_app.config['USER_AGENT'],
                                            'Authorization-Key': current_app.config['API_KEY']})
        search_results = json.loads(request.content.decode('utf-8'))
        if 'LocationName' in payload:
            location_lat_long = su.get_location_lat_long(payload.get('LocationName'))
        else:
            location_lat_long = None
        jobs = su.get_jobs(search_results)

        payload = su.fix_text_for_display(payload)

        folium_map = su.make_map(jobs['jobs'], continental_us, location_lat_long,
                                 payload.get('LocationName'), payload.get('Radius'),
                                 flask.request.full_path[2:])

        payload['first'], payload['previous'], payload['next'], payload['last'] = su.set_buttons(flask.request.full_path, int(jobs['number_of_pages']))
        
        payload['map'] = folium_map._repr_html_()
        payload['returned_results'] = jobs['returned_results']
        payload['total_results'] = jobs['total_results']
        payload['total_jobs'] = jobs['total_locations']
        payload['continental_us'] = continental_us
        payload['number_of_pages'] = jobs['number_of_pages']
        payload['scrol_to_anchor'] = 'map'

        return render_template('index.html', content=payload)

    else:
        payload['map'] = su.make_map()._repr_html_()
        payload['Page'] = 1
        payload['SortField'] = 'default'
        payload['SortDirection'] = 'Asc'
        payload['continental_us'] = True
        payload['SortDirection'] = 'Asc'

        return render_template('index.html', content=payload)
