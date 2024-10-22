import streamlit as st

pg = st.navigation([
    st.Page("home_page.py", title="Welcome!"),
    st.Page("df.py", title="Summary table of incidents"),
    st.Page("Visuals.py", title = "Graphical overview of incident data"),
    st.Page("datix_wordcloud_app.py", title = "Wordclouds"),
    st.Page("Common_Words.py", title="Common Words")
])

#st.logo("hsma_logo.png")

pg.run()
