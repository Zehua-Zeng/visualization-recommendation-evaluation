import os
import json
import pandas as pd

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

path_to_json = '../logs/'

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
        
#         row = [participant_id, dataset, oracle, search, task, num_interacted_variable_set]
#         jsons_data.loc[index] = row

# jsons_data.to_csv('num_of_interacted_variable_set_split.csv', index=False)


## calculating how many unqiue visual designs participants interacted with

jsons_data = pd.DataFrame(columns=['participant_id',
                                   'dataset',
                                   'oracle',
                                   'search',
                                   'task',
                                   'num_interacted_visual_design'])

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p3_logs.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p4_logs.json')]

for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        logs = json.load(json_file)

        split_filename = js.split('_')
        participant_id = split_filename[0].replace('partcipant','')
        experimental_setup = split_filename[1]
        dataset = dataset_dict[experimental_setup[0]]
        oracle = oracle_dict[experimental_setup[1]]
        search = search_algorithm_dict[experimental_setup[2]]
        task = task_dict[split_filename[2]]

        interacted_visual_design = []

        if_mouseover = False
        prev_time = 0

        for log in logs:
            
            if log["Interaction"] == "main chart changed because of clicking a field" or log["Interaction"] == "specified chart" or log["Interaction"] == "added chart to bookmark":
                if "Value" in log:
                    interacted_visual_design.append(log["Value"])
                continue

            if log["Interaction"].startswith("mouseover"):
                prev_time = log["Time"]
                if_mouseover = True
                continue
            
            if if_mouseover and log["Interaction"].startswith("mouseout"):
                time_period = (log["Time"] - prev_time) / 1000
                if time_period > 0.5 and "Value" in log:
                    interacted_visual_design.append(log["Value"])
                if_mouseover = False
                continue
        
        num_interacted_visual_design = len(set(interacted_visual_design))
        
        row = [participant_id, dataset, oracle, search, task, num_interacted_visual_design]
        jsons_data.loc[index] = row

jsons_data.to_csv('num_of_interacted_visual_design_split.csv', index=False)