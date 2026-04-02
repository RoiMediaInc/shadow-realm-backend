import re

@app.route('/voice', methods=['POST'])
def voice():
    data = request.json
    character = data.get('character', 'Damian')
    text = data.get('text', '')

    # NUCLEAR cleaning — this is the strongest version possible
    voice_text = re.sub(r'\*[\s\S]*?\*', '', text)        # removes every *action*
    voice_text = re.sub(r'[_*]+', '', voice_text)         # removes any leftover * or _
    voice_text = re.sub(r'\s+', ' ', voice_text).strip()  # cleans extra spaces

    # Extra safety — removes the word "asterisk" if it slips through
    voice_text = voice_text.replace('asterisk', '').replace('Asterisk', '')

    # Shorten for better latency
    if len(voice_text) > 160:
        voice_text = voice_text[:160] + "..."

    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_monolingual_v1",
                "text": voice_text,
                "voice_settings": {
                    "stability": 0.92,
                    "similarity_boost": 0.65
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
            }
        )
        response.raise_for_status()

        return Response(
            response.content,
            mimetype="audio/mpeg"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
