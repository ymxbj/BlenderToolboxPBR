import os
import trimesh
import numpy as np

mesh_path = './telescope/mesh.obj'

def scale_to_unit_sphere(mesh, evaluate_metric = False):
  if isinstance(mesh, trimesh.Scene):
    mesh = mesh.dump().sum()

  vertices = mesh.vertices - mesh.bounding_box.centroid
  distances = np.linalg.norm(vertices, axis=1)
  vertices /= np.max(distances)
  if evaluate_metric:
        vertices /= 2
  return trimesh.Trimesh(vertices=vertices, faces=mesh.faces, vertex_colors=mesh.visual.vertex_colors)

mesh = trimesh.load(mesh_path, force = 'mesh')
mesh = scale_to_unit_sphere(mesh)
mesh.export(mesh_path)
