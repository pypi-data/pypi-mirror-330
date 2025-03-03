class Dict2Obj:
    """Convert a dictionary into an object with attribute-style access and provide flattening functionality."""

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input should be a dictionary.")
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Dict2Obj(value))  # Recursively convert nested dicts
            else:
                setattr(self, key, value)

    def __getattr__(self, name):
        """Return None if the attribute does not exist."""
        return None

    def to_dict(self):
        """Convert the object back to a dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Dict2Obj):
                result[key] = value.to_dict()  # Recursively convert back
            else:
                result[key] = value
        return result

    def to_dot_dict(self, parent_key=""):
        """Flatten the dictionary into a dot notation format."""
        dot_dict = {}

        def flatten(obj, parent_key=""):
            if isinstance(obj, Dict2Obj):
                obj = obj.to_dict()
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{parent_key}.{key}" if parent_key else key
                    if isinstance(value, dict):
                        flatten(value, full_key)  # Recursively flatten nested dicts
                    else:
                        dot_dict[full_key] = value
            else:
                dot_dict[parent_key] = obj

        flatten(self.to_dict(), parent_key)
        return dot_dict
