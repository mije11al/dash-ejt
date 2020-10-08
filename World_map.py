from plotly.offline import plot
import pandas as pd
import json
import re
import plotly.express as px

with open("Geojson of the world/custom.geo.json") as file:
    countries = json.load(file)

df = pd.read_excel("Data/Situationsrapporter.xlsx",
                   dtype={"Landekode": str})


fig = px.choropleth_mapbox(df, geojson=countries, locations='Landekode', color='Farve', featureidkey = "properties.iso_a3",
                           color_continuous_scale="Viridis",
                           color_discrete_map= {'Grå':'#bfbeba', 'Gul':'#fcf50f','Orange':'#fca10f'},
                           hover_name='Land',
                           hover_data= {"Tekst":True, "Farve":False,"Landekode":False},
                           range_color=(0, 12),
                           mapbox_style="stamen-watercolor",
                           zoom=1,
                           opacity=0.5,
                           labels={'Farve':'Rejseanbefaling'},
                           custom_data=["URL"]
                          )



fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell",
    ),
    hovermode="x unified"
)

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
        console.log(point.customdata[0]);
        window.open(point.customdata[0]);
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
with open('hyperlink_fig_positron.html', 'w') as f:
    f.write(html_str)
