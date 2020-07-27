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

# render index at route /
@app.route('/')
@app.route('/proc/')
@app.route('/proc/<pid>')
def index(pid = None):
    return render_template("index.html", pid=pid)

@app.route('/demo')
def demo():
    return render_template("demo.html")

@app.route('/<version>/<interface>')
def study(version, interface):
    if interface.startswith("t"):
        return render_template("task.html", version = version, interface = interface)
    elif interface.startswith("p"):
        return render_template("perform.html", version = version, interface = interface)


## reading files
# movies = pd.read_json('./web/static/data/movies/movies.json')
# movies_base = Chart(movies)
# movies_fields = movies_base.get_fields()

# birdstrikes = pd.read_json('./web/static/data/birdstrikes/birdstrikes.json')
# birdstrikes_base = Chart(birdstrikes)
# birdstrikes_fields = birdstrikes_base.get_fields()

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
    vgl["data"] = {"url": "data/" + dataset + ".json"}
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