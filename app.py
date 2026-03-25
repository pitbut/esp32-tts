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
    "Сегодня хороший день для работы.",
    "Напоминание: проверь все датчики.",
]

@app.route('/')
def index():
    return "ESP32 TTS Server работает! Используй /pcm или /pcm?text=Твой текст"

@app.route('/pcm')
def get_pcm():
    text = request.args.get('text', random.choice(PHRASES))
    print(f"[TTS] Говорю: {text}")

    try:
        # Генерируем MP3 через gTTS
        tts = gTTS(text=text, lang='ru')
        mp3_buf = io.BytesIO()
        tts.write_to_fp(mp3_buf)
        mp3_buf.seek(0)

        # Конвертируем в сырой PCM: 44100 Гц, 16-bit, моно
        audio = AudioSegment.from_mp3(mp3_buf)
        audio = audio.set_frame_rate(44100).set_sample_width(2).set_channels(1)
        pcm_data = audio.raw_data

        print(f"[TTS] PCM размер: {len(pcm_data)} байт, длина: {len(audio)/1000:.1f} сек")
        return Response(pcm_data, mimetype='application/octet-stream',
                        headers={'X-Text': text, 'X-Duration': str(len(audio)/1000)})

    except Exception as e:
        print(f"[TTS] Ошибка: {e}")
        return Response(status=500)

@app.route('/phrase')
def get_phrase():
    """Просто текст фразы — для отладки"""
    return random.choice(PHRASES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
