@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    character = data.get('character', 'Damian')
    message = data.get('message', '')
    history = data.get('history', [])

    # Force clean JSON output — this is the method that actually works
    SYSTEM_PROMPTS = {
        "Lenai": "You are Lenai Devereaux from Shadows of Seduction. ... (keep your existing description) "
                 "ALWAYS respond in this exact JSON format and nothing else: "
                 "{\"dialogue\": \"your spoken words here\"}. "
                 "Never use asterisks, *action*, markdown, or any formatting. Never add extra text outside the JSON.",

        "Elena": "You are Elena Voss. ... (keep your existing description) "
                 "ALWAYS respond in this exact JSON format and nothing else: "
                 "{\"dialogue\": \"your spoken words here\"}. "
                 "Never use asterisks, *action*, markdown, or any formatting. Never add extra text outside the JSON.",

        "Victor": "You are Victor Kane. ... (keep your existing description) "
                 "ALWAYS respond in this exact JSON format and nothing else: "
                 "{\"dialogue\": \"your spoken words here\"}. "
                 "Never use asterisks, *action*, markdown, or any formatting. Never add extra text outside the JSON.",

        "Damian": "You are Damian Fraser. ... (keep your existing description) "
                 "ALWAYS respond in this exact JSON format and nothing else: "
                 "{\"dialogue\": \"your spoken words here\"}. "
                 "Never use asterisks, *action*, markdown, or any formatting. Never add extra text outside the JSON."
    }

    system_prompt = SYSTEM_PROMPTS.get(character, SYSTEM_PROMPTS["Damian"])

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            temperature=0.85,
            messages=messages
        )
        raw_reply = response.content[0].text.strip()

        # Extract only the clean dialogue from JSON
        import json
        try:
            parsed = json.loads(raw_reply)
            clean_reply = parsed.get("dialogue", raw_reply)
        except:
            clean_reply = raw_reply

        return jsonify({"reply": clean_reply})
    except Exception as e:
        import re

@app.route('/voice', methods=['POST'])
def voice():
    data = request.json
    character = data.get('character', 'Damian')
    text = data.get('text', '')

    # Nuclear cleaning for asterisks
    voice_text = re.sub(r'\*[\s\S]*?\*', '', text)
    voice_text = re.sub(r'[_*]+', '', voice_text)
    voice_text = re.sub(r'\s+', ' ', voice_text).strip()
    voice_text = voice_text.replace('asterisk', '').replace('Asterisk', '')

    if len(voice_text) > 150:
        voice_text = voice_text[:150] + "..."

    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_monolingual_v1",
                "text": voice_text,
                "voice_settings": {"stability": 0.92, "similarity_boost": 0.65},
                "optimize_streaming_latency": 0
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
            }
        )
        response.raise_for_status()
        return Response(response.content, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        return jsonify({"reply": f"Error: {str(e)}"}), 500
