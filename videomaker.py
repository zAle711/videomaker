import os
import subprocess
import cv2
from PIL import Image
from setup import DOWNLOAD_FOLDER, TEMP_FOLDER, TEST_FOLDER


class VideoMaker:

    def __init__(self, video_name = "test.mp4") -> None:
        self.video_name = video_name
        self.width = 1280
        self.height = 720
        self.images = [img for img in os.listdir("download")]
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.resized_images = self.resize_images()

    def print_images(self):
        for img in self.images:
            print(img)
    
    def resize_images(self):
        images_path = []
        for image in self.images:
            img = Image.open(DOWNLOAD_FOLDER.joinpath(image), "r")
            img_w, img_h = img.size
            black_background = Image.new("RGB", (self.width, self.height), (0,0,0))
            offset = ( (self.width - img_w) // 2, (self.height - img_h) //2 )
            black_background.paste(img, offset)
            path = TEMP_FOLDER.joinpath(image[:-3]+"jpg")
            images_path.append(path)
            black_background.save(path)
        return images_path
    
    def add_text(self, resized_image):
        
        pass    
    
    def add_audio(self):
        subprocess.call(r"ffmpeg -i test\test.mp4 -i test\audio.wav  -vcodec copy -acodec copy -c:a aac output\test.mp4 ")
        
    def create_video(self):
        path = str(TEST_FOLDER.joinpath(self.video_name))
        video = cv2.VideoWriter(path, self.fourcc, 60, (self.width, self.height))
        for image in self.resized_images:
            #print(DOWNLOAD_FOLDER.joinpath(image))
            for i in range(0,60):
                video.write(cv2.imread(os.path.join("download", image)))

        cv2.destroyAllWindows()
        video.release()
        self.add_audio()
if __name__ == "__main__":
    VideoMaker().create_video()
