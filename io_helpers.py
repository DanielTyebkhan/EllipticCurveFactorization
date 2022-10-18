import os
import pickle

def load_pickle(path: os.PathLike) -> any:
    with open(path, 'rb') as f:
        res = pickle.load(f)
    return res

def pickle_obj(to_pickle: any, path: os.PathLike):
    with open(path, 'wb') as f:
        pickle.dump(to_pickle, f)