# Import libraries
import streamlit as st
import pydeck as pdk
import pandas as pd

# Neuron 5 logo
st.logo('img/favicon.ico', size='large', link=None, icon_image=None)
st.image('img/bg_logo.png', width=400)  # width in pixels#

# Describe page
st.title(':blue[Global Career Experience]')
st.markdown('**Visualising significant Global experience with PyDeck and GIS data.**')

# # Break down of career locations using GIS data
# st.write('')
# st.header('Edinburgh -> Destination', divider='red', width='content')
# st.write('')

# # Get city data for showing global experience
# df = pd.read_json('data/cities.json')

# # Origin (Edinburgh)
# origin = df[df['city'] == 'Edinburgh'].iloc[0]

# # Arc layer: connect all to Edinburgh
# arc_data = pd.DataFrame([
#     {
#         'from_lat': origin.lat,
#         'from_lon': origin.lon,
#         'to_lat': row.lat,
#         'to_lon': row.lon,
#         'city': row.city
#     }
#     for _, row in df.iterrows() if row.city != 'Edinburgh'
# ])

# # Scatterplot for cities
# point_layer = pdk.Layer(
#     'ScatterplotLayer',
#     data=df,
#     get_position='[lon, lat]',
#     get_fill_color='[255, 70, 30, 200]',
#     get_radius=40000,
#     pickable=True
# )

# # Arc layer
# arc_layer = pdk.Layer(
#     'ArcLayer',
#     data=arc_data,
#     get_source_position='[from_lon, from_lat]',
#     get_target_position='[to_lon, to_lat]',
#     get_source_color=[0, 128, 200],
#     get_target_color=[0, 128, 200],
#     auto_highlight=True,
#     get_width=2,
#     pickable=True
# )

# # Text layer (bold by increasing size)
# text_layer = pdk.Layer(
#     'TextLayer',
#     data=df,
#     get_position='[lon, lat]',
#     get_text='city',
#     get_color=[255, 255, 255, 255],
#     get_size=14,                    # bigger = bolder
#     get_alignment_baseline='"bottom"',
#     pickable=True
# )

# # Map view
# view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1, pitch=30)

# # Draw deck
# r = pdk.Deck(
#     layers=[point_layer, arc_layer, text_layer], 
#     initial_view_state=view_state,
#     tooltip={'html': '<b>{city}</b>'}
# )

# st.pydeck_chart(r, use_container_width=True, height=600)


# Load arcs and prepare data
df = pd.read_json('data/arcs.json', encoding='UTF-8')
df['color_tuple'] = df['color'].apply(tuple)
unique_from = sorted(df['from'].unique())


# Prepare filters
st.write('&nbsp;')
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