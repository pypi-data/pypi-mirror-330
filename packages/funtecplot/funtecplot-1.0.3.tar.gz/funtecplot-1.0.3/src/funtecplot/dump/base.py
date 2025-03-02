class Base:
    def __init__(self, variables=None, title=None):
        self.variables = variables

        self.title = title
        self.zone = {}
        self.data = []

    def dump(self, filepath):
        variables = self.variables
        if isinstance(self.variables, str):
            variables = self.variables.strip().split(",")

        variables = ", ".join([f'"{var}"' for var in variables])
        with open(filepath, "w") as f:
            if self.title:
                f.write(f"TITLE = {self.title}")
                f.write("\n")
            f.write(f"VARIABLES = {variables}")
            f.write("\n")
            zone = " ".join([f"{k}={v}" for k, v in self.zone.items()])
            f.write(f"ZONE {zone}")
            f.write("\n")
            for d in self._dump():
                f.write(d)
                f.write("\n")

    def _dump(self):
        raise NotImplementedError()
