# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:08:01 2019

@author: NishantParmar
"""
from constants import DATE_PATTERNS
from datetime import datetime as dt
from pandas import Series
import errno
import google_translator as translator
import json
import os
import re


date_prefix = lambda param: str(param) if int(param) > 10 else "0"+str(param)


def create_subdirectory(directory_path):
    """
    Creates the new date-wise directory (if it doesn't exist) to store data in 
    separate folders.
    Keyword arguments:
        directory_path - path of the diretory of the destination
    """      
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as exc:
            """Guard against race condition"""
            if exc.errno != errno.EEXIST:
                raise


def write_responses(response, file):
    """Writes the returned JSON responses for record keeping
    Keyword arguments:
        response - object (response) returned by the API call;
        file - string representing the corresponding search keyword of the 
        response as file names
    """
    day_key = "{}-{}-{}".format(
            dt.today().year, 
            dt.today().month, 
            dt.today().day)
    daywise_dir = os.path.join(os.getcwd(), 'Response Outputs', day_key)
    
    if not os.path.isdir(daywise_dir):
        create_subdirectory(daywise_dir)
    
    file_name = os.path.join(daywise_dir, file+'.json')
    with open(file_name, 'a') as resp_f:
        resp_f.writelines(json.dumps(response, indent=4))


def display_date_valid(date_text):
    """Returns True if the "displayed date" is in a proper parsable format;
        False otherwise
    Keyword arguments:
        date_text - string representing the text of snippet from the repsonse
    """
    if not date_text:
        return False
    format_pattern = "(\d+.*\w+.*\s+)(\d+)"
    year_matcher = re.match(format_pattern, date_text)
    if year_matcher:
        year = year_matcher.groups()[-1]
        if int(year.strip()) == dt.today().year:
            return True
        else:
            return False


def format_date(date_text):
    """Returns formatted and english-translated string of date_text
        False otherwise
    Keyword arguments:
        date_text - string representing the text of snippet from the repsonse
    """
    date_pattern = "^(\d+\s\w+(\.)*\s\d+)|^(\d+\s\w+\sago)|^"
    matcher = re.match(date_pattern, date_text)
    if matcher:
        if matcher.groups()[0]:
            
            date_en = translator.translate_keyword(matcher.groups()[0], "en")
            suffix_matcher = re.match("(\d+)(st|nd|rd|th)(.*)", date_en)
            if suffix_matcher:
                date_en = "".join([suffix_matcher.groups()[0], 
                                suffix_matcher.groups()[-1]])
                
            special_ptrn = '([^\d+\s\w+])'
            #'\d+([^\d+\s\w+]*)\s\w+([^\d+\s\w+]*)\s\d+([^\d+\s\w+]*)'
            special_chars = re.search(special_ptrn, date_en)
            if special_chars:
                date_en = date_en.replace(special_chars.group()[-1], '')
            try:
                if dt.strptime(date_en, "%d %b %Y"):
                    return date_en
            except ValueError:
                try:
                    if dt.strptime(date_en, "%d %B %Y"):
                        return date_en
                except ValueError:
                    return matcher.groups()[0]
        if matcher.groups()[1]:
            return translator.translate_keyword(matcher.groups()[1], "en")
    else:
        return ""


def unify_results(resultset):
    """Returns list of relevant search responses from the returned Responses
        (present under the "items" key of the resultset)
    Keyword arguments:
        resultset - object representing Responses
    """
    results = dict()
    results["items"] = list()
    
    for items in resultset:
        if "items" in items.keys():
            for item in items["items"]:
                results["items"].append(item)

    return results


previous_years = lambda base_year, n_years: list(
        range(base_year, base_year-n_years-1, -1))


def previous_months(base_month, n_months):
    months_list = [i for i in map(
            lambda x: x % 12 if x % 12 != 0 else 12, list(
                    range(base_month, base_month-n_months-1, -1)
                    )
            )]
    months_series = Series(months_list)
    months_series.drop_duplicates(inplace=True)
    return list(months_series)


def validate_parts(year, user_attr, month=None):
    """Validates the year of the date string (published/displayed) to be within
    a range.
    Keyword arguments:
        year - string: the year part of the date;
        user_attr - dictionary mapping of a flag representing the validity of 
                    search results and date range parameter, specific to the 
                    user;
        month - string: the month part of the date if the month is to be 
                considered for validation
    """
    print("year = {}".format(year))
    if year:
        filter_match = re.match("(\w)\[(\d+)\]", user_attr["date_restrict"])
        if filter_match:
            restrict_on, num_months = filter_match.groups()
            num_months = int(num_months)
            if restrict_on == "w":
                num_months = num_months // 4
            elif restrict_on == "d":
                num_months = num_months // 30
            elif user_attr["recent_filter"] and restrict_on == "y" and \
            int(year) in previous_years(int(year), num_months):
                return True
        else:
            user_attr["recent_filter"] = False
        if user_attr["recent_filter"]:
            current_year = dt.today().year
            if month and str.isdigit(month):

                if int(month) in previous_months(
                        base_month=int(month), n_months=num_months):
                    if int(month) == 12 and \
                    int(year) in [(current_year - 1), current_year]:
                        return True
                    elif int(month) != 12 and int(year) == current_year:
                        return True
                return False
            else:
                if (int(year.strip()) == current_year):
                    return True
                return False
        return True
    return False


def format_date_string(date_format, date_collection):
    """Formats the output date string on the basis of a date format and a 
    mapping of valid date components.
    Keyword arguments:
        date_format - string : the date format of the output;
        date_collection - dictionary of valid date components
    """
    formatting_split = [i for i in list(re.split("\W+", date_format)) if i]
    formatter = dict()
    for component in formatting_split:
        value = date_collection[component]
        print("value = {}".format(value))
        print("len(value) = {}".format(len(value)))
        if str.isdigit(value) and len(value) == 1:
            value = date_prefix(value)
        formatter[component] = value.strip()
    if formatter:
        formatted_date = date_format.format(**formatter)
        return formatted_date
    return ""


def within_range(date_string, user_attr):
    """On the basis of whether the 
    argument date_string matches one of the regular expression-patterns listed
    below in the list, returns tuple of boolean and string: True if the match 
    was successful along with the formatted date string;(False, None) otherwise
        (present under the "items" key of the resultset)
    Keyword arguments:
        date_string - object representing Responses;
        recent_filter - whether the dates should obey the one-month rule
    """
    for pattern, part in DATE_PATTERNS.items():
        date_match = re.match(pattern, date_string)
        if date_match:
            grouped_date = list(date_match.groups())
            date_components = [date for date in grouped_date if date]
            pos = part["positions"]
            output_format = part["output_format"]
            try:
                year_ = date_components[pos["year"]]
                month_ = date_components[pos["month"]]
                if user_attr["recent_filter"] and \
                not validate_parts(year=year_, month=month_, 
                                   user_attr=user_attr):
                    return (False, None)
                day_ = date_components[pos["day"]]
                date_collection = dict()
                date_collection["year"] = year_
                date_collection["month"] = month_
                date_collection["day"] = day_
    
                readable = format_date_string(output_format, date_collection)
                if readable:
                    return (True, readable)
                return (False, None)
            except KeyError:
                write_print_logs("date string {} didn't match any group. \
                                 Retutrning True for now".format(date_string))
                return (True, date_string)
        else:
            continue
    return (False, None)


def fetch_useful_info(resultset, keyword, user_attr):
    """Returns a list of dictionaries, each representing relevant data from the
    Response object formatted and stored
    Keyword arguments:
        resultset - object formatted to contain "items" from the Results;
        keyword - string representing the search keyword passed to the CSE API
    """
    write_print_logs("\nfetch_useful_info")
    results = resultset["items"]
    collection = list()
    valid_keys = ["metatags", "newsarticle", "creativework", "article", 
                  "blogposting"]
    for result in results:
        write_print_logs("parsing the results...")
        write_print_logs("result[link] = {}".format(result["link"]))
        
        if not result["link"] or result["link"].strip() == "":
            continue
        
        formatted_date = format_date(result["snippet"])
        write_print_logs("formatted_date = {}".format(formatted_date))
        if formatted_date:
            write_print_logs("display_date_valid = {}".format(
                    display_date_valid(formatted_date)))

        info = dict()
        info["link"] = result["link"]
        info["published_date"] = ""
        info["valid_pubdate"] = False
        if "pagemap" in result.keys():
            for pagemap_keys in result["pagemap"].keys():
                
                selected_keys = result["pagemap"][pagemap_keys]
                if "metatags" in pagemap_keys:
                    page_info = selected_keys[-1]
                    meta_tag = set(["article:published_time", 
                            "og:article:published_time",
                             "pubdate"]) & set(page_info.keys())
                    write_print_logs("meta_tag = {}".format(meta_tag))
                    if meta_tag:
                        write_print_logs("Found meta-tag")
                        meta_value = meta_tag.pop()
                        write_print_logs("meta_value = {}".format(meta_value))
                        flag, date = within_range(page_info[meta_value], 
                                                  user_attr)
                        write_print_logs(
                                "flag = {}, date = {}".format(flag, date))
                        if flag:
                            write_print_logs("Setting date")
                            info["valid_pubdate"] = True
                            info["published_date"] = date
                            break
                        else:
                            write_print_logs("published_date_flag -> False")
                            info["valid_pubdate"] = False
                write_print_logs("pubdate of metatags was not found")
                entry_other = result["pagemap"][pagemap_keys]
                if isinstance(selected_keys, list):
                    entry_other = entry_other[-1]
                if "datepublished" in entry_other.keys():
                    pub_date = entry_other["datepublished"]
                    if pub_date:
                        flag, date = within_range(pub_date, user_attr)
                        write_print_logs(
                        "flag = {}, date = {}".format(flag, date))
                        if flag:
                            write_print_logs("Setting date")
                            info["published_date"] = date
                            info["valid_pubdate"] = True
                            break
                        else:
                            write_print_logs(
                                    "published_date_flag -> False")
                            info["valid_pubdate"] = False
        write_print_logs("info['valid_pubdate']: {}".format(
                info["valid_pubdate"]))
        if not info["valid_pubdate"]:
            continue

        info["search_query"] = keyword
        info["title"] = result["title"]
        info["displayed_date"] = formatted_date
        write_print_logs("displayed_date: {}".format(formatted_date))
        write_print_logs("published_date: {}".format(info["published_date"]))
        del info["valid_pubdate"]
        collection.append(info)
    return collection


def write_print_logs(message):
    """Timestamped custom log-composer of events that need to be logged 
    on a processing day's hour and minute.
    Keyword arguments:
        message - object representing Responses
    """
    logs_directory = os.path.join(os.getcwd(), "Logs")
    if not os.path.exists(logs_directory):
        try:
            os.makedirs(logs_directory)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    time_stamp = "{}".format(str(dt.now().replace(microsecond=0)))
    logs_filename = "logs_{dd}{mm}{yyyy}_{h}{m}.txt".format(
            dd=date_prefix(dt.now().day), 
            mm=date_prefix(dt.now().month), 
            yyyy=dt.now().year, 
            h=date_prefix(dt.now().hour), 
            m=date_prefix(dt.now().minute))
    logs_file = os.path.join(logs_directory, logs_filename)
    with open(logs_file, "a", encoding="UTF-8") as log_file:
        log_file.write("\n\n{}: {}".format(time_stamp, message))


def check_equality(df_1, df_2):
    """Checks if two dataframes are equal.
    Keyword arguments:
        df_1 - first dataframe;
        df_2 - second dataframe
    """
    if df_1.shape[0] != df_2.shape[0]:
        return False
    df_1_temp = df_1.fillna("NULL_VALUE")
    df_2_temp = df_2.fillna("NULL_VALUE")
    df_eq = df_1_temp.eq(df_2_temp)
    df_eq.drop_duplicates(inplace=True)
    if df_eq.shape[0] == 1:
        eq_values = df_eq.T.drop_duplicates()
        if len(eq_values) > 1:
            return False
        elif len(eq_values) == 1:
            return True
    else:
        return False


def get_current_date():
    """Generates current date (string) in YYYY-MM-DD format."""
    year = str(dt.now().year)
    month_num = dt.now().month
    month = date_prefix(month_num)
    date_num = dt.now().day
    day = date_prefix(date_num)
    current_date = "{year}-{month}-{day}".format(year=year,month=month,day=day)
    return current_date
