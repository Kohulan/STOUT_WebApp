import streamlit as st
import requests

API_URL = "http://backend:3000"


def generate_smiles_from_iupac(
    iupac_name: str, converter: str = "opsin", visualize: str = "2D"
) -> dict:
    """
    Generate SMILES from a given IUPAC name using the IUPAC2SMILES API endpoint.

    Args:
        iupac_name (str): The IUPAC name of the molecule.
        converter (str, optional): The type of converter to use ("opsin" or "stout"). Defaults to "opsin".
        visualize (str, optional): Whether to visualize the generated SMILES in 2D or 3D. Defaults to "2D".

    Returns:
        dict: A dictionary containing the generated SMILES string and the corresponding depiction.
    """
    try:
        # Make the API request
        url = f"{API_URL}/latest/stout/IUPAC2SMILES"
        params = {
            "input_text": iupac_name,
            "converter": converter,
            "visualize": visualize,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Return the response data
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None


def show_convert_iupac():
    """
    Display a Streamlit app for converting IUPAC names to SMILES using OPSIN/STOUT.

    This function creates a Streamlit user interface for converting IUPAC names to SMILES using either the OPSIN
    or STOUT converters. It provides options for visualization (2D or 3D) and displays the generated SMILES along
    with its depiction.

    The interface includes:
    - A subheader for the app's purpose.
    - A text input for entering the IUPAC name, with a default value.
    - A dropdown for selecting the converter (OPSIN or STOUT).
    - A dropdown for selecting the visualization type (2D or 3D).
    - A button to trigger the conversion process.

    When the "Generate" button is clicked:
    - A spinner is displayed while the SMILES is being generated.
    - The generated SMILES is displayed along with the input IUPAC name.
    - The depiction of the generated SMILES is shown in the chosen visualization format (2D/3D).

    A footer is included at the bottom of the app with information about the creators and maintainers.

    Note:
        - The `generate_smiles_from_iupac` function is called to perform the conversion from IUPAC name to SMILES.
        - The depiction of the SMILES is displayed either as an HTML component or directly in Markdown.

    """
    st.subheader("Convert IUPAC name to SMILES using OPSIN/STOUT")
    iupac_name = st.text_input(
        "Enter IUPAC Name", value="1,3,7-trimethylpurine-2,6-dione"
    )
    converter = st.selectbox("Converter", ["stout", "opsin"], index=0)
    visualize = st.selectbox("Visualization", ["2D", "3D"], index=0)

    if st.button("Generate"):
        with st.spinner("Generating SMILES..."):
            result = generate_smiles_from_iupac(iupac_name, converter, visualize)

            if result:
                st.subheader("Generated SMILES")
                st.write(f"<b>Input name:</b> {iupac_name}", unsafe_allow_html=True)
                st.markdown(
                    f"<b>Output SMILES:</b> {result['SMILES']}", unsafe_allow_html=True
                )

                st.subheader("Depiction")
                depiction_data = result["Depiction"]
                if "html" in depiction_data:
                    st.components.v1.html(depiction_data, height=512, scrolling=False)
                else:
                    st.markdown(
                        f'<div style="text-align: center;">{result["Depiction"]}</div>',
                        unsafe_allow_html=True,
                    )
