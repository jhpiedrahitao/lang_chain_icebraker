import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {
        "Authorization": f'Bearer {os.environ.get("NUBELA_PROXY_CURL_API_KEY")}'
    }
    params = {
        "url": linkedin_profile_url,  #'https://www.linkedin.com/in/jhpiedrahitao',
        #'fallback_to_cache': 'on-error',
        #'use_cache': 'if-present',
        #'skills': 'include',
        #'inferred_salary': 'include',
        #'personal_email': 'include',
        #'personal_contact_number': 'include',
        #'twitter_profile_id': 'include',
        #'facebook_profile_id': 'include',
        #'github_profile_id': 'include',
        #'extra': 'include',
    }
    response = requests.get(api_endpoint, params=params, headers=header_dic)

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
