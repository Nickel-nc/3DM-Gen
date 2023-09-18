import numpy as np
import librosa


def read_wav(path):
    signal, sr = librosa.load(path)
    time = np.linspace(0, 1 / sr * len(signal), num=len(signal))
    return {'signal': signal, 'time': time, 'sr': sr}


def stft(audio_dict, **kwargs):
    n_fft = kwargs.get('n_fft', 2048)
    hop_len = kwargs.get('hop_len', 2048//4)
    y = librosa.stft(audio_dict['signal'], n_fft=n_fft, hop_length=hop_len)
    S_db = librosa.amplitude_to_db(np.abs(y))
    return y, S_db


def extract_beats(audio_dict):
    tempo, beats = librosa.beat.beat_track(y=audio_dict['signal'], sr=audio_dict['sr'])
    beats_time = librosa.frames_to_time(beats, sr=audio_dict['sr'])
    return beats_time


def hpss_decompose(y, sr):
    y_harmonic, y_percussive = librosa.decompose.hpss(y)
    sig_harmonic, sig_percussive = librosa.istft(y_harmonic), librosa.istft(y_percussive)
    return sig_harmonic, sig_percussive