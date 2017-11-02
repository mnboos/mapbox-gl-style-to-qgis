import os
import uuid
import ast


def create_style_file(output_directory, layer_style):
    with open(os.path.join(__file__, "../templates/polygon_template.xml"), 'r') as f:
        template = f.read()

    rules = []
    symbols = []

    for index, s in enumerate(layer_style["styles"]):
        rules.append(_get_rule(index, s))
        symbols.append(_get_fill_symbol(index, s))

    rule_string = """<rules key="{key}">
    {rules}
    </rules>""".format(key=str(uuid.uuid4()), rules="\n".join(rules))

    symbol_string = """<symbols>
    {symbols}
    </symbols>""".format(symbols="\n".join(symbols))

    template = template.format(rules=rule_string, symbols=symbol_string)
    file_path = os.path.join(output_directory, layer_style["file_name"])
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    with open(file_path, 'w') as f:
        f.write(template)


def _get_fill_symbol(index, style):
    opacity = _get_value_safe(style, "fill-opacity", 1)
    offset = map(lambda o: str(o), _get_value_safe(style, "fill-translate", default=[0, 0]))
    offset = ",".join(offset)
    fill_color_rgba = _get_value_safe(style, "fill-color", "")

    symbol = """<symbol alpha="{opacity}" clip_to_extent="1" type="fill" name="{index}">
            <layer pass="0" class="SimpleFill" locked="0">
                <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
                <prop k="color" v="{fill_color}"/>
                <prop k="joinstyle" v="bevel"/>
                <prop k="offset" v="{offset}"/>
                <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
                <prop k="offset_unit" v="MapUnit"/>
                <prop k="outline_color" v="195,181,170,255"/>
                <prop k="outline_style" v="solid"/>
                <prop k="outline_width" v="0.1"/>
                <prop k="outline_width_unit" v="MapUnit"/>
                <prop k="style" v="solid"/>
            </layer>
        </symbol>
        """.format(opacity=opacity,
                   index=index,
                   fill_color=fill_color_rgba,
                   offset=offset)
    return symbol


def _get_rule(index, style):
    rule_key = str(uuid.uuid4())
    max_denom = ""
    min_denom = ""
    label = style["name"]
    if style["zoom_level"]:
        label = "{}-zoom-{}".format(label, style["zoom_level"])

    max_denom_value = _get_value_safe(style, "max_scale_denom")
    min_denom_value = _get_value_safe(style, "min_scale_denom")

    if style["zoom_level"]:
        if not max_denom_value:
            raise RuntimeError("max denom missing: {}".format(style))
        assert max_denom_value
        assert min_denom_value

    if max_denom_value:
        max_denom = ' scalemaxdenom="{}"'.format(max_denom_value)
    if min_denom_value:
        min_denom = ' scalemindenom="{}"'.format(min_denom_value)

    rule = """<rule key="{rule_key}" symbol="{symbol}"{max_denom}{min_denom} label="{label}"/>""".format(
        max_denom=max_denom,
        min_denom=min_denom,
        rule_key=rule_key,
        symbol=index,
        label=label)
    return rule


def _get_value_safe(obj, key, default=None):
    result = default
    if key in obj:
        result = obj[key]
    return result
