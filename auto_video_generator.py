from dotenv import load_dotenv
import pandas as pd

from scrapers import SpodeliScraper
from subtitles_generator import SubtitlesGenerator
from text_to_speech import text_to_speech_bulgarian_eleven_labs
from video_generator import VideoGenerator
import re


class AutoVideoGenerator:
    def __init__(self, background_video_path='background_videos/minecraft_jump_map.webm') -> None:
        self.subttitles_generator = SubtitlesGenerator()
        self.scraper = SpodeliScraper()

        self.video_generator = VideoGenerator(background_video_path)

    def create_valid_images_and_audio_from_url(self, url):
        title, paragraphs = self.scraper.get_story_paragraphs(url)
        sentances = [sentance+'.' for sentance in re.split(
            r'\.\.\.|\.|\?|\!|\;', ' '.join(paragraphs)) if not sentance == '']

        resulit_paragraphs = [sentance.replace(
            '&quot', '') for sentance in sentances]

        res = [title + '! ' + resulit_paragraphs[0]]
        # remove short sentance that are result from splitting
        for sentance in resulit_paragraphs[1:]:
            if len(sentance) < 8:
                res[-1] = res[-1]+sentance
            else:
                res.append(sentance)
        resulit_paragraphs = res

        for i, paragraph in enumerate(resulit_paragraphs):
            self.subttitles_generator.create_image_with_text(
                paragraph, output_path=f"images/paragraphs_output_image{i}.png")
            text_to_speech_bulgarian_eleven_labs(
                paragraph, output_file=f"audios/audio{i}.mp3")
        return len(resulit_paragraphs)

    def create_video_shitpost(self, url, title):
        print('createing images and audio')

        files_length = self.create_valid_images_and_audio_from_url(url)
        audio_files = [f'audios/audio{i}.mp3' for i in range(files_length)]
        image_files = [
            f"images/paragraphs_output_image{i}.png" for i in range(files_length)]
        output_file = f'results/{title}_video.mp4'

        print('creating video')
        self.video_generator.combine_audio_images_video(
            audio_files, image_files)
        self.video_generator.add_audio_to_video()
        self.video_generator.add_gifs([
            f'popups/brainrot{i}.gif' for i in range(53)])
        self.video_generator.save_video(output_file)
        self.video_generator.reset_video()

    def scrape_stories(self, list_urls, output_file='urls.csv'):
        return self.scraper.extract_post_info(list_urls, output_file)

    def generate_video_shitpost(self):
        df = pd.read_csv('urls.csv', index_col=0)
        title, url, length = list(df[(df['length'] < 1400) & (df['length'] > 700) & (
            df['used'] == False)].sample()[['tile', 'URL', 'length']].values[0])
        title = title.replace('!', '').replace(
            '?', '').replace('"', '').replace("'", '').replace('/', '')
        self.create_video_shitpost(url, title)
        print(title, url)
        df.loc[df['URL'] == url, ['used']] = True
        df.to_csv('urls.csv')

    def create_video_cats(self, url, title):
        print('createing images and audio')

        files_length = self.create_valid_images_and_audio_from_url(url)

        audio_files = [f'audios/audio{i}.mp3' for i in range(files_length)]
        image_files = [
            f"images/paragraphs_output_image{i}.png" for i in range(files_length)]
        output_file = f'results/{title}_video.mp4'

        print('creating video')
        self.video_generator.combine_audio_images_video(
            audio_files, image_files)
        self.video_generator.add_gifs([
            f'popups/cat{i}.gif' for i in range(31)])
        self.video_generator.save_video(output_file)
        self.video_generator.reset_video()

    def generate_video_cats(self):
        df = pd.read_csv('urls.csv', index_col=0)
        title, url, length = list(df[(df['length'] < 1400) & (df['length'] > 700) & (
            df['used'] == False)].sample()[['tile', 'URL', 'length']].values[0])
        title = title.replace('!', '').replace(
            '?', '').replace('"', '').replace("'", '').replace('/', '')
        self.create_video_cats(url, title)
        print(title, url)
        df.loc[df['URL'] == url, ['used']] = True
        df.to_csv('urls.csv')


load_dotenv()

auto_generator = AutoVideoGenerator()

auto_generator.generate_video_cats()
