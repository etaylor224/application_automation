import pandas as pd
import yaml
from resume_reader import resume_parser
from job_scraper import api_scrape, job_parser_for_df, job_parser
from resume_matcher import new_matching, matches_to_files


#TODO create database tables for information
#TODO create and build web front end that accesses the database tables and reads data or moves the data
#TODO Create trigger for the script on the web front end API calls
#TODO create docker file and k8s file to run entire thing in K8s

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
url = "https://jsearch.p.rapidapi.com/search"

def run_matching(title):

    resume_text = resume_parser(config["resume_path"])

    jobs = api_scrape(config["url"], title, config['api_key'])

    scored_jobs = new_matching(resume_text, jobs)
    print(f"Matching resume with {title}")

    high_score_job = list()
    low_score_job = list()

    for job in scored_jobs:
        if job['score'] >= 50.00:
            high_score_job.append(job)
        else:
            low_score_job.append(job)

    print(f"Found {len(high_score_job)} jobs with a rating over 50")
    print(f"Found {len(low_score_job)} jobs with a rating less than 50")
    high_prep = job_parser_for_df(high_score_job)
    high_job = matches_to_files(high_prep)
    low_prep = job_parser_for_df(low_score_job)
    low_score = matches_to_files(low_prep)

    print("Creating Excel file")
    with pd.ExcelWriter(f"{title}-positions.xlsx", engine="openpyxl") as w:
        high_job.to_excel(w, sheet_name="High Rating", index=False)
        low_score.to_excel(w, sheet_name="Low Rating", index=False)
    return

if __name__ == "__main__":
    for title in config['job_titles']:
        print(f"Running search for {title}")
        run_matching(title)
