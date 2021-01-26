import os
import json
import pandas as pd
import statistics

dataset_dict = {
    'a': 'movies',
    'b': 'birdstrikes'
}

oracle_dict = {
    'c': 'compassql',
    'd': 'dziban'
}

search_algorithm_dict = {
    'e': 'bfs',
    'f': 'dfs'
}

task_dict = {
    'p1': '1. Find Extremum',
    'p2': '2. Retrieve Value',
    'p3': '3. Prediction',
    'p4': '4. Exploration'
}

# path_to_json = '../logs/'
## calculate mean and deviation
path_to_json = '../pilots'

def get_fields_from_vglstr(vglstr):
    encoding_str = vglstr.split(';')[1]
    encoding_str = encoding_str.split(':')[1]
    encodings = encoding_str.split(',')
    fields = []
    for encode in encodings:
        field = encode.split('-')[0]
        if field == '':
            continue
        fields.append(field)
    fields.sort()
    return '+'.join(fields)

## interactions:
## main chart changed because of clicking a field
## specified chart
## added chart to bookmark
## mouseover a related chart - mouseout a related chart
## mouseover on the specified chart - mouseout on the specified chart

## calculate how many unique variable set participants interact with

# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'num_interacted_variable_set'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p3_logs.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p4_logs.json')]

# # calculate mean and deviation
# # res_lst = []

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         logs = json.load(json_file)

#         split_filename = js.split('_')
#         participant_id = split_filename[0].replace('partcipant','')
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]

#         interacted_variable_set = []

#         if_mouseover = False
#         prev_time = 0

#         for log in logs:
            
#             if log["Interaction"] == "main chart changed because of clicking a field" or log["Interaction"] == "specified chart" or log["Interaction"] == "added chart to bookmark":
#                 if "Value" in log:
#                     interacted_variable_set.append(get_fields_from_vglstr(log["Value"]))
#                 continue

#             if log["Interaction"].startswith("mouseover"):
#                 prev_time = log["Time"]
#                 if_mouseover = True
#                 continue
            
#             if if_mouseover and log["Interaction"].startswith("mouseout"):
#                 time_period = (log["Time"] - prev_time) / 1000
#                 if time_period > 0.5 and "Value" in log:
#                     interacted_variable_set.append(get_fields_from_vglstr(log["Value"]))
#                 if_mouseover = False
#                 continue
        
#         num_interacted_variable_set = len(set(interacted_variable_set))
#         # calculate mean and deviation
#         # res_lst.append(num_interacted_variable_set * 1.67)

# # print (sum(res_lst) / len(res_lst), statistics.pstdev(res_lst))

        
#         row = [participant_id, dataset, oracle, search, task, num_interacted_variable_set]
#         jsons_data.loc[index] = row

# jsons_data.to_csv('num_of_interacted_variable_set_split.csv', index=False)


## calculating how many unqiue visual designs participants interacted with

# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'num_interacted_visual_design'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p3_logs.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p4_logs.json')]

# calculate mean and deviation
# res_lst = []

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         logs = json.load(json_file)

#         split_filename = js.split('_')
#         participant_id = split_filename[0].replace('partcipant','')
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]

#         interacted_visual_design = []

#         if_mouseover = False
#         prev_time = 0

#         for log in logs:
            
#             if log["Interaction"] == "main chart changed because of clicking a field" or log["Interaction"] == "specified chart" or log["Interaction"] == "added chart to bookmark":
#                 if "Value" in log:
#                     interacted_visual_design.append(log["Value"])
#                 continue

#             if log["Interaction"].startswith("mouseover"):
#                 prev_time = log["Time"]
#                 if_mouseover = True
#                 continue
            
#             if if_mouseover and log["Interaction"].startswith("mouseout"):
#                 time_period = (log["Time"] - prev_time) / 1000
#                 if time_period > 0.5 and "Value" in log:
#                     interacted_visual_design.append(log["Value"])
#                 if_mouseover = False
#                 continue
        
#         num_interacted_visual_design = len(set(interacted_visual_design))
#         # calculate mean and deviation
# #         res_lst.append(num_interacted_visual_design * 1.67)

# # print (sum(res_lst) / len(res_lst), statistics.pstdev(res_lst))
        
#         row = [participant_id, dataset, oracle, search, task, num_interacted_visual_design]
#         jsons_data.loc[index] = row

# jsons_data.to_csv('num_of_interacted_visual_design_split.csv', index=False)


## interactions that change exposure
## main chart changed because of clicking a field
## clicked load more button (doesnt have value, need to know what is the current main view)
# specified chart

## calculating how many unqiue varibale sets were exposed to participants
# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'num_exposed_variable_set'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p3_logs.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p4_logs.json')]

# # calculate mean and deviation
# # res_lst = []

# ## fields
# movies_fields = ['Title', 'US_Gross', 'Worldwide_Gross', 'US_DVD_Sales', 'Production_Budget', 'Release_Date', 'MPAA_Rating', 'Running_Time_min', 'Distributor', 'Source', 'Major_Genre', 'Creative_Type', 'Director', 'Rotten_Tomatoes_Rating', 'IMDB_Rating', 'IMDB_Votes']

# bs_fields = ['Airport_Name', 'Aircraft_Make_Model', 'Effect_Amount_of_damage', 'Flight_Date', 'Aircraft_Airline_Operator', 'Origin_State', 'When_Phase_of_flight', 'Wildlife_Size', 'Wildlife_Species', 'When_Time_of_day', 'Cost_Other', 'Cost_Repair', 'Cost_Total', 'Speed_IAS_in_knots']

# ## movies
# ## dziban
# read_movies_diban_flds_to_vglstr = open('../../web/static/data/movies/dziban_fields_to_vglstr.json', 'r')
# movies_dziban_flds_to_vglstr = json.load(read_movies_diban_flds_to_vglstr)

# read_movies_dziban_bfs_results = open('../../web/static/data/movies/dziban_bfs_results.json', 'r')
# movies_dziban_bfs_results = json.load(read_movies_dziban_bfs_results)

# read_movies_dziban_dfs_results = open('../../web/static/data/movies/dziban_dfs_results.json', 'r')
# movies_dziban_dfs_results = json.load(read_movies_dziban_dfs_results)

# ## cql
# read_movies_cql_flds_to_vglstr = open('../../web/static/data/movies/cql_fields_to_vglstr.json', 'r')
# movies_cql_flds_to_vglstr = json.load(read_movies_cql_flds_to_vglstr)

# read_movies_cql_bfs_results = open('../../web/static/data/movies/cql_bfs_results.json', 'r')
# movies_cql_bfs_results = json.load(read_movies_cql_bfs_results)

# read_movies_cql_dfs_results = open('../../web/static/data/movies/cql_dfs_results.json', 'r')
# movies_cql_dfs_results = json.load(read_movies_cql_dfs_results)

# ## birdstrikes
# ## dziban
# read_bs_dizban_flds_to_vglstr = open('../../web/static/data/birdstrikes/dziban_fields_to_vglstr.json', 'r')
# bs_dziban_flds_to_vglstr = json.load(read_bs_dizban_flds_to_vglstr)

# read_bs_dziban_bfs_results = open('../../web/static/data/birdstrikes/dziban_bfs_results.json', 'r')
# bs_dziban_bfs_results = json.load(read_bs_dziban_bfs_results)

# read_bs_dziban_dfs_results = open('../../web/static/data/birdstrikes/dziban_dfs_results.json', 'r')
# bs_dziban_dfs_results = json.load(read_bs_dziban_dfs_results)

# ## cql
# read_bs_cql_flds_to_vglstr = open('../../web/static/data/birdstrikes/cql_fields_to_vglstr.json', 'r')
# bs_cql_flds_to_vglstr = json.load(read_bs_cql_flds_to_vglstr)

# read_bs_cql_bfs_results = open('../../web/static/data/birdstrikes/cql_bfs_results.json', 'r')
# bs_cql_bfs_results = json.load(read_bs_cql_bfs_results)

# read_bs_cql_dfs_results = open('../../web/static/data/birdstrikes/cql_dfs_results.json', 'r')
# bs_cql_dfs_results = json.load(read_bs_cql_dfs_results)

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         logs = json.load(json_file)

#         split_filename = js.split('_')
#         participant_id = split_filename[0].replace('partcipant','')
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]

#         exposed_variable_set = []

#         cur_results = {}
#         cur_flds_to_vglstr = {}

#         if dataset == "movies":
#             for elem in movies_fields:
#                 exposed_variable_set.append(elem)
#             if oracle == "compassql":
#                 cur_flds_to_vglstr = movies_cql_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = movies_cql_bfs_results
#                 else:
#                     cur_results = movies_cql_dfs_results
#             else:
#                 cur_flds_to_vglstr = movies_dziban_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = movies_dziban_bfs_results
#                 else:
#                     cur_results = movies_dziban_dfs_results
#         else:
#             for elem in bs_fields:
#                 exposed_variable_set.append(elem)
#             if oracle == "compassql":
#                 cur_flds_to_vglstr = bs_cql_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = bs_cql_bfs_results
#                 else:
#                     cur_results = bs_cql_dfs_results
#             else:
#                 cur_flds_to_vglstr = bs_dziban_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = bs_dziban_bfs_results
#                 else:
#                     cur_results = bs_dziban_dfs_results
        
#         cur_vlg = ""
#         cur_flds = ""
#         cur_ranked_lst = []
#         cur_pos = 0
#         for log in logs:
#             if log["Interaction"] == "main chart changed because of clicking a field" or log["Interaction"] == "specified chart":
#                 cur_vlg = log["Value"]
#                 exposed_variable_set.append(get_fields_from_vglstr(cur_vlg))
#                 cur_pos = 5
#                 if oracle == "compassql":
#                     cur_flds = get_fields_from_vglstr(cur_vlg)
#                     cur_ranked_lst = sorted(cur_results[cur_flds], key=cur_results[cur_flds].get)
#                 else:
#                     if cur_vlg in cur_results:
#                         cur_ranked_lst = sorted(cur_results[cur_vlg], key=cur_results[cur_vlg].get)
#                     else:
#                         cur_flds = get_fields_from_vglstr(cur_vlg)
#                         new_vlg = cur_flds_to_vglstr[cur_flds]
#                         cur_ranked_list = sorted(cur_results[new_vlg], key=cur_results[new_vlg].get)
                    
#                 if len(cur_ranked_lst) < cur_pos:
#                     for vlg in cur_ranked_lst[0:]:
#                         exposed_variable_set.append(get_fields_from_vglstr(vlg))
#                 else:
#                     for vlg in cur_ranked_lst[0:cur_pos]:
#                         exposed_variable_set.append(get_fields_from_vglstr(vlg))
#                 continue
            
#             if log["Interaction"] == "clicked load more button":
#                 if len(cur_ranked_lst) <= cur_pos:
#                     continue
#                 if len(cur_ranked_lst) < cur_pos + 5:
#                     for vlg in cur_ranked_lst[cur_pos:]:
#                         exposed_variable_set.append(get_fields_from_vglstr(vlg))
#                     cur_pos = len(cur_ranked_lst)
#                 else:
#                     for vlg in cur_ranked_lst[cur_pos: cur_pos + 5]:
#                         exposed_variable_set.append(get_fields_from_vglstr(vlg))
#                     cur_pos += 5
#                 continue
        
#         num_exposed_variable_set = len(set(exposed_variable_set))
#         res_lst.append(num_exposed_variable_set * 1.67)

# print (sum(res_lst) / len(res_lst), statistics.pstdev(res_lst))
#         row = [participant_id, dataset, oracle, search, task, num_exposed_variable_set]
#         jsons_data.loc[index] = row

# jsons_data.to_csv('num_of_exposed_variable_set_split.csv', index=False)

## calculating how many unqiue varibale sets were exposed to participants
# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'num_exposed_visual_design'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p3_logs.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p4_logs.json')]

# # calculate mean and deviation
# # res_lst = []

# ## fields
# movies_fields = ['Title', 'US_Gross', 'Worldwide_Gross', 'US_DVD_Sales', 'Production_Budget', 'Release_Date', 'MPAA_Rating', 'Running_Time_min', 'Distributor', 'Source', 'Major_Genre', 'Creative_Type', 'Director', 'Rotten_Tomatoes_Rating', 'IMDB_Rating', 'IMDB_Votes']

# bs_fields = ['Airport_Name', 'Aircraft_Make_Model', 'Effect_Amount_of_damage', 'Flight_Date', 'Aircraft_Airline_Operator', 'Origin_State', 'When_Phase_of_flight', 'Wildlife_Size', 'Wildlife_Species', 'When_Time_of_day', 'Cost_Other', 'Cost_Repair', 'Cost_Total', 'Speed_IAS_in_knots']

# ## movies
# ## dziban
# read_movies_diban_flds_to_vglstr = open('../../web/static/data/movies/dziban_fields_to_vglstr.json', 'r')
# movies_dziban_flds_to_vglstr = json.load(read_movies_diban_flds_to_vglstr)

# read_movies_dziban_bfs_results = open('../../web/static/data/movies/dziban_bfs_results.json', 'r')
# movies_dziban_bfs_results = json.load(read_movies_dziban_bfs_results)

# read_movies_dziban_dfs_results = open('../../web/static/data/movies/dziban_dfs_results.json', 'r')
# movies_dziban_dfs_results = json.load(read_movies_dziban_dfs_results)

# ## cql
# read_movies_cql_flds_to_vglstr = open('../../web/static/data/movies/cql_fields_to_vglstr.json', 'r')
# movies_cql_flds_to_vglstr = json.load(read_movies_cql_flds_to_vglstr)

# read_movies_cql_bfs_results = open('../../web/static/data/movies/cql_bfs_results.json', 'r')
# movies_cql_bfs_results = json.load(read_movies_cql_bfs_results)

# read_movies_cql_dfs_results = open('../../web/static/data/movies/cql_dfs_results.json', 'r')
# movies_cql_dfs_results = json.load(read_movies_cql_dfs_results)

# ## birdstrikes
# ## dziban
# read_bs_dizban_flds_to_vglstr = open('../../web/static/data/birdstrikes/dziban_fields_to_vglstr.json', 'r')
# bs_dziban_flds_to_vglstr = json.load(read_bs_dizban_flds_to_vglstr)

# read_bs_dziban_bfs_results = open('../../web/static/data/birdstrikes/dziban_bfs_results.json', 'r')
# bs_dziban_bfs_results = json.load(read_bs_dziban_bfs_results)

# read_bs_dziban_dfs_results = open('../../web/static/data/birdstrikes/dziban_dfs_results.json', 'r')
# bs_dziban_dfs_results = json.load(read_bs_dziban_dfs_results)

# ## cql
# read_bs_cql_flds_to_vglstr = open('../../web/static/data/birdstrikes/cql_fields_to_vglstr.json', 'r')
# bs_cql_flds_to_vglstr = json.load(read_bs_cql_flds_to_vglstr)

# read_bs_cql_bfs_results = open('../../web/static/data/birdstrikes/cql_bfs_results.json', 'r')
# bs_cql_bfs_results = json.load(read_bs_cql_bfs_results)

# read_bs_cql_dfs_results = open('../../web/static/data/birdstrikes/cql_dfs_results.json', 'r')
# bs_cql_dfs_results = json.load(read_bs_cql_dfs_results)

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         logs = json.load(json_file)

#         split_filename = js.split('_')
#         participant_id = split_filename[0].replace('partcipant','')
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]

#         exposed_visual_design = []

#         cur_results = {}
#         cur_flds_to_vglstr = {}

#         if dataset == "movies":
#             if oracle == "compassql":
#                 cur_flds_to_vglstr = movies_cql_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = movies_cql_bfs_results
#                 else:
#                     cur_results = movies_cql_dfs_results
#             else:
#                 cur_flds_to_vglstr = movies_dziban_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = movies_dziban_bfs_results
#                 else:
#                     cur_results = movies_dziban_dfs_results
#             for elem in movies_fields:
#                 exposed_visual_design.append(cur_flds_to_vglstr[elem])
#         else:
#             if oracle == "compassql":
#                 cur_flds_to_vglstr = bs_cql_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = bs_cql_bfs_results
#                 else:
#                     cur_results = bs_cql_dfs_results
#             else:
#                 cur_flds_to_vglstr = bs_dziban_flds_to_vglstr
#                 if search == "bfs":
#                     cur_results = bs_dziban_bfs_results
#                 else:
#                     cur_results = bs_dziban_dfs_results
#             for elem in bs_fields:
#                 exposed_visual_design.append(cur_flds_to_vglstr[elem])
        
#         cur_vlg = ""
#         cur_flds = ""
#         cur_ranked_lst = []
#         cur_pos = 0
#         for log in logs:
#             if log["Interaction"] == "main chart changed because of clicking a field" or log["Interaction"] == "specified chart":
#                 cur_vlg = log["Value"]
#                 exposed_visual_design.append(cur_vlg)
#                 cur_pos = 5
#                 if oracle == "compassql":
#                     cur_flds = get_fields_from_vglstr(cur_vlg)
#                     cur_ranked_lst = sorted(cur_results[cur_flds], key=cur_results[cur_flds].get)
#                 else:
#                     if cur_vlg in cur_results:
#                         cur_ranked_lst = sorted(cur_results[cur_vlg], key=cur_results[cur_vlg].get)
#                     else:
#                         cur_flds = get_fields_from_vglstr(cur_vlg)
#                         new_vlg = cur_flds_to_vglstr[cur_flds]
#                         cur_ranked_list = sorted(cur_results[new_vlg], key=cur_results[new_vlg].get)
                    
#                 if len(cur_ranked_lst) < cur_pos:
#                     for vlg in cur_ranked_lst[0:]:
#                         exposed_visual_design.append(vlg)
#                 else:
#                     for vlg in cur_ranked_lst[0:cur_pos]:
#                         exposed_visual_design.append(vlg)
#                 continue
            
#             if log["Interaction"] == "clicked load more button":
#                 if len(cur_ranked_lst) <= cur_pos:
#                     continue
#                 if len(cur_ranked_lst) < cur_pos + 5:
#                     for vlg in cur_ranked_lst[cur_pos:]:
#                         exposed_visual_design.append(vlg)
#                     cur_pos = len(cur_ranked_lst)
#                 else:
#                     for vlg in cur_ranked_lst[cur_pos: cur_pos + 5]:
#                         exposed_visual_design.append(vlg)
#                     cur_pos += 5
#                 continue
        
#         # print (set(exposed_visual_design), len(set(exposed_visual_design)))
#         # break
        
#         num_exposed_visual_design = len(set(exposed_visual_design))
# #         res_lst.append(num_exposed_visual_design * 1.67)

# # print (sum(res_lst) / len(res_lst), statistics.pstdev(res_lst))

# #         row = [participant_id, dataset, oracle, search, task, num_exposed_visual_design]
# #         jsons_data.loc[index] = row

# # jsons_data.to_csv('num_of_exposed_visual_design_split.csv', index=False)

### statistical results from pilots (mean pstdev):
## p3 num_of_interacted_variable_set (38.64857142857142 26.621834984823707)
## p4 num_of_interacted_variable_set (27.276666666666667 19.869179371299886)

## p3 num_of_interacted_visual_design (39.36428571428571 26.58332391188283)
## p4 num_of_interacted_visual_design (27.833333333333332 19.586441455478553)

## p3 num_of_exposed_variable_set (125.72714285714285 92.55956533332402)
## p4 num_of_exposed_variable_set (111.89 82.11918289900356)

## p3 num_of_exposed_visual_design (140.28 124.11080982044115)
## p4 num_of_exposed_visual_design (135.82666666666668 111.36394579136564)