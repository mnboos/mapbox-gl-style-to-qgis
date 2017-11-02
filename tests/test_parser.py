import os
import sys
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import parser


def test_generate():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    output_directory = os.path.join(os.path.dirname(__file__), "generated")
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    parser.generate_qgis_styles(mapbox_gl_style_path=path, output_directory=output_directory)
