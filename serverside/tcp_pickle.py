import pickle

def pack(in_data):
    data = pickle.dumps(in_data)
    return data