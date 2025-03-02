import numpy as np


from .base import Base


class PointData(Base):
    def __init__(self, data: np.array, axis_dim=2, data_dim=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.axis_dim = axis_dim
        self.data_dim = data_dim
        assert len(self.variables) == self.data_dim + self.axis_dim
        self.axis_shape = data.shape[: self.axis_dim]
        if axis_dim >= 1:
            self.zone["I"] = self.axis_shape[-1]
        if axis_dim >= 2:
            self.zone["J"] = self.axis_shape[-2]
        if axis_dim >= 3:
            self.zone["K"] = self.axis_shape[-3]
        self.zone["f"] = "point"

    def data_format(self, data):
        if isinstance(data, list) or isinstance(data, np.ndarray):
            return " ".join([f"{data[k]:6f}" for k in range(self.data_dim)])
        else:
            return f"{data:6f}"

    def _dump(self):
        if self.axis_dim == 1:
            for i in range(self.axis_shape[0]):
                yield f"{i + 1:6f} {self.data_format(self.data[i])}"
        elif self.axis_dim == 2:
            for i in range(self.axis_shape[0]):
                for j in range(self.axis_shape[1]):
                    yield f"{i + 1:6f} {j + 1:6f} {self.data_format(self.data[i][j])}"
        elif self.axis_dim == 3:
            for i in range(self.axis_shape[0]):
                for j in range(self.axis_shape[1]):
                    for k in range(self.axis_shape[2]):
                        yield f"{i + 1:6f} {j + 1:6f} {k + 1:6f} {self.data_format(self.data[i][j][k])}"


def example():
    PointData(
        data=np.random.rand(30), variables=["x", "u"], axis_dim=1, data_dim=1
    ).dump("example_1_1_1.txt")
    PointData(
        data=np.random.rand(30, 1), variables=["x", "u"], axis_dim=1, data_dim=1
    ).dump("example_1_1_2.txt")
    PointData(
        data=np.random.rand(30, 3),
        variables=["x", "ux", "uy", "uz"],
        axis_dim=1,
        data_dim=3,
    ).dump("example_1_3_1.txt")

    PointData(
        data=np.random.rand(3, 5, 4),
        variables=["x", "y", "z", "u"],
        axis_dim=3,
        data_dim=1,
    ).dump("example_3_1_1.txt")
    PointData(
        data=np.random.rand(3, 5, 4, 1),
        variables=["x", "y", "z", "u"],
        axis_dim=3,
        data_dim=1,
    ).dump("example_3_1_2.txt")
    PointData(
        data=np.random.rand(3, 5, 4, 3),
        variables=["x", "y", "z", "ux", "uy", "uz"],
        axis_dim=3,
        data_dim=3,
    ).dump("example_3_3_1.txt")


# example()
