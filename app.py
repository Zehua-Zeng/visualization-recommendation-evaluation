from flask import Flask, render_template, request, jsonify, send_from_directory, current_app
import os
import json

## dziban
# from dziban.mkiv import Chart
# from vega_datasets import data
# from vega import VegaLite
# import pandas as pd

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


## dziban:
# movies = pd.read_json('./web/static/data/movies/movies.json')
# movies_base = Chart(movies)
# movies_fields = movies_base.get_fields()

# birdstrikes = pd.read_json('./web/static/data/birdstrikes/birdstrikes.json')
# birdstrikes_base = Chart(birdstrikes)
# birdstrikes_fields = birdstrikes_base.get_fields()

# cars = pd.read_json('./web/static/data/cars/cars.json')
# cars_base = Chart(cars)
# cars_fields = cars_base.get_fields()

# temp:
cars_fields = ["Cylinders", "Name", "Origin", "Year", "Acceleration", "Displacement", "Horsepower", "Miles_per_Gallon", "Weight_in_lbs"]

## read dataset:
read_cars_flds_to_vglstr = open('./web/static/data/cars/fields_to_vglstr.json', 'r')
cars_flds_to_vglstr = json.load(read_cars_flds_to_vglstr)

read_cars_results = open('./web/static/data/cars/results.json', 'r')
cars_results = json.load(read_cars_results)


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
    actual_vgl = {}
    if cars_flds_to_vglstr[fields_str] == "":
        return jsonify(status="empty")
    
    # if not empty chart:
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

## communicate with main

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