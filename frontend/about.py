import streamlit as st
from streamlit_extras.bottom_container import bottom


def show_about():
    st.markdown(
        "<h3 style='text-left: center;'>How to cite us?</h3>", unsafe_allow_html=True
    )
    st.code(
        "Rajan, K., Zielesny, A. & Steinbeck, C. STOUT: SMILES to IUPAC names using neural machine translation.\nJ Cheminform 13, 34 (2021). https://doi.org/10.1186/s13321-021-00512-4",
        language="html",
    )

    st.markdown("<h3 style='text-align: left;'>Contact Us</h3>", unsafe_allow_html=True)

    iframe_src = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2503.2949726059553!2d11.581905350629135!3d50.93352470346138!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a6a898c3634fbb%3A0xdf22378d9f537b71!2sLessingstra%C3%9Fe%208%2C%2007743%20Jena%2C%20Germany!5e0!3m2!1sen!2s!4v1681045800175!5m2!1sen!2s"

    col1, col2 = st.columns([1, 1])

    with col1:
        st.components.v1.html(
            f"""
            <iframe src="{iframe_src}" width="100%" height="300" frameborder="0" style="border:0;" allowfullscreen></iframe>
            """,
            height=400,
        )

    with col2:
        st.markdown(
            """
            <h5 style='text-align: left;'>Prof. Dr. Christoph Steinbeck</h5>
            <strong>EMAIL:</strong>
            <a href="mailto:christoph.steinbeck@uni-jena.de">christoph.steinbeck@uni-jena.de</a><br><br>
            <h5 style='text-align: left;'>Dr. Kohulan Rajan</h5>
            <strong>EMAIL:</strong>
            <a href="mailto:kohulan.rajan@uni-jena.de">kohulan.rajan@uni-jena.de</a><br><br>
            <strong>ADDRESS</strong><br>
            Institute for Inorganic and Analytical Chemistry, Friedrich Schiller University, Lessingstraße 8, Jena 07743, Germany
            """,
            unsafe_allow_html=True,
        )

    with bottom():
        st.markdown(
            "<h4 style='text-align: center;'>Acknowledgement</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center;'>Research supported with Cloud TPUs from Google's TPU Research Cloud (TRC)</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <footer>
                <p align='center'>
                    <img src='https://user-images.githubusercontent.com/30716951/220350828-913e6645-6a0a-403c-bcb8-160d061d4606.png' width='250'>
                </p>
            </footer>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <footer style='text-align: center; margin-top: 10px; padding: 10px; background-color: #f2f2f2;'>
                <p>&copy; 2024 <strong>stout.decimer.ai</strong> is created and maintained by the <a href="https://cheminf.uni-jena.de" target="_blank">Steinbeck Group</a></p>
            </footer>
            """,
            unsafe_allow_html=True,
        )
