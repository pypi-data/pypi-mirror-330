import numpy as np
from curvedpy.geodesics.blackhole import BlackholeGeodesicIntegrator
from curvedpy.utils.utils import getImpactParam
import random
import os
import pickle 
import time
from multiprocess import Process, Manager, Pool, cpu_count #Queue
from functools import partial


#import mathutils # I do not want to use this in the end but need to check with how Blender rotates things compared to scipy
from scipy.spatial.transform import Rotation
 
class RelativisticCamera:

    # https://en.wikipedia.org/wiki/Euler_angles
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html#scipy.spatial.transform.Rotation.from_euler
    #start_R = Rotation.from_euler(seq='XYZ', angles=[0, 90, 0], degrees=True)
    start_R = Rotation.from_euler('x', 0, degrees=True)
    #rot = Rotation.from_euler('x', 45, degrees=True)#.as_matrix()

    def __init__(self,  camera_location = np.array([0.0001, 0, 30]), \
                        camera_rotation_euler_props=['x', 0], \
                        resolution = [64, 64],\
                        field_of_view = [0.3, 0.3],\
                        coordinates = "",\
                        M=1.0, \
                        a = 0.0,\
                        theta_switch = "",\
                        samples = 1,\
                        sampling_seed = 43,\
                        y_lim = [], x_lim = [],\
                        max_step = np.inf,\
                        verbose=False,\
                        verbose_init = True):

        self.verbose = verbose

        self.M = M
        self.a = a
        self.theta_switch = theta_switch

        self.camera_location = camera_location
        self.camera_rotation_euler_props = camera_rotation_euler_props
        self.camera_rotation_euler = Rotation.from_euler(camera_rotation_euler_props[0], camera_rotation_euler_props[1], degrees=True)
        self.camera_rotation_matrix = self.camera_rotation_euler.as_matrix()

        self.field_of_view = field_of_view
        self.field_of_view_x, self.field_of_view_y = self.field_of_view

        self.height, self.width = resolution

        if len(y_lim) == 0: self.y_lim = [0, self.height]
        else: self.y_lim = y_lim
        if len(x_lim) == 0: self.x_lim = [0, self.width]
        else: self.x_lim = x_lim

        self.aspectratio = self.height/self.width
        
        self.dy = self.aspectratio/self.height  
        self.dx = 1/self.width  
        random.seed(sampling_seed)  
        self.samples = samples
        self.N = self.samples*self.width*self.height

        self.max_step = max_step
        if coordinates == "":
            coordinates = "SPH2PATCH"
        self.coordinates = coordinates


        if self.theta_switch == "":
            self.gi = BlackholeGeodesicIntegrator(mass=self.M, a=self.a, coordinates=self.coordinates, verbose = self.verbose)
        else:
            self.gi = BlackholeGeodesicIntegrator(mass=self.M, a=self.a, theta_switch = self.theta_switch, coordinates=self.coordinates, verbose = self.verbose)

        self.results = None

        if verbose_init:
            print("Camera Settings: ")
            print(f"  - {self.coordinates=}")
            print(f"  - {self.M=}")
            print(f"  - {self.a=}")
            print(f"  - {self.theta_switch=}")
            print(f"  - {self.verbose=}")
            print(f"  - {verbose_init=}")
            print(f"  - {self.camera_location=}")
            print(f"  - {self.camera_rotation_euler_props=}")
            print(f"  - {resolution=}")
            print(f"  - {field_of_view=}")
            print(f"  - {self.samples=}")
            print(f"  - {sampling_seed=} not supported")
            print(f"  - {self.y_lim=}")
            print(f"  - {self.x_lim=}")
            print(f"  - {self.max_step=}")
            #print(f"  - {force_schwarzschild_integrator=}")
            print("--")



    def filename_suggestion(self):
        fn = "coordinates_"+str(self.coordinates)+"_res_"+str(self.height)+"x"+str(self.width)+\
                "_fov-x_"+str(self.field_of_view_x)+"_fov-y_"+str(self.field_of_view_y)+\
                "_a_"+str(self.a)+"_M_"+str(self.M)+\
                "_xyz0_"+str(self.camera_location[0])+"_"+str(self.camera_location[1])+"_"+str(self.camera_location[2])+\
                f"_rot_{self.camera_rotation_euler_props[0]}_angle_{self.camera_rotation_euler_props[1]}"+\
                "_max_step_"+str(self.max_step)
                #"_rot_"+rot_axis+"_angle_"+str(degrees)

        # if self.schwarzschild_integrator:
        #     fn += "_forceSS_"+str(self.schwarzschild_integrator)
        return fn

    def cam_information_dict(self):
        return \
            {"M":self.M, "a":self.a, "camera_location": self.camera_location, \
            "camera_rotation_euler_props":self.camera_rotation_euler_props, \
            "field_of_view": self.field_of_view, \
            "height":self.height, "width":self.width,\
            "y_lim":self.y_lim, "x_lim":self.x_lim,\
            "max_step":self.max_step,"coordinates":self.coordinates,\
            }

    def get_x_render(self, x):
        return self.field_of_view_x * (x-int(self.width/2))/self.width
    def get_y_render(self, y):
        return self.field_of_view_y * (y-int(self.height/2))/self.height * self.aspectratio 
    def get_ray_direction(self, y_render, x_render):
        ray_direction = np.array( [ x_render, y_render, -1 ] )
        # The ray direction relative to the camera
        ray_direction = self.camera_rotation_matrix @ ray_direction
        # Normalize the direction ray
        ray_direction = ray_direction / np.linalg.norm(ray_direction)
        return ray_direction

    def get_start_values(self, verbose=False, verbose_lvl = 1):

        self.ray_end = np.zeros(self.width * self.height * 6) # The six is for 3 end coordinates and 3 end directions
        self.ray_end.shape = self.height, self.width, 6

        self.ray_blackhole_hit = np.zeros(self.width * self.height * 1)
        self.ray_blackhole_hit.shape = self.height, self.width


        k0, x0, pixel_coordinates = [], [], []

        for s in range(self.samples):
            for y in range(self.height):
                if y >= self.y_lim[0] and y <= self.y_lim[1]:
                    y_render = self.get_y_render(y)#self.field_of_view_y * (y-int(self.height/2))/self.height * self.aspectratio 
                    for x  in range(self.width):
                        if x >= self.x_lim[0] and x <= self.x_lim[1]:
                            x_render = self.get_x_render(x)#self.field_of_view_x * (x-int(self.width/2))/self.width

                            # The ray direction in the -z direction:
                            # ray_direction = np.array( [ x_render + self.dx*(random.random()-0.5), y_render + self.dy*(random.random()-0.5), -1 ] )
                            # ray_direction = np.array( [ x_render, y_render, -1 ] )

                            # # The ray direction relative to the camera
                            # ray_direction = self.camera_rotation_matrix @ ray_direction
                            # # Normalize the direction ray
                            # ray_direction = ray_direction / np.linalg.norm(ray_direction)

                            k0.append(self.get_ray_direction(y_render, x_render))
                            x0.append(self.camera_location)
                            pixel_coordinates.append((y,x))

        return k0, x0, pixel_coordinates

    #def get_start_values_radial_line(self, verbose=False):

    def get_camera_vis_properties(self, scale=5):
        corners = [(0,0), (0,self.width), (self.height, self.width), (self.height, 0)]
        corner_rays = [scale*self.get_ray_direction(self.get_y_render(y), self.get_x_render(x)) for y, x in corners]
        corner_points = [self.camera_location+c for c in [*corner_rays, corner_rays[0]]] # Add the first one to make a closed loop for plotting

        # PLOTTING EXAMPLE!
        # ax = plt.figure().add_subplot(projection='3d')
        # ax.view_init(elev=0, azim=90, roll=0)
        # lim = 5
        # ax.set_xlabel("x")
        # ax.set_xlim(-lim,lim)
        # ax.set_ylim(-lim,lim)
        # ax.set_zlim(20,31)

        # for c in corner_rays:
        #     ax.quiver(*camera_location, *c, color="k")
        # ax.plot(*list(zip(*corner_points)))

        return self.camera_location, corner_points, corner_rays


    def run_mp(self, verbose=False, cores = cpu_count(), *args, **kargs):
        self.ray_end = np.zeros(self.width * self.height * 6) # The six is for 3 end coordinates and 3 end directions
        self.ray_end.shape = self.height, self.width, 6

        self.ray_blackhole_hit = np.zeros(self.width * self.height * 1)
        self.ray_blackhole_hit.shape = self.height, self.width

        # Geodesics have different lengths, so we use lists to save them
        self.geodesics = []

        if verbose: print(f"Starting run_mp on {cores=}")
        k0, x0, self.pixel_coordinates = self.get_start_values()
        if verbose: print(f"  We have {len(k0)} models to run at {self.height}x{self.width}")

        start_values = list(zip(np.array_split(k0, cores), np.array_split(x0, cores)))
        
        def wrap_calc_trajectory(k0_xyz, x0_xyz, shared, mes="no mes"):
            res = shared['gi'].geodesic(k0_xyz = k0_xyz, x0_xyz = x0_xyz, max_step = self.max_step, verbose=False, *args, **kargs)
            return res

        with Manager() as manager:
            shared = manager.dict()
            shared['gi'] = self.gi
            #_ = time.time()
            partial_wrap_calc_trajectory = partial(wrap_calc_trajectory, shared=shared)
            with Pool(cores) as pool:
                results_pool = pool.starmap(partial_wrap_calc_trajectory, start_values)

        self.results = [ x for xs in results_pool for x in xs]
        #self.ray_end[y, x, 0:3] = list(zip(*x_xyz))[-1]
        #self.ray_end[y, x, 3:6] = list(zip(*k_xyz))[-1]

        for i in range(len(self.pixel_coordinates)):
            y, x = self.pixel_coordinates[i]
            # if y==16 and x == 32:
            #     print(y, x, self.results[i][2])#["hit_blackhole"], )

            if isinstance(self.results[i][2], list):
                self.ray_blackhole_hit[y, x] = int(self.results[i][2][-1].hit_blackhole)
            else:
                self.ray_blackhole_hit[y, x] = int(self.results[i][2]["hit_blackhole"])
            k_xyz, x_xyz = self.results[i][0], self.results[i][1]
            self.geodesics.append([k_xyz, x_xyz])
            #print("plplpl", x_xyz)

            #print(f"Strating point is {list(zip(*x_xyz))[0]} and should be {x0[i]}")
            #print(f"Strating k is {list(zip(*k_xyz))[0]} and should be {k0[i]}")

            self.ray_end[y, x, 0:3] = list(zip(*x_xyz))[-1]
            self.ray_end[y, x, 3:6] = list(zip(*k_xyz))[-1]
            
        #MOET NOG DE RAY_END EN DERGELIJKE SETTEN!
        if verbose: print(f"  Running is done and we have {len(self.results)} results")


    # def run(self, verbose=False, verbose_lvl = 1):

    #     self.ray_end = np.zeros(self.width * self.height * 6) # The six is for 3 end coordinates and 3 end directions
    #     self.ray_end.shape = self.height, self.width, 6

    #     self.ray_blackhole_hit = np.zeros(self.width * self.height * 1)
    #     self.ray_blackhole_hit.shape = self.height, self.width



    #     #camera_locations = []
    #     #ray_directions = []

    #     self.results = []
    #     start = time.time()
    #     for s in range(self.samples):
    #         for y in range(self.height):
    #             if y%verbose_lvl == 0 and verbose:
    #                 print(" Status, starting y: ", y, ", elap time: ", round(time.time()-start, 5))
    #             y_render = self.field_of_view_y * (y-int(self.height/2))/self.height * self.aspectratio 
                
    #             # temp. store the geodesics in the width direction

    #             for x  in range(self.width):

    #                 #camera_locations.append(self.camera_location)

    #                 x_render = self.field_of_view_x * (x-int(self.width/2))/self.width

    #                 # The ray direction in the -z direction:
    #                 # ray_direction = np.array( [ x_render + self.dx*(random.random()-0.5), y_render + self.dy*(random.random()-0.5), -1 ] )
    #                 ray_direction = np.array( [ x_render, y_render, -1 ] )

    #                 # The ray direction relative to the camera
    #                 ray_direction = self.camera_rotation_matrix @ ray_direction
    #                 # Normalize the direction ray
    #                 ray_direction = ray_direction / np.linalg.norm(ray_direction)

    #                 #ray_directions.append(ray_direction)

    #                 k_xyz, x_xyz, res = self.gi.geodesic( k0_xyz = ray_direction, \
    #                                             x0_xyz = self.camera_location,\
    #                                             R_end = -1,\
    #                                             curve_start = 0, \
    #                                             curve_end = 50, \
    #                                             nr_points_curve = 50, \
    #                                             method = "RK45",\
    #                                             max_step = self.max_step,\
    #                                             first_step = None,\
    #                                             rtol = 1e-3,\
    #                                             atol = 1e-6,\
    #                                             verbose = self.verbose \
    #                                             )
    #                 #print(list(zip(*x_xyz))[0], list(zip(*k_xyz))[0])
    #                 #print(x_xyz.shape, x_xyz[-1].shape)

    #                 self.ray_end[y, x, 0:3] = list(zip(*x_xyz))[-1]# x_xyz[-1]#, *k_xyz[-1]]
    #                 self.ray_end[y, x, 3:6] = list(zip(*k_xyz))[-1]

    #                 self.ray_blackhole_hit[y, x] = int(res.hit_blackhole)

    #                 self.results.append([k_xyz, x_xyz, res])
    #                 geodesics_width.append([k_xyz, x_xyz])

    #             # Save the goedesics in the width direction into the global list of geodesics
    #             self.geodesics.append(geodesics_width)

    def save(self, fname, directory):
        if os.path.isdir(directory):
            with open(os.path.join(directory, fname+'.pkl'), 'wb') as f:
                info = self.cam_information_dict()
                pickle.dump({"info": info, "geodesics": self.geodesics, "pixel_coordinates": self.pixel_coordinates, \
                    "results": self.results, "ray_end": self.ray_end, "ray_blackhole_hit": self.ray_blackhole_hit}, f)

        else:
            print("dir not found")

    def save_minimal(self, fname, directory="."):
        extension = ".csv"
        if os.path.isdir(directory):
            x, y, z = self.ray_end[:,:,0], self.ray_end[:,:,1], self.ray_end[:,:,2]
            kx, ky, kz = self.ray_end[:,:,3], self.ray_end[:,:,4], self.ray_end[:,:,5]

            h = "Cartesian x component in 3-space of end direction of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'k_x_'+fname+extension), kx, header = h)
            h = "Cartesian y component in 3-space of end direction of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'k_y_'+fname+extension), ky, header=h)
            h = "Cartesian z component in 3-space of end direction of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'k_z_'+fname+extension), kz, header=h)

            h = "Cartesian x component in 3-space of end point of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'x_'+fname+extension), x, header=h)
            h = "Cartesian y component in 3-space of end point of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'y_'+fname+extension), y, header=h)
            h = "Cartesian z component in 3-space of end point of a photon. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'z_'+fname+extension), z, header=h)

            h = "Hit blackhole: 1 if the photon end in the black hole and 0 if not. \n"+\
                "Rows are camera height direction, columns are width direction. \n"+\
                "You can, for example, load this file using numpy.loadtxt. \n"+\
                str(self.cam_information_dict())
            np.savetxt(os.path.join(directory, 'hit_blackhole'+extension), self.ray_blackhole_hit, header=h)

            with open(os.path.join(directory, "full_geodesics_"+fname+'.pkl'), 'wb') as f:
                k, x, res = list(zip(*self.results))
                pickle.dump({"cam_info": self.cam_information_dict(), "k":k, "x":x }, f)

    


    def load(self, filepath):
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                filecontent = pickle.load(f)
                print(filecontent.keys())
                self.results = filecontent["results"]
                self.ray_end = filecontent["ray_end"]
                self.ray_blackhole_hit = filecontent["ray_blackhole_hit"]
                self.pixel_coordinates = filecontent["pixel_coordinates"]
        else:

            print(f"CAM: FILE NOT FOUND {filepath}")




    # DEBUG FUNCTIONS
    def calcStats(self, select_by_impact_parameter = [0, np.inf]):
        stats = []
        for el in self.results:
            k, x, res = el
            x0 = np.column_stack(x)[0]
            #print(x0)
            k0 = np.column_stack(k)[0]
            impact_vector_normed, impact_par = getImpactParam(x0, k0)
            if impact_par >= select_by_impact_parameter[0] and impact_par <= select_by_impact_parameter[1]:
                x_end = np.column_stack(x)[-1]
                k_end = np.column_stack(k)[-1]
                deflect = k_end.dot(k0)
                hit = int(res.hit_blackhole)
                stats.append((x0, k0, x_end, k_end, impact_vector_normed, impact_par, deflect, hit))

        x0, k0, x_end, k_end, impact_vector_normed, impact_par, deflect, hit = list(zip(*stats))
        
        return {"x0":x0, "k0":k0, "x_end":x_end, "k_end":k_end, "impact_vector_normed":impact_vector_normed, \
                "impact_par":impact_par, "deflect":deflect, "hit":hit}

    #def deflectImage(self):



# Or do the follwoing:
# np.array(cameuler.to_matrix())
# np.array(bpy.data.scenes['Scene'].camera.matrix_world.to_euler().to_matrix())@np.array([0,0,-1])

# The standard direction from which the rotation is measured in Blender is the 0,0,-1 direction, So downwards in the z direction


# Do the following inside blender:
# Get the Euler rotation of the camera:
# cam_euler = bpy.data.scenes['Scene'].camera.matrix_world.to_euler()
# Put this rotation in a scipy rotation:
# r = Rotation.from_euler(cam_euler.order, [cam_euler.x, cam_euler.y, cam_euler.z], degrees=False)
# Give this r as camera_rotation to this class


# For more information:
# Eurler rotations in Blender are given like this:
# cameuler = C.scene.camera.matrix_world.to_euler()
# > Euler((1.1093189716339111, -0.0, 0.8149281740188599), 'XYZ')
# (https://blender.stackexchange.com/questions/130948/blender-api-get-current-location-and-rotation-of-camera-tracking-an-object)
# cameuler.order gives the 'XYZ'
# 

# In scipy a rotation can be created using:
# r = Rotation.from_euler('zyx', [90, 45, 30], degrees=True)
