from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx.all import resize, loop
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
from moviepy.video.fx.resize import resize
import random
from PIL import Image
import numpy as np


class VideoGenerator:
    def __init__(self, background_video_file, gif_duration=3) -> None:

        self.background_video_file = background_video_file
        self.gif_duration = gif_duration
        self.video = VideoFileClip(background_video_file)

    def add_popup_at_the_start(self, video, img_path):
        image_clip = ImageClip(img_path).set_duration(5)

        # Set the image clip to the size of the video (optional)
        image_clip = image_clip.resize(
            newsize=(video.size[0] // 3, video.size[1] // 3))

        image_clip = image_clip.set_position("right", "center")

        # Concatenate the image clip with the original video
        return CompositeVideoClip([video, image_clip.set_start(0)])

    def overlay_gifs_on_video(self, video_clip, gif_paths, gif_duration=3):

        # List to hold the GIF clips (resized and adjusted for duration)
        gif_clips = []

        for gif_path in gif_paths:
            # Load GIF as an ImageSequenceClip and resize it (if necessary)
            gif_clip = VideoFileClip(gif_path)

            # Resize GIF if you want it to fit within the video size (optional)
            # gif_clip = resize(gif_clip, width=video_clip.w //
            #                  4, height=video_clip.h//4)
            gif_clip = resize(gif_clip, (500, 500))

            gif_clip = loop(gif_clip, duration=gif_duration)

            # Set GIF duration to 3 seconds
            gif_clip = gif_clip.set_duration(gif_duration)

            # Set position (optional) for the GIF in the video (center, top-right, etc.)
            gif_clip = gif_clip.set_position(('center', 'center'))

            gif_clips.append(gif_clip)

        # Concatenate GIF clips
        final_gif_clip = concatenate_videoclips(gif_clips, method="compose")

        # Set the duration of the final GIF sequence to match the video or GIFs total length
        total_duration = video_clip.duration

        # Overlay GIFs on top of the video
        final_video = CompositeVideoClip(
            [video_clip, final_gif_clip.set_position((270, 350))]).set_duration(total_duration)
        for gif in gif_clips:
            gif.close()

        return final_video

    def combine_audio_images_video(self, audio_files, image_files):
        # Define TikTok-like video resolution
        tiktok_width, tiktok_height = 1080, 1920

        # Load the video

        # Add black bars to the sides if necessary to match 1080x1920 resolution
        if self.video.w < tiktok_width:
            self.video = self.video.on_color(size=(tiktok_width, tiktok_height), color=(
                0, 0, 0), pos=('center', 'center'))

        # Ensure the number of audio files and images are the same
        if len(audio_files) != len(image_files):
            raise ValueError(
                "The number of audio files must match the number of images")

        video_clips = []
        current_time = 0
        to_close = []
        for audio_file, image_file in zip(audio_files, image_files):
            # Load the audio file and create an audio clip
            audio_clip = AudioFileClip(audio_file)

            # Load the image file and create an image clip
            pil_image = Image.open(image_file).convert("RGBA")
            pil_image.putalpha(185)  # Set transparency

            # Calculate the aspect ratio of the image
            aspect_ratio = pil_image.width / pil_image.height

            # Define the maximum allowed width and height for the image
            max_width = tiktok_width * 0.9  # Allow some padding around the image
            max_height = tiktok_height * 0.5  # Max height should be half the screen

            # Resize the image to fit within the max dimensions while preserving aspect ratio
            if pil_image.width > max_width or pil_image.height > max_height:
                if pil_image.width / max_width > pil_image.height / max_height:
                    target_width = int(max_width)
                    target_height = int(target_width / aspect_ratio)
                else:
                    target_height = int(max_height)
                    target_width = int(target_height * aspect_ratio)
            else:
                target_width, target_height = pil_image.width, pil_image.height

            resized_pil_image = pil_image.resize(
                (target_width, target_height), Image.LANCZOS)

            # Create the image clip
            image = ImageClip(np.array(resized_pil_image), transparent=True)
            image = image.set_duration(
                audio_clip.duration).set_position(("center", "top"))
            new_start = 0.75 * random.random() * self.video.duration
            clip = self.video.subclip(new_start)
            # Create a video clip with the image overlayed
            video_with_image = CompositeVideoClip(
                [clip.set_duration(audio_clip.duration), image])
            video_with_image = video_with_image.set_audio(audio_clip)

            # Append the video segment with audio and image
            video_clips.append(video_with_image.set_start(current_time))

            # Update the current time
            current_time += audio_clip.duration

            to_close.append(audio_clip)
            to_close.append(pil_image)

        # Concatenate all video clipss
        self.video = concatenate_videoclips(video_clips)

    def add_gifs(self, gif_paths):

        random.shuffle(gif_paths)
        self.video = self.overlay_gifs_on_video(
            self.video, gif_paths[:int(self.video.duration//3)])

    def reset_video(self):
        self.video.close()
        self.video = VideoFileClip(self.background_video_file)

    def save_video(self, output_file_path):
        self.video.write_videofile(
            output_file_path, codec='libx264', audio_codec='aac')

    def add_audio_to_video(self, audio_path='audios/sound1.mp3', moments=[3, 10, 15, 20,  30]):
        # Load video and audio files
        audio = AudioFileClip(audio_path)

        # Create a list of subclips where the audio should be added
        audio_clips = []
        for moment in moments:
            # Create a copy of the audio starting at the moment specified
            audio_start = audio.set_start(moment)
            audio_clips.append(audio_start)

        # Combine all audio clips with the video’s original audio
        combined_audio = CompositeAudioClip([self.video.audio] + audio_clips)

        # Set the combined audio to the video
        self.video = self.video.set_audio(combined_audio)
