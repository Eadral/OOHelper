class Config:
    TIME_LIMIT = 200

    MIN_LEVEL = -3
    MAX_LEVEL = 20
    MAX_REQUEST = 50
    MAX_TIME = 200

    CLOSE_STDERR = True

    # LEVEL_TIME = 0.4
    LEVEL_TIME_A = 0.4
    LEVEL_TIME_B = 0.5
    LEVEL_TIME_C = 0.6
    LEVEL_TIME = {
        "A": 0.4,
        "B": 0.5,
        "C": 0.6,
    }

    DOOR_TIME = 0.2

    EPS = 0.0001


cfg = Config()
