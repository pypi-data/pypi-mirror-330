import pandas as pd
import re
import numpy as np
from typing import Union, Literal,Optional
from fuzzywuzzy import process
from .const import *



class TextFormatters:
    @staticmethod
    def strip_bracketed_suffix(str_name:str):
        """
        This method removes alpahbets present within the brackets at the end

        Args:
        ------------
        str_name: str
            parse the string that has (S)/(P) in the brackets at the end of the survey number

        Return:
        ---------
            :code:`string`
        
        """
        pattern_comparing = r'\([a-zA-Z]\)*$'
        new_d1 = re.sub(pattern_comparing,'',str_name).strip().lower() #converted to lower for matching states that have alphabets and can be either in upper or lower case
        return new_d1
    


    @staticmethod
    def regional_to_english_village(eng_name:str,region:Literal['Hi','Tel','Ka','Od']='Tel'):
        r"""
        converts the village names with regional character to english.

        Args:
        ------
        eng_name: str
            The name (regional) that needs to be converted to english.
        region: str
            the char to be replaced with. Supports :code:`Hi`, :code:`Tel (default)`, :code:`Ka`, and :code:`Od`.

        Return:
        --------
            :code:`string`

        Example:
        ------------
        >>> string = '12/अ/1'
        >>> print(TextFormatters.regional_to_english_village(string,'Hi'))
            '12/A/1'
        """
        if region=='Tel':
            dict_ref = replace_dict_tel
            patter_ref = r'([\u0C00-\u0C7F]+)'

        elif region=='Ka':
            dict_ref = replace_dict_kar
            patter_ref = r'([\u0C80-\u0CFF]+)'

        elif region=='Hi':
            dict_ref =replace_dict_Hin
            patter_ref = r'([\u0900-\u097F\u200d]+)'

        elif region=='Od':
            dict_ref = replace_dict_Od
            patter_ref = r'([\u0B00-\u0B7F]+)'

        else:
            raise ValueError("Supports only 'Hi', 'Tel', 'Ka' or 'Od'")

        sub_value = re.sub(patter_ref,lambda x:  dict_ref.get(x.group().lower()) if dict_ref.get(x.group().lower()) else x.group(),eng_name)
        return sub_value
    

    @staticmethod
    def normalize_alpha_num_slash(string:str,pattern:Literal['En','Hi','Tel','Ka','Od']= 'En'):
        r"""
        This method adds **'/'** inbetween an alphabet and a digit, if alphabet is preceded or succeeded by a digit.
    
        Args:
        -----------
        string: str
            string you want to change
        pattern: str
            the string you are passing has to refer which pattern; supports :code:`En (default)`, :code:`Hi`, :code:`Tel`, :code:`Ka`, and :code:`Od`

        Return:
        -----------
        :code:`string`

        Example:
        ----------------
            
        >>> data = '13/1AA/BB1/E'
        >>> updated_data = normalize_alpha_num_slash(data,'En')
        >>> print(updated_data)
            '13/1/AA/BB/1/E'
        """
        if pattern=='En':
            pattern_ref = pattern_eng

        elif pattern=='Hi':
            pattern_ref = pattern_hi

        elif pattern=='Tel':
            pattern_ref = pattern_tel

        elif pattern=='Ka':
            pattern_ref = pattern_kan

        elif pattern=='Od':
            pattern_ref = pattern_od
        
        else:
            raise ValueError("The pattern did not match. Pattern supports 'En','Hi',and 'Tel' ")

        new_string=string
        ser = re.search(pattern_ref,new_string)
        while re.search(pattern_ref,new_string):
            ser = re.search(pattern_ref,new_string)
            new_string = new_string[:ser.start()+1]+'/'+new_string[ser.start()+1:]

        return new_string




    @staticmethod
    def pick_biggest_parcel(actual_val:str,group_val:list,region:Literal['Hi','Tel','Ka','Od']='Tel',split_pat: str = r"\/|\-"):
        r"""
        If you have one-to-many matches and want to select the first bigger parcel (survey number)
        amongst the list

        Args:
        ---------
        actual_val: str
            The survey number (provided by the client) based on which parcel needs to be selected

        group_val: list
            The list of survey number amongst which you want to know the best parcel to retain

        region: str
            the char to be replaced with. Supports :code:`Hi`, :code:`Tel (default)`, :code:`Ka`, and :code:`Od`. If survey_number is in english than use :code:`Hi`.

        split_pat: str
            The pattern (regex prefered) based on which the text has to split. The default is :code:`\/|\-` i.e. split is based on either **'/'** or **'-'**.

        Return:
        ------------
        The function will return the :code:`index` of the best parcel from the list
        """
        actual_val = TextFormatters.regional_to_english_village(actual_val,region)
        group_val = [TextFormatters.regional_to_english_village(i,region) for i in group_val]
        # print(group_val)
        if actual_val.strip() in [i.strip() for i in group_val]:
            temp_ind = [i.strip() for i in group_val].index(actual_val)
            return temp_ind

        elif len(re.split(split_pat,actual_val))>1:
            if any(len(re.split(split_pat,actual_val)) >= len(re.split(split_pat,matching))for matching in group_val):
                for i in range(len(re.split(split_pat,actual_val)),0,-1):
                    rem = [match for match in group_val if len(re.split(split_pat,match))==i] 
                    if rem:
                        best_ind = group_val.index(process.extractOne(actual_val,rem)[0])
                        # print(best_ind)
                        return best_ind
            else:
                rem_ind = group_val.index(process.extractOne(actual_val,group_val)[0])
                return rem_ind
        else:
            rem_ind = group_val.index(process.extractOne(actual_val,group_val)[0])
            return rem_ind