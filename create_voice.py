import os
from dotenv import load_dotenv
import openai
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save

load_dotenv()

# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
            
"""
Calls the OpenAI chat completions API to get a response from the AI assistant model.

Returns the text response from the AI assistant.
"""
def get_openai_response():
    try:
        completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "You are Igor Moreira's personal assistant and schedule manager. What should I say when calling a restaurant to cancel a reservation at 2 PM for Igor Moreira, for 4 people? Ask about rescheduling for the next Saturday at 1 PM for 4 people, too. If you can confirm that you can reschedule, or if you have a message to pass to Igor, just press the star button once you are ready to speak, or the hash button to repeat this message. No preamble and not too chatty, try to sound natural as a human and not too robotic",
          },
        ],
        )
        # Call the OpenAI API
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

if __name__ == "__main__":
    response_text = get_openai_response()
    audio = client.generate(
    text=response_text,
    voice="Rachel",
    model="eleven_monolingual_v1",
    )
    save(audio, 'audio.mp3')