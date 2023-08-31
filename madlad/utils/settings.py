import json

class config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

        for data in self.data:
            if "model" in data:
                self.model = data
            elif "nevents" in data:
                self.run = data
            elif "decays" in data:
                self.madspin = data
            elif "param" in data:
                self.param = data
            elif "custom_scales" in data:
                self.scales = data

        self.process_dir = self.model['save_dir']

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # If the file doesn't exist, initialize with an empty dictionary
            return {}

    def save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()
