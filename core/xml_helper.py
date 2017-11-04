import os
import uuid

_join_styles = {
    None: "round",
    "bevel": "bevel",
    "round": "round",
    "miter": "miter"
}

_cap_styles = {
    None: "round",
    "butt": "flat",
    "square": "square",
    "round": "round"
}


def create_style_file(output_directory, layer_style):
    with open(os.path.join(os.path.dirname(__file__), "templates/qml_template.xml"), 'r') as f:
        template = f.read()

    geo_type = layer_style["geo_type"]
    rules = []
    symbols = []

    for index, s in enumerate(layer_style["styles"]):
        rules.append(_get_rule(index, s))
        if geo_type == 1:
            symbols.append(_get_line_symbol(index, s))
        elif geo_type == 2:
            symbols.append(_get_fill_symbol(index, s))

    rule_string = """<rules key="{key}">
    {rules}
    </rules>""".format(key=str(uuid.uuid4()), rules="\n".join(rules))

    symbol_string = """<symbols>
    {symbols}
    </symbols>""".format(symbols="\n".join(symbols))

    template = template.format(rules=rule_string,
                               symbols=symbol_string,
                               geo_type=geo_type)
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
    fill_outline_color_rgba = _get_value_safe(style, "fill-outline-color", fill_color_rgba)
    label = style["name"]
    if style["zoom_level"]:
        label = "{}-zoom-{}".format(label, style["zoom_level"])

    symbol = """<!-- {label} -->
    <symbol alpha="{opacity}" clip_to_extent="1" type="fill" name="{index}">
            <layer pass="{rendering_pass}" class="SimpleFill" locked="0">
                <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
                <prop k="color" v="{fill_color}"/>
                <prop k="joinstyle" v="bevel"/>
                <prop k="offset" v="{offset}"/>
                <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
                <prop k="offset_unit" v="Pixel"/>
                <prop k="outline_color" v="{fill_outline_color}"/>
                <prop k="outline_style" v="solid"/>
                <prop k="outline_width" v="0.7"/>
                <prop k="outline_width_unit" v="Pixel"/>
                <prop k="style" v="solid"/>
            </layer>
        </symbol>
        """.format(opacity=opacity,
                   index=index,
                   fill_color=fill_color_rgba,
                   fill_outline_color=fill_outline_color_rgba,
                   offset=offset,
                   label=label,
                   rendering_pass=style["rendering_pass"])
    return symbol


def _get_line_symbol(index, style):
    color = _get_value_safe(style, "line-color")
    width = _get_value_safe(style, "line-width", 1)
    capstyle = _cap_styles[_get_value_safe(style, "line-cap")]
    joinstyle = _join_styles[_get_value_safe(style, "line-join")]
    opacity = _get_value_safe(style, "line-opacity", 1)
    dashes = _get_value_safe(style, "line-dasharray", None)
    dash_string = "0;0"
    use_custom_dash = 0
    if dashes:
        use_custom_dash = 1
        dash = dashes[0] * width
        space = dashes[1] * width
        if space <= width:
            space += width
        dash_string = "{};{}".format(dash, space)

    label = style["name"]
    if style["zoom_level"]:
        label = "{}-zoom-{}".format(label, style["zoom_level"])
    symbol = """<!-- {label} -->
    <symbol alpha="{opacity}" clip_to_extent="1" type="line" name="{index}">
        <layer pass="{rendering_pass}" class="SimpleLine" locked="0">
          <prop k="capstyle" v="{capstyle}"/>
          <prop k="customdash" v="{custom_dash}"/>
          <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="{joinstyle}"/>
          <prop k="line_color" v="{line_color}"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="{line_width}"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="use_custom_dash" v="{use_custom_dash}"/>
          <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
        </layer>
      </symbol>
      """.format(index=index,
                 opacity=opacity,
                 line_color=color,
                 line_width=width,
                 capstyle=capstyle,
                 joinstyle=joinstyle,
                 use_custom_dash=use_custom_dash,
                 custom_dash=dash_string,
                 label=label,
                 rendering_pass=style["rendering_pass"])
    return symbol


def _get_rule(index, style):
    rule_key = str(uuid.uuid4())
    max_denom = ""
    min_denom = ""
    rule_filter = ""
    label = style["name"]
    if style["zoom_level"]:
        label = "{}-zoom-{}".format(label, style["zoom_level"])
    if style["rule"]:
        rule_filter = 'filter="{}"'.format(style["rule"])

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

    rule = """<rule key="{rule_key}" {filter} symbol="{symbol}"{max_denom}{min_denom} label="{label}"/>""".format(
        max_denom=max_denom,
        min_denom=min_denom,
        rule_key=rule_key,
        symbol=index,
        label=label,
        filter=rule_filter)
    return rule


def _get_value_safe(obj, key, default=None):
    result = default
    if key in obj:
        result = obj[key]
    return result
