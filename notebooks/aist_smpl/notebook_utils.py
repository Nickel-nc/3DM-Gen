from glob import glob
import pickle
import os

import torch
import numpy as np
import scipy
from scipy.spatial.transform import Rotation as R

from smplx import SMPL
from aist_plusplus.features.kinetic import extract_kinetic_features
from aist_plusplus.features.manual import extract_manual_features

try:
    from motion_feature import calculate_motion_beats
except:
    from aist_smpl.motion_feature import calculate_motion_beats

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
root_fp = 'aist_smpl/'

def get_sample_3d_pts(sample_idx=0,
                      keypoints_fp = 'aist_plusplus_final/keypoints3d'):

    key_pts_files = glob(f"{root_fp}{keypoints_fp}/*.pkl")
    # print(f"sequence length: {len(key_pts_files)}")
    with open(key_pts_files[sample_idx], 'rb') as f:
        pts = pickle.load(f)
    return pts

def get_aist_smpl_sample(sample_idx=0,
                         motion_fp = 'aist_plusplus_final/motions/'):

    motion_data = glob(f"{root_fp}{motion_fp}/*.pkl")
    # print(f"sequence length: {len(motion_data)}")
    with open(motion_data[sample_idx], 'rb') as f:
        data = pickle.load(f)
    smpl_poses = data['smpl_poses']  # (N, 24, 3)
    smpl_scaling = data['smpl_scaling']  # (1,)
    smpl_trans = data['smpl_trans']  # (N, 3)
    return smpl_poses, smpl_scaling, smpl_trans

def get_smpl_model_data(smpl_fp = 'smpl'):
    models = glob(f'{root_fp}{smpl_fp}/models/*.pkl')
    with open(models[2], 'rb') as f:
        data_struct = pickle.load(f, encoding='latin1')
    return data_struct

def extract_aist_feats(sample_idx=0,
                      smpl_fp = 'smpl/models'):

    smpl = SMPL(model_path=f'{root_fp}{smpl_fp}', gender='MALE', batch_size=1)
    smpl_poses, smpl_scaling, smpl_trans = get_aist_smpl_sample(sample_idx)
    keypoints3d = smpl.forward(
        global_orient=torch.from_numpy(smpl_poses[:, 0:1]).float(),
        body_pose=torch.from_numpy(smpl_poses[:, 1:]).float(),
        transl=torch.from_numpy(smpl_trans / smpl_scaling).float(),
    ).joints.detach().numpy()[:, 0:24, :]

    kinetic_features = extract_kinetic_features(keypoints3d)
    manual_features = extract_manual_features(keypoints3d)

    return kinetic_features, manual_features

def extract_foot_contact(keypoints3d, velfactor=1.):
    # [
    #     "nose",
    #     "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder",
    #     "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip",
    #     "left_knee", "right_knee", "left_ankle", "right_ankle"
    # ]
    l_foot = keypoints3d[:, -2, :]
    r_foot = keypoints3d[:, -1, :]
    lfoot_xyz = (l_foot[1:, :] - l_foot[:-1, :]) ** 2
    lfoot = np.sqrt(np.sum(lfoot_xyz, axis=-1))
    lfoot = scipy.signal.savgol_filter(lfoot, 9, 2)
    contacts_l = (lfoot < velfactor)

    rfoot_xyz = (r_foot[1:, :] - r_foot[:-1, :]) ** 2
    rfoot = np.sqrt(np.sum(rfoot_xyz, axis=-1))
    rfoot = scipy.signal.savgol_filter(rfoot, 9, 2)
    contacts_r = (rfoot < velfactor)

    # Duplicate the last frame for shape consistency
    contacts_l = np.expand_dims(np.concatenate([contacts_l, contacts_l[-1:]], axis=0), axis=-1)
    contacts_r = np.expand_dims(np.concatenate([contacts_r, contacts_r[-1:]], axis=0), axis=-1)

    return contacts_l, contacts_r

def detect_beat(smpl_poses, seq_len):
    smpl_poses_euler = smpl_poses.as_euler('XYZ').reshape(seq_len, 24, 3).reshape(seq_len, -1)
    beats = calculate_motion_beats(smpl_poses_euler, 3)
    beats_onehot = np.zeros(seq_len)
    beats_onehot[beats.tolist()] = 1
    return np.expand_dims(beats_onehot, axis=-1)

def process_motion_data(sample_idx=0):

    smpl_poses, smpl_scaling, smpl_trans = get_aist_smpl_sample(sample_idx)
    smpl_trans /= smpl_scaling
    seq_len = smpl_poses.shape[0]

    keypoint3d = get_sample_3d_pts(sample_idx=0)['keypoints3d']
    contacts_l, contacts_r = extract_foot_contact(keypoint3d)
    smpl_poses = R.from_rotvec(
        smpl_poses.reshape(-1, 3))
    beats = detect_beat(smpl_poses, seq_len)
    extracts = np.concatenate([contacts_l, contacts_r, beats], axis=-1)

    smpl_poses = smpl_poses.as_matrix().reshape(seq_len, -1)
    smpl_motion = np.concatenate([smpl_trans, smpl_poses, extracts], axis=-1)
    # sample_index = [i * 3 for i in range(smpl_motion.shape[0] // 3)]
    # smpl_motion_downsample = smpl_motion[sample_index]
    return smpl_motion, beats


# Test run routine

if __name__ == "__main__":
    smpl_motion, beats = process_motion_data()
    # print("smpl_motion", smpl_motion)
    fp = 'data_samples/motion_beats.pkl'
    os.makedirs(fp,exist_ok=True)
    with open(fp, 'wb') as f:
        pickle.dump((smpl_motion, beats), f)

