from dataclasses import dataclass
import datetime

from flask import current_app
import folium
from geopy.geocoders import Nominatim  # https://www.geonames.org/ account needed

# from config import user_agent

d = {'PositionID': '5A-AFPC-11066755-207281-BAF',
     'PositionTitle': 'FIREFIGHTER',
     'PositionURI': 'https://www.usajobs.gov:443/GetJob/ViewDetails/595827800',
     'ApplyURI': ['https://www.usajobs.gov:443/GetJob/ViewDetails/595827800?PostingChannelID='],
     'PositionLocationDisplay': 'Goodfellow AFB, Texas',
     'PositionLocation': [{'LocationName': 'Goodfellow AFB, Texas',
                           'CountryCode': 'United States',
                           'CountrySubDivisionCode': 'Texas',
                           'CityName': 'Goodfellow AFB, Texas',
                           'Longitude': -100.40798, 'Latitude': 31.342018}],
     'OrganizationName': 'Air Education and Training Command',
     'DepartmentName': 'Department of the Air Force',
     'JobCategory': [{'Name': 'Fire Protection and Prevention',
                      'Code': '0081'}],
     'JobGrade': [{'Code': 'GS'}],
     'PositionSchedule': [{'Name': 'Full-time',
                           'Code': '1'}],
     'PositionOfferingType': [{'Name': 'Permanent',
                               'Code': '15317'}],
     'QualificationSummary': "QUALIFICATIONS: In order to qualify, you must meet the specialized experience requirements described in the Office of Personnel Management (OPM) Qualification Standards for General Schedule Positions, to include the Individual Occupational Requirements (IOR) for the GS-0081, Fire Protection and Prevention Series. SPECIALIZED EXPERIENCE FOR GS-0081-06: Applicants must have at least one (1) year of specialized experience at the next lower grade GS-05, or equivalent in other pay systems. Examples of specialized experience includes airfield and structural, driving and operating firefighting vehicles, crash-rescue operations and reducing/eliminating potential fire hazards. NOTE: You must submit a copy of your resume. FEDERAL TIME-IN-GRADE (TIG) REQUIREMENT FOR GENERAL SCHEDULE (GS) POSITIONS: Merit promotion applicants must meet applicable time-in-&shy;grade requirements to be considered eligible. One year at the GS-05 level is required to meet the time-in-grade requirements for the GS-06 level. TIG applies if you are in a current GS position or held a GS position within the previous 52 weeks. KNOWLEDGE, SKILLS AND ABILITIES (KSAs): Your qualifications will be evaluated on the basis of your level of knowledge, skills, abilities and/or competencies in the following areas: Knowledge to drive and operate firefighting vehicles of significant complexity; of the principles of hydraulics as they pertain to water flow, water pressure, water levels, line (friction) losses, etc; and of basic and specialized firefighting equipment (fire alarm system operation, fire extinguishing equipment operation, etc.), techniques, and procedures. Knowledge of basic building design, construction, and occupancy. Knowledge to apply emergency first aid techniques; and of safety requirements as outlined in applicable safety standards, regulations, and/or technical orders. Skill in operating communications equipment; and in detecting and recognizing fire hazards (potential and immediate). Ability to maintain good working relations; to communicate orally and in writing; and to lift and carry heavy loads. Ability to drive and operate firefighting vehicles of significant complexity; and to apply emergency first aid techniques. MAXIMUM ENTRY AGE: Title 5 U.S.C. 3307 authorizes the head of any agency to establish a maximum entry age for the original appointment of individuals to the position of primary and rigorous firefighter. For initial appointments, applicants cannot have reached their 37th birthday by date of appointment. Individuals who are past the maximum entry age limit (37 years) and have prior Federal civilian firefighter experience covered by title 5 U.S.C. section 8336(c), need to upload their first Appointment SF50's into a GS-0081 position to verify if age waiver is still required or if that time can be subtracted from your current age and qualify for reentry without the age waiver. Effective 1 Jun 00, all DoD firefighters and contract fire and emergency service personnel must be certified at the next higher level before being eligible for promotion to that level. Applicants must list their current firefighter related licenses and certificates on their resumes. Please attach copies of certifications when you submit the resume to verify qualification requirements for the position. Certification requirements for this position are: Firefighter II (includes Firefighter I), Hazmat Operations (includes Hazmat Awareness), Apparatus Driver Operator- Pumper. IMPORTANT: If you have received a Student ID# for the DoD Fire and Emergency Services Certification Program website (https://go.usa.gov/xdsTR) please provide a copy of your most recent certification transcript. Note: If you do not know your Student ID, you may contact the AFCEC Reachback center at afcec.rbc@us.af.mil. If you do not have a Student ID and/or cannot access the Certificate Program site, you must upload a copy of your individual certifications or transcript at the time of your application or you will be removed from consideration. Special Retirement Provisions Authority: FERS Position covered as rigorous under the FERS special retirement provisions for Federal firefighters [5 U.S.C. 8401(14), 5 U.S.C. 8412(d), and 5 CFR 842.802]. OR CSRS Position covered as rigorous/secondary under the CSRS special retirement provisions for Federal firefighters [5 U.S.C. 8331(21), 5 U.S.C. 8336(c), and 5 CFR 831.902]. PART-TIME OR UNPAID EXPERIENCE: Credit will be given for appropriate unpaid and or part-time work. You must clearly identify the duties and responsibilities in each position held and the total number of hours per week. VOLUNTEER WORK EXPERIENCE: Refers to paid and unpaid experience, including volunteer work done through National Service Programs (i.e., Peace Corps, AmeriCorps) and other organizations (e.g., professional; philanthropic; religious; spiritual; community; student and social). Volunteer work helps build critical competencies, knowledge and skills that can provide valuable training and experience that translates directly to paid employment. You will receive credit for all qualifying experience, including volunteer experience.",
     'PositionRemuneration': [{'MinimumRange': '39311.0',
                               'MaximumRange': '51103.0',
                               'RateIntervalCode': 'Per Year'}],
     'PositionStartDate': '2021-03-22',
     'PositionEndDate': '2021-07-09',
     'PublicationStartDate': '2021-03-22',
     'ApplicationCloseDate': '2021-07-09',
     'PositionFormattedDescription': [{'Label': 'Dynamic Teaser',
                                       'LabelDescription': 'Hit highlighting for keyword searches.'}],
     'UserArea': {'Details': {
         'JobSummary': 'Click on "Learn more about this agency" button below to view Eligibilities being considered and other IMPORTANT information. The primary purpose of this position is to serve as a firefighter assigned to drive and operate firefighting\nvehicles of significant complexity engaged in structural firefighting and rescue operations and assist in reducing\nand/or eliminating potential fire hazards.',
         'WhoMayApply': {'Name': '',
                         'Code': ''},
         'LowGrade': '6',
         'HighGrade': '6',
         'PromotionPotential': 'None',
         'HiringPath': ['fed-transition', 'overseas', 'fed-competitive', 'fed-excepted', 'disability', 'land',
                        'mspouse', 'peace', 'vet'],
         'TotalOpenings': 'Few',
         'AgencyMarketingStatement': 'The mission of the United States Air Force is to fly, fight and win...in air, space and cyberspace. To achieve that mission, the Air Force has a vision of Global Vigilance, Reach and Power. That vision orbits around three core competencies: Developing Airmen, Technology-to-Warfighting and Integrating Operations. Core competencies and distinctive capabilities are based on a shared commitment to three core values -- integrity first, service before self, and excellence in all we do. Click here to view the AF Civilian Employment Eligibility Guide: 30 Percent or More Disabled VeteransAF DCIPS InterchangeAF Internal EmployeeDIBF or MRTFBDoD Transfer (Excluding Air Force)EO 12721 Certain Former Overseas EmployeesEO 13473 Appointment of Certain Military SpousesFormer Federal Employees (Reinstatement)Interagency Career Transition Assistance PlanLand Management EmployeeMilitary Spouse PreferenceNational Service (Peace Corps and VISTA)Non-AF DCIPS InterchangeNon-Appropriated FundNon-DoD TransferOther (Interchange Agreements)People with Disabilities, Schedule AVeterans Employment Opportunities ActVeterans Recruitment Authority',
         'TravelCode': '1',
         'ApplyOnlineUrl': 'https://apply.usastaffing.gov/Application/Apply',
         'DetailStatusUrl': 'https://apply.usastaffing.gov/Application/ApplicationStatus'
     },
         'IsRadialSearch': False}}


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