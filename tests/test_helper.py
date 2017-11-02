from core.helper import get_styles


def test_zoom_level_zero():
    paint = {
        "fill-opacity": {
          "base": 1,
          "stops": [
            [
              0,
              0.9
            ],
            [
              10,
              0.3
            ]
          ]
        }
      }
    style = get_styles(paint)
    print style
    assert False


# def test_get_styles_float():
#     paint = {
#         "fill-opacity": 0.7,
#         "fill-color": "#f2eae2",
#     }
#     styles = get_styles(paint)
#     print styles
#     assert styles[0] == {
#         "fill-color": "#f2eae2",
#         "fill-opacity": 0.7,
#         "zoom_level": None,
#         "min_scale_denom": None,
#         "max_scale_denom": None
#     }
#
#
# def test_get_styles_simple():
#     paint = {
#         "fill-outline-color": "#dfdbd7",
#         "fill-color": "#f2eae2",
#     }
#     styles = get_styles(paint)
#     assert len(styles) == 1
#     assert styles[0] == {
#         "fill-outline-color": "#dfdbd7",
#         "fill-color": "#f2eae2",
#         "zoom_level": None,
#         "min_scale_denom": None,
#         "max_scale_denom": None
#     }
#
#
# def test_get_styles_complex():
#     paint = {
#         "fill-color": {
#             "stops": [
#                 [14, "fill-@-14"],
#                 [16, "fill-@-16"],
#             ]
#         },
#         "fill-outline-color": {
#             "stops": [
#                 [13, "outline-@-13"],
#                 [15, "outline-@-15"],
#             ]
#         },
#     }
#     styles = list(sorted(get_styles(paint), key=lambda s: s["zoom_level"]))
#     assert len(styles) == 4
#     assert _are_dicts_equal(styles[0], {
#         'min_scale_denom': 50000,
#         'fill-outline-color': 'outline-@-13',
#         'fill-color': 'fill-@-14',
#         'zoom_level': 13,
#         'max_scale_denom': 1000000000})
#
#     assert _are_dicts_equal(styles[1], {
#         'min_scale_denom': 25000,
#         'fill-outline-color': 'outline-@-13',
#         'fill-color': 'fill-@-14',
#         'zoom_level': 14,
#         'max_scale_denom': 50000})
#
#     assert _are_dicts_equal(styles[2], {
#         'min_scale_denom': 12500,
#         'fill-outline-color': 'outline-@-15',
#         'fill-color': 'fill-@-14',
#         'zoom_level': 15,
#         'max_scale_denom': 25000})
#
#     assert _are_dicts_equal(styles[3], {
#         'min_scale_denom': 1,
#         'fill-outline-color': 'outline-@-15',
#         'fill-color': 'fill-@-16',
#         'zoom_level': 16,
#         'max_scale_denom': 12500})
#
#
# def test_get_styles():
#     paint = {
#         "fill-outline-color": "#dfdbd7",
#         "fill-color": "#f2eae2",
#         "fill-opacity": {
#           "base": 1,
#           "stops": [
#             [
#               13,
#               0
#             ],
#             [
#               16,
#               1
#             ]
#           ]
#         }
#       }
#     styles = get_styles(paint)
#     assert len(styles) == 2
#     styles = sorted(styles, key=lambda s: s["zoom_level"])
#     assert _are_dicts_equal(styles[0], {
#         'fill-outline-color': '#dfdbd7',
#         'fill-color': '#f2eae2',
#         'zoom_level': 13,
#         'fill-opacity': 0,
#         'max_scale_denom': 1000000000,
#         'min_scale_denom': 12500
#     })
#     assert _are_dicts_equal(styles[1], {
#         'fill-outline-color': '#dfdbd7',
#         'fill-color': '#f2eae2',
#         'zoom_level': 16,
#         'fill-opacity': 1,
#         'max_scale_denom': 12500,
#         'min_scale_denom': 1
#     })
#
#
# def _are_dicts_equal(d1, d2):
#     for k in d1:
#         if k not in d2:
#             raise AssertionError("Key '{}' not in d2: {}".format(k, d2))
#     for k in d2:
#         if k not in d1:
#             raise AssertionError("Key '{}' not in d1: {}".format(k, d1))
#     for k in d1:
#         if d1[k] != d2[k]:
#             raise AssertionError("Key '{}' not equal: {} != {}".format(k, d1[k], d2[k]))
#     return True
