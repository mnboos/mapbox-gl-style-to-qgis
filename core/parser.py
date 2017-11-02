import os
import json
import sys
import traceback
from xml.sax.saxutils import escape
from helper import get_qgis_rule, get_styles
from xml_helper import create_style_file


def generate_qgis_styles(mapbox_gl_style_path, output_directory):
    if not os.path.isfile(mapbox_gl_style_path):
        raise RuntimeError("File does not exist: {}".format(mapbox_gl_style_path))
    with open(mapbox_gl_style_path, 'r') as f:
        js = json.load(f)

    all_layers = set()
    for l in js["layers"]:
        if "source-layer" in l:
            all_layers.add(l["source-layer"])

    styles_by_target_layer = {}
    for l in js["layers"]:
        if "source-layer" in l and l["type"] == "fill":
            name = l["source-layer"]
            if name not in styles_by_target_layer:
                styles_by_target_layer[name] = {
                    "file_name": "{}.polygon.qml".format(l["source-layer"]),
                    "styles": []
                }
            qgis_styles = get_styles(l["paint"], l["id"])
            # target_file_name =
            # print("Create polygon style: {}".format(target_file_name))
            filter_expr = None
            if "filter" in l:
                filter_expr = get_qgis_rule(l["filter"])
                if filter_expr:
                    filter_expr = escape(filter_expr, entities={'"': "&quot;"})
                    # print("'{}'  ==>  '{}'".format(l["filter"], filter_expr))
            for s in qgis_styles:
                s["rule"] = filter_expr

            styles_by_target_layer[name]["styles"].extend(qgis_styles)
    # print styles_by_target_layer
    for layer_name in styles_by_target_layer:
        style = styles_by_target_layer[layer_name]
        create_style_file(output_directory=output_directory, layer_style=style)
