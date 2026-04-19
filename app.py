import os
import asyncio
from flask import Flask, render_template, request, send_file, jsonify
import edge_tts
from datetime import datetime

app = Flask(__name__)

PRIVATE_OWNER = "Ali Ibrahim Ali Ibrahim"
PUBLIC_BRAND = "Ali Al-Faris AI Studio"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
async def generate():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'ar-EG-ShakirNeural')
        rate = data.get('rate', '+0%')
        pitch = data.get('pitch', '+0Hz')
        
        # نظام السكتات التنفسية التلقائي
        refined_text = text.replace(".", ". ").replace(",", ", ")
        
        output_path = "static/output.mp3"
        if not os.path.exists('static'): os.makedirs('static')
        
        communicate = edge_tts.Communicate(refined_text, voice, rate=rate, pitch=pitch)
        await communicate.save(output_path)
        
        return jsonify({"status": "success", "audio_url": "/static/output.mp3"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download')
def download():
    return send_file("static/output.mp3", as_attachment=True, 
                     download_name=f"Ali_AlFaris_HD_{datetime.now().strftime('%Y%m%d')}.mp3")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
