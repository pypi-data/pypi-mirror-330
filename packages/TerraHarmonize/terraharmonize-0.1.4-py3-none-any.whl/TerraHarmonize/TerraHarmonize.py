import pandas as pd
import re
import numpy as np
from typing import Union, Literal,Optional
from fuzzywuzzy import process
from .const import *
from .utils import TextFormatters
import random


class SurveyMatching:
    """
    Args:
    --------
    comp: str
        The survey number that needs to be looked for a match.
    check_list: list
        List containing survey number from our database for POC
            
    .. note::

        Make sure it is a :code:`list` and not a :code:`string list`. Import :code:`ast` and use :code:`ast.literal_eval(<list>)` to convert :code:`string-list` to :code:`list`.
    """ 
   
    

    def __init__(self,comp:str,check_list:list[str]):
        """

        Args:
        --------
        comp: The survey number that needs to be looked for a match.
        to_check_list: List containing survey number from our database for POC
                
        .. note::

           Make sure it is a `list` and not a `string list`. Import ast and use ast.literal_eval(<list>) to convert `string list` to `list`.
        """ 
        
        self.compare = comp
        self.to_check_list =check_list

    
    def d1_d2_matching(self,strip_brackets=True) -> list:
        """
        This method prevents one-to-many matches (one-D1 and many-D2) in D1-D2 matching

        Parameters:
        -------------
        strip_brackets : bool, optional
            If True, removes trailing bracketed alphabets from survey numbers (default is True).

        Return:
        -------------
        :code:`list` containing the index of the correct survey number

        Example:
        -------------
        >>> string = '13/1'
        >>> comparing_list = ['13 (s)','14/1 (s)','13/2 (p)','13/1/1 (p)','13/1/2 (p)']
            # correct index is [0] i.e ['13 (s)']
        >>> print(SurveyMatching(string,comparing_list).d1_d2_matching())
            [0]
        """
        if strip_brackets:
            new_compare = TextFormatters.strip_bracketed_suffix(self.compare)

        else:
            new_compare = self.compare.strip().lower()
        correct_index = []
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            if strip_brackets:
                updated_sur = TextFormatters.strip_bracketed_suffix(sur)
            else:
                updated_sur = sur.strip().lower()

            split_val =[re.sub(r'^0+','',numb).strip() for numb in new_compare.split('/')]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in updated_sur.split('/')]
            if len(split_val)<len(split_val2):
                continue
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass

        return correct_index
    
    
    def poc_matching_simple(self,split_pattern: str = r"\/|\-",
                            strip_brackets:bool=True) -> list:
        r"""  
        A simplified version of POC matching applicable to states like :code:`MP`, :code:`MH`, :code:`OD`, and :code:`RJ`.  

        **Behavior:**  
        - **Does not** add **'/'** between numbers and alphabets.  
        - **Does not** convert regional characters to English.  
        - Only performs simple POC matching based on a split pattern.

        Parameters:
        ------------
        split_pattern : str, default r"\/|\-"
            The regex pattern used for splitting the survey number.

        strip_brackets : bool, default True
            If True, removes bracketed characters at the end of the string.

        Return:
        -------------
        :code:`list` containing the index of the correct survey number

        .. note::

           This method is used for states that do not have regional language issues and the client data format matches the DB format of the survey number

        Example:
        -------------
        >>> string = '13/1'
        >>> comparing_list = ['13/1 (s)','14/1 (s)','13/2 (p)','13/1/1 (p)']
            # correct index is [0,3] i.e ['13/1 (s)','13/1/1 (p)']
        >>> print(SurveyMatching(string,comparing_list).poc_matching_simple())
            [0,3]
        """
        if strip_brackets:
            new_compare = TextFormatters.strip_bracketed_suffix(self.compare.strip())

        else:
            new_compare = self.compare.lower().strip()

        correct_index = []
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            if strip_brackets:
                updated_sur = TextFormatters.strip_bracketed_suffix(sur.strip())

            else:
                updated_sur = sur.strip().lower()
            split_val =[re.sub(r'^0+','',numb).strip() for numb in re.split(split_pattern,new_compare)]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in re.split(split_pattern,updated_sur)]
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass

        return correct_index
    

    def poc_matching(self,
                        include:Literal['normal','both']='normal',
                        state:Optional[Literal['TS','AP','MH','KA','RJ','OD']]=None,
                        split_pat: str = r"\/|\-",
                        strip_brackets:bool=True,
                        **kwargs) -> list:
        r"""
        Used for poc matching states that have regional/english alphabet in survey_no. This can also be used if the survey_number has different pattern for spliting.
        This will normalize the string i.e. adds **'/'** inbetween an alphabet and a digit.

        Args:
        --------------------- 
        include: str
            It includes :code:`normal (default)` which is used when you want to match without changing the characters i.e the english alphabet will not be converted to Regional character for matching and `both`, which is first matched without changing 
            alphabets and then matched by changing alphabets.
         
        state: str
            The state you are working with. By default state is :code:`None`. The :code:`state` can be anything if :code:`include` is :code:`normal`, but if include is :code:`both`, the :code:`state` has to be mentioned. It takes :code:`TS`, :code:`AP`, :code:`MH`, :code:`RJ`, :code:`OD` or :code:`KA`
           
        split_pat: str
            The pattern (regex prefered) based on which the text has to split. The default is :code:`\/|\-` i.e. split is based on either **'/'** or **'-'**.

        strip_brackets : bool, optional
            If True, removes trailing bracketed alphabets from survey numbers (default is True).            

        Return:
        -------------
        :code:`list` containing the index of the correct survey number
        
        Example:
        -------------------  
        >>> string = '13/A1'
        >>> comparing_list = ['13/A1','14/A/1','12/A/1','13/అ','13-అ/1']
            #correct matching is [0,3,4] index i.e. '13/A1','13/అ','13-అ/1' 
        >>> print(SurveyMatching(string,comparing_list).poc_matching(include='normal'))
            [0]
        >>> print(SurveyMatching(string,comparing_list).poc_matching(include='both',state='AP'))
            [0, 3, 4]
        
        """
        if state is None:
            ref = 'En'

        elif state in ['TS','AP']:
            ref = 'Tel'

        elif state in ['RJ','MH']:
            ref = 'Hi'

        elif state == 'KA':
            ref = 'Ka'

        elif state == 'OD':
            ref = 'Od'

        else:
            raise ValueError("Please enter valid argument. It supports 'TS','AP','MH','KA', 'OD', and 'RJ'")
        
        if strip_brackets:
            new_compare = TextFormatters.strip_bracketed_suffix(TextFormatters.normalize_alpha_num_slash(self.compare.strip(),ref).strip())
        else:
            new_compare = TextFormatters.normalize_alpha_num_slash(self.compare.lower().strip(),ref).strip()
        correct_index = []
        pattern = split_pat
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            if strip_brackets:
                updated_sur = TextFormatters.strip_bracketed_suffix(TextFormatters.normalize_alpha_num_slash(sur.strip()).strip())

            else:
                updated_sur = TextFormatters.normalize_alpha_num_slash(sur.strip().lower()).strip()

            split_val =[re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,new_compare)]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,updated_sur)]
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass
        if include=='both':
            correct_index_up = self._poc_dual_match(self.compare,self.to_check_list,correct_index,ref,pattern,strip_brackets)

        else:
            correct_index_up = correct_index.copy()

        return list(set(correct_index_up))
    

    def _poc_dual_match(self,
                        comparing:str,
                        to_check_list:list[str],
                        index_correct:list[int],
                        refer:str,
                        pattern_spliting,
                        strip_brackets:bool) -> list :
        """
        This method is called by the method 'poc_matching' if 'both' is mentioned as an args.

        Return:
        -------------
        :code:`list` containing the index of the correct survey number
        """
        
        compare = TextFormatters.regional_to_english_village(comparing,refer)

        if strip_brackets:
            new_compare = TextFormatters.strip_bracketed_suffix(TextFormatters.normalize_alpha_num_slash(compare.strip(),refer).strip())

        else:
            new_compare = TextFormatters.normalize_alpha_num_slash(compare.strip().lower(),refer).strip()
        
        pattern = pattern_spliting
        for i, row in enumerate(to_check_list):
            if not pd.notna(row):
                continue
            sur = TextFormatters.regional_to_english_village(row,refer)
            if strip_brackets:
                updated_sur = TextFormatters.strip_bracketed_suffix(TextFormatters.normalize_alpha_num_slash(sur.strip(),refer).strip())

            else:
                updated_sur = TextFormatters.normalize_alpha_num_slash(sur.strip().lower(),refer).strip()
            split_val =[re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,new_compare)]
            
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,updated_sur)]
            
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                index_correct.append(i)
            
            else:
                # print('Not correct')
                pass

        return index_correct
    

    @classmethod
    def poc_matching_dataframe(cls,input_frame:pd.DataFrame,
                            client_survey_col_name:str,
                            satsure_survey_col_name:str,
                            satsure_survey_id_col:str,
                            include:Literal['normal','both']='normal',
                                state:Optional[Literal['TS','AP','MH','KA','RJ','OD']]=None,
                                split_pat: str = r"\/|\-",
                                strip_brackets:bool=True):
        """
        Matches client survey numbers with corresponding Satsure survey numbers and IDs.

        This method processes a DataFrame containing survey details and attempts to match 
        the `client survey number` with entries in `SatSure survey numbers`. 
        It refines the matches based on configurable parameters such as state and string formatting.
        This will normalize the string i.e. adds **'/'** inbetween an alphabet and a digit.

        Parameters:
        -----------
        input_frame : pd.DataFrame
            The input DataFrame containing survey-related data.
        
        client_survey_col_name : str
            The column name in `input_frame` containing client survey numbers as strings.
        
        satsure_survey_col_name : str
            The column name in `input_frame` containing Satsure survey numbers (list of strings).
        
        satsure_survey_id_col : str
            The column name in `input_frame` containing Satsure survey IDs (list of strings, same length as `satsure_survey_col_name`).
        
        include : {'normal', 'both'}, default='normal'
            Specifies the matching mode:
            - 'normal': Standard matching logic i.e regional characters are not changed for matching.
            - 'both': Includes additional matching criteria.
        
        state : {'TS', 'AP', 'MH', 'KA', 'RJ', 'OD'}, optional
            Specifies the state to apply state-specific rules for survey number matching. The default is `None` and should have a value
            if include is `both` 
        
        split_pat : str, default= r"\/|\-"
            Regular expression pattern for splitting survey numbers during processing.
        
        strip_brackets : bool, default=True
            If True, removes bracketed alphabets from suffix from survey numbers before matching.

        Returns:
        --------
        pd.DataFrame
            A modified DataFrame where the matched Satsure survey number and survey id 
            are extracted based on the given criteria. Unmatched entries will have NaN values.

        Raises:
        -------
        ValueError
            If required columns are missing, contain NaN values, or have unexpected data types.

        Example:
        --------
        >>> data = {
        ...     "district": ["A", "B"],
        ...     "survey_number_client": ["12/3", "45-A"],
        ...     "survey_number_satsure": [["12/3అ", "14/5"], ["45-A", "46-B"]],
        ...     "survey_id": [["ID1", "ID2"], ["ID3", "ID4"]]
        ...         }
        >>> df = pd.DataFrame(data)
        >>> SurveyMatching.poc_matching_dataframe(df, "survey_number_client", "survey_number_satsure", "survey_id",'both','TS')
        """
        
        if input_frame[[client_survey_col_name,satsure_survey_col_name]].isna().any().any():
            raise ValueError(f'The input columns {client_survey_col_name} or {satsure_survey_col_name} have NaN values')
        
        if not input_frame[satsure_survey_col_name].apply(lambda x: isinstance(x,list)).all():
            raise ValueError(f'The column {satsure_survey_col_name} should be a list')
        
        if not {client_survey_col_name,satsure_survey_col_name,satsure_survey_id_col} <= set(input_frame.columns):
            missing_column = {client_survey_col_name,satsure_survey_col_name,satsure_survey_id_col}- set(input_frame.columns)
            raise ValueError(f"The following column(s) are missing in the input frame: {','.join(missing_column)}")
        
        column_correct_index = 'correct_index'
        while column_correct_index in input_frame.columns:
            column_correct_index = f'correct_index_{random.randint(1, 25)}'

        state_language_map = {'TS':'Tel','AP':'Tel','MH':'Hi','KA':'Ka','RJ':'Hi','OD':'Od'}
        # to pick only those survey number list whose suffix matches with client data after considering only digits from starting
        input_frame_updated = input_frame.assign(**{
                                                    column_correct_index : lambda file: file.apply(lambda x: [x[satsure_survey_col_name].index(i) for i in x[satsure_survey_col_name]
                                                                                                    if i.strip().startswith((match.group() if (match := re.search(r'^[0-9]{1,}',re.split(r'[\/\-]',x[client_survey_col_name])[0])) else ""))]
                                                                                                    ,axis=1)
                                                    },
                                                **{
                                                    satsure_survey_col_name:lambda file:file.apply(lambda x: [x[satsure_survey_col_name][i] for i in x[column_correct_index]]
                                                                                                            if len(x[column_correct_index])>0
                                                                                                            else np.nan,axis=1)
                                                    },

                                                **{
                                                    satsure_survey_id_col: lambda file:file.apply(lambda x: [x[satsure_survey_id_col][i] for i in x[column_correct_index]]
                                                                                                    if len(x[column_correct_index])>0
                                                                                                    else np.nan,axis=1)
                                                                        
                                                    })
        
        # getting the index of the correct match and updating simultaneously
        matched_index = input_frame_updated.assign(**{column_correct_index: lambda file: file.apply(lambda x:cls(
                                                                                                                x[client_survey_col_name],x[satsure_survey_col_name]
                                                                                                                ).poc_matching(include=include,
                                                                                                                            state=state,
                                                                                                                            split_pat=split_pat,
                                                                                                                            strip_brackets=strip_brackets)
                                                                                                                    if isinstance(x[satsure_survey_col_name],list)
                                                                                                                    else np.nan ,axis=1)
                                                                                                                    
                                                    },
                                                    **{satsure_survey_col_name: lambda file:file.apply(lambda x: [x[satsure_survey_col_name][i] for i in x[column_correct_index]]
                                                                                                        if (isinstance(x[column_correct_index],list) and len(x[column_correct_index])>0)
                                                                                                        else np.nan,axis=1)
                                                                                        
                                                        },
                                                        
                                                    **{satsure_survey_id_col:lambda file:file.apply(lambda x: [x[satsure_survey_id_col][i] for i in x[column_correct_index]]
                                                                                                                if (isinstance(x[column_correct_index],list) and len(x[column_correct_index])>0)
                                                                                                                else np.nan,axis=1)
                                                                                        
                                                        })
        
        # final dataframe with correct matched survey number and survey id corresponding to it
        matched_frame = matched_index.assign(**{column_correct_index:lambda file: file.apply(lambda x: TextFormatters.pick_biggest_parcel(x[client_survey_col_name],
                                                                                                    x[satsure_survey_col_name],
                                                                                                    state_language_map.get(state),split_pat=split_pat)
                                                                                                    if isinstance(x[satsure_survey_col_name],list)
                                                                                                    else np.nan,axis=1)
                                            },
                                            **{satsure_survey_col_name:lambda file:file.apply(lambda x:x[satsure_survey_col_name][int(x[column_correct_index])]
                                                                                                        if pd.notna(x[column_correct_index])
                                                                                                        else np.nan,axis=1)
                                                },
                                            
                                            **{satsure_survey_id_col:lambda file:file.apply(lambda x:x[satsure_survey_id_col][int(x[column_correct_index])]
                                                                                if pd.notna(x[column_correct_index])
                                                                                else np.nan ,axis=1)
                                                                                
                                                }).drop(columns=column_correct_index)
        
        return matched_frame


   
    




