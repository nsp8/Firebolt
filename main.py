# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 23:52:01 2019

@author: NishantParmar
"""
from constants import USERS
import database_handler as db
import google_search as search
import gsuite_handler as gs
import os
import pandas as pd
import util

CLM = db.table_to_dataframe(table_name="country_language_map")
existing_data = db.table_to_dataframe(table_name="search_results")
data_final_columns = ["search_query", "user", "title", "link", "sector", 
                      "displayed_date", "published_date", "created_date", 
                      "relevance"]
"""Initiating process for each user"""
util.write_print_logs("main.py: Initiating process for each user")


def read_file_inputs(user):
    try:
        input_dir = os.path.join(os.getcwd(), user)
        if os.path.isdir(input_dir):
            input_file = os.path.join(input_dir, "inputs.xlsx")
        else:
            return None

        inputs = pd.read_excel(input_file, sheet_name=None)
        return inputs
    except FileNotFoundError:
        return None

    except ImportError:
        os.system("pip install xlrd >= 1.0.0")
        inputs = pd.read_excel(input_file, sheet_name=None)   
        return inputs


def seek():
    """Initiates the collection of search results and returns a dictionary of 
    user-specific dictionary of search results"""
    collection = dict()
    for user, user_attr in USERS.items():
        """Handle reading the "inputs" file of the user from Google Drive"""
        inputs = gs.handle_inputs(user)

        """
        # Default method of reading inputs:
        inputs = read_file_inputs(user)
        """

        if not inputs:
            continue        
        """Handle preparing DataFrame out of existing data"""
        existing_user_data = existing_data[existing_data["user"] == user]
        print("\nexisting user data: {}".format(existing_user_data.shape))

        """Initiate saving the output in DB"""
        user_data_collection = dict()
        for sheet_name, inputs_df in inputs.items():
            print("\nsheet_name = {}".format(sheet_name))
            
            if not inputs_df.empty:
                inputs_df.dropna(inplace=True)
                inputs_df.reset_index(inplace=True)
                data_final = list()
                for i in range(len(inputs_df)):
                    (_, country, search_term) = inputs_df.loc[i]
                    country = country.strip().lower()
                    sub_df = CLM[CLM["country_name"] == country]
                    target_lang = sub_df["language_ISO"].squeeze()
                    country_code = sub_df["country_ISO"].squeeze()
                    search_string = "{} {}".format(country, 
                                     search_term.strip())
                    
                    """Fetch search results"""
                    util.write_print_logs("search string:{}".format(
                            search_string))
                    
                    is_target_lang_empty = 'empty' in dir(target_lang)
                    is_country_code_empty = 'empty' in dir(country_code)
                    if is_target_lang_empty or is_country_code_empty:
                        msg_ = "Is target_lang empty: {}\n"
                        msg_ += "Is country code empty: {}\n"
                        msg_ += "Skipping this row!"
                        util.write_print_logs(
                                msg_.format(is_target_lang_empty,
                                            is_country_code_empty))
                        continue
                    search_results = search.get_search_results(
                            query=search_string, 
                            lang=target_lang, 
                            geoloc=country_code,
                            user_attr=user_attr)
    
                    if search_results:
                        util.write_print_logs("Found search results")
                        util.write_responses(search_results, search_term)
                        unified_results = util.unify_results(search_results)
                        if unified_results:
                            util.write_print_logs("Fetching Useful Info")
                            search_response = util.fetch_useful_info(
                                    unified_results, search_string, user_attr)
    
                            for response in search_response:
                                data_final.append(response)
    
                data_final_df = pd.DataFrame(data_final,
                                             columns=data_final_columns)
                data_final_df["user"] = user
                data_final_df["sector"] = sheet_name
                data_final_df["created_date"] = util.get_current_date()

                """Removing duplicate results from the final object"""
                data_final_df.drop_duplicates(subset="link", inplace=True)
                data_final_df.sort_values(by="search_query", inplace=True)
                user_data_collection[sheet_name] = data_final_df
        collection[user] = user_data_collection
    return collection


def materialize(collection):
    """Serializes the collection of search results to the database
    Keyword arguments:
        message - dictionary of user-specific search results
    """
    super_dataframe = pd.DataFrame()
    for user, user_output in collection.items():
        for sector, dataframe in user_output.items():
            util.write_print_logs("Sector: {}".format(sector))
            if super_dataframe.empty:
                super_dataframe = dataframe
            else:
                super_dataframe = super_dataframe.append(dataframe, 
                                                         ignore_index=True)
    if not super_dataframe.empty:
        db.dataframe_to_table(dataframe=super_dataframe, 
                              table_name="search_results")
