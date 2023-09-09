from flask import Flask, request, send_from_directory, Response
from pytube import YouTube
import os
from flask_cors import CORS
 

app = Flask(__name__)
CORS(app)
# Define the folder path where you want to store downloaded files
DOWNLOAD_FOLDER = 'usdl'

# Create the download folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route('/', methods=['GET'])
def download_and_show_path():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        quality = request.form['quality']
    else:
        youtube_url = request.args.get('url', '')
        quality = request.args.get('quality', '')

    if youtube_url and quality:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(res=f"{quality}p", file_extension="mp4", progressive=True).first()
        
        video_filename = os.path.join(DOWNLOAD_FOLDER, f"{yt.video_id}.mp4")
        video_stream.download(filename=video_filename)
        
        
        return f"The video with ID {yt.video_id} is saved in the folder."

@app.route('/files/<video_id>')
def view_file(video_id):
    video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")
    if os.path.exists(video_path):
        return send_from_directory(DOWNLOAD_FOLDER, f"{video_id}.mp4")
    else:
        return "Video not found", 404

@app.route('/dl/<video_id>')
def download_video(video_id):
    video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")
    if os.path.exists(video_path):
        response = send_from_directory(DOWNLOAD_FOLDER, f"{video_id}.mp4")
        response.headers["Content-Disposition"] = f"attachment; filename={video_id}.mp4"
        os.remove(video_path)
        return response
    else:
        return "Video not found", 404
      

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
      
