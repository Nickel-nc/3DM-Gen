### Hexapod model settings ###


# model physical dimensions
BASE_DIMENSIONS = {
    "front": 118//2,
    "side": 240//2,
    "middle": 184//2,
    "coxia": 45,
    "femur": 75,
    "tibia": 135,
}

BASE_PARAMS = {
        "tx": 0,
        "tz": 0,
        "rx": 0,
        "ry": 0,
        "legStance": -20,
        "hipStance": 25,
        "stepCount": 4,
        "hipSwing": 25,
        "liftSwing": 40}

START_POSE = {
    'rightMiddle': {'alpha': 45, 'beta': -20.0, 'gamma': 20.0},
    'rightFront': {'alpha': 45, 'beta': -20.0, 'gamma': 20.0},
    'leftFront': {'alpha': -45, 'beta': -20.0, 'gamma': 20.0},
    'leftMiddle': {'alpha': -45, 'beta': -20.0, 'gamma': 20.0},
    'leftBack': {'alpha': 0, 'beta': -20.0, 'gamma': 20.0},
    'rightBack': {'alpha': 0, 'beta': -20.0, 'gamma': 20.0}
}

LEG_NAMES = [
    "rightMiddle",
    "rightFront",
    "leftFront",
    "leftMiddle",
    "leftBack",
    "rightBack",
]

LEG_POINT_TYPES_LIST = [
    "bodyContactPoint",
    "coxiaPoint",
    "femurPoint",
    "footTipPoint",
]

BASE_IK_PARAMS = {
    "hip_stance": 0,
    "leg_stance": 0,
    "percent_x": 0,
    "percent_y": 0,
    "percent_z": 0,
    "rot_x": 0,
    "rot_y": 0,
    "rot_z": 0,
}

DEFAULT_POSE = {
    0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
}

POSITION_NAME_TO_AXIS_ANGLE_MAP = {
    "rightMiddle": 0,
    "rightFront": 45,
    "leftFront": 135,
    "leftMiddle": 180,
    "leftBack": 225,
    "rightBack": 315,
}

POSITION_NAME_TO_ID_MAP = {
    "rightMiddle": 0,
    "rightFront": 1,
    "leftFront": 2,
    "leftMiddle": 3,
    "leftBack": 4,
    "rightBack": 5,
}

MAX_ANGLES = {
    "alpha": 90,
    "beta": 180,
    "gamma": 180,
}

POSITION_NAME_TO_IS_LEFT_MAP = {
    "rightMiddle": False,
    "rightFront": False,
    "leftFront": True,
    "leftMiddle": True,
    "leftBack": True,
    "rightBack": False,
}

MAX_HIP_SWING = 25
P_LEN = 90
NUMBER_OF_LEGS = 6
BODY_MAX_ANGLE = 20
LEG_STANCE_MAX_ANGLE = 90
HIP_STANCE_MAX_ANGLE = 20
DEBUG_MODE = False
ASSERTION_ENABLED = False


# The inverse kinematics solver already updates the points of the hexapod
# But there is no guarantee that this pose is correct
# So better update a fresh hexapod with the resulting poses
RECOMPUTE_HEXAPOD = True
PRINT_IK_LOCAL_LEG = False
PRINT_IK = False
PRINT_MODEL_ON_UPDATE = False
