from plotly.offline import plot
import pandas as pd
import plotly.graph_objs as go
import json
import re

with open("Geojson of the world/custom.geo (1).json") as file:
    countries = json.load(file)


#print(countries['features'][0]["properties"]["iso_a3"])

df = pd.read_excel("data/Rejsevejledning.xlsx",
                   dtype={"Landekode": str})

ls = df.URL.to_list()
print(ls)
import plotly.express as px

fig = go.Figure(go.Choroplethmapbox(geojson=countries, locations=df.Landekode, z=df.Farve,
                           featureidkey='properties.iso_a3',
                           colorscale="Viridis",
                           zmin=0,
                           zmax=12,
                           marker_opacity=0.5,
                           marker_line_width=0,
                           customdata=ls
                          ))


fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



print(type(fig))
data = [fig]

with open("data.txt", 'w') as file:
    file.write(str(data))
# Get HTML representation of plotly.js and this figure
plot_div = plot(fig, output_type='div', include_plotlyjs=True)

# Get id of html div element that looks like
# <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
res = re.search('<div id="([^"]*)"', plot_div)
div_id = res.groups()[0]

# Build JavaScript callback for handling clicks
# and opening the URL in the trace's customdata
js_callback = """
<script>
var plot_element = document.getElementById("{div_id}");
plot_element.on('plotly_click', function(data){{
    console.log(data);
    var point = data.points[0];
    if (point) {{
        console.log(point.customdata);
        window.open(point.customdata);
    }}
}})
</script>
""".format(div_id=div_id)

# Build HTML string
html_str = """
<html>
<body>
{plot_div}
{js_callback}
</body>
</html>
""".format(plot_div=plot_div, js_callback=js_callback)

# Write out HTML file
with open('hyperlink_fig.html', 'w') as f:
    f.write(html_str)
