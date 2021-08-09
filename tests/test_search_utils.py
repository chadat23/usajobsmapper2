def test_job_dataclass():
    from usajobsmapper.search_utils import Job

    job = Job('title', 
              'location', 
              'low_grade', 
              'high_grade', 
              'position_start_date', 
              'position_end_date', 
              'url', 
              'lat_long')

    assert job.title == 'title'
    assert job.location == 'location'
    assert job.low_grade == 'low_grade'
    assert job.high_grade == 'high_grade'
    assert job.position_start_date == 'position_start_date'
    assert job.position_end_date == 'position_end_date'
    assert job.url == 'url'
    assert job.lat_long == 'lat_long'


def test_get_flask_rewuqest_args():
    from usajobsmapper.search_utils import get_flask_request_args

    args = {'Keyword': 'one two'}
    actual = get_flask_request_args(args)
    assert actual == 'one%20two'
