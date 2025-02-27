import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class Save_state:
    """
    This class saves the state of all dictionaries and reads them
    **
    To do
    Read the dicts
    """
    def __init__(self,data,folder='./data',state='write'):

        self.state = state
        self.data = data
        self.folder = folder

    def save_state(self):
        """
        Saves the dictionaries
        """
        json_object = json.dumps(self.data, cls=NpEncoder, indent = 4)#, default=vars)#,indent = 4) 
        with open(self.folder+'.json','w') as f:
            
            f.write(json_object)

        f.close()

    def read_state(self):
        """
        Reads the dictionaries
        """
        with open(self.folder+'.json','r') as f:

            object=json.load(f)
        f.close()

        return(object)


