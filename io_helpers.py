import os
import pickle


def pickle_obj(to_pickle: any, path: os.PathLike):
    with open(path, 'wb') as f:
        pickle.dump(to_pickle, f)