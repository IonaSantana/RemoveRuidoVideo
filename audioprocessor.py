from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
from scipy.io.wavfile import write
import noisereduce as nr
import scipy.io.wavfile as wav
from pydub import AudioSegment

class AudioVideoProcessor:
    """
    Class for processing audio and video files by extracting audio from video,
    reducing noise, adjusting volume, and combining the processed audio with the video.

    Attributes:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the input audio file (optional, not used directly in this class).
        output_dir (str): Directory where output files will be saved.
        mp3_file (str): Path to the temporary MP3 file created from the video.
        wav_file (str): Path to the temporary WAV file created from the MP3 file.
        filtered_audio_wav_file (str): Path to the WAV file with reduced noise.
        filtered_audio_mp3_file (str): Path to the MP3 file with reduced noise.
        output_video_file (str): Path to the final output video file.
    """

    def __init__(self, video_path, audio_path, output_dir):
        """
        Initialize the AudioVideoProcessor with paths for video, audio (optional), and output directory.

        Args:
            video_path (str): Path to the input video file.
            audio_path (str): Path to the input audio file (optional, not used directly in this class).
            output_dir (str): Directory where output files will be saved.
        """
        self.video_path = video_path
        self.audio_path = audio_path
        self.output_dir = output_dir

        self.mp3_file = f"{output_dir}/audio.mp3"
        self.wav_file = f"{output_dir}/temp.wav"
        self.filtered_audio_wav_file = f"{output_dir}/arquivo_filtrado.wav"
        self.filtered_audio_mp3_file = f"{output_dir}/audio_filtrado.mp3"
        self.output_video_file = f"{output_dir}/video_final.mp4"

    def extract_audio_from_video(self):
        """
        Extract audio from the video file and save it as an MP3 file.
        """
        video_clip = VideoFileClip(self.video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(self.mp3_file)
        audio_clip.close()
        video_clip.close()

    def convert_mp3_to_wav(self):
        """
        Convert the extracted MP3 audio to WAV format.
        """
        audio = AudioSegment.from_mp3(self.mp3_file)
        audio.export(self.wav_file, format="wav")

    def reduce_noise_and_save(self):
        """
        Apply noise reduction to the WAV audio file and save the processed audio.
        """
        rate, data = wav.read(self.wav_file)
        
        if len(data.shape) == 2:
            data = np.mean(data, axis=1)

        reduced_noise = nr.reduce_noise(y=data, sr=rate)
        write(self.filtered_audio_wav_file, rate, reduced_noise.astype(np.int16))

        filtered_audio = AudioSegment.from_wav(self.filtered_audio_wav_file)
        filtered_audio.export(self.filtered_audio_mp3_file, format="mp3")

    def adjust_volume_and_combine(self):
        """
        Increase the volume of the processed audio, combine it with the original video,
        and save the final video.
        """
        processed_audio = AudioFileClip(self.filtered_audio_mp3_file)

        def increase_volume(audio_clip, factor):
            return audio_clip.volumex(factor)

        processed_audio = increase_volume(processed_audio, 1000)

        video_clip = VideoFileClip(self.video_path)
        final_video = video_clip.set_audio(processed_audio)
        final_video.write_videofile(self.output_video_file, codec="libx264")

        video_clip.close()
        processed_audio.close()

    def process(self):
        """
        Perform the complete audio and video processing workflow: extract audio,
        convert formats, reduce noise, adjust volume, and combine with video.
        """
        self.extract_audio_from_video()
        self.convert_mp3_to_wav()
        self.reduce_noise_and_save()
        self.adjust_volume_and_combine()

# Usage Example
if __name__ == "__main__":
    video_file = "/content/drive/MyDrive/Por que você deveria usar/copy_01DF8629-6E7D-4ACF-AC25-D8F2589CDC6D.MOV"
    output_directory = "/content/drive/MyDrive/Por que você deveria usar"

    processor = AudioVideoProcessor(video_file, None, output_directory)
    processor.process()
