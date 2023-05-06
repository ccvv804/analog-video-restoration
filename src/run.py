from real_world_test_no_video import main
import subprocess
import os
from argparse import ArgumentParser
from pathlib import Path

def clean(filepath):
    if os.path.exists(filepath):
        for file in os.scandir(filepath):
            os.remove(file.path)

def mainrun(args):
    clean("tempin")
    clean("results/video_swin_unet/tempin/") 
    results_path = Path("./results/video_swin_unet/tempin/")
    results_path.mkdir(parents=True, exist_ok=True)
    if args.patch_size % 64 != 0 or args.patch_size < 512 :   
        print("patch size must be a multiple of 64 greater than or equal to 512")
    elif os.path.isfile(args.fileinput):
        readfps=os.popen("ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate "+args.fileinput).read()[:-1]
        subprocess.call('ffmpeg -i '+args.fileinput+' -r '+readfps+' -vf "scale='+str(args.patch_size)+':480:flags=bicubic,pad='+str(args.patch_size)+':'+str(args.patch_size)+',setsar=1/1" -qscale:v 2 tempin/%00d.jpg')
        main(args)
        if args.patch_size <= 640:
            subprocess.call('ffmpeg -y -r '+readfps+' -i ./results/video_swin_unet/tempin/%00d.jpg -i '+args.fileinput+' -map 0:v:0 -map 1:a:0 -c:a aac -b:a 160k -c:v h264_nvenc -vf "yadif=1:-1:0,crop='+str(args.patch_size)+':480:0:0,scale=640:480:flags=bicubic,setsar=1/1" -profile:v main -preset p7 -tune:v hq -cq 23 -r '+readfps+' -pix_fmt yuv420p '+ args.fileinput + '-out.mp4')
        elif args.patch_size > 640: 
            subprocess.call('ffmpeg -y -r '+readfps+' -i ./results/video_swin_unet/tempin/%00d.jpg -i '+args.fileinput+' -map 0:v:0 -map 1:a:0 -c:a aac -b:a 160k -c:v h264_nvenc -vf "yadif=1:-1:0,crop='+str(args.patch_size)+':480:0:0,scale=720:480:flags=bicubic,setsar=8/9" -profile:v main -preset p7 -tune:v hq -cq 23 -r '+readfps+' -pix_fmt yuv420p '+ args.fileinput + '-out.mp4')
    elif args.fileinput == "09kane.avi":
        print("No input specified!")
    else :
        print("File not found!")
    clean("tempin")
    clean("results/video_swin_unet/tempin/")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--experiment-name", type=str, default="video_swin_unet")
    parser.add_argument("--data-base-path", type=str, default=".\\tempin")
    parser.add_argument("--results-path", type=str, default="results")
    parser.add_argument("-p", "--patch-size", type=int, default=512)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("-i", "--input", dest="fileinput", action="store", default="09kane.avi")
    args = parser.parse_args()
    mainrun(args)
