from glob import glob
import pickle



aist_fp = 'aist_smpl/aist_plusplus_final'
keypoints_fp = 'aist_smpl/aist_plusplus_final/keypoints3d'
motion_fp = 'aist_smpl/aist_plusplus_final/motions/'
smpl_fp = 'aist_smpl/smpl'


def get_sample_3d_pts(sample_idx=0):
    key_pts_files = glob(f"{keypoints_fp}/*.pkl")
    print(f"sequence length: {len(key_pts_files)}")
    with open(key_pts_files[sample_idx], 'rb') as f:
        pts = pickle.load(f)
    return pts

def get_aist_smpl_sample(sample_idx=0):
    motion_data = glob(f"{motion_fp}/*.pkl")
    print(f"sequence length: {len(motion_data)}")
    with open(motion_data[sample_idx], 'rb') as f:
        data = pickle.load(f)
    smpl_poses = data['smpl_poses']  # (N, 24, 3)
    smpl_scaling = data['smpl_scaling']  # (1,)
    smpl_trans = data['smpl_trans']  # (N, 3)
    return smpl_poses, smpl_scaling, smpl_trans


def get_smpl_model_data():
    models = glob(f'{smpl_fp}/models/*.pkl')
    with open(models[2], 'rb') as f:
        data_struct = pickle.load(f, encoding='latin1')
    return data_struct
