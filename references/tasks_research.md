# Task relevant technologies and SOTA models

### 3D Motion Generation

[Robust Dancer: Long-term 3D Dance Synthesis Using Unpaired Data](https://arxiv.org/pdf/2303.16856v1.pdf)

Notes:
- Model: Transformer-based. music-encoder, style condition transformer
- uses unaligned music-motions data
- uses SMPL-X - joint 3D model of the human body
- inputs: historical motions, beat context, style exemplars

[Weakly Supervised Deep Recurrent Neural Networks for Basic Dance Step Generation](https://paperswithcode.com/paper/weakly-supervised-deep-recurrent-neural)

Notes:
- Model: multilayer LSTM and convolutions to encode audio spectrum
- can be performed without massive hand-constructed data
- 20 stars 4 forks (git upd 5 years ago) - has broken links
- year: 2021

Investigation results:
- Unclear, not explained dataset
- Music bit feature extraction contains marsyas lib with broken links that can't be installed

[EDGE: Editable Dance Generation From Music](https://paperswithcode.com/paper/edge-editable-dance-generation-from-music)

Notes:
- Model: Diffusion. Takes a noisy sequence. Learns to denoise dance sequences from time
t = T to t = 0, conditioned on music. 
Music embedding information is provided by a frozen Jukebox model 
and acts as cross-attention context. 
zT ∼ N (0, I) and produces the estimated final sequence xˆ, noising it back to zˆT −1 
and repeating until T = 0
- uses blender 3d rendering
- uses AIST++ dataset
- Declared outperform over other approaches
- 234 stars 24 forks (upd in 2023.06) Created by Standford
- year: 2023

[Listen, Denoise, Action! Audio-Driven Motion Synthesis with Diffusion Models](https://paperswithcode.com/paper/listen-denoise-action-audio-driven-motion)

Notes:
- Model: Diffusion
- lim: slow generation speed (for all diffusion models)
- starts 53 forks 7 (last upd 2023.09)
- year: 2023

[Robust Dancer: Long-term 3D Dance Synthesis Using Unpaired Data](https://paperswithcode.com/paper/robust-dancer-long-term-3d-dance-synthesis)

Notes:
- Model: Transformer-based
- Uses AIST++
- 11 stars 1 fork (last upd 2023.03)
- year: 2023

[Bailando: 3D Dance Generation by Actor-Critic GPT with Choreographic Memory](https://paperswithcode.com/paper/bailando-3d-dance-generation-by-actor-critic)

Notes:
- Model: GPT-like. 4 steps of model sequence
  - Step 1: Train pose VQ-VAE (without global velocity)
  - Step 2: Train glabal velocity branch of pose VQ-VAE
  - Step 3: Train motion GPT
  - Step 4: Actor-Critic finetuning on target music
- Separate learning for pose generation and music feature processing 
- A100 cluster training
- 300+ stars 50+ forks (upd in 2022 )
- Needs to make huge work to adapt for non-human models
- year: 2022

[AlignNet: A Unifying Approach to Audio-Visual Alignment](https://paperswithcode.com/paper/alignnet-a-unifying-approach-to-audio-visual)

Notes:
- Model: Consists of attention, pyramidal processing, time warping, 
affinity and correspondence prediction
- 24 stars 3 forks
- year: 2020


[L2D: Learning to dance from music audio](https://github.com/verlab/Learning2Dance_CAG_2020)

Notes:
 
- Model: graph convolutional adversarial network 
Estimates a motion to fit the audio
- Dataset: audio-visual - poses and audio are extracted from video
- only 2d representation
- needs big dataset
- year: 2020

[CSGN Long sequences of skeletons generation](https://paperswithcode.com/paper/convolutional-sequence-generation-for)

Notes: 

- Model: CSGN convolution sequence generation network on graphs
GCNs generates a set of skeleton poses
by saampling random vectors from a Gaussian process
- needs big dataset
- year: 2019

https://www.resolutiongames.com/blog/creating-a-dancing-character-with-machine-learning


### Datasets

[AIST++](https://paperswithcode.com/dataset/aist)

Notes:

- 3D dance dataset which contains 3D motion reconstructed from real dancers paired with music
- Used in creation of several SOTA approaches

[Dance50](None)

### Audio-visual alignment

[AlignNet: A Unifying Approach to Audio-Visual Alignment](https://arxiv.org/pdf/2002.05070v1.pdf)

Notes:
- Attention transformer based model
- audio-pose alignment fpr each frame
- Log-mel spectrogram as audio feats 
- end-to-end dense correspondence between each frame of a video and an audio
- dance50 dataset
- year: 2020

### Side relevants

[TM2D: Bimodality Driven 3D Dance Generation via Music-Text Integration](https://paperswithcode.com/paper/tm2d-bimodality-driven-3d-dance-generation)

Notes:
- Model: Transformers uses music-dance and text-motion
- 36 stars 0 forks (WIP no code)
- year: 2023

[Dance Dance Convolution](https://arxiv.org/pdf/1703.06891v3.pdf)

Notes:
- Nice article on audio processing to generate bitmap applied for the DDR rhythm game


[Animating Non-Humanoid Characters
with Human Motion Data](https://la.disneyresearch.com/wp-content/uploads/Animating-Non-Humanoid-Characters-with-Human-Motion-Data-Paper.pdf)

Notes:
- An algorithmic approach on datapoints conversion 