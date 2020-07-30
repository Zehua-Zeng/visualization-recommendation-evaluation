from flask import Flask, render_template, request, jsonify, send_from_directory, current_app
import os
import json

## flask
app = Flask(__name__, static_folder='web/static',
            template_folder='web/templates')

# send static files from directory (data)
@app.route('/data/<path:filename>')
def send_data(filename):
    return send_from_directory('web/static/data', filename)

@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('web/static/css', filename)

@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('web/static/js', filename)

# online consent form at / or /proc/online-consent-form
# pre-study survey at /proc/pre-study-survey
# tutorial at /proc/tutorial
# demo at /proc/demo
@app.route('/')
@app.route('/proc/')
@app.route('/proc/<pid>')
def index(pid = None):
    if pid == "demo":
        return render_template("demo.html")
    return render_template("index.html", pid=pid)

@app.route('/<username>/<version>/<interface>')
def study(username, version, interface):
    if interface.startswith("t"):
        return render_template("task.html", username = username, version = version, interface = interface)
    elif interface.startswith("p"):
        return render_template("perform.html", username = username, version = version, interface = interface)
    elif interface.startswith("q"):
        return render_template("post-task-quest.html", username = username, version = version, interface = interface)
    elif interface.startswith("intv"):
        return render_template("post-study-intv.html", username = username, version = version, interface = interface)

@app.route('/test')
def test():
    return render_template("test.html")


## fields
movies_fields = ['Title', 'US_Gross', 'Worldwide_Gross', 'US_DVD_Sales', 'Production_Budget', 'Release_Date', 'MPAA_Rating', 'Running_Time_min', 'Distributor', 'Source', 'Major_Genre', 'Creative_Type', 'Director', 'Rotten_Tomatoes_Rating', 'IMDB_Rating', 'IMDB_Votes']

bs_fields = ['Airport_Name', 'Aircraft_Make_Model', 'Effect_Amount_of_damage', 'Flight_Date', 'Aircraft_Airline_Operator', 'Origin_State', 'When_Phase_of_flight', 'Wildlife_Size', 'Wildlife_Species', 'When_Time_of_day', 'Cost_Other', 'Cost_Repair', 'Cost_Total', 'Speed_IAS_in_knots']

cars_fields = ["Cylinders", "Name", "Origin", "Year", "Acceleration", "Displacement", "Horsepower", "Miles_per_Gallon", "Weight_in_lbs"]

## read dataset:
## demo - car
read_cars_flds_to_vglstr = open('./web/static/data/cars/fields_to_vglstr.json', 'r')
cars_flds_to_vglstr = json.load(read_cars_flds_to_vglstr)

read_cars_results = open('./web/static/data/cars/results.json', 'r')
cars_results = json.load(read_cars_results)

## movies
read_movies_flds_to_vglstr = open('./web/static/data/movies/fields_to_vglstr.json', 'r')
movies_flds_to_vglstr = json.load(read_movies_flds_to_vglstr)

read_movies_dziban_bfs_results = open('./web/static/data/movies/dziban_bfs_results.json', 'r')
movies_dziban_bfs_results = json.load(read_movies_dziban_bfs_results)

read_movies_dziban_dfs_results = open('./web/static/data/movies/dziban_dfs_results.json', 'r')
movies_dziban_dfs_results = json.load(read_movies_dziban_dfs_results)

## birdstrikes
read_bs_flds_to_vglstr = open('./web/static/data/birdstrikes/fields_to_vglstr.json', 'r')
bs_flds_to_vglstr = json.load(read_bs_flds_to_vglstr)

read_bs_dziban_bfs_results = open('./web/static/data/birdstrikes/dziban_bfs_results.json', 'r')
bs_dziban_bfs_results = json.load(read_bs_dziban_bfs_results)

read_bs_dziban_dfs_results = open('./web/static/data/birdstrikes/dziban_dfs_results.json', 'r')
bs_dziban_dfs_results = json.load(read_bs_dziban_dfs_results)

## communicate with demo
@app.route('/demo_snd_flds', methods=['POST'])
def demo_snd_flds():
    received_data = json.loads(request.form.get('data'))
    fields = received_data["fields"]

    # init:
    if len(fields) == 0:
        initCharts = []
        for fld in cars_fields:
            temp = {}
            vstr = cars_flds_to_vglstr[fld]
            temp[vstr] = get_vgl_from_vglstr(vstr, "cars")
            initCharts.append(temp)
        return jsonify(status="success", recVegalite=initCharts)
    
    # if empty chart:
    fields.sort()
    fields_str = "+".join(fields)
    if cars_flds_to_vglstr[fields_str] == "":
        return jsonify(status="empty")
    
    # if not empty chart:
    actual_vgl = {}
    vglstr = cars_flds_to_vglstr[fields_str]
    actual_vgl[vglstr] = get_vgl_from_vglstr(vglstr, "cars")
    # get recomendation:
    rec_vgl = cars_results[vglstr]
    # print (bfs_vl)
    rec_ranked = sorted(rec_vgl, key=rec_vgl.get)
    # print (bfsRanked)
    rec_ranked_final = []
    for vstr in rec_ranked:
        temp = {}
        temp[vstr] = get_vgl_from_vglstr(vstr, "cars")
        rec_ranked_final.append(temp)
    return jsonify(status="success", actualVegalite=actual_vgl, recVegalite=rec_ranked_final)


@app.route('/demo_snd_spcs', methods=['POST'])
def demo_snd_spcs():
    received_data = json.loads(request.form.get('data'))
    vgl = received_data["vgl"]
    vglstr = get_vglstr_from_vgl(vgl)

    if vglstr in cars_results:
        print ("bfs vglstr exists.")
        rec_vgl = cars_results[vglstr]
    else:
        print ("bfs vglstr does not exist.")
        fields = get_fields_from_vglstr(vglstr)
        new_vglstr = cars_flds_to_vglstr["+".join(fields)]
        rec_vgl = cars_results[new_vglstr]
    
    rec_ranked = sorted(rec_vgl, key=rec_vgl.get)
    rec_ranked_final = []
    
    for vstr in rec_ranked:
        temp = {}
        temp[vstr] = get_vgl_from_vglstr(vstr, "cars")
        rec_ranked_final.append(temp)
    
    return jsonify(status="success", recVegalite=rec_ranked_final)

## communicate with perform
## a - movies, b - birdstrikes, c - compassql, d - dziban, e - bfs, f - dfs
@app.route('/perform_snd_flds', methods=['POST'])
def perform_snd_flds():
    received_data = json.loads(request.form.get('data'))
    fields = received_data["fields"]
    version = received_data["version"]
    print (version)

    cur_fields = []
    cur_flds_to_vglstr = {}
    cur_results = {}
    cur_dataset = ""

    if version[0] == "a":
        cur_fields = movies_fields
        cur_flds_to_vglstr = movies_flds_to_vglstr
        cur_dataset = "movies"
        if version[1] == "d" and version[2] == "e":
            cur_results = movies_dziban_bfs_results
        elif version[1] == "d" and version[2] == "f":
            cur_results = movies_dziban_dfs_results
    elif version[0] == "b":
        cur_fields = bs_fields
        cur_flds_to_vglstr = bs_flds_to_vglstr
        cur_dataset = "birdstrikes"
        if version[1] == "d" and version[2] == "e":
            cur_results = bs_dziban_bfs_results
        elif version[1] == "d" and version[2] == "f":
            cur_results = bs_dziban_dfs_results

    # init:
    if len(fields) == 0:
        initCharts = []
        for fld in cur_fields:
            temp = {}
            vstr = cur_flds_to_vglstr[fld]
            temp[vstr] = get_vgl_from_vglstr(vstr, cur_dataset)
            initCharts.append(temp)
        return jsonify(status="success", recVegalite=initCharts)
    
    # if empty chart:
    fields.sort()
    fields_str = "+".join(fields)
    if cur_flds_to_vglstr[fields_str] == "":
        return jsonify(status="empty")
    
    # if not empty chart:
    actual_vgl = {}
    vglstr = cur_flds_to_vglstr[fields_str]
    actual_vgl[vglstr] = get_vgl_from_vglstr(vglstr, cur_dataset)
    # get recomendation:
    rec_vgl = cur_results[vglstr]
    # print (bfs_vl)
    rec_ranked = sorted(rec_vgl, key=rec_vgl.get)
    # print (bfsRanked)
    if len(rec_ranked) > 20:
        rec_ranked = rec_ranked[:20]
    rec_ranked_final = []
    for vstr in rec_ranked:
        temp = {}
        temp[vstr] = get_vgl_from_vglstr(vstr, cur_dataset)
        rec_ranked_final.append(temp)
    return jsonify(status="success", actualVegalite=actual_vgl, recVegalite=rec_ranked_final)

@app.route('/perform_snd_spcs', methods=['POST'])
def perform_snd_spcs():
    received_data = json.loads(request.form.get('data'))
    vgl = received_data["vgl"]
    version = received_data["version"]
    vglstr = get_vglstr_from_vgl(vgl)

    cur_fields = []
    cur_flds_to_vglstr = {}
    cur_results = {}
    cur_dataset = ""

    if version[0] == "a":
        cur_fields = movies_fields
        cur_flds_to_vglstr = movies_flds_to_vglstr
        cur_dataset = "movies"
        if version[1] == "d" and version[2] == "e":
            cur_results = movies_dziban_bfs_results
        elif version[1] == "d" and version[2] == "f":
            cur_results = movies_dziban_dfs_results
    elif version[0] == "b":
        cur_fields = bs_fields
        cur_flds_to_vglstr = bs_flds_to_vglstr
        cur_dataset = "birdstrikes"
        if version[1] == "d" and version[2] == "e":
            cur_results = bs_dziban_bfs_results
        elif version[1] == "d" and version[2] == "f":
            cur_results = bs_dziban_dfs_results

    if vglstr in cur_results:
        print ("bfs vglstr exists.")
        rec_vgl = cur_results[vglstr]
    else:
        print ("bfs vglstr does not exist.")
        fields = get_fields_from_vglstr(vglstr)
        new_vglstr = cur_flds_to_vglstr["+".join(fields)]
        rec_vgl = cur_results[new_vglstr]
    
    rec_ranked = sorted(rec_vgl, key=rec_vgl.get)
    if len(rec_ranked) > 20:
        rec_ranked = rec_ranked[:20]
    rec_ranked_final = []
    
    for vstr in rec_ranked:
        temp = {}
        temp[vstr] = get_vgl_from_vglstr(vstr, cur_dataset)
        rec_ranked_final.append(temp)
    
    return jsonify(status="success", recVegalite=rec_ranked_final)

## get username-version:
@app.route('/snd_uname_version', methods=['POST'])
def snd_uname_version():
    received_data = json.loads(request.form.get('data'))
    username = received_data["username"]
    version = received_data["version"]
    uv_file = open("username-version.txt", "a")  # append mode 
    uv_file.write(username + ',' + version + '\n') 
    uv_file.close()
    return jsonify(status="success")

## get study interaction log:
@app.route('/snd_interaction_logs', methods=['POST'])
def snd_interaction_logs():
    received_data = json.loads(request.form.get('data'))
    interaction_logs = received_data["interactionLogs"]
    username = received_data["username"]
    version = received_data["version"]
    interface = received_data["interface"]
    bookmarked = received_data["bookmarked"]

    with open('./logs/' + username + '_' + version + '_' + interface + '.json', 'w') as out:
        json.dump(interaction_logs, out, indent=2)

    with open('./logs/' + username + '_' + version + '_' + interface + '_bookmarked.json', 'w') as out:
        json.dump(bookmarked, out, indent=2)

    if "answer" in received_data:
        answer = received_data["answer"]
        ans_file = open('./logs/' + username + '_' + version + '_' + interface + '_answer.json', "w")
        ans_file.write(answer)
        ans_file.close()

    return jsonify(status="success")


## get post-task quest / post-study interview ans:
@app.route('/post_snd_ans', methods=['POST'])
def ptsk_snd_ans():
    received_data = json.loads(request.form.get('data'))
    questAns = received_data["questAns"]
    username = received_data["username"]
    version = received_data["version"]
    interface = received_data["interface"]

    with open('./logs/' + username + '_' + version + '_' + interface + '.json', 'w') as out:
        json.dump(questAns, out, indent=2)
    return jsonify(status="success")

# helper methods:
def get_vglstr_from_vgl(vgl):
    vglstr = ""
    vglstr += "mark:" + vgl["mark"] + ';'
    encoding_arr = []
    for encoding in vgl["encoding"]:
        if encoding == "undefined":
            continue
        encoding_str = ""
        if "field" in vgl["encoding"][encoding]:
            encoding_str += vgl["encoding"][encoding]["field"] + "-"
        else:
            encoding_str += "-"
        encoding_str += vgl["encoding"][encoding]["type"] + "-"
        encoding_str += encoding
        if "aggregate" in vgl["encoding"][encoding]:
            encoding_str += "<" + "aggregate" + ">" + vgl["encoding"][encoding]["aggregate"]
        if "bin" in vgl["encoding"][encoding]:
            encoding_str += "<" + "bin" + ">"
        
        encoding_arr.append(encoding_str)
    
    encoding_arr.sort()
    vglstr += "encoding:" + ",".join(encoding_arr)

    return vglstr

def get_vgl_from_vglstr(vglstr, dataset):
    vgl = {}
    vgl["$schema"] = "https://vega.github.io/schema/vega-lite/v3.json"
    # vgl["data"] = {"url": "data/movies.json"}
    vgl["data"] = {"url": "/data/" + dataset + "/" + dataset +".json"}
    mark = vglstr.split(';')[0]
    encoding = vglstr.split(';')[1]
    vgl["mark"] = mark.split(':')[1]
    encodings = {}
    fields = []
    encoding = encoding.split(':')[1]
    encoding_arr = encoding.split(',')
    for encode in encoding_arr:
        one_encoding = {}
        if '<' in encode:
            regular = encode.split('<')[0]
            transform = encode.split('<')[1]

            regular_split = regular.split('-')
            if len(regular_split) != 3:
                print ("something wrong with regular string.")
            field = regular_split[0]
            attr_type = regular_split[1]
            encoding_type = regular_split[2]

            one_encoding["type"] = attr_type
            if field != '':
                one_encoding["field"] = field
                fields.append(field)

            transform_split = transform.split('>')
            transform_type = transform_split[0]
            transform_val = transform_split[1]

            if transform_type == "bin":
                one_encoding["bin"] = True
            else:
                one_encoding[transform_type] = transform_val
            
            encodings[encoding_type] = one_encoding

        else:
            encode_split = encode.split('-')
            if len(encode_split) != 3:
                print ("something wrong with encode string.")
            
            field = encode_split[0]
            attr_type = encode_split[1]
            encoding_type = encode_split[2]

            one_encoding["type"] = attr_type
            if field != '':
                one_encoding["field"] = field
                fields.append(field)
            else:
                print ("something wrong:")
                print (vglstr)
            
            ## for bs Flight_Date
            if encode == "Flight_Date-nominal-row":
                if "-x" not in vglstr:
                    encoding_type = "x"
                elif "-y" not in vglstr:
                    encoding_type = "y"
                elif "-color" not in vglstr:
                    encoding_type = "color"
                else:
                    encoding_type = "shape"
                
            if "Flight_Date-nominal" in encode:
                one_encoding["timeUnit"] = "month"
            
            encodings[encoding_type] = one_encoding
    
    vgl["encoding"] = encodings
    return vgl

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
    return fields


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)