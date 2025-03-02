import numpy as np

from .base import Base


class TriangleData(Base):
    def __init__(
        self,
        point: np.array,
        data: np.array,
        edge: np.array,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.point = point
        self.data = data
        self.edge = edge
        self.zone["n"] = point.shape[0]
        self.zone["e"] = edge.shape[0]
        self.zone["f"] = "fepoint"
        self.zone["et"] = "triangle"

    def data_format(self, data):
        if isinstance(data, list) or isinstance(data, np.ndarray):
            return " ".join([f"{data[k]:6f}" for k in range(len(data))])
        else:
            return f"{data:6f}"

    def _dump(self):
        for i in range(self.point.shape[0]):
            yield f"{self.data_format(self.point[i])} {self.data_format(self.data[i])}"
        for i in range(self.edge.shape[0]):
            yield f"{self.data_format(self.edge[i])}"
