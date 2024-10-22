import streamlit as st
import pandas as pd
from collections import Counter # automatically creates a frequency distribution of the elements
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import re #regex :( get rid of any non words


# Get data
datix_df = pd.read_csv("../data/1924_Total.csv")

# get stopwords
nltk.download('stopwords')

default_stop_words = set(stopwords.words('english'))

# create function to clean the lessons learned
def preprocess_text(text, stop_words):
    # Remove special characters, tokenize, and remove stopwords
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters, yeah regex!
    tokens = text.lower().split()  # Convert to lowercase and split into tokens
    filtered_tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    return filtered_tokens

# Preprocess the lessons learned column with default stopwords
datix_df['Lessons Learned Processed'] = datix_df['Lessons Learned'].fillna('').apply(lambda x: preprocess_text(x, default_stop_words))

# Concatenate lessons learned for each result category
result_grouped_lessons = datix_df.groupby('Result')['Lessons Learned Processed'].apply(lambda x: ' '.join([' '.join(lst) for lst in x]))

# Create a list for the tabs, so it the tabs can be created dymanically!
tab_names = list(result_grouped_lessons.index)

# Orginal wordcloud to the effect with out removing the addional stopwords, create a for loop to iterate through
tabs = st.tabs(tab_names)
for i, result in enumerate(tab_names):
    with tabs[i]:
        st.subheader(f'Most Common Words for Result: {result}')
        
        # Get freq using the counter
        word_counts = Counter(result_grouped_lessons[result].split())
        
        # Display word count?
        word_count = sum(word_counts.values())
        st.write(f"Total number of words after stopword removal: {word_count}")
        
        # word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
        
        # Plot word cloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Common Words in "Lessons Learned" for {result}', fontsize=16)
        st.pyplot(plt)
        
        # Add session state so users can download the what they can see and it doens't re-run the code
        st.session_state[f'wordcloud_{result}'] = wordcloud

# Add user input to get adddional stopwords for example patient?
st.markdown("## Add Custom Stopwords")
additional_stopwords = st.text_area("Enter additional stopwords (please separate words by commas):", "")

# Process additional stopwords
if additional_stopwords:
    user_stop_words = set(map(str.strip, additional_stopwords.split(',')))
else:
    user_stop_words = set()

# Combine default stopwords and user input stopwords
combined_stop_words = default_stop_words.union(user_stop_words)

# "Execute" button to regenerate word clouds with updated stopwords
if st.button('Re-run'):
    # Reprocess the "Lessons Learned" column with updated stopwords - copy code above etc.
    datix_df['Lessons Learned Processed'] = datix_df['Lessons Learned'].fillna('').apply(lambda x: preprocess_text(x, combined_stop_words))

    # Concatenate lessons learned for each result category with the new stopwords
    result_grouped_lessons = datix_df.groupby('Result')['Lessons Learned Processed'].apply(lambda x: ' '.join([' '.join(lst) for lst in x]))

    # Regenerate word clouds adding in additonal stopwords etc.
    for i, result in enumerate(tab_names):
        with tabs[i]:
            st.subheader(f'Most Common Words for Result (with Custom Stopwords): {result}')
            
            word_counts = Counter(result_grouped_lessons[result].split())
            
            word_count = sum(word_counts.values())
            st.write(f"Total number of words after stopword removal: {word_count}")
            
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Common Words in "Lessons Learned" for {result}', fontsize=16)
            st.pyplot(plt)
            
            st.session_state[f'wordcloud_{result}'] = wordcloud