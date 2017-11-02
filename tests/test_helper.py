from core.helper import get_styles

def test_get_styles():
    paint = {
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
      }
    styles = get_styles(paint)
    print styles
    assert styles == [{
        'fill-outline-color': '#dfdbd7',
        'fill-color': '#f2eae2',
        'zoom_level': 16,
        'fill-opacity': 1,
        'min_scale': 12500,
        'max_scale': 1
    }, {
        'fill-outline-color': '#dfdbd7',
        'fill-color': '#f2eae2',
        'zoom_level': 13,
        'fill-opacity': 0,
        'min_scale': 1000000000,
        'max_scale': 12500
    }]
