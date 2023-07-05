import re
from django.http import HttpResponse
from django.shortcuts import render
from pytube import YouTube

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '', filename)

def download_youtube_video(request):
    if request.method == 'POST':
        download_type = int(request.POST.get('download_type'))
        link = request.POST.get('link')

        try:
            yt = YouTube(link)
            print('Downloading.... Please wait....')
            print(yt.title)

            if download_type == 1:
                print('Downloading mp3')
                # Download audio as MP3
                audio_stream = yt.streams.filter(only_audio=True).first()
                file_extension = 'mp3'

            elif download_type == 2:
                print('Downloading mp4') 
                # Download video
                video_stream = yt.streams.get_highest_resolution()
                file_extension = 'mp4'

            else:
                print("Invalid input")
                return HttpResponse("Invalid input")

            response = HttpResponse(content_type='application/octet-stream')
            sanitized_title = sanitize_filename(yt.title)
            response['Content-Disposition'] = f'attachment; filename="{sanitized_title}.{file_extension}"'
            yt.streams.first().stream_to_buffer(response)

            print("Download completed successfully!")
            return response

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("An error occurred")
            return HttpResponse("An error occurred")

    return render(request, 'download/index.html')
