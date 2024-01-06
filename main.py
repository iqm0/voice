import os
from dotenv import load_dotenv
import openai
from elevenlabs import generate, stream

load_dotenv()

# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
            
def get_openai_response(prompt_text):
    try:
        # Call the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another engine you prefer
            prompt=prompt_text,
            max_tokens=150  # adjust as needed
        )
        # Extracting the text from the response
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"



if __name__ == "__main__":
    prompt_text = "You are Igor Moreira's personal assistant and schedule manager. What should I say when calling a restaurant to cancel a reservation at 2 PM for Igor Moreira, for 4 people? Ask about rescheduling for the next Saturday at 1 PM for 4 people, too. If you can confirm that you can reschedule, or if you have a message to pass to Igor, just press the star button once you are ready to speak, or the hash button to repeat this message. No preamble and not too chatty, try to sound natural as a human and not too robotic"
    response_text = get_openai_response(prompt_text)
    audio = generate(
    text=response_text,
    api_key=os.getenv("ELEVENLABS_API_KEY"),
    voice="Bella",
    model="eleven_monolingual_v1",
    stream=True,
    latency=4
    )
    stream(audio)