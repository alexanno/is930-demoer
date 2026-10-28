import colorsys
from qgis.core import (QgsProject, QgsMapLayerType, QgsWkbTypes,
                       QgsSingleSymbolRenderer, QgsFillSymbol,
                       QgsLineSymbol, QgsMarkerSymbol)
from qgis.PyQt.QtGui import QPainter, QColor
from qgis.utils import iface

MODE = "dark"   # "dark" = glowing overlaps (Addition) | "light" = darkening overlaps (Multiply)
FILL_ALPHA = 45  # 0-255, lower = more transparent

if MODE == "dark":
    iface.mapCanvas().setCanvasColor(QColor(0, 0, 0))
    blend = QPainter.CompositionMode_Plus
    sat, val = 0.85, 1.0
else:
    iface.mapCanvas().setCanvasColor(QColor(255, 255, 255))
    blend = QPainter.CompositionMode_Multiply
    sat, val = 0.9, 0.75

layers = [l for l in QgsProject.instance().mapLayers().values()
          if l.type() == QgsMapLayerType.VectorLayer]

for i, layer in enumerate(layers):
    # Evenly spread hues (golden-ratio step) so neighbouring layers differ
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((i * 0.618) % 1, sat, val)]
    solid = f"{r},{g},{b},255"
    faint = f"{r},{g},{b},{FILL_ALPHA}"

    gt = layer.geometryType()
    if gt == QgsWkbTypes.PolygonGeometry:
        sym = QgsFillSymbol.createSimple({
            "color": faint, "outline_color": solid, "outline_width": "0.25"})
    elif gt == QgsWkbTypes.LineGeometry:
        sym = QgsLineSymbol.createSimple({"line_color": solid, "line_width": "0.3"})
    elif gt == QgsWkbTypes.PointGeometry:
        sym = QgsMarkerSymbol.createSimple({
            "color": faint, "outline_color": solid, "outline_width": "0.2", "size": "2"})
    else:
        continue

    layer.setRenderer(QgsSingleSymbolRenderer(sym))
    layer.setBlendMode(blend)
    layer.setOpacity(1.0)
    layer.triggerRepaint()

iface.mapCanvas().refresh()