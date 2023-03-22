#Creates a point cloud from the two stl meshes procided, pre processes the point cloud and normalizes and aligns the point cloud
# future revisions can have automated systematic alignment techniques that can automatically rotate incrementaly the point cloud
#Usses ICP algorighin to reister point cloud. Usses Root Mean square deviation to calcuate distance between two point clouds

import numpy as np
import open3d as o3d
import trimesh
import sys

# Use like this  rmsd = calculate_similarity(file1, file2)

#Loads the stl file and returns point cloud object
def load_stl_point_cloud(file_path):
    mesh = trimesh.load_mesh(file_path)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(mesh.vertices)
    return point_cloud

#Preprocess point clou, normalizes the vertices
def preprocess_point_cloud(point_cloud):
    point_cloud = point_cloud.voxel_down_sample(voxel_size=0.05)
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    return point_cloud

#Usses RMSD technique to guage similiarity between point clouds
def calculate_similarity(file1, file2):
    pc1 = load_stl_point_cloud(file1)
    pc2 = load_stl_point_cloud(file2)

    pc1 = preprocess_point_cloud(pc1)
    pc2 = preprocess_point_cloud(pc2)

    threshold = 0.1
    trans_init = np.identity(4)
    result_icp = o3d.registration.registration_icp(pc1, pc2, threshold, trans_init,
                                                   o3d.registration.TransformationEstimationPointToPoint(),
                                                   o3d.registration.ICPConvergenceCriteria(max_iteration=2000))

    distances = pc1.compute_point_cloud_distance(o3d.geometry.PointCloud(pc2.points))
    rmsd = np.sqrt(np.mean(np.square(distances)))
    return rmsd

# This method usses the hausdorff distance, this guages via getting the distance between two sets as defined by the greatest
#distance between point a and B or vice vers.
#d_H(A, B) = max( sup_{a \in A} inf_{b \in B} d(a,b), sup_{b \in B} inf_{a \in A} d(a,b) )
# d(a,b) is the distance between points a and b in space
def calculate_similarity_hausdorf(file1, file2):
    pc1 = load_stl_point_cloud(file1)
    pc2 = load_stl_point_cloud(file2)

    pc1 = preprocess_point_cloud(pc1)
    pc2 = preprocess_point_cloud(pc2)

    threshold = 0.1
    trans_init = np.identity(4)
    result_icp = o3d.registration.registration_icp(pc1, pc2, threshold, trans_init,
                                                   o3d.registration.TransformationEstimationPointToPoint(),
                                                   o3d.registration.ICPConvergenceCriteria(max_iteration=2000))

    pc1.transform(result_icp.transformation)

    hausdorff_distance = o3d.geometry.compute_hausdorff_distance(pc1, pc2)
    return hausdorff_distance

