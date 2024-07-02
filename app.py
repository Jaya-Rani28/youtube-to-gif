from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['GIF_FOLDER'] = 'static/gifs'

if not os.path.exists(app.config['GIF_FOLDER']):
    os.makedirs(app.config['GIF_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename='video.mp4')

    video = VideoFileClip('video.mp4')
    gif_path = os.path.join(app.config['GIF_FOLDER'], 'output.gif')
    video.subclip(0, 5).write_gif(gif_path)  # Convert first 5 seconds to GIF

    return send_from_directory(app.config['GIF_FOLDER'], 'output.gif', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
