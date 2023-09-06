import glob
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt, rcParams
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from hexapod.hexapod import Hexapod
from hexapod.model_settings import BASE_DIMENSIONS


""" Plot Style Settings """

plt.style.use('dark_background')

rcParams["figure.figsize"] = (12,12)

rcParams['patch.facecolor'] = '#3c638250'
rcParams['axes.prop_cycle'] = plt.cycler(color=["#EE5A24"])
rcParams['lines.linewidth'] = 5
rcParams['scatter.edgecolors'] = 'red'

rcParams['axes.facecolor'] = '#2D3437'
rcParams['axes.edgecolor'] = '#2D3437'
rcParams['axes.spines.left'] = False

rcParams['xtick.labelbottom'] = False
rcParams['ytick.labelleft'] = False
rcParams['ytick.left'] = False

rcParams['axes3d.grid'] = False
rcParams['axes3d.xaxis.panecolor'] = '#2D3437'
rcParams['axes3d.yaxis.panecolor'] = '#2D3437'
rcParams['axes3d.zaxis.panecolor'] = '#3c638220'

""" #################### """

class SequenceDataGen:
    """
    constrained for 18 joints 6 legged hexapod model
    """

    def __init__(self):

        self.body_vertices = []
        self.body_poly = []
        self.leg_lines = []

    def get_ext_joints_dict(self, start_pose, end_pose, n_frames):
        s = np.ravel(start_pose)
        e = np.ravel(end_pose)
        poses = []
        for i in range(18):
            poses.append(np.linspace(s[i], e[i], n_frames).astype('int'))

        sequence = []
        for i in range(n_frames):
            sequence.append(
                {
                    'rightMiddle': {'alpha': poses[0][i], 'beta': poses[1][i], 'gamma': poses[2][i]},
                    'rightFront': {'alpha': poses[3][i], 'beta': poses[4][i], 'gamma': poses[5][i]},
                    'leftFront': {'alpha': poses[6][i], 'beta': poses[7][i], 'gamma': poses[8][i]},
                    'leftMiddle': {'alpha': poses[9][i], 'beta': poses[10][i], 'gamma': poses[11][i]},
                    'leftBack': {'alpha': poses[12][i], 'beta': poses[13][i], 'gamma': poses[14][i]},
                    'rightBack': {'alpha': poses[15][i], 'beta': poses[16][i], 'gamma': poses[17][i]}
                }
            )
        return sequence

    def update_sequence(self, joint_sequence, reverse=False):
        for pos in joint_sequence:
            hexapod = Hexapod(BASE_DIMENSIONS, pos)

            pts = []
            for leg in hexapod.legs:
                pts.append(self.unpack_vector_list(leg.allPointsList))
            leg_pts = np.array(pts)

            # setup z-axis min point to be on the ground with bias (crappy correction)
            local_bias = min(leg_pts[::,2][::,3])
            leg_pts[::,2] -= local_bias

            vertices = np.array(self.unpack_vector_list(hexapod.body.verticesList, cyclic=True))
            vertices[2] -= local_bias

            poly = np.array(self.unpack_vector_zip_list(hexapod.body.verticesList))
            poly[::,2] -= local_bias

            self.leg_lines.append(leg_pts)
            self.body_vertices.append(vertices)
            self.body_poly.append(poly)

        if reverse:
            self.update_sequence(joint_sequence[::-1], reverse=False)

    def get_sequence(self, start_pose, end_pose, n_frames, reverse):

        """
        Calculate sequence kinematic movement from start to end pose
        Concatenate calculations with stored sequence
        """
        # create sequence dict from start to end pose of given length
        joint_sequence = self.get_ext_joints_dict(start_pose, end_pose, n_frames)
        self.update_sequence(joint_sequence, reverse)


    def unpack_vector_list(self, vectors: list, cyclic=False) -> list:
        """

        :param vectors:
            list of Vector objects with params:
                x,y,z,name,id
        :return:
        """
        x,y,z = [],[],[]
        for v in vectors:
            x.append(v.x)
            y.append(v.y)
            z.append(v.z)
            # out.append([v.x, v.y, v.z]) # v.name, v.id
        if cyclic:
            x.append(x[0])
            y.append(y[0])
            z.append(z[0])
        return [x,y,z]

    def unpack_vector_zip_list(self, vectors: list) -> list:
        out = []
        for v in vectors:
            out.append([v.x, v.y, v.z])
        return out


class Plotter:

    def __init__(self, savefig=False, save_dir='../../misc/figs'):
        self.savefig = savefig
        self.save_dir = save_dir
        self.frame_speed = 0.02  # seconds per frame

    def draw_hexapod(self, leg_lines, body_poly, body_vertices):

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # stand_pts = [
        #     [-300, -300, 0],
        #     [300, -300, 0],
        #     [300, 300, 0],
        #     [-300, 300, 0]
        # ]
        for i in range(len(leg_lines)):
            plt.cla()
            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])

            # plot base stand polygon
            # base_poly = Poly3DCollection([stand_pts], alpha=0.5)
            # ax.add_collection3d(base_poly)

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
            ax.set_xlim3d([-400,400])
            ax.set_ylim3d([-400,400])
            ax.set_zlim3d([0,300])
            # ax.margins(x=0, y=-0.25, z=50)
            ax.set_aspect('equal')
            ax.view_init(elev=30, azim=75)

            if self.savefig and i:
                plt.savefig(f'{self.save_dir}/{str(i).zfill(3)}.png')

            plt.pause(0.1)

        if self.savefig:
            self.make_gif()

    def make_gif(self):

        target = f'{self.save_dir}/*.png'
        output = f'{self.save_dir}/output.gif'

        images = []
        basewidth = 640
        files = glob.glob(target)
        # Create images list
        for filename in files:
            img = Image.open(filename)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.LANCZOS)

            images.append(img)
        duration = len(files) * self.frame_speed
        images[0].save(output, format='GIF', append_images=images[1:], save_all=True, duration=duration, loop=0)

#  Test routine
if __name__ == "__main__":

    """Joints angle lists"""
    start = [
        [45, -20, 20],   # 'rightMiddle'
        [45, 110, 20],   # 'rightFront'
        [-45, 110, 20],  # 'leftFront'
        [-45, -20, 20],  # 'leftMiddle'
        [0, -20, 20],    # 'leftBack'
        [0, -20, 20]     # 'rightBack'
    ]
    end = [
        [45, -20, 20],
        [0, 110, -80],
        [-90, 110, -80],
        [-45, -20, 20],
        [0, -20, 20],
        [0, -20, 20]
    ]
    new_end = [
        [45, -20, 20],
        [90, 110, -80],
        [0, 110, -80],
        [-45, -20, 20],
        [0, -20, 20],
        [0, -20, 20]
    ]

    s = SequenceDataGen()
    # create position points sequence from start to end of given lenght
    s.get_sequence(start_pose=start, end_pose=end, n_frames=20, reverse=True)
    s.get_sequence(start_pose=start, end_pose=new_end, n_frames=20, reverse=True)

    Plotter(savefig=True).draw_hexapod(s.leg_lines, s.body_poly, s.body_vertices)
