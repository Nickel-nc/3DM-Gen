import numpy as np
import librosa
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from moviepy.editor import VideoClip, AudioFileClip
from moviepy.video.io.bindings import mplfig_to_npimage

from plotter import SequenceDataGen


def extract_beats(audio_dict):
    tempo, beats = librosa.beat.beat_track(y=audio_dict['signal'], sr=audio_dict['sr'])
    beats_time = librosa.frames_to_time(beats, sr=audio_dict['sr'])
    return beats_time


class VideoGenerator:
    def __init__(self, events_extractor, moves_choice, fps=30):
        self.fps = fps
        self.vid_dt = 1./fps
        self.events_extractor = events_extractor
        self.moves_choice = moves_choice
        self.sequence = SequenceDataGen()

    @staticmethod
    def read_wav(path):
        signal, sr = librosa.load(path)
        time = np.linspace(0, 1 / sr * len(signal), num=len(signal))
        return {'signal': signal, 'time': time, 'sr': sr}

    def draw_hexapod(self, fig, ax, t, leg_lines, body_poly, body_vertices):

        ax.clear()
        i = int(t / self.vid_dt)

        # plot hexapod body polygon
        poly = Poly3DCollection([body_poly[i]], alpha=0.5)
        ax.add_collection3d(poly)
        # plot poly vertices
        ax.plot(body_vertices[i][0], body_vertices[i][1], body_vertices[i][2])
        ax.scatter(body_vertices[i][0], body_vertices[i][1], body_vertices[i][2])
        # plot legs
        for leg in leg_lines[i]:
            ax.plot(leg[0], leg[1], leg[2])
            ax.scatter(leg[0], leg[1], leg[2])

        # remove axis info
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis._axinfo['tick']['inward_factor'] = 0.0
            axis._axinfo['tick']['outward_factor'] = 0.0

        # setup current frame settings
        ax.set_xlim3d([-400, 400])
        ax.set_ylim3d([-400, 400])
        ax.set_zlim3d([0, 300])
        # ax.margins(x=0, y=-0.25, z=50)
        # ax.set_aspect('equal')
        ax.view_init(elev=30, azim=75)

        # plt.pause(0.1)
        return mplfig_to_npimage(fig)

    def generate_video(self, audio_path, path_to_save):
        audio = self.read_wav(audio_path)
        audio_len = len(audio['signal']) / audio['sr']
        events = self.events_extractor(audio)
        moves = self.moves_choice(events)
        for ix, ev in enumerate(events[:-1]):
            n_frames = int(np.floor((events[ix + 1] - events[ix]) / self.vid_dt))
            self.sequence.get_sequence(start_pose=moves[ix], end_pose=moves[ix+1], n_frames=n_frames, reverse=False)
            print(n_frames)
        # filling
        n_fr_miss = int((audio_len - len(self.sequence.leg_lines) / self.fps) * self.fps)
        self.sequence.get_sequence(start_pose=moves[-1], end_pose=moves[-1], n_frames=n_fr_miss, reverse=False)
        #
        video_dur = len(self.sequence.leg_lines) / self.fps
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        video = VideoClip(lambda x: self.draw_hexapod(fig, ax, x,
                                                      self.sequence.leg_lines,
                                                      self.sequence.body_poly,
                                                      self.sequence.body_vertices),
                          duration=video_dur)
        audio = AudioFileClip(audio_path)
        final_vid = video.set_audio(audio)
        final_vid.write_videofile(fps=self.fps, codec='libx264', filename=path_to_save)


