import argparse
from pathlib import Path
from pytube import YouTube


def get_args():
    parser = argparse.ArgumentParser(description='YouTube parser')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Output directory for downloading videos')
    parser.add_argument('--youtube_id', type=str, required=True,
                        help='YouTube id for video to be loaded')
    parser.add_argument('--label', type=str, required=True,
                        help='Action class label for video')
    return parser.parse_args()

def download_video(output_dir: str, youtube_id: str, label: str):

    output = Path(output_dir)
    if not output.exists():
        raise Exception('Output directory does not exist')
    
    link = f"https://www.youtube.com/watch?v={youtube_id}"
    
    try:
        yt = YouTube(link)
    except Exception as e:
        print("Connection Error")
        raise e

    video_streams = yt.streams.filter(file_extension='mp4')
    stream = video_streams.get_lowest_resolution()

    download_file = output / f"video{youtube_id}_{label.replace(' ', '_')}.mp4"
    if download_file.exists():
        raise Exception(f'Video {download_file} already downloaded')

    print(f'Video will be downloaded as: {download_file}')
    stream.download(download_file)
    

if __name__ == '__main__':
    args = get_args()

    try:
        download_video(args.output_dir, args.youtube_id, args.label)
        print('Video downloaded')
    except Exception as e:
        print(f'Error: {e}. Video could not be downloaded')
