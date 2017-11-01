## Fill-Styles (for Polygons)
The following properties have to be respected:

Mapbox | QGIS UI | QML
--- | --- | ---
fill-color | Fill | color
fill-outline-color | Outline | outline_color
fill-translate | Offset X,Y | offset
fill-opacity | Transparency | alpha (attribute of 'symbol')

If any of these values is zoom_level dependent, rules for each zoom_level have to be created.
E.g. fill-color is specified for zoom_level 14,15 and fill-opacity is
specified for zoom levels 13,16 then in total 4 rules will be created.
The rules have to be created in ascending order in regard to the zoom level.
This means, the first rule will be for the lowest zoom level.
Each other rule will be equal to the prior rule except for the changed
property.

- The zoom level will be set as scale-range of a rule.
- The rule with the lowest zoom level will have no 'Min. Scale'
- The rule with the highest zoom level will have no 'Max. Scale'




