import numpy as np
#import matplotlib.pyplot as plt
#############################################
# Example 3x3 tensor matrix
tensor_matrix = np.array([[2, -0.5, 0],
                           [0.5, 1, 0.3],
                           [0, 0.3, 1.5]])

#############################################

def visualize_tensor(tensor):
    # Generate a unit sphere
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    
    # Scale the unit sphere by the normal components (diagonal elements of tensor)
    x_trans = x * tensor[0, 0]
    y_trans = y * tensor[1, 1]
    z_trans = z * tensor[2, 2]
    
    # Compute shear vectors (off-diagonal elements of tensor)
    shear_vectors = np.zeros((x.shape[0], x.shape[1], 3))
    shear_vectors[..., 0] = tensor[0, 1] * y + tensor[0, 2] * z
    shear_vectors[..., 1] = tensor[1, 0] * x + tensor[1, 2] * z
    shear_vectors[..., 2] = tensor[2, 0] * x + tensor[2, 1] * y
    
    # Export data for ParaView
    export_to_paraview("tensor_visualization.vtk", x_trans, y_trans, z_trans, shear_vectors)
    
    # Plot the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the ellipsoid scaled by normal components
    ax.plot_surface(x_trans, y_trans, z_trans, color='c', alpha=0.6, edgecolor='k')
    
    # Plot shear vectors as arrows
    ax.quiver(x_trans, y_trans, z_trans, shear_vectors[..., 0], shear_vectors[..., 1], shear_vectors[..., 2], length=0.2, color='r')
    
    # Labels and aspect ratio
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('2nd Order Tensor; normal compoennt shown by elongation and shear stress shown by vector')
    xx=tensor[0, 0]
    yy=tensor[1, 1]
    zz=tensor[2, 2]
    ax.set_box_aspect([xx, yy, zz])


    ax.set_xlim([-tensor[0, 0], tensor[0, 0]])
    ax.set_ylim([-tensor[1, 1], tensor[1, 1]])
    ax.set_zlim([-tensor[2, 2], tensor[2, 2]])
    plt.show()
#############################################

def export_to_paraview(filename, x, y, z, shear_vectors):
    with open(filename, 'w') as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("Tensor Visualization\n")
        f.write("ASCII\n")
        f.write("DATASET STRUCTURED_GRID\n")
        f.write(f"DIMENSIONS {x.shape[0]} {x.shape[1]} 1\n")
        f.write(f"POINTS {x.size} float\n")
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                f.write(f"{x[i, j]} {y[i, j]} {z[i, j]}\n")
        f.write("POINT_DATA {}\n".format(x.size))
        f.write("VECTORS shear_vectors float\n")
        for i in range(shear_vectors.shape[0]):
            for j in range(shear_vectors.shape[1]):
                f.write(f"{shear_vectors[i, j, 0]} {shear_vectors[i, j, 1]} {shear_vectors[i, j, 2]}\n")


#############################################
visualize_tensor(tensor_matrix)