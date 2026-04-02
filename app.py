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
        return jsonify({"reply": f"Error: {str(e)}"}), 500
