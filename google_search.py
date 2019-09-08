"""
@author: NishantParmar
@description: Testing the Google Custom Search API.
"""
import api_usage_monitor
import google_translator as translator
import os
import util

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import HttpError
except ImportError:
    os.system("pip install --upgrade google-api-python-client")
    from googleapiclient.discovery import build
    from googleapiclient.http import HttpError

API_USAGE_FILE = "CSE_USAGE.json"
DAILY_LIMIT = 1000
PAGE_COUNT = 2
application_map = {
        "key": "#######",
        "cx": "####:####"
}


def get_search_results(query, lang, geoloc, user_attr):
    """Returns a list of search results fetched from the CSE API
    Keyword arguments:
        query - string of the search query;
        lang - string representing the ISO-code of the language;
        geoloc - string representing the code of the country
    """
    util.write_print_logs("*** get_search_results ***")
    current_usage = api_usage_monitor.get_usage_object(API_USAGE_FILE)
    util.write_print_logs("current_usage = {}" .format(current_usage))
    result_set = list()
    _, count_ = list(current_usage.items())[0]
    updated_count = count_
    if updated_count < DAILY_LIMIT:
        num, start, i = (10, 1, 0)
        while (num + start < 100) & (i < PAGE_COUNT) & \
        (updated_count < DAILY_LIMIT):
            service = build("customsearch", "v1", 
                            developerKey=application_map["key"])
            keyword = translator.translate_keyword(query, lang)
            try:
                res = service.cse().list(
                    q=keyword,
                    cx=application_map["cx"],
                    start=start+(num*i),
                    num=10,
                    gl=geoloc,
                    dateRestrict=user_attr["date_restrict"]
                ).execute()
                print(str(start+(num*i)))
                i += 1
                updated_count += 1
            except HttpError as e:
                print("Could not get search result for keyword: {} from \
                      country: {} because - \n{}".format(keyword, geoloc, e))
                continue
            result_set.append(res)

    api_usage_monitor.save_usage_count(usage_count=updated_count, 
                                       file_path=API_USAGE_FILE)
    return result_set
