from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/signup', methods=['POST'])
def signup():
    print("🚀 /signup called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        
        tier = data.get('tier', 'free')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'no-email')
        timestamp = datetime.utcnow().isoformat()

        # Insert into Supabase table
        response = supabase.table("subscribers").insert({
            "name": name,
            "email": email,
            "tier": tier,
            "status": "active"
        }).execute()

        print(f"✅ SUBSCRIBER SAVED IN SUPABASE → {name} | {email} | Tier: {tier}")

        return jsonify({"status": "success", "message": "Subscriber added"}), 200

    except Exception as e:
        print(f"❌ Signup error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Shadow Realm Backend is running with Supabase ✅"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
