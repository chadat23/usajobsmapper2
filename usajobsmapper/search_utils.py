from dataclasses import dataclass
import datetime

from flask import current_app
import folium
from geopy.geocoders import Nominatim  # https://www.geonames.org/ account needed


@dataclass
class Job:
    title: str
    location: str
    low_grade: str
    high_grade: str
    position_start_date: str
    position_end_date: str
    url: str
    # organization: str
    # job_grade: str
    lat_long: list


def get_flask_request_args(args):
    payload = {}

    if vals := args.get('Keyword'):
        payload['Keyword'] = vals.replace(' ', '%20')
    if vals := args.get('PositionTitle'):
        payload['PositionTitle'] = vals.replace(' ', '%20')
    if vals := args.get('PayGradeHigh'):
        payload['PayGradeHigh'] = vals
    if vals := args.get('PayGradeLow'):
        payload['PayGradeLow'] = vals
    if vals := args.get('JobCategoryCode'):
        payload['JobCategoryCode'] = vals.replace(' ', ';')
    if vals := args.get('LocationName'):
        payload['LocationName'] = vals.replace(' ', '%20')
    if vals := args.getlist('Organization'):
        payload['Organization'] = ';'.join(vals)
    else:
        payload['Organization'] = ''
    if vals := args.getlist('PositionScheduleTypeCode'):
        payload['PositionScheduleTypeCode'] = ';'.join(vals)
    else:
        payload['PositionScheduleTypeCode'] = ''
    payload['RelocationIndicator'] = 'True' if args.get('RelocationIndicator') else ''
    if vals := args.get('JobGradeCode'):
        payload['JobGradeCode'] = vals.replace(' ', ';')
    if vals := args.get('SortField'):
        payload['SortField'] = vals
    else:
        payload['SortField'] = 'default'
    if vals := args.get('SortDirection'):
        payload['SortDirection'] = vals
    if vals := args.get('Radius'):
        payload['Radius'] = vals
    payload['Fields'] = 'Min'
    if vals := args.getlist('HiringPath'):
        payload['HiringPath'] = ';'.join(vals)
    else:
        payload['HiringPath'] = ''
    if vals := args.get('Page'):
        payload['Page'] = vals

    if vals := args.get('nav-button'):
        page = vals
    else:
        page = None

    if vals := args.get('number-of-pages'):
        number_of_pages = vals
    else:
        number_of_pages = 1

    continental_us = True if args.get('ContinentalUS') else False
    searched = True if len(args) else False

    return payload, continental_us, searched, page, number_of_pages


def fix_text_for_display(payload):
    if val := payload.get('Keyword'):
        payload['Keyword'] = val.replace('%20', ' ')
    if val := payload.get('PositionTitle'):
        payload['PositionTitle'] = val.replace('%20', ' ')
    if val := payload.get('LocationName'):
        payload['LocationName'] = val.replace('%20', ' ')
    if val := payload.get('JobCategoryCode'):
        payload['JobCategoryCode'] = val.replace(';', ' ')
    if val := payload.get('Keyword'):
        payload['Keyword'] = val.replace(';', ' ')

    return payload


def make_url(base_url, payload):
    payload = '&'.join([f'{k}={v}' for k, v in payload.items() if v != ''])
    
    return base_url + payload


def get_jobs(contents):
    jobs = {}

    _search_results = contents['SearchResult']
    _search_result_items = _search_results.get('SearchResultItems')
    jobs['number_of_pages'] = _search_results.get('UserArea').get('NumberOfPages')

    jobs['returned_results'] = _search_results['SearchResultCount']
    jobs['total_results'] = _search_results['SearchResultCountAll']
    print('returned results', jobs['returned_results'])
    print('total results', jobs['total_results'])

    listings = []
    for result in _search_result_items:
        _matched_object_descriptor = result['MatchedObjectDescriptor']

        title = _matched_object_descriptor['PositionTitle']
        url = _matched_object_descriptor['PositionURI']
        job_grade = _matched_object_descriptor['JobGrade'][0]['Code']

        position_start_date = _matched_object_descriptor['PositionStartDate']
        position_start_date = position_start_date[:10]
        d = datetime.datetime.strptime(position_start_date, '%Y-%m-%d')
        position_start_date = d.strftime('%m/%d/%Y')

        position_end_date = _matched_object_descriptor['PositionEndDate']
        position_end_date = position_end_date[:10]
        d = datetime.datetime.strptime(position_end_date, '%Y-%m-%d')
        position_end_date = d.strftime('%m/%d/%Y')

        _user_area = _matched_object_descriptor['UserArea']
        _details = _user_area['Details']
        low_grade = _details['LowGrade']
        high_grade = _details['HighGrade']
        low_grade = f'{job_grade}-{low_grade.zfill(2)}'
        high_grade = f'{job_grade}-{high_grade.zfill(2)}'

        for _position_location in _matched_object_descriptor['PositionLocation']:
            location = _position_location['LocationName']
            lat_long = [float(_position_location['Latitude']), float(_position_location['Longitude'])]

            listings.append(Job(title, location, 
                            low_grade, high_grade, 
                            position_start_date, position_end_date,
                            url, lat_long)
                            )

    jobs['jobs'] = listings

    jobs['total_locations'] = len(listings)

    print('number of job locations', jobs['total_locations'])

    return jobs

    # return jobs, returned_results, total_results, number_of_pages


def make_map(jobs=[], continental_us=None, location_lat_long=None, location_name=None, radius=None):
    #  https://coolum001.github.io/foliummaps.html
    max_lat = 49.371643
    min_lat = 25.827089
    max_long = -66.927119
    min_long = -124.639440

    if jobs:
        if continental_us:
            jobs = [j for j in jobs if min_lat < j.lat_long[0] < max_lat and min_long < j.lat_long[1] < max_long]

        sw = min([lat.lat_long[0] for lat in jobs]), min([lat.lat_long[1] for lat in jobs])
        ne = max([long.lat_long[0] for long in jobs]), max([long.lat_long[1] for long in jobs])
    else:
        sw = min_lat, min_long
        ne = max_lat, max_long

    start_coords = (sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2

    folium_map = folium.Map(location=start_coords)
    folium_map.fit_bounds([sw, ne])

    for job in jobs:
        tool_tip = f'''{job.title}
                        <br>
                        {job.location}
                        <br>
                        Flying: {job.position_start_date} - {job.position_end_date}
                        <br>
                        {job.low_grade}{'' if job.low_grade == job.high_grade else f' - {job.high_grade}'}
                    '''
        popup = f'<a href="{job.url}" target="_blank">{job.url}</a>'
        folium.Marker(job.lat_long, popup=popup, tooltip=tool_tip).add_to(folium_map)

    if location_lat_long:
        folium.Marker(location=location_lat_long, tooltip=location_name,
                      icon=folium.Icon(color='green')).add_to(folium_map)

    if location_lat_long and radius:
        folium.Circle(location_lat_long,
                      radius=float(radius) / 0.0006213712,
                      color="green",
                      fill=False,
                      ).add_to(folium_map)

    # folium.raster_layers.TileLayer(tiles='OpenStreetMap', name='Open Street Map').add_to(folium_map)
    # folium.raster_layers.TileLayer(tiles='stamentoner', name='Black/White Map').add_to(folium_map)
    folium.raster_layers.TileLayer(tiles='stamenterrain', name='Stamen Terrain').add_to(folium_map)
    # folium.raster_layers.TileLayer(tiles='CartoDB dark_matter', name='CartoDB dark_matter').add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    return folium_map


def get_location_lat_long(location):
    location = location.replace('%20', ' ')

    geolocator = Nominatim(user_agent=current_app.config['USER_AGENT'])
    location = geolocator.geocode(location)

    return location.latitude, location.longitude


def set_page(payload, page, number_of_pages):
    if page == 'first':
        return '1'
    elif int(payload['Page']) > 1 and page == 'previous':
        return str(int(payload['Page']) - 1)
    elif page == 'next':
        return str(int(payload['Page']) + 1)
    elif int(payload['Page']) < int(number_of_pages) and page == 'last':
        return number_of_pages

    return payload['Page']