import os
import json
import sys
import traceback
from xml.sax.saxutils import escape
from helper import get_qgis_rule

def generate_qgis_styles(mapbox_gl_style_path):
    if not os.path.isfile(mapbox_gl_style_path):
        raise RuntimeError("File does not exist: {}".format(mapbox_gl_style_path))
    with open(mapbox_gl_style_path, 'r') as f:
        js = json.load(f)

    all_layers = set()
    for l in js["layers"]:
        if "source-layer" in l:
            all_layers.add(l["source-layer"])
    all_layers = list(sorted(all_layers))
    print("all layers")
    print("----------------------")
    for l in all_layers:
        print(l)
    print("----------------------")

    try:
        for l in js["layers"]:
            if "source-layer" in l and l["type"] == "fill":
                target_file_name = "{}.polygon.qml".format(l["source-layer"])
                print("Create polygon style: {}".format(target_file_name))
                if "filter" in l:
                    filter_expr = get_qgis_rule(l["filter"])
                    if filter_expr:
                        filter_expr = escape(filter_expr, entities={'"': "&quot;"})
                        print("'{}'  ==>  '{}'".format(l["filter"], filter_expr))
    except RuntimeError:
        print(sys.exc_info()[1])
    except:
        print("Error: {}, {}", sys.exc_info()[1], traceback.format_exc())
        return None


