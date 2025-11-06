# Import libraries
import streamlit as st
import pydeck as pdk
import pandas as pd
from components.footer import show_footer
from components.sidebar import show_sidebar
from components.header import show_header


# ---- Sidebar ----
show_sidebar()

# ---- Header ----
show_header(page_title='Neuron 5 - Global Map',
            title = 'Global Career Experience',
            subtitle = 'Visualising significant Global experience with PyDeck and GIS data.')

# ---- Main content ----
# Load arcs and prepare data
df = pd.read_json('data/arcs.json', encoding='UTF-8')
df['color_tuple'] = df['color'].apply(tuple)
unique_from = sorted(df['from'].unique())

# Prepare filters
st.header("Filter locations", divider='red')
# Checkbox selection (pre-select all)
unchecked = ['Edinburgh', 'Swansea']
selected_from = []
cols = st.columns(3)
for i, city in enumerate(unique_from):
    col = cols[i % 3]
    with col:
        # check the box unless city is in the unchecked list
        if st.checkbox(city, value=(city not in unchecked)):
            selected_from.append(city)

# Filter arcs for selected origins
filtered_df = df[df['from'].isin(selected_from)]

# Constants for points
POINT_RADIUS, POINT_ALPHA = 25000, 125

# Gather unique points from 'from' and 'to'
points_df = pd.DataFrame(
    [
        {'city': row['from'], 'lat': row['lat_from'], 'lon': row['lon_from'], 'color_tuple': row['color']}
        for _, row in filtered_df.iterrows()
    ] + [
        {'city': row['to'], 'lat': row['lat_to'], 'lon': row['lon_to'], 'color_tuple': row['color']}
        for _, row in filtered_df.iterrows()
    ]
)

# Scatterplot layer for points
point_layer = pdk.Layer("ScatterplotLayer",
    data=points_df,
    get_position = '[lon, lat]',
    get_fill_color = f'[color_tuple[0], color_tuple[1], color_tuple[2], {POINT_ALPHA}]',
    get_radius = POINT_RADIUS,
    pickable = False
)

# Arc layer
arc_layer = pdk.Layer("ArcLayer",
    data = filtered_df,
    get_source_position = '[lon_from, lat_from]',
    get_target_position = '[lon_to, lat_to]',
    get_source_color = 'color_tuple',
    get_target_color = 'color_tuple',
    get_width = 3,
    auto_highlight = True,
    pickable = True
)

# Text layer for city names
text_layer = pdk.Layer("TextLayer",
    data = points_df,
    get_position = '[lon, lat]',
    get_color = [255, 255, 255],
    get_size = 12,
    get_alignment_baseline = '"bottom"',
    pickable = False
)

# Map view
view_state = pdk.ViewState(latitude=20, longitude=50, zoom=1, pitch=30)

# Deck object
r = pdk.Deck(
    layers = [point_layer, arc_layer, text_layer],
    initial_view_state = view_state,
    tooltip = {"html": "<b>From:</b> {from}<br><b>To:</b> {to}"}
)

st.pydeck_chart(r, use_container_width=True, height=600)

# ---- Footer ----
show_footer()