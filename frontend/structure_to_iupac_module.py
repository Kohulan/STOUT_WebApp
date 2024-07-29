import streamlit as st
import requests
from html import unescape
from streamlit_ketcher import st_ketcher
from streamlit_extras.bottom_container import bottom

API_URL = "http://backend:3000"
HEADERS = {"Content-Type": "text/plain", "accept": "application/json"}


def show_draw_structure(API_URL: str = API_URL) -> None:
    """
    Display a Streamlit app for generating IUPAC names from molecular structures.

    This function creates a Streamlit user interface that allows users to input a molecular structure
    in SMILES format, visualize it using the Ketcher molecular editor, and generate the corresponding
    IUPAC name. The interface provides options for retranslation using OPSIN and for selecting the
    output format (HTML, JSON, TEXT).

    The interface includes:
    - A header for the app's purpose.
    - Columns for layout organization.
    - A text input for entering the molecule in SMILES format.
    - An embedded Ketcher molecular editor for visualizing and editing the molecule.
    - Options for retranslation and output format.
    - A button to trigger the generation of the IUPAC name.

    When the "Generate" button is clicked:
    - A spinner is displayed while the IUPAC name is being generated.
    - The generated IUPAC name is displayed in the chosen format (HTML/JSON/TEXT).
    - An error message is displayed if the generation fails.

    A footer is included at the bottom of the app with information about the creators and maintainers.

    Note:
        - The `st_ketcher` function is used to embed the Ketcher molecular editor.
        - The `API_URL` is assumed to be predefined and points to the backend service for generating IUPAC names.
        - The `bottom` container is used to display a footer with creator and maintainer information.

    """
    st.markdown(
        """
        <h3 style='text-align: center; font-family: Bahnschrift, sans-serif;'>Generate IUPAC Name from structure</h3>
        """,
        unsafe_allow_html=True,
    )

    # Molecule input
    col1, col2, col3 = st.columns([2, 3, 4])

    with col2:
        molecule = st.text_input(
            "Molecule SMILES input",
            "CC(C)CCO",
        )

    # Ketcher window
    with col3:
        SMILES_out = st_ketcher(molecule)

    # Output and options
    with col2:
        st.markdown(f"SMILES output: ```{SMILES_out}```")
        retranslate = st.checkbox("Retranslate (OPSIN)")
        output_format = st.radio(
            "Output Format", ["HTML", "JSON", "TEXT"], horizontal=True
        )
        generate_button = st.button("Generate")

    if generate_button:
        api_endpoint = f"{API_URL}/latest/stout/SMILE2IUPAC?"

        if output_format == "TEXT":
            params = {"retranslate": str(retranslate).lower()}
        else:
            params = {
                "retranslate": str(retranslate).lower(),
                "format": output_format.lower(),
            }

        with st.spinner("Generating IUPAC name..."):
            response = requests.post(
                api_endpoint, params=params, headers=HEADERS, data=SMILES_out
            )

            if response.status_code == 200:
                if output_format == "HTML":
                    st.markdown(
                        unescape(response.text.replace("\\\\n", "")),
                        unsafe_allow_html=True,
                    )
                elif output_format == "JSON":
                    result = response.json()
                    st.json(result)
                else:
                    result = response.json()
                    st.json(result)
            else:
                st.error("Error occurred while generating IUPAC name.")
