import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import parser


def test_generate():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    parser.generate_qgis_styles(path)
    assert True
