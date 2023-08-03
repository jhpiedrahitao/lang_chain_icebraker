import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    print(linkedin_profile_url)
    response = requests.get(
        "https://gist.githubusercontent.com/jhpiedrahitao/50e69934c67895e4147b1d6ba836d80e/raw/683d093020eed7b9f39a163cb65bab1542aac8d0/jhpiedrahitao.json"
    )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
