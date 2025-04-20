import pygame
import numpy as np


def generate_tone(freq, duration, volume=1.0, sample_rate=44100):
    # Generate a numpy array representing a sine wave tone
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    waveform = np.sin(2 * np.pi * freq * t) * volume
    # Convert waveform to 16-bit signed integers
    waveform_integers = np.int16(waveform * 32767)
    return pygame.sndarray.make_sound(waveform_integers)


def init_audio():
    try:
        # Initialize the mixer to use 44100 Hz, 16-bit signed, 1 channel (mono)
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        global shoot_sound, explosion_sound, hit_sound, background_music_sound
        shoot_sound = generate_tone(800, 0.1, volume=0.5)         # Shooting sound: 800Hz for 0.1 sec
        explosion_sound = generate_tone(120, 0.3, volume=0.7)       # Explosion: 120Hz for 0.3 sec
        hit_sound = generate_tone(300, 0.05, volume=0.5)            # Hit sound: 300Hz for 0.05 sec
        # Background music: a continuous 440Hz tone looped as a chiptune background
        background_music_sound = generate_tone(440, 1.0, volume=0.3)
        background_music_sound.play(loops=-1)
    except Exception as e:
        print("Audio initialization error:", e)


def play_shoot():
    try:
        shoot_sound.play()
    except Exception as e:
        print("Error playing shoot sound:", e)


def play_explosion():
    try:
        explosion_sound.play()
    except Exception as e:
        print("Error playing explosion sound:", e)


def play_hit():
    try:
        hit_sound.play()
    except Exception as e:
        print("Error playing hit sound:", e) 