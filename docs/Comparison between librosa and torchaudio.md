

| Функция         | librosa     | torchaudio |
|-----------------|-------------|------------|
| stft | +      | +        |
| inverse stft      | +  | -       |
| griffinlim      | +  | +       |
| Mel-scale spectrogram      | +  | +       |
| Pitch detection      | +  | +       |
| beats detection      | +  | -       |
| harmonic percussive source separation      | +  | -       |



According to https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html#comparison-against-librosa torchaudio is faster for resampling tasks.

griffinlim - another algorythm for inversing stft to time domain. (similar to invese stft)

