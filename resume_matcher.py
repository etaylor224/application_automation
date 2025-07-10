from sentence_transformers import SentenceTransformer, util
import pandas as pd

def new_matching(resume:str, postings:list):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    resume_embed = model.encode(resume)

    matches = []

    for jobs in postings:

        desc_embed = model.encode(jobs['job_description'])
        sim = util.cos_sim(resume_embed, desc_embed).item()
        value = round((sim * 100), 2)
        jobs['score'] = value
        matches.append(jobs)
        # if value >= 40.0:
        #     jobs['score'] = value
        #     matches.append(jobs)
    return matches

def matches_to_files(spots:list):
    df = pd.DataFrame()
    for spot in spots:
        temp = pd.DataFrame().from_dict(spot)
        df = pd.concat([df, temp])
    return df