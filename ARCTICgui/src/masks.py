
from enum import Enum
class IOType(Enum):
    NOTHING = 0
    PATH = 1
    NUMBER = 2
    BOOL = 3
    SEARCH_ALGO = 4
    OPTIMIZATION_TYPE = 5
    BAB_SEARCH_STRATEGY = 6
    BAB_TYPE = 7
    TEXT = 8
    SIMULATOR = 9


synthesis_settings = {
    "OUTPUT_DIR": IOType.PATH,
    "SYN_LIMIT_THREAD_NUM": IOType.NUMBER,
    "SYNTHESIS_MODE":False,
    "SYNTHESIS_DEPTH": IOType.NUMBER,
    "SYNTHESIS_WEIGHT": IOType.NUMBER,
    "SYNTHESIS_WEIGHT_RELAXATION": IOType.NUMBER,
    "SYNTHESIS_LIMIT_STRUCTURES_NUM": IOType.NUMBER,
    "SYNTHESIS_PROCEED_WITH_TM": IOType.BOOL,
}

synthesis_mask = {
    "OUTPUT_DIR": False,
    "SYN_LIMIT_THREAD_NUM": False,
    "SYNTHESIS_MODE":False,
    "SYNTHESIS_DEPTH": False,
    "SYNTHESIS_WEIGHT": False,
    "SYNTHESIS_WEIGHT_RELAXATION": False,
    "SYNTHESIS_LIMIT_STRUCTURES_NUM": False,
    "SYNTHESIS_PROCEED_WITH_TM": True
}

technology_mapping_settings = {
    "LIBRARY" : IOType.PATH,
    "COMPACT_LIBRARY" : IOType.PATH,
    "SEARCH_ALGORITHM" : IOType.SEARCH_ALGO,
    "OPTIMIZATION_TYPE" : IOType.OPTIMIZATION_TYPE,
    "STATISTICS" : IOType.BOOL,
    "BAB-SEARCH_STRATEGY" : IOType.BAB_SEARCH_STRATEGY,
    "BAB-TYPE" : IOType.BAB_TYPE,
    "BAB-VISUALIZE" : IOType.BOOL,
    "BAB-STATISTICS" : IOType.BOOL,
    "BAB-FAST" : IOType.BOOL,
}

technology_mapping_mask = {
    "LIBRARY" : True,
    "COMPACT_LIBRARY" : False,
    "SEARCH_ALGORITHM" : False,
    "OPTIMIZATION_TYPE" : False,
    "STATISTICS" : False,
    "BAB-SEARCH_STRATEGY" : False,
    "BAB-TYPE" : False,
    "BAB-VISUALIZE" : False,
    "BAB-STATISTICS" : False,
    "BAB-FAST" : False,
}

default_simulator_settings = {
    "SIMULATOR" : IOType.SIMULATOR,
    "PYTHON_BINARY":IOType.PATH,
    "SIM_LIMIT_THREADS_NUM":IOType.NUMBER,
    "SIM_PATH":IOType.PATH,
    "SIM_SCRIPT":IOType.PATH,
    "SIM_INIT_ARGS":IOType.TEXT,
    "SIM_ARGS":IOType.TEXT,
}

default_simulator_mask = {
    "PYTHON_BINARY":True,
    "SIM_LIMIT_THREADS_NUM":False,
    "SIM_SCRIPT":True,
    "SIM_INIT_ARGS":True,
    "SIM_PATH":True,
    "SIM_ARGS":False
}

plasmid_settings = {
}

plasmid_mask = {
}