import os
from dotenv import load_dotenv
import tempfile
import openai
import sounddevice as sd
import soundfile as sf
from elevenlabs import generate, stream

load_dotenv()

# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
            
def get_openai_response(message):
    try:
        # Call the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another engine you prefer
            prompt=message,
            max_tokens=150  # adjust as needed
        )
        # Extracting the text from the response
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Set recording parameters
duration = 5  # duration of each recording in seconds
fs = 44100  # sample rate
channels = 1  # number of channels


def record_audio(duration, fs, channels):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    print("Finished recording.")
    return recording


def transcribe_audio(recording, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        sf.write(temp_audio.name, recording, fs)
        temp_audio.close()
        with open(temp_audio.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        os.remove(temp_audio.name)
    return transcript["text"].strip()


if __name__ == "__main__":
    recorded_audio = record_audio(duration, fs, channels)
    message = transcribe_audio(recorded_audio, fs)
    print(f"You: {message}")
    response_text = get_openai_response(message)
    audio = generate(
    text=response_text,
    api_key=os.getenv("ELEVENLABS_API_KEY"),
    voice="Bella",
    model="eleven_monolingual_v1",
    stream=True,
    latency=4
    )
    stream(audio)