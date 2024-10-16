import streamlit as st
import pandas as pd
from theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator

def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Filter out the 'dialogue' theme
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    # Sum the theme scores
    summed_df = output_df.sum().reset_index()
    summed_df.columns = ['Theme', 'Score']

    return summed_df

def get_character_network(subtitles_path, ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)

    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)

    return html

def main():
    st.set_page_config(layout="wide")  # Use wide layout for more space

    # Row 1: Theme Classification Section
    st.subheader("Theme Classification (Zero Shot Classifiers)")
    col1, col2 = st.columns([3, 2])  # Graph on the left, inputs on the right

    with col2:
        theme_list = st.text_input("Themes (comma-separated)", key="theme_list")
        subtitles_path_themes = st.text_input("Subtitles or Script Path", key="subtitles_path_themes")
        save_path = st.text_input("Save Path", key="save_path")

        if st.button("Get Themes", key="themes_button"):
            if theme_list and subtitles_path_themes and save_path:
                with st.spinner("Processing..."):
                    summed_df = get_themes(theme_list, subtitles_path_themes, save_path)
                    st.session_state.summed_df = summed_df  # Save to session state
                    st.session_state.theme_generated = True  # Track if themes were generated
                    st.success("Themes generated successfully!")
            else:
                st.error("Please fill in all fields.")

    with col1:
        if "summed_df" in st.session_state and st.session_state.theme_generated:
            st.subheader("Theme Scores")
            st.dataframe(st.session_state.summed_df)
            st.bar_chart(st.session_state.summed_df.set_index('Theme'))
        else:
            st.write("The theme graph will appear here after generation.")

    # Row 2: Character Network Section
    st.subheader("Character Network (NERs and Graphs)")
    col3, col4 = st.columns([3, 2])  # Graph on the left, inputs on the right

    with col4:
        subtitles_path_network = st.text_input("Subtitles or Script Path", key="subtitles_path_network")
        ner_path = st.text_input("NERs Save Path", key="ner_path")

        if st.button("Get Character Network", key="network_button"):
            if subtitles_path_network and ner_path:
                with st.spinner("Generating character network..."):
                    network_html = get_character_network(subtitles_path_network, ner_path)
                    st.session_state.network_html = network_html  # Save to session state
                    st.session_state.network_generated = True  # Track if network was generated
                    st.success("Character network generated!")
            else:
                st.error("Please provide both subtitles and NER paths.")

    with col3:
        if "network_html" in st.session_state and st.session_state.network_generated:
            st.components.v1.html(st.session_state.network_html, height=600, scrolling=True)
        else:
            st.write("The character network graph will appear here after generation.")

if __name__ == '__main__':
    main()
