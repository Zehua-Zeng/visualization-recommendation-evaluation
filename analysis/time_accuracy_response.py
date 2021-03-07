import os, json
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

response_to_score_dict = {
    'sdisagree': -2,
    'disagree': -1,
    'neutral': 0,
    'agree': 1,
    'sagree': 2
}

path_to_json = '../../logs/'

## completion time
# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'participant_group',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'completion_time'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_logs.json')]

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         json_text = json.load(json_file)

#         split_filename = js.split('_')

#         participant_id = split_filename[0]
#         participant_group = ''
#         if participant_id.startswith('pro'):
#             participant_group = 'professional'
#         elif participant_id.startswith('stu'):
#             participant_group = 'student'
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]

#         completion_time = (json_text[-1]["Time"] - json_text[0]["Time"]) / 1000

#         row = [participant_id, participant_group, dataset, oracle, search, task, completion_time]
#         jsons_data.loc[index] = row
    
# jsons_data.to_csv('completion_time.csv', index=False)


## accuracy
jsons_data = pd.DataFrame(columns=['participant_id',
                                   'participant_group',
                                   'dataset',
                                   'oracle',
                                   'search',
                                   'task',
                                   'accuracy'])

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p1_answer.json')] + [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_p2_answer.json')]

for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)

        split_filename = js.split('_')

        participant_id = split_filename[0]
        participant_group = ''
        if participant_id.startswith('pro'):
            participant_group = 'professional'
        elif participant_id.startswith('stu'):
            participant_group = 'student'
        experimental_setup = split_filename[1]
        dataset = dataset_dict[experimental_setup[0]]
        oracle = oracle_dict[experimental_setup[1]]
        search = search_algorithm_dict[experimental_setup[2]]
        task = task_dict[split_filename[2]]

        accuracy = -1

        if experimental_setup[0] == "a" and split_filename[2] == "p1":
            if json_text["answer"] == "contemporary_fiction":
                accuracy = 1
            else:
                accuracy = 0
        
        if experimental_setup[0] == "a" and split_filename[2] == "p2":
            if json_text["answer"] == "151":
                accuracy = 1
            else:
                accuracy = 0
        
        if experimental_setup[0] == "b" and split_filename[2] == "p1":
            if json_text["answer"] == "approach":
                accuracy = 1
            else:
                accuracy = 0
        
        if experimental_setup[0] == "b" and split_filename[2] == "p2":
            if json_text["answer"] == "235":
                accuracy = 1
            else:
                accuracy = 0

        row = [participant_id, participant_group, dataset, oracle, search, task, accuracy]
        jsons_data.loc[index] = row
    
jsons_data.to_csv('accuracy.csv', index=False)

## user response
# jsons_data = pd.DataFrame(columns=['participant_id',
#                                    'participant_group',
#                                    'dataset',
#                                    'oracle',
#                                    'search',
#                                    'task',
#                                    'confidence-udata', 
#                                    'confidence-ans', 
#                                    'efficiency',
#                                    'ease-of-use', 
#                                    'utility', 
#                                    'overall'])

# json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('_ptask.json')]

# for index, js in enumerate(json_files):
#     with open(os.path.join(path_to_json, js)) as json_file:
#         json_text = json.load(json_file)
        
#         split_filename = js.split('_')
        
#         participant_id = split_filename[0]
#         participant_group = ''
#         if participant_id.startswith('pro'):
#             participant_group = 'professional'
#         elif participant_id.startswith('stu'):
#             participant_group = 'student'
        
#         experimental_setup = split_filename[1]
#         dataset = dataset_dict[experimental_setup[0]]
#         oracle = oracle_dict[experimental_setup[1]]
#         search = search_algorithm_dict[experimental_setup[2]]
#         task = task_dict[split_filename[2]]
            
#         confidence_udata = response_to_score_dict[json_text['confidence-udata']]
#         confidence_ans = response_to_score_dict[json_text['confidence-ans']]
#         efficiency = response_to_score_dict[json_text['efficiency']]
#         ease_of_use = response_to_score_dict[json_text['ease-of-use']]
#         utility = response_to_score_dict[json_text['utility']]
#         overall = response_to_score_dict[json_text['overall']]
        
#         row = [participant_id, participant_group, dataset, oracle, search, task, confidence_udata, confidence_ans, efficiency, ease_of_use, utility, overall]
#         jsons_data.loc[index] = row

# jsons_data.to_csv('ptask_responses.csv', index=False)