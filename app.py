import streamlit as st
import pandas as pd
from theme_classifier import ThemeClassifier

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

def main():
    st.title("Theme Classification (Zero Shot Classifiers)")
    
    # Input fields
    theme_list = st.text_input("Themes (comma-separated)")
    subtitles_path = st.text_input("Subtitles or Script Path")
    save_path = st.text_input("Save Path")
    
    if st.button("Get Themes"):
        if theme_list and subtitles_path and save_path:
            with st.spinner("Processing..."):
                summed_df = get_themes(theme_list, subtitles_path, save_path)
                
                # Display the results
                st.subheader("Theme Scores")
                st.dataframe(summed_df)

                # Create a bar plot
                st.bar_chart(summed_df.set_index('Theme'))

        else:
            st.error("Please fill in all fields.")

if __name__ == '__main__':
    main()
