import os
import sys
import shutil
from xml.sax.saxutils import unescape
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import parser


def test_generate_qgis():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    output_directory = r"C:\DEV\Vector-Tiles-Reader-QGIS-Plugin\styles"
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    styles = parser.generate_qgis_styles(mapbox_gl_style_path=path)
    parser.write_styles(styles, output_directory)


def test_generate_local():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    output_directory = os.path.join(os.path.dirname(__file__), "generated")
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    styles = parser.generate_qgis_styles(mapbox_gl_style_path=path)
    parser.write_styles(styles, output_directory)


def test_filter():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "with_filter.json")
    style_obj = parser.generate_qgis_styles(mapbox_gl_style_path=path)
    styles = style_obj["landuse_overlay"]["styles"]
    print styles
    assert len(styles) == 1
    assert "rule" in styles[0]
    assert unescape(styles[0]["rule"], entities={"&quot;": '"'}) == "(\"class\" = \'national_park\')"
