import static_ffmpeg
static_ffmpeg.add_paths()

from flask import Flask, Response, request
from gtts import gTTS
from pydub import AudioSegment
import io, random

app = Flask(__name__)

PHRASES = [
    "Привет! Система работает нормально.",
    "Робот приветствует тебя!",
    "Проверь оборудование в лаборатории.",
    "Хорошего тебе дня, Пит!",
    "Все системы в норме.",
]

@app.route('/')
def index():
    return "ESP32 TTS Server работает!"

@app.route('/pcm')
def get_pcm():
    text = request.args.get('text', random.choice(PHRASES))
    print(f"[TTS] Говорю: {text}")
    tts = gTTS(text=text, lang='ru')
    mp3_buf = io.BytesIO()
    tts.write_to_fp(mp3_buf)
    mp3_buf.seek(0)
    audio = AudioSegment.from_mp3(mp3_buf)
    audio = audio.set_frame_rate(22050).set_sample_width(2).set_channels(1)
    return Response(audio.raw_data, mimetype='application/octet-stream')

@app.route('/phrase')
def get_phrase():
    return random.choice(PHRASES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
