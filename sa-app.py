import streamlit as st

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
except ModuleNotFoundError as e:
    st.error(f"Required packages are not installed: {e}")
    st.stop()

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# App title
st.title("Sentiment Analysis App")

# Instructions
st.write("Enter text in the box below and click 'Analyze' to get the sentiment score.")

# Text input from the user
user_input = st.text_area("Enter text to analyze sentiment:")

# Function to perform sentiment analysis
def analyze_sentiment(text):
    tokens = tokenizer.encode(text, return_tensors='pt')
    result = model(tokens)
    sentiment = int(torch.argmax(result.logits)) + 1
    return sentiment

# Analyze the sentiment of the user input when the button is pressed
if st.button("Analyze"):
    if user_input.strip():
        sentiment = analyze_sentiment(user_input)
        sentiment_mapping = {
            1: ("1 😡 Worst Review", "red"),
            2: ("2 😖 Bad Review", "orange"),
            3: ("3 🙂 Moderate Review", "blue"),
            4: ("4 😁 Good Review", "lightgreen"),
            5: ("5 😍 Excellent Review", "darkgreen")
        }
        sentiment_text, sentiment_color = sentiment_mapping[sentiment]
        st.subheader("Sentiment Result:")
        st.markdown(
            f"""
            <div style="
                border: 2px solid {sentiment_color}; 
                padding: 10px; 
                border-radius: 5px; 
                text-align: center;
            ">
                <h2 style="color: {sentiment_color};"><strong>{sentiment_text}</strong></h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.write("Please enter some text to analyze.")

# Hide the result section initially
else:
    st.write("")
