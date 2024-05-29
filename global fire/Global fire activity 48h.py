import csv
from datetime import datetime

from plotly.graph_objects import Scattergeo, Layout
from plotly import offline

num_rows = 10_000

filename = 'MODIS_C6_1_Global_48h.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # latitudes and longitudes, and dates.
    dates, brightnesses = [], []
    lats, lons = [], []
    hover_texts = []
    row_num = 0
    for row in reader:
        date = datetime.strptime(row[5], '%Y-%m-%d')
        brightness = float(row[2])
        label = f"{date.strftime('%m/%d/%y')} - {brightness}"

        dates.append(date)
        brightnesses.append(brightness)
        lats.append(row[0])
        lons.append(row[1])
        hover_texts.append(label)
        
        row_num += 1
        if row_num == num_rows:
            break

#map
data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text': hover_texts,
    'marker': {
        'size': [brightness/20 for brightness in brightnesses],
        'color': brightnesses,
        'colorscale': 'YlOrRd',
        'reversescale': True,
        'colorbar': {'title': 'Brightness'},
    },
}]

my_layout = Layout(title='Global Fire Activity in 48 hours')

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global_fires.html')