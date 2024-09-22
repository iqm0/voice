from flask import (
    Flask,
    send_file,
    render_template,
    request,
    url_for
)
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/')
@app.route('/call')
def home():
    return render_template('index.html')

@app.route("/call/welcome", methods=['GET', 'POST'])
def welcome():
    response = VoiceResponse()
    response.play('https://iqm0.github.io/audio.mp3')
    print(response)
    
if __name__ == "__main__":
    app.run(debug=True)