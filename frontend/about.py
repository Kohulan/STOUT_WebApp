import streamlit as st
from streamlit_extras.bottom_container import bottom


def show_about():
    """
    Display the 'About' page of the Streamlit app.

    This function creates an 'About' section in a Streamlit app, providing
    information on how to cite the project, contact details for the authors,
    and acknowledgments. It includes embedded Google Maps for the address,
    links to email addresses, and acknowledgment of support and licensing.

    Usage:
        Call this function to display the 'About' page within the Streamlit app.

    Example:
        show_about()
    """
    # Apply custom styles for the page
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f0ed;
            color: #4a4a4a;
        }
        .container {
            background-color: #FFFFFF;
            border-radius: 0;
            box-shadow: none;
            padding: 24px;
            margin-bottom: 24px;
        }
        .header {
            color: #4a4a4a;
            font-size: 32px;
            font-weight: 300;
            margin-bottom: 16px;
            text-transform: uppercase;
        }
        .subheader {
            color: #4a4a4a;
            font-size: 20px;
            font-weight: 400;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        .text {
            color: #4a4a4a;
            font-size: 16px;
            line-height: 1.5;
            font-weight: 300;
        }
        .code {
            background-color: #f5f0ed;
            border-radius: 0;
            padding: 16px;
            font-family: 'Roboto', sans-serif;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #4a4a4a;
            font-weight: 300;
        }
        .map {
            border-radius: 0;
            overflow: hidden;
            margin-bottom: 16px;
        }
        .contact {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }
        .contact-icon {
            margin-right: 8px;
            color: #4a4a4a;
        }
        .footer {
            text-align: center;
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid #e0e0e0;
        }
        a {
            color: #4a4a4a;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 'About' Section
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown(
        """
        <p style="text-align: center; font-size: 24px;" class="text">
            🔬 STOUT was developed by <a href="https://www.linkedin.com/in/kohulanrajan/" target="_blank">Dr. Kohulan Rajan</a> under the supervision of
            <a href="https://www.w-hs.de/service/informationen-zur-person/person/zielesny/" target="_blank">Prof. Achim Zielesny</a> and
            <a href="https://www.linkedin.com/in/steinbeck/" target="_blank">Prof. Christoph Steinbeck</a>.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Citation Section
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1 class="header">How to cite us?</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="code">Rajan, K., Zielesny, A. & Steinbeck, C. STOUT: SMILES to IUPAC names using neural machine translation. J Cheminform 13, 34 (2021). https://doi.org/10.1186/s13321-021-00512-4</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Contact Section
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h2 class="header">Contact Us</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        iframe_src = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2503.2949726059553!2d11.581905350629135!3d50.93352470346138!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a6a898c3634fbb%3A0xdf22378d9f537b71!2sLessingstra%C3%9Fe%208%2C%2007743%20Jena%2C%20Germany!5e0!3m2!1sen!2s!4v1681045800175!5m2!1sen!2s"
        st.markdown(
            f'<div class="map"><iframe src="{iframe_src}" width="100%" height="300" frameborder="0" style="border:0;" allowfullscreen></iframe></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <p class="subheader"><b>Address:</b></p>
            <p class="text">Institute for Inorganic and Analytical Chemistry, Friedrich Schiller University, Lessingstraße 8, Jena 07743, Germany</p>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <h3 class="subheader"><b>Authors:</b></h3>
            <div class="contact">
                <h4 class="subheader" style="margin: 0;">- Prof. Dr. Christoph Steinbeck:</h4>
                <span class="contact-icon">📧</span>
                <a href="mailto:christoph.steinbeck@uni-jena.de" class="text">christoph.steinbeck@uni-jena.de</a>
            </div>
            <div class="contact">
                <h4 class="subheader" style="margin: 0;">- Prof. Dr. Achim Zielesny:</h4>
                <span class="contact-icon">📧</span>
                <a href="mailto:achim.zielesny@w-hs.de" class="text">achim.zielesny@w-hs.de</a>
            </div>
            <div class="contact">
                <h4 class="subheader" style="margin: 0;">- Dr. Kohulan Rajan:</h4>
                <span class="contact-icon">📧</span>
                <a href="mailto:kohulan.rajan@uni-jena.de" class="text">kohulan.rajan@uni-jena.de</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Acknowledgement Section
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
            "<p style='text-align: center;'>We greatly acknowledge OpenEye for granting us an academic license to their Lexichem software, without which this work would not have been possible.</p>",
            unsafe_allow_html=True,
        )
