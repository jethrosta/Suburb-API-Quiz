import streamlit as st
import folium
from streamlit_folium import st_folium

# Import the functions from your new library file
from cma_utils import get_address_from_coords, run_cma_workflow

# ---------------------------------
# Main Page Logic
# ---------------------------------

st.title("🏘️ CMA Search")
st.warning("**Note:** This sandbox API only works for *exact* demo addresses. Use the search bar for the most reliable test.")

# --- 1. Search Bar ---
st.header("Search by Address (Recommended)")
with st.form(key="address_search_form"):
    address_input = st.text_input(
        "Enter a demo address", 
        value="27 Arlington Street, Belmont North" # Pre-fill the working address
    )
    submit_button = st.form_submit_button("Generate Report")

if submit_button:
    # Call the workflow function from our utils file
    run_cma_workflow(address_input)

st.divider()

# --- 2. Map Click ---
st.header("Or Click on the Map")
st.markdown("Map click is less reliable as the sandbox requires an *exact* demo address.")

# Center the map on the known demo address
map_center = [-32.9912, 151.6845] 
m = folium.Map(location=map_center, zoom_start=17) # Zoom in
map_data = st_folium(m, width=700, height=500)

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.info(f"Coordinates selected: {lat:.6f}, {lon:.6f}")
    
    address_string = None
    with st.spinner("Finding address for coordinates..."):
        # Call the geocoding function from our utils file
        address_string = get_address_from_coords(lat, lon)
    
    if address_string:
        # Call the same workflow function as the search bar
        run_cma_workflow(address_string)
    else:
        st.error("Could not find a valid address for the clicked location.")