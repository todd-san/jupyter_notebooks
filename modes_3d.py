import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import math

# arbitrary 'mode' frequency, or natural frequency
wn = 1

# arbitrary amount of time the animation should perform
t = np.arange(0, 10, 0.001)

# arbitary eigenvectors for 6 free-body modes in 6DOF
eigv = [-3.406e-2, -1.654e-1, 1.672e-1, -9.988e-1, -3.823e-1, -7.623e-2]
# eigv = [-4.619e-1,  3.597e-1, -4.013e-4,  1.361e-2, -8.785e-1,  9.680e-1]  ##  X Translation
# eigv = [-8.862e-2, -9.180e-2, -9.860e-2, -4.679e-3,  2.864e-2,  2.389e-2]  ##  Y Translation
# eigv = [-1.503e-1,  1.845e-2,  1.646e-2,  4.313e-4,  8.095e-3, -1.391e-2]  ## Z Translation
# eigv = [ 1.968e-2,  3.761e-2, -1.553e-2, -1.562e-2,  8.576e-2,  2.219e-2]  ## XYZ Translation
# eigv = [ 3.315e-2,  6.037e-2, -8.172e-2, -6.324e-3, -3.541e-2, -2.326e-2]   ## XYZ Translation

# generating inital arbitrary point cloud
eng = [1500., -10., 140.]
pt1 = [1700., -250., 15.]
pt2 = [1400., -250., 10.]
pt3 = [1375., 200.,   0.]
pt4 = [1725., 200.,  25.]
pt5 = [1550.,   0., 200.]
pt6 = [1650., -20., 150.]
pt7 = [1450.,  20., 150.]
pt8 = [1375.,   0.,  100.]
pt9 = [1725.,   0.,  100.]

p_cld = [eng, pt6, pt7, pt8, pt9]
pts   = np.array(p_cld)


def periodic_motion_gen(eigv, wn, time):
    #I probably want to increase the scale of the movement
    t_sf = 100  # scale factor for translation
    r_sf = 20   # scale factor for rotation
    dx = []
    for i, eig in enumerate(eigv):
        if i<3:
            dx.append(eig*np.sin(wn*t)*t_sf)
        else:
            dx.append(eig*np.sin(wn*t)*r_sf)
    np.array(dx)
    return np.transpose(dx)
dx = periodic_motion_gen(eigv, wn, t)


def create_cg_path(cg, dx):
    cg_p = []
    for i, dx_i in enumerate(dx):
        cg += dx_i[:3]
        cg_p.append([cg[0], cg[1], cg[2]])
    return np.asarray(cg_p)
cg_path = create_cg_path(cg=[1500., -10., 140.], dx=dx)


def create_pt_paths(cg_path, dx, pt):
    pt_path = []

    def trans_pt_by_sig(p, xi, i):
        tpbs = []
        p += dx[i][:3]
        tpbs.append([p[0], p[1], p[2]])
        return np.asarray(tpbs)

    def trans_pt_2_origin(p, xi, i):
        tp2o = []
        T = np.matrix([[1, 0, 0, -xi[0]],
                       [0, 1, 0, -xi[1]],
                       [0, 0, 1, -xi[2]],
                       [0, 0, 0, 1]])

        tmp = np.insert(p, 3, 1)
        tmp = np.matmul(T, tmp)
        tmp = np.delete(tmp, 3)
        tp2o.append(tmp)
        return np.asarray(tp2o)

    def rotate_pt(p, xi, i):
        rp = []
        a = dx[i][3]
        b = dx[i][4]
        g = dx[i][5]

        Rx = np.matrix([[1, 0, 0],
                        [0, np.cos(a), -np.sin(a)],
                        [0, np.sin(a), np.cos(a)]])

        Ry = np.matrix([[np.cos(b), 0, np.sin(b)],
                        [0, 1, 0],
                        [-np.sin(b), 0, np.cos(b)]])

        Rz = np.matrix([[np.cos(g), -np.sin(g), 0],
                        [np.sin(g), np.cos(g), 0],
                        [0, 0, 1]])

        p = np.squeeze(p)
        tmp = p
        tmp = np.matmul(tmp, Rx)
        tmp = np.matmul(tmp, Ry)
        tmp = np.matmul(tmp, Rz)
        rp.append(tmp)
        return np.asarray(rp)

    def trans_pt_2_cg_instance(p, xi, i):
        tp2ci = []
        T = np.matrix([[1, 0, 0, -xi[0]],
                       [0, 1, 0, -xi[1]],
                       [0, 0, 1, -xi[2]],
                       [0, 0, 0, 1]])

        invT = np.linalg.inv(T)
        tmp = np.insert(p, 3, 1)
        tmp = np.matmul(invT, tmp)
        tmp = np.delete(tmp, 3)

        tp2ci.append(tmp)
        return np.asarray(tp2ci)

    for i, inst in enumerate(cg_path):
        pt_f1 = trans_pt_by_sig(pt, inst, i)
        pt_f2 = trans_pt_2_origin(pt_f1, inst, i)
        pt_f3 = rotate_pt(pt_f2, inst, i)
        pt_f4 = trans_pt_2_cg_instance(pt_f3, inst, i)
        pt_path.append(pt_f4)

    return np.asarray(pt_path)


print pts

pt_copy = []
for p in pts:
    pt_copy.append(p)
pt_path = np.asarray([create_pt_paths(cg_path, dx, pt=p) for p in pt_copy])
pt_path = np.squeeze(pt_path)
print pts


x_t = pt_path
N_trajectories = len(pts)




# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((1300, 1800))
ax.set_ylim((-250, 250))
ax.set_zlim((-250, 250))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines+pts

# animation function.  This will be called sequentially with the frame number
def animate(i):

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    # ax.view_init(30, 0.3 * i)  ## changed!
    # fig.canvas.draw()
    return lines+pts

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=3, blit=False)

# Save as mp4. This requires mplayer or ffmpeg to be installed
# anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()