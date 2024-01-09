import openai
from midiutil import MIDIFile
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Expanded scales for different genres
scales = {
    'minor': [0, 2, 3, 5, 7, 8, 10],  
    'major': [0, 2, 4, 5, 7, 9, 11],
    'blues': [0, 3, 5, 6, 7, 10],
    'jazz': [0, 2, 4, 6, 7, 9, 11],
    'rock': [0, 2, 4, 5, 7, 9, 11],
    'classical': [0, 2, 4, 5, 7, 9, 11],
    'pop': [0, 2, 4, 5, 7, 9, 11],
    'ambient': [0, 2, 4, 5, 7, 9, 10],
    'electronic': [0, 2, 3, 5, 7, 8, 11],
    'folk': [0, 2, 4, 5, 7, 9, 10],
    # Add more genres and scales as needed
}

# Expanded start pitches
start_pitches = {
    'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68, 'Ab': 68,
    'A': 69, 'A#': 70, 'Bb': 70, 'B': 71,
    # Add more if needed
}

# Function for sentiment analysis
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    print(f"Sentiment Analysis Score: {sentiment_score}")
    return sentiment_score['compound']

# Function to interact with OpenAI API
def get_music_attributes_from_text(text, api_key):
    openai.api_key = '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'
    try:
        prompt = (
            "Analyze the following user's music description and provide detailed musical attributes including genre, key, and BPM: '{}' to the best of your abilities."
        ).format(text)

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100
        )
        api_response = response.choices[0].text.strip()
        print(f"OpenAI API Response: {api_response}")  # Print the response here
        return api_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def create_melody(scale_notes, sentiment, length=32):
    melody = []
    for _ in range(length):
        note = random.choice(scale_notes)
        duration_choices = [1, 0.5, 0.25, 0.75] if sentiment > 0 else [1, 0.5]
        duration = random.choice(duration_choices)
        dynamics = random.choice(range(70, 110)) if sentiment > 0 else random.choice(range(50, 90))
        melody.append((note, duration, dynamics))
    return melody

# Function to create MIDI file from attributes
def create_midi_from_attributes(attributes, sentiment, file_name="output.mid"):
    midi_file = MIDIFile(1)
    track = 0
    time = 0
    midi_file.addTempo(track, time, attributes['bpm'])

    genre = attributes.get('genre', 'major').lower()
    genre_scale = scales.get(genre, scales['major'])
    key = attributes.get('key', 'C').upper()
    start_pitch = start_pitches.get(key, 60)
    scale_notes = [start_pitch + interval for interval in genre_scale]

    melody = create_melody(scale_notes, sentiment)

    for note, duration, dynamics in melody:
        midi_file.addNote(track, 0, note, time, duration, dynamics)
        time += duration

    with open(file_name, "wb") as output_file:
        midi_file.writeFile(output_file)
    print(f"MIDI file {file_name} has been created")

# Main function
def main():
    api_key = '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'
    user_input = input("Enter your music description: ")
    sentiment = get_sentiment(user_input)

    attributes_text = get_music_attributes_from_text(user_input, api_key)
    if attributes_text:
        attributes_list = attributes_text.lower().split()
        attributes = {
            'genre': next((word for word in attributes_list if word in scales.keys()), 'major'),
            'bpm': int(next((attributes_list[i-1] for i, word in enumerate(attributes_list) if word == 'bpm'), 120)),
            'key': next((word.upper() for word in attributes_list if word.upper() in start_pitches), 'C'),
        }
        create_midi_from_attributes(attributes, sentiment)
    else:
        print("No response was received from the API.")

if __name__ == "__main__":
    main()

