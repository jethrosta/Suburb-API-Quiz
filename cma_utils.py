import streamlit as st
import requests
import pandas as pd

# ---------------------------------
# API Call Functions
# ---------------------------------

@st.cache_data
def get_address_from_coords(lat, lon):
    """
    Uses Nominatim (OpenStreetMap) to reverse geocode lat/lon to an address.
    """
    URL = "https://nominatim.openstreetmap.org/reverse"
    PARAMS = {'format': 'json', 'lat': lat, 'lon': lon, 'addressdetails': 1}
    headers = {'User-Agent': 'StreamlitCMAApp/1.0'}
    
    try:
        response = requests.get(URL, params=PARAMS, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'display_name' in data:
                return data['display_name']
    except Exception as e:
        st.error(f"Reverse Geocoding Error: {e}")
        return None
    return None

@st.cache_data
def get_cma_data_from_address(address_query):
    """
    Calls the SANDBOX API.
    --- FIX: Corrected the typo in the API_URL ---
    """
    # --- FIX: Changed 'https.` to 'https://' ---
    API_URL = "https://www.microburbs.com.au/report_generator/api/cma"
    
    # We must use GET, so we use 'params'
    params = {"address": address_query}
    
    try:
        # We are still using requests.get, which is correct.
        response = requests.get(API_URL, params=params, timeout=30) 
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 405:
            st.error("API Error (405): Method Not Allowed. This API is very confusing.")
            return None

        else:
            try:
                error_data = response.json()
                st.error(f"API Error (Status {response.status_code}): {error_data.get('detail', response.text)}")
            except:
                st.error(f"API Error (Status {response.status_code}): Response was empty or not JSON. Check if the sandbox URL is correct.")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Network Error (CMA): {e}")
        return None

# ---------------------------------
# UI & Logic Functions
# ---------------------------------

def display_cma_results(cma_data):
    """
    Takes the JSON data from the API and displays it in Streamlit.
    """
    st.success("Report Generated Successfully!")
    
    st.header(f"Report for: {cma_data.get('address', 'N/A')}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Estimated Value", f"${cma_data.get('value', 0):,}", 
                help=f"Confidence: {cma_data.get('confidence')*100:.1f}%")
    col2.metric("Beds", cma_data.get('beds', 'N/A'))
    col3.metric("Baths", cma_data.get('baths', 'N/A'))
    
    st.divider()

    st.header("📍 Property Location")
    subject_loc = cma_data.get('location', {})
    map_data = []
    
    if 'lat' in subject_loc and 'lon' in subject_loc:
        map_data.append({"lat": subject_loc['lat'], "lon": subject_loc['lon']})
    
    if map_data:
        map_df = pd.DataFrame(map_data)
        st.map(map_df, zoom=13)
    else:
        st.write("Could not retrieve location data to display map.")

    st.divider()

    st.header("📊 Comparable Properties")
    comparables = cma_data.get('comparables', [])
    if comparables:
        comp_list = []
        for comp in comparables:
            comp_list.append({
                "Address": comp.get('address'),
                "Value": f"${comp.get('value', 0):,}",
                "Beds": comp.get('beds', 'N/A'),
                "Baths": comp.get('baths', 'N/A'),
                "Distance (km)": f"{comp.get('distance', 0):.2f}",
                "Similarity": f"{comp.get('similarity', 0)*100:.1f}%"
            })
        
        comp_df = pd.DataFrame(comp_list)
        st.dataframe(comp_df, use_container_width=True)
    else:
        st.write("No comparable properties found.")

    with st.expander("Show Raw API Data"):
        st.json(cma_data)

def run_cma_workflow(address_string):
    """
    A central function to run the simplified API chain.
    """
    if not address_string:
        st.error("No address provided.")
        return

    st.write(f"**Searching for:** {address_string}")
    
    with st.spinner(f"Generating CMA report for '{address_string}'..."):
        cma_data = get_cma_data_from_address(address_string)
        
    if cma_data:
        display_cma_results(cma_data)
    else:
        st.error("Could not generate a CMA report. Please check the error messages above.")