import regex as re
import pandas as pd
from collections import defaultdict
import neo4j
from functools import reduce


def identify_variables_and_construct_query(pattern):
    '''
    Identify node and relationship variables from a Cypher pattern and construct a dynamic query.
    '''
    node_var_pattern =  r"\((\w+)\)"
    rel_var_pattern =  r"\[(\w+)\]"
    
    # Identify node and relationship variables
    node_vars = re.findall(node_var_pattern, pattern)
    rel_vars = re.findall(rel_var_pattern, pattern)
    
    # If exist variables of nodes or rels
    if node_vars or rel_vars:
        # Match the pattern for extracting possible labels for nodes and relationships
        match_clause = f"MATCH {pattern}"
        
        # Prepare the WITH clause for nodes (extracting labels) and relationships (extracting types)
        with_clause = "WITH DISTINCT "
        
        # Collect node labels
        for node in node_vars:
            with_clause += f"labels({node}) AS {node}_labels, "
        
        # Collect relationship types
        for rel in rel_vars:
            with_clause += f"type({rel}) AS {rel}_type, "

        # Remove the trailing comma from the WITH clause
        with_clause = with_clause.rstrip(', ')
        
        # Create the UNWIND clause to unwind node labels and relationship types
        unwind_clause = ""
        for node in node_vars:
            unwind_clause += f"UNWIND {node}_labels AS {node}\n"
        
        for rel in rel_vars:
            unwind_clause += f"UNWIND [{rel}_type] AS {rel}\n"
        
        
        # Combine node_vars and rel_vars into a single list
        variables = [*node_vars, *rel_vars]

        # Construct the RETURN clause
        return_clause = "RETURN DISTINCT " + ", ".join(map(str, variables)).strip(', ')

        # Construct the full query
        query = match_clause + "\n" + with_clause + "\n" + unwind_clause + "" + return_clause

        return query, node_vars, rel_vars
    
    else:
        return '',node_vars,rel_vars

def get_paths_after_inference(driver,all_paths_with_vars):
    ''' Gets as input a list with all the paths that have variables to be inferred.
    For each path we call the infer label that infers the combination of labels for all the variables in the path.
    The result is a dataframe with columns the variables and values the labels of each variable. Each row is a valid combination of labels.
    If the columns of dataframe (the variables of the path) are not mentioned again in any other dataframe from the other paths then i keep it as it is
    If at least one column of the dataframe matches the column of another dataframe then i join these 2 (so that ikeep only the valid combination of labels among all the variables)
    Finally return all the dataframes '''

    df_list = [] # list to store all the final dataframes
    for path in all_paths_with_vars:
        query_w_labels, _, _ = identify_variables_and_construct_query(path) 
        df_var_labels = driver.execute_query(query_w_labels,database_="neo4j",result_transformer_=neo4j.Result.to_df)# dataframe with columns the vars of the path and rows the valid label combinations
        df_var_labels_columns = set(df_var_labels.columns)

        entered = False #flag to check if the df_var_labels entered the list

        # Check for joinable DataFrames in the list ( the joinable if nay will be only one)
        matched_indexes = {} # dict of the indexes of the dfs in df_list the df_var_labels matched and the joinable columns
        merged_dfs = [] #list of the merged datadrames with df_var_labels 
        
        for i, df in enumerate(df_list):    
            df_columns = set(df.columns)
            joinable_columns = list(df_var_labels_columns & df_columns)
            if joinable_columns:
                inner_join = df_var_labels.merge(df, on=joinable_columns, how="inner")
                merged_dfs.append(inner_join)
                matched_indexes[i] = joinable_columns

        #Merge the list of merged dataframes into one df
        if merged_dfs:
            merged_df = reduce(lambda left, right: left.merge(right, how='inner'), merged_dfs)

            # Replace the original DataFrames (in the indexes in matched_index) in the list with the joined result
            for index in sorted(matched_indexes.keys(), reverse=True):
                del df_list[index]

            # Add the new element
            df_list.append(merged_df)
            entered = True
            
        if not entered: #it didnt join , so it didnt enter the list        
            df_list.append(df_var_labels)#No joinable DataFrame found, i leave the df as it is and add it on the list   

    return df_list

def replace_with_labels(path, replacements):
    """
    Replace variables inside nodes (parentheses) or relationships (square brackets) 
    in the query with corresponding values from replacements.
    
    Args:
        query (str): The query string where replacements are to be made.
        replacements (dict): A dictionary where each key is an identifier to be replaced, and each value is the replacement.

    Returns:
        str: The updated query with identifiers replaced by their corresponding values from replacements.
    """
    # Pattern to match both variables inside parentheses (nodes) and square brackets (relationships)
    pattern = r"\(\s*(\w+)\s*\)|\[\s*(\w+)\s*\]"
    # Use re.sub to replace variables with corresponding values from the replacements dictionary
    return re.sub(pattern, lambda match: (f"({match.group(1)}:{replacements.get(match.group(1))})" if match.group(1) in replacements# if exists in nodes with labels and also is about node
                                        else f"[{match.group(2)}:{replacements.get(match.group(2))}]"  if match.group(2) in replacements# if exists in rels with labels and also is about rel
                                        else match.group(0) # as it is
                                    ), path)
