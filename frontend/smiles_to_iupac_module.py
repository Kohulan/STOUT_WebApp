import requests
import html
import streamlit as st

API_URL = "http://backend:3000"
HEADERS = {"Content-Type": "text/plain", "accept": "application/json"}


def show_generate_iupac(API_URL: str = API_URL) -> None:
    """
    Display a Streamlit app for generating IUPAC names from SMILES strings.

    This function creates a Streamlit user interface for converting SMILES strings to IUPAC names
    using an external API. It provides options for retranslation using OPSIN and for selecting the
    output format (HTML, JSON, TEXT).

    The interface includes:
    - A subheader for the app's purpose.
    - A text area for entering SMILES strings, with a default value and adjustable height.
    - A toggle for retranslation using OPSIN.
    - Radio buttons for selecting the output format (HTML, JSON, TEXT).
    - A button to trigger the conversion process.

    When the "Generate" button is clicked:
    - A spinner is displayed while the IUPAC names are being generated.
    - The generated IUPAC names are displayed in the chosen format (HTML/JSON/TEXT).
    - An error message is displayed if the conversion fails.

    A footer is included at the bottom of the app with information about the creators and maintainers.

    Args:
        API_URL (str): The base URL of the API for generating IUPAC names. Defaults to "http://backend:3000".

    Note:
        - The `generate_smiles_from_iupac` function is called to perform the conversion from SMILES to IUPAC name.
        - The depiction of the SMILES is displayed either as an HTML component or directly in Markdown.
        - The `bottom` container is used to display a footer with creator and maintainer information.
    """
    st.subheader("Generate IUPAC Name from SMILES")
    smiles_input = st.text_area("Enter SMILES string(s)", "CCC\nCCO", height=200)
    retranslate = st.toggle("Retranslate (OPSIN)")

    output_format = st.radio("Output Format", ["HTML", "JSON", "TEXT"], horizontal=True)

    if st.button("Generate"):
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
                api_endpoint, params=params, headers=HEADERS, data=smiles_input
            )

        if response.status_code == 200:
            if output_format == "HTML":
                st.markdown(
                    html.unescape(response.text.replace("\\n", "")),
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
        More than 50 SMILES will be discarded, and only the IUPAC names for the first 50 will be displayed.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
