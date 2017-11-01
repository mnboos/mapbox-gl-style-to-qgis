import os
import json
import sys
import traceback
from xml.sax.saxutils import escape

_comparision_operators = {
    "==": "=",
    "<=": "<=",
    ">=": ">=",
    "<": "<",
    ">": ">",
    "!=": "!="
}

_combining_operators = {
    "all": "and",
    "any": "or",
    "none": "and not"
}

_membership_operators = {
    "in": "in",
    "!in": "not in"
}

_existential_operators = {
    "has": "is not null",
    "!has": "is null"
}


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
                    filter_expr = _get_rule(l["filter"])
                    if filter_expr:
                        filter_expr = escape(filter_expr, entities={'"': "&quot;"})
                        print("'{}'  ==>  '{}'".format(l["filter"], filter_expr))
    except RuntimeError:
        print(sys.exc_info()[1])
    except:
        print("Error: {}, {}", sys.exc_info()[1], traceback.format_exc())
        return None


def _get_rule(mb_filter):
    op = mb_filter[0]
    if op in _comparision_operators:
        result = _get_comparision_expr(mb_filter)
    elif op in _combining_operators:
        is_none = op == "none"
        all_exprs = map(lambda f: _get_rule(f), mb_filter[1:])
        all_exprs = filter(lambda e: e is not None, all_exprs)
        if is_none:
            "not {}".format(all_exprs)
        full_expr = " {} ".format(_combining_operators[op]).join(all_exprs)
        result = full_expr
    elif op in _membership_operators:
        result = _get_membership_expr(mb_filter)
    elif op in _existential_operators:
        result = _get_existential_expr(mb_filter)
    else:
        raise NotImplementedError("Not Implemented Operator: '{}', Filter: {}".format(op, mb_filter))

    if result:
        result = "({})".format(result)
    return result


def _get_qml_rules(filter_expr):
    pass


def _get_comparision_expr(mb_filter):
    assert mb_filter[0] in _comparision_operators
    assert len(mb_filter) == 3
    op = _comparision_operators[mb_filter[0]]
    attr = mb_filter[1]
    value = mb_filter[2]
    if attr == '$type':
        return None
    return "\"{attr}\" {op} '{value}'".format(attr=attr, op=op, value=value)


def _get_membership_expr(mb_filter):
    assert mb_filter[0] in _membership_operators
    assert len(mb_filter) >= 3
    what = "\"{}\"".format(mb_filter[1])
    op = _membership_operators[mb_filter[0]]
    collection = "({})".format(", ".join(map(lambda e: "'{}'".format(e), mb_filter[2:])))
    return "{what} {op} {coll}".format(what=what, op=op, coll=collection)


def _get_existential_expr(mb_filter):
    assert mb_filter[0] in _existential_operators
    assert len(mb_filter) == 2
    op = _existential_operators[mb_filter[0]]
    key = mb_filter[1]
    return "attribute($currentfeature, '{key}') {op}".format(key=key, op=op)
