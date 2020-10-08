import pandas as pd
import json

with open("Geojson of the world/custom.geo (1).json") as file:
    countries = json.load(file)


#print(countries['features'][0]["properties"]["iso_a3"])

df = pd.read_excel("data/Rejsevejledning.xlsx",
                   dtype={"Landekode": str})

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=countries, locations='Landekode', color='Farve', featureidkey = "properties.iso_a3",
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="stamen-watercolor",
                           zoom=1,
                           opacity=0.5,
                           labels={'Farve':'Rejseanbefaling'},
                           hover_data=["Land", "URL"],
                           custom_data=["URL"]
                          )



fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell",
    ),
)

def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with f.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s


fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("test.html")
