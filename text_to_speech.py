import requests
import os


def text_to_speech_bulgarian_eleven_labs(text, voice_id="cgSgspJ2msm6clMCkdW9", output_file="audios/output.mp3"):
    # API endpoint
    url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    # Headers for the request
    headers = {
        "xi-api-key": os.environ.get("ELEVEN_LABS_API_KEY"),
        "Content-Type": "application/json"
    }

    # Data for the request
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75
        }
    }

    # Send the request to Eleven Labs API
    response = requests.post(url.format(
        voice_id=voice_id), json=data, headers=headers)

    # Save the audio content to a file
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {output_file}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
