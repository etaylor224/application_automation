import requests

def api_scrape(url:str, query:str, key:str):

    querystring = {"query": {query}, "page": "1", "num_pages": "20", "country": "us",
                   "date_posted": "all"}

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['data']


def job_parser(scored_job: list):
    cleaned_jobs = list()
    for x in scored_job:
        job = {
            'job_title': x['job_title'],
            'employer_name': x['employer_name'],
            'employer_web': x['employer_website'],
            'employment_type': x['job_employment_type'],
            'publisher': x['job_publisher'],
            'apply_link': x['job_apply_link'],
            'job_description': x['job_description'],
            'remote': x['job_is_remote'],
            'score': x['score'],
        }
        cleaned_jobs.append(job)
    return cleaned_jobs
