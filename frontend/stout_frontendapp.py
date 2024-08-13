import streamlit as st
import pubchempy as pcp

import requests
import os
from streamlit_navigation_bar import st_navbar
from smiles_to_iupac_module import show_generate_iupac
from iupac_to_smiles_module import show_convert_iupac
from structure_to_iupac_module import show_draw_structure
from about import show_about

API_URL = "http://backend:3000"


def show_footer():
    """
    Display a fixed footer at the bottom of the Streamlit app.

    This function renders an HTML and CSS-styled footer that is fixed
    at the bottom of the page. The footer contains a copyright notice
    and a link to the Steinbeck Group's website, attributing the creation
    and maintenance of the application.

    Usage:
        Call this function at the end of your Streamlit app script to display
        the footer at the bottom of the app.

    Example:
        show_footer()
    """
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f2f2f2;
            color: black;
            text-align: center;
            padding: 10px;
            z-index: 999;
        }
        </style>
        <div class="footer">
            <p>&copy; 2024 <strong>stout.decimer.ai</strong> is created and maintained by the <a href="https://cheminf.uni-jena.de" target="_blank">Steinbeck Group</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_home(API_URL: str = API_URL) -> None:
    """
    Display the home page of the Smiles TO iUpac Translator Streamlit app.

    This function creates a Streamlit user interface that allows users to input a molecular structure
    in SMILES format and generate the corresponding IUPAC name. It also provides an option to search
    for the IUPAC name on PubChem.

    The interface includes:
    - A centered logo and title for the app.
    - A text input for entering the molecule in SMILES format.
    - Buttons to generate the IUPAC name and search PubChem for the IUPAC name.
    - A display of the generated IUPAC name and a link to the PubChem entry if found.

    When the "Get IUPAC name" button is clicked:
    - A spinner is displayed while the IUPAC name is being generated.
    - The generated IUPAC name is displayed in the session state.

    When the "Search PubChem" button is clicked:
    - A spinner is displayed while the PubChem search is performed.
    - The retrieved IUPAC name from PubChem is displayed with a link to the PubChem entry.

    Args:
        API_URL (str): The base URL of the API for generating IUPAC names. Defaults to `API_URL`.

    Note:
        - The `API_URL` is assumed to be predefined and points to the backend service for generating IUPAC names.
        - The `st.session_state` is used to store the generated IUPAC name and the PubChem IUPAC name for display.
        - The `pypubchem` package is used to retrieve compound information from PubChem.

    Raises:
        - RequestsException: If there is an error with the API request for generating the IUPAC name.
        - Exception: If there is an error while searching PubChem.
    """

    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://github.com/Kohulan/cheminf-jena-logos/blob/main/STOUT/STOUT.png?raw=true' width='30%'>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h3 style='text-align: center; font-family: Bahnschrift, sans-serif;'>Smiles TO iUpac Translator</h3>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([3, 6, 3])
    with col2:
        molecule = st.text_input("Molecule SMILES input", "CCO")

    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 2])

    # Initialize session state
    if "iupac_name" not in st.session_state:
        st.session_state["iupac_name"] = ""
    if "pubchem_iupac" not in st.session_state:
        st.session_state["pubchem_iupac"] = ""

    with col3:
        if st.button("Get IUPAC name", key="centered"):
            api_endpoint = f"{API_URL}/latest/stout/SMILE2IUPAC?"
            headers = {"Content-Type": "text/plain", "accept": "application/json"}

            with st.spinner("Generating IUPAC name..."):
                response = requests.post(api_endpoint, headers=headers, data=molecule)

                if response.status_code == 200:
                    result = response.text.replace('["', "").replace('"]', "")
                    st.session_state["iupac_name"] = result
                else:
                    st.error("Error occurred while generating IUPAC name.")
        st.markdown(
            f"<h4 style='text-align: left;'>{st.session_state['iupac_name']}</h4>",
            unsafe_allow_html=True,
        )

    with col4:
        if st.button("Search PubChem"):
            try:
                with st.spinner("Retrieving IUPAC name..."):
                    compounds = pcp.get_compounds(molecule, "smiles")
                    if compounds:
                        pubchem_iupac = compounds[0].iupac_name
                        pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{compounds[0].cid}"
                        st.session_state[
                            "pubchem_iupac"
                        ] = f"<h4 style='text-align: left;'><a href='{pubchem_url}' target='_blank'>{pubchem_iupac}</a></h4>"
                    else:
                        st.error("No compound found with the provided SMILES.")
            except Exception as e:
                st.error(f"Error occurred while searching PubChem: {str(e)}")
        st.markdown(
            st.session_state["pubchem_iupac"],
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p style='text-align: center;'>To draw a structure, please visit the <b>Structure to IUPAC tab</b>.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center;'>
            <img src='https://github.com/Kohulan/cheminf-jena-logos/blob/main/STOUT/stout.gif?raw=true' style='max-width: 10%; height: auto;' loop="false">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align: center;'>The first open-source SMILES to IUPAC name Translator, <b>STOUT</b>: Bridging the Gap Between Molecules and Names!</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<style>
.warning-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 20px;
    margin-bottom: 20px;
}
.stWarning {
    background-color: #FFF9C4;
    border-left: 6px solid #FBC02D;
    color: #212121;
    padding: 16px;
    border-radius: 4px;
    text-align: center;
    box-shadow: 0 2px 5px 0 rgba(0,0,0,0.16);
    max-width: 80%;
    width: fit-content;
}
</style>
<div class="warning-container">
    <div class="stWarning">
        ⚠️ Disclaimer: STOUT is a language model that can make mistakes
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def show_health_check():
    """
    Display the Health Check page of the Streamlit app.

    This function creates a Streamlit user interface for checking the health status of the API.
    The interface includes:
    - A subheader titled "Health Check".
    - A button to trigger the health check.
    - A footer with information about the app and its creators.

    When the "Check Health" button is clicked:
    - Sends a GET request to the API's health endpoint.
    - Displays a success message with the health status if the API is healthy.
    - Displays an error message if the API is not healthy.

    Note:
        - The `API_URL` is assumed to be predefined and points to the backend service for health checks.

    Raises:
        - HTTPException: If the API request fails or returns a non-200 status code.
    """
    st.subheader(
        "If the API is experiencing issues, please check the API Health status here.."
    )

    if st.button("Check Health"):
        api_endpoint = f"{API_URL}/latest/stout/health"
        response = requests.get(api_endpoint)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Health Status: {result['status']}")
        else:
            st.error("API is not healthy.")


def main():
    """
    Main function for running the STOUT Webservice.

    This function configures the Streamlit page settings, defines the navigation bar with pages and URLs,
    and specifies the styles and options for the navigation bar. It associates each page with its respective
    function to be executed when the page is selected.

    The interface includes the following pages:
    - Home: Displays the home page with options to generate IUPAC names from SMILES and structures, and to perform health checks.
    - SMILES to IUPAC: Provides functionality to generate IUPAC names from SMILES.
    - Structure to IUPAC: Allows users to draw molecular structures and generate corresponding IUPAC names.
    - IUPAC to SMILES: Offers the capability to convert IUPAC names to SMILES.
    - Health Check: Allows users to check the health status of the API.
    - About: Displays information about the STOUT Webservice.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    st.set_page_config(
        page_title="STOUT Microservice",
        page_icon=":chemistry:",
        layout="wide",
    )

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(parent_dir, "public/STOUT.svg")

    pages = [
        "Home",
        "SMILES to IUPAC",
        "Structure to IUPAC",
        "IUPAC to SMILES",
        "Health Check",
        "About",
        "GitHub",
    ]

    urls = {"GitHub": "https://github.com/Kohulan/STOUT_WebApp"}

    styles = {
        "nav": {
            "background-color": "#0086ad",
            "justify-content": "middle",
            "font-family": "Bahnschrift, sans-serif",
        },
        "img": {
            "padding-right": "14px",
        },
        "span": {
            "color": "white",
            "padding": "14px",
            "font-family": "Bahnschrift, sans-serif",
        },
        "active": {
            "color": "var(--text-color)",
            "background-color": "white",
            "font-weight": "normal",
            "padding": "14px",
            "font-family": "Bahnschrift, sans-serif",
        },
    }

    options = {
        "show_menu": False,
        "show_sidebar": False,
    }

    page = st_navbar(
        pages,
        logo_path=logo_path,
        urls=urls,
        styles=styles,
        options=options,
    )

    functions = {
        "Home": show_home,
        "SMILES to IUPAC": show_generate_iupac,
        "Structure to IUPAC": show_draw_structure,
        "IUPAC to SMILES": show_convert_iupac,
        "Health Check": show_health_check,
        "About": show_about,
    }

    go_to = functions.get(page)
    if go_to:
        go_to()

    # Add the permanent footer
    show_footer()


if __name__ == "__main__":
    main()
