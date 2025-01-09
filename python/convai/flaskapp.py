from flask import Flask, request, jsonify
import os
import sys
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

app = Flask(__name__)

# Load your environment variables
AGENT_ID = os.getenv('AGENT_ID')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
SKYVERN_API_KEY = os.getenv('SKYVERN_API_KEY')  # Assuming Skyvern also uses an API key

# Initialize ElevenLabs client
if not AGENT_ID or not ELEVENLABS_API_KEY:
    sys.stderr.write("Check your ElevenLabs environment variables.\n")
    sys.exit(1)

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

@app.route('/start-conversation', methods=['POST'])
def start_conversation():
    conversation = Conversation(
        elevenlabs_client,
        AGENT_ID,
        requires_auth=bool(ELEVENLABS_API_KEY),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda response: print(f"Agent: {response}"),
        callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
        callback_user_transcript=lambda transcript: print(f"User: {transcript}")
    )
    conversation.start_session()
    conversation_id = conversation.wait_for_session_end()
    return jsonify({"conversation_id": conversation_id})

# Example endpoint for integrating with Skyvern API
@app.route('/skyvern-action', methods=['POST'])
def skyvern_action():
    data = request.json
    # Implement your Skyvern API interaction here
    response = {"status": "Action completed"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
