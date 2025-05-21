import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import re
import random
from moviepy.editor import ImageSequenceClip, AudioFileClip

class VideoGenerator:
    def __init__(self, image_wq, image_q):
        self.Image_without_quote : str = image_wq
        self.Image_Quoted : str = image_q

    def get_images_from_image(self, img_path:str, dur:int):
        img = Image.open(img_path)
        frames = dur * 30
        for i in range(frames):
            crop_box = (100+i, 100, 1180+i, 2020)
            cropped_img = img.crop(crop_box)
            cropped_img.save(f'{self.Image_without_quote}/reel_img_{i}.jpg')

    def get_quotes(self):
        file_path = "./TempFiles/quotes/quotes.csv"
        data_f = pd.read_csv(file_path)
        data_f.dropna()
        lis = []
        for author, quote in zip(data_f['Author'], data_f['Quote']):
            lis.append({'a':author, 'q': quote})
        return lis

    def write_on_images(self):
        quotes = self.get_quotes()
        quote = quotes[random.randint(0, len(quotes)-1)]
        author = quote['a']
        line = quote['q'].split(" ")
        # text = f'"{line}" - {author}'
        text1 = ' '.join(line[:8])
        text2 = " ".join(line[8:])
        position1 = (100,800)
        position2 = (100,900)
        font = ImageFont.truetype('arial.ttf', size=32)
        images = self.sort_images_inorder(self.Image_without_quote)


        for i in images:
            image = Image.open(f'{self.Image_without_quote}/{i}')
            draw = ImageDraw.Draw(image)

            draw.text(position1, f'"{text1}', fill='white', font=font)
            draw.text(position2, f'{text2}"', fill='white', font=font)
            draw.text((200,1000), f'- {author}', fill='white', font=font)
            image_save_path = os.path.join(self.Image_Quoted, i)
            image.save(image_save_path)

        self.remove_all_temp_images(self.Image_without_quote)

    def create_video_from_images(self, name):
        images = self.sort_images_inorder(self.Image_Quoted)
        images = list(map(lambda x : os.path.join(self.Image_Quoted, x), images))
        video_clip = ImageSequenceClip(images, fps=30)
        audio_clip = AudioFileClip(self.get_BackGround_music())
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(f'./TempFiles/OutputVideos/{name}.mp4', codec='libx264', audio_codec='aac')
        self.remove_all_temp_images(self.Image_Quoted)




    def get_BackGround_music(self):
        music_path = './TempFiles/music'
        lis = os.listdir(music_path)
        return os.path.join(music_path, lis[random.randint(0, len(lis)-1)])



    def sort_images_inorder(self, foldername):
        lis = os.listdir(foldername)
        def extract_number(fileName):
            match_re = re.search(r'(\d+)(?=\.\w+$)', fileName)
            return int(match_re.group(1)) if match_re else -1
        lis = sorted(lis, key=extract_number)
        return lis


    def remove_all_temp_images(self, folder_path):
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)

            if os.path.isfile(filepath):
                os.remove(filepath)

    def video_generator(self, num: int, dur: int):
        bg_img = './TempFiles/Images'
        lis = os.listdir(bg_img)
        lis = list(map(lambda x: os.path.join('./TempFiles/Images', x), lis))

        for i in range(num):
            img = lis[random.randint(0, len(lis)-1)]
            self.get_images_from_image(img, dur)
            self.write_on_images()
            self.create_video_from_images(i)
            print(f'{i+1} th - video ')

