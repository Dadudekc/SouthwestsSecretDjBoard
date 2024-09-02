# -------------------------------------------------------------------
# File Path: virtual_dj_backend.py
# Description: This script provides the backend functionality for a virtual DJ application,
# focusing on core features like track loading, pitch control, and playback.
# -------------------------------------------------------------------

from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

# -------------------------------------------------------------------
# Section 1: Audio Track Class
# -------------------------------------------------------------------

class AudioTrack:
    def __init__(self, file_path):
        # Load the audio file
        self.track = AudioSegment.from_file(file_path)
        self.original_track = self.track
        self.playback_obj = None
        self.pitch = 1.0

    def set_pitch(self, pitch_factor):
        """
        Adjust the pitch of the track.
        :param pitch_factor: A float representing the pitch change (e.g., 0.5 for half speed, 2.0 for double speed)
        """
        self.pitch = pitch_factor
        new_frame_rate = int(self.original_track.frame_rate * self.pitch)
        self.track = self.original_track._spawn(self.original_track.raw_data, overrides={'frame_rate': new_frame_rate})
        self.track = self.track.set_frame_rate(44100)  # Standard frame rate

    def play(self):
        """
        Play the audio track with the current settings.
        """
        if self.playback_obj:
            self.stop()
        
        # Export the track as a temporary file to play with simpleaudio
        playback_data = self.track.export(format="wav")
        self.playback_obj = sa.play_buffer(playback_data.read(), num_channels=2, bytes_per_sample=2, sample_rate=44100)
    
    def stop(self):
        """
        Stop the audio playback.
        """
        if self.playback_obj:
            self.playback_obj.stop()

    def apply_flanger(self):
        """
        Apply a simple flanger effect.
        """
        # This is a basic example; you may want to use an actual DSP library for more complex effects.
        self.track = self.track.flanger()

    def apply_brake_start(self, speed_decrease=0.9, duration_ms=2000):
        """
        Apply a brake start effect to the track.
        :param speed_decrease: The factor by which speed decreases.
        :param duration_ms: Duration of the brake effect in milliseconds.
        """
        start_speed = int(self.track.frame_rate)
        end_speed = int(start_speed * speed_decrease)
        brake_duration = duration_ms

        self.track = self.track.fade(to_gain=-30.0, start=0, duration=brake_duration)
        self.set_pitch(end_speed / start_speed)

# -------------------------------------------------------------------
# Section 2: Example Usage (Main Section)
# -------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage of the AudioTrack class
    file_path = "example_track.mp3"  # Replace with your audio file path

    # Initialize the track
    track = AudioTrack(file_path)

    # Set pitch to slow down (screwed effect)
    track.set_pitch(0.5)

    # Apply flanger effect
    track.apply_flanger()

    # Play the track
    track.play()

    # Stop after 10 seconds for demonstration
    import time
    time.sleep(10)
    track.stop()
