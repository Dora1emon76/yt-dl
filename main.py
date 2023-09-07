from flask import Flask, request, send_from_directory
from pytube import YouTube
import pymongo
from gridfs import GridFS

app = Flask(__name__)

# Initialize MongoDB and GridFS
client = pymongo.MongoClient('mongodb+srv://abhisharma71599:dora1emon@cluster0.mzpomjy.mongodb.net/?retryWrites=true&w=majority')  # Replace with your MongoDB URI
db = client['video_db']
fs = GridFS(db)

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
        
        # Download the video
        video_filename = "video.mp4"
        video_stream.download(filename=video_filename)
        
        # Save the video to MongoDB GridFS
        with open(video_filename, 'rb') as video_file:
            fs.put(video_file, filename=yt.video_id)
        
        return f"The video with ID {yt.video_id} is saved in MongoDB."

@app.route('/files/<video_id>')
def download_file(video_id):
    # Retrieve the video from MongoDB GridFS
    video = fs.find_one({"filename": video_id})
    if video:
        return video.read(), 200, {"Content-Type": "video/mp4"}
    else:
        return "Video not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

  
  
  
  
