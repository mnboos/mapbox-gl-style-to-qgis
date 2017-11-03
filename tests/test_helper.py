from core.helper import get_styles, parse_color


def test_parse_rgb():
    rgba = parse_color("rgb(1,2,3)")
    assert rgba == "1,2,3,255"


def test_parse_rgba():
    rgba = parse_color("rgba(1, 2, 3, 0.5)")
    assert rgba == "1,2,3,128"


def test_parse_hsl():
    rgba = parse_color("hsl(28, 76%, 67%)")
    assert rgba == "235,167,107,255"


def test_parse_hsla():
    rgba = parse_color("hsla(28, 76%, 67%, 0.5)")
    assert rgba == "235,167,107,128"


def test_parse_hex_alpha():
    rgba = parse_color("#ffff0c32")
    assert rgba == "255,255,12,50"


def test_parse_hex():
    rgba = parse_color("#ffff0c")
    assert rgba == "#ffff0c"


def test_parse_short_hex():
    rgba = parse_color("#abc")
    assert rgba == "170,187,204"


def test_zoom_level_zero():
    style = _get_style({
        "fill-opacity": {
          "base": 1,
          "stops": [[0, 0.9], [10, 0.3]]
        }
      })
    styles = get_styles(style)
    assert len(styles) == 2
    assert styles[0] == {
        'zoom_level': 0,
        'min_scale_denom': 750000,
        'max_scale_denom': 10000000000L,
        'fill-opacity': 0.9
    }

    assert styles[1] == {
        'min_scale_denom': 1,
        'zoom_level': 10,
        'max_scale_denom': 750000,
        'fill-opacity': 0.3
    }


def test_get_styles_float():
    style = _get_style({
        "fill-opacity": 0.7,
        "fill-color": "#f2eae2",
    })
    styles = get_styles(style)
    print styles
    assert styles[0] == {
        "fill-color": "#f2eae2",
        "fill-opacity": 0.7,
        "zoom_level": None,
        "min_scale_denom": None,
        "max_scale_denom": None
    }


def test_get_styles_simple():
    style = _get_style({
        "fill-outline-color": "#dfdbd7",
        "fill-color": "#f2eae2",
    })
    styles = get_styles(style)
    assert len(styles) == 1
    assert styles[0] == {
        "fill-outline-color": "#dfdbd7",
        "fill-color": "#f2eae2",
        "zoom_level": None,
        "min_scale_denom": None,
        "max_scale_denom": None
    }


def test_get_styles():
    style = _get_style({
        "fill-outline-color": "#dfdbd7",
        "fill-color": "#f2eae2",
        "fill-opacity": {
          "base": 1,
          "stops": [
            [
              13,
              0
            ],
            [
              16,
              1
            ]
          ]
        }
      })
    styles = get_styles(style)
    assert len(styles) == 2
    styles = sorted(styles, key=lambda s: s["zoom_level"])
    assert _are_dicts_equal(styles[0], {
        'fill-outline-color': '#dfdbd7',
        'fill-color': '#f2eae2',
        'zoom_level': 13,
        'fill-opacity': 0,
        'max_scale_denom': 100000,
        'min_scale_denom': 12500
    })
    assert _are_dicts_equal(styles[1], {
        'fill-outline-color': '#dfdbd7',
        'fill-color': '#f2eae2',
        'zoom_level': 16,
        'fill-opacity': 1,
        'max_scale_denom': 12500,
        'min_scale_denom': 1
    })


def _are_dicts_equal(d1, d2):
    for k in d1:
        if k not in d2:
            raise AssertionError("Key '{}' not in d2: {}".format(k, d2))
    for k in d2:
        if k not in d1:
            raise AssertionError("Key '{}' not in d1: {}".format(k, d1))
    for k in d1:
        if d1[k] != d2[k]:
            raise AssertionError("Key '{}' not equal: {} != {}".format(k, d1[k], d2[k]))
    return True

def _get_style(paint):
    return {
        "id": None,
        "type": "fill",
        "paint": paint
    }