import os
import sys
import shutil
from xml.sax.saxutils import unescape
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import process, write_styles


def test_generate_qgis():
    # path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    # path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "klokantech_basic.json")
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "positron.json")
    data = _load_file(path)
    output_directory = r"C:\DEV\Vector-Tiles-Reader-QGIS-Plugin\styles"
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    styles = process(data)
    write_styles(styles, output_directory)


def test_generate_local():
    # path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "osm_bright.json")
    # path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "klokantech_basic.json")
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "positron.json")
    data = _load_file(path)
    output_directory = os.path.join(os.path.dirname(__file__), "generated")
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    styles = process(data)
    write_styles(styles, output_directory)


def test_filter():
    path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "with_filter.json")
    data = _load_file(path)
    style_obj = process(data)
    styles = style_obj["landuse_overlay.polygon.qml"]["styles"]
    assert len(styles) == 1
    assert "rule" in styles[0]
    assert unescape(styles[0]["rule"], entities={"&quot;": '"'}) == "\"class\" is not null and \"class\" = \'national_park\'"


def _load_file(path):
    with open(path, 'r') as f:
        data = f.read()
    return data
