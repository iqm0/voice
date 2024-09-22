import os
import requests  # Use requests to interact with a local server
from elevenlabs import generate, save

def create_prompt(action, user_name):
    if action == "cancel":
        return f"""
        You are {user_name}'s personal assistant and schedule manager. You will help in talking to the restaurant and cancelling a restaurant reservation at 2 PM for {user_name}, for 4 people at the Byron restaurant. No preamble and not too chatty, try to sound natural as a human and not too robotic. Just say what you would say to the restaurant on the phone to cancel.
        """
    elif action == "reschedule":
        return f"""
        You are {user_name}'s personal assistant and schedule manager. You will help in talking to the restaurant and rescheduling a reservation for 4 people. The current reservation is at 2 PM for {user_name}, at the Byron restaurant. Try to reschedule for the next Saturday at 1 PM for 4 people. No preamble and not too chatty, try to sound natural as a human and not too robotic. Just say what you would say to the restaurant on the phone to reschedule.
        """
    elif action == "special_adjustments":
        return f"""
        You are {user_name}'s personal assistant and schedule manager. You will help in talking to the restaurant and requesting special adjustments for a reservation for 4 people. Explain the adjustments needed and inquire if they can accommodate. No preamble and not too chatty, try to sound natural as a human and not too robotic. Just say what you would say to the restaurant on the phone to request special adjustments.
        """
    else:
        raise ValueError("Invalid action type provided")

def get_ollama_response(action, user_name):
    try:
        prompt = create_prompt(action, user_name)
        # Prepare the payload for the Ollama request
        payload = {
            "model": "orca-mini",  # Adjust this if your Ollama setup uses different model identifiers
            "prompt": prompt,
            "stream": False
        }
        # Send a post request to your Ollama server
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response_data = response.json()
        return response_data['response']
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    action = "cancel"  # Change this to "reschedule" or "special_adjustments" as needed
    user_name = "John Doe"  # Placeholder for the user's name
    response_text = get_ollama_response(action, user_name)
    print(response_text)
    audio = generate(
        text=response_text,
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        voice="Rachel",
        model="eleven_monolingual_v1",
    )
    save(audio, 'audio.mp3')

    # Assuming Ollama also handles text-to-speech, you'd replace the ElevenLabs code with something similar
    # Here's a placeholder example for how that might look; adjust based on your actual setup
    # audio_response = requests.post("http://localhost:11434/tts", json={"text": response_text, "voice": "Rachel"})
    # with open('audio.mp3', 'wb') as f:
    #     f.write(audio_response.content)