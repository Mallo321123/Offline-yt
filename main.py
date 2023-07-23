import yt_dlp, configparser, time, os

config = configparser.ConfigParser()

config.read('yt.conf')
count = len(config.options("urls"))

urls = []

for i in range(0, count):
    j = i + 1
    location = "url" + str(j)
    urls.insert(i, config['urls'][location])

options = {
    'format': 'bestvideo+bestaudio',
    'playlistend': config['generell']['count_history'],
    'paths': {
        'home': config['generell']['download_path'],
        'temp': config['generell']['tmp_path']
    }
}

ydl = yt_dlp.YoutubeDL(options)

def get_file_age():
    try:
        file_stats = os.stat(config['generell']['download_path'])
        modification_time = file_stats.st_mtime
        current_time = time.time()
        age_seconds = current_time - modification_time
        age_days = age_seconds / (60 * 60 * 24)
        
        return age_days
    except FileNotFoundError:
        return None

def delete_old_videos():
    for filename in os.listdir(config['generell']['download_path']):
        file_path = os.path.join(config['generell']['download_path'], filename)
        
        if filename.lower().endswith(('.mp4', '.webm')):
            age_in_days = get_file_age(file_path)

            if age_in_days is not None and age_in_days > config['generell']['history']:
                os.remove(file_path)
                print(f"Gelöscht: {filename}")
    
while True:
    for i in range(0, len(urls)):
        url = urls[i]
        ydl.download(url)
        
    delete_old_videos()
    
    time.sleep(config['generell']['intervall'])