import os
import subprocess
import cv2
from PIL import Image, ImageDraw, ImageFont
from setup import DOWNLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER, TEST_FOLDER
from pathlib import Path
from util import replaceText
import re


class VideoMaker:

    def __init__(self, video_name = "test.mp4") -> None:
        self.video_name = video_name
        self.width = 1280
        self.height = 720
        self.images = [img for img in os.listdir("download")]
        self.font_path = "arial.ttf"
        self.font_size = 75
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.resized_images = self.resize_images()

    def print_images(self):
        for img in self.images:
            print(img)
    
    def resize_images(self):
        images_path = []
        #loop throught downloaded images, place them in the middle of a black image and add text to it.
        for image in self.images:
            img = Image.open(DOWNLOAD_FOLDER.joinpath(image), "r")
            img_w, img_h = img.size
            black_background = Image.new("RGB", (self.width, self.height), (0,0,0))
            offset = ( (self.width - img_w) // 2, (self.height - img_h) //2 )
            black_background.paste(img, offset)
            self.add_text(black_background, img.filename)
            path = TEMP_FOLDER.joinpath(image[:-3]+"jpg")
            images_path.append(path)
            black_background.save(path)
        return images_path
    
    #add text to image
    def add_text(self, resized_image, file_name):
        #get text to write from file name
        text = Path(file_name[:-4]).name.strip().split("-")[1]
        #remove special characters
        text = replaceText(text)
        #create font and find offset to draw text on image
        font = ImageFont.truetype(self.font_path, self.font_size)
        offset = ((self.width - font.getsize(text)[0])/2, self.height - 100)
        stroke_color = (0,0,0)
        image = ImageDraw.Draw(resized_image)
        image.text(offset, text, font=font, stroke_width=4, stroke_fill=stroke_color) 
    
    def add_audio(self):
        subprocess.call(r"ffmpeg -i output\test.mp4 -i test\audio.wav  -vcodec copy -acodec copy -c:a aac output\test_with_audio.mp4 ")

    def getImageName(self, line:str):
        line = line.strip()
        line += ".jpg"
        line = re.sub("\?", "$", line)
        return line
       
    def create_video(self):
        path = str(OUTPUT_FOLDER.joinpath(self.video_name))
        video = cv2.VideoWriter(path, self.fourcc, 60, (self.width, self.height))
        with open("text.txt", "r") as file:
            for line in file.readlines():
                time = line.split("-")[0]
                image = self.getImageName(line)
                frames_to_write = int(float(time)*60)
                print(f"Writing image: {image} for {frames_to_write} frames")
                for i in range(0,frames_to_write):
                    video.write(cv2.imread(os.path.join("temp", image)))

        cv2.destroyAllWindows()
        video.release()
        self.add_audio()

if __name__ == "__main__":
    VideoMaker().create_video()