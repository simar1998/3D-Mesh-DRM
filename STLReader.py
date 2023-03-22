import numpy as np
from stl import mesh

class STLReader:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def read_stl_files(self):
        # Read in the first STL file and extract the vertex coordinates
        mesh1 = mesh.Mesh.from_file(self.file1)
        coords1 = mesh1.vectors.reshape(-1, 3)

        # Read in the second STL file and extract the vertex coordinates
        mesh2 = mesh.Mesh.from_file(self.file2)
        coords2 = mesh2.vectors.reshape(-1, 3)

        # Return the two arrays of vertex coordinates
        return coords1, coords2
