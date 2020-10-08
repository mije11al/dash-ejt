import plotly.graph_objects as go
import pandas as pd



df = pd.read_excel('Data/china_gdp_growth.xlsx')



gdp1 = df.iloc[:5]
gdp2 = df.loc[4:]

fig = go.FigureWidget(data=[
    go.Scatter(x=gdp1.TIME, y=gdp1.Value, mode='lines', line={'dash': 'solid', 'color': 'green'}),
    go.Scatter(x=gdp2.TIME, y=gdp2.Value, mode='lines', line={'dash': 'dash', 'color': 'green'}),
])


fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("linje-graf.html")