#
# BSD 3-Clause License
#
# Copyright (c) 2022 University of Wisconsin - Madison
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.#

# General Imports
import numpy as np
import os

# Chrono Imports
import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as irr
import pychrono.sensor as sens

#// =============================================================================

def main():
    
    def AddRandomCones(count, filename, class_id=1):
        mmesh = chrono.ChTriangleMeshConnected()
        mmesh.LoadWavefrontMesh(filename, False, True)  
        mmesh.Transform(chrono.ChVectorD(0, 0, 0), chrono.ChMatrix33D(1)) 
        for i in range(count):
            # Generate a random position
            x = (chrono.ChRandom() - .5) * cone_spread_x + cone_offset_x
            y = (chrono.ChRandom() - .5) * cone_spread_y + cone_offset_y
            z = terrain.GetHeight(chrono.ChVectorD(x, y, 1000)) # get the terrain z
            pos = chrono.ChVectorD(x, y, z)

            trimesh_shape = chrono.ChTriangleMeshShape()
            trimesh_shape.SetMesh(mmesh)
            trimesh_shape.SetName(filename)
            trimesh_shape.SetMutable(False)
            trimesh_shape.SetScale(chrono.ChVectorD(1, 1, 1))

            mesh_body = chrono.ChBody()
            mesh_body.SetPos(pos)
            mesh_body.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))
            mesh_body.AddVisualShape(trimesh_shape)
            mesh_body.SetBodyFixed(True)
            vehicle.GetSystem().Add(mesh_body)

            if (class_id == 1):
                red_cone_assets.append(trimesh_shape)
                red_cones.append(mesh_body)
            else:
                green_cone_assets.append(trimesh_shape)
                green_cones.append(mesh_body)

    def AddConesFromFile():
        green_cone_mesh = chrono.ChTriangleMeshConnected()
        green_cone_mesh.LoadWavefrontMesh(chrono.GetChronoDataFile("sensor/cones/green_cone.obj"), False, True) 
        green_cone_mesh.Transform(chrono.ChVectorD(0, 0, 0), chrono.ChMatrix33D(1))

        red_cone_mesh = chrono.ChTriangleMeshConnected()
        red_cone_mesh.LoadWavefrontMesh(chrono.GetChronoDataFile("sensor/cones/red_cone.obj"), False, True)
        red_cone_mesh.Transform(chrono.ChVectorD(0, 0, 0), chrono.ChMatrix33D(1))

        with open(chrono.GetChronoDataFile("autonomy-toolkit/paths/cone_paths_0.csv")) as cone_file:
            while True:
                line = cone_file.readline()
                if not line:
                    break
                x_inner, y_inner, x_outer, y_outer = map(float, line.split(' ')) 

                pos_green_x = x_inner + cone_offset_x
                pos_green_y = y_inner + cone_offset_y
                pos_green_z = terrain.GetHeight(chrono.ChVectorD(pos_green_x, pos_green_y, 1000))

                pos_red_x = x_outer + cone_offset_x
                pos_red_y = y_outer + cone_offset_y
                pos_red_z = terrain.GetHeight(chrono.ChVectorD(pos_red_x, pos_red_y, 1000))

                pos_green = chrono.ChVectorD(pos_green_x, pos_green_y, pos_green_z)
                pos_red = chrono.ChVectorD(pos_red_x, pos_red_y, pos_red_z)
                rot = chrono.ChQuaternionD(1, 0, 0, 0)

                green_cone_shape = chrono.ChTriangleMeshShape()
                green_cone_shape.SetMesh(green_cone_mesh)
                green_cone_shape.SetName("green_cone_shape")
                # green_cone_shape.SetStatic(True)
                green_cone_shape.SetMutable(False)

                green_cone_assets.append(green_cone_shape)
                green_body = chrono.ChBody()
                green_body.SetPos(pos_green)
                green_body.SetRot(rot)
                green_body.AddVisualShape(green_cone_shape)
                green_body.SetBodyFixed(True)
                green_cones.append(green_body)
                vehicle.GetSystem().Add(green_body)

                red_cone_shape = chrono.ChTriangleMeshShape()
                red_cone_shape.SetMesh(red_cone_mesh)
                red_cone_shape.SetName("red_cone_shape")
                # red_cone_shape.SetStatic(True)
                green_cone_shape.SetMutable(False)

                red_cone_assets.append(red_cone_shape)
                red_body = chrono.ChBody()
                red_body.SetPos(pos_red)
                red_body.SetRot(rot)
                red_body.AddVisualShape(red_cone_shape)
                red_body.SetBodyFixed(True)
                red_cones.append(red_body)
                vehicle.GetSystem().Add(red_body)
            
    def LabelConeAssets():
            cone_id = 0
            for cone in red_cone_assets:
                cone_id += 1
                for mat in cone.GetMaterials():
                    mat.SetClassID(1)
                    mat.SetInstanceID(cone_id)


            cone_id = 0
            for cone in green_cone_assets:
                cone_id += 1
                for mat in cone.GetMaterials():
                    mat.SetClassID(2)
                    mat.SetInstanceID(cone_id)

    def RedistributeCones():
        for cone in green_cones:
            x = (chrono.ChRandom() - .5) * cone_spread_x + cone_offset_x
            y = (chrono.ChRandom() - .5) * cone_spread_y + cone_offset_y
            z = terrain.GetHeight((x, y, 1000))
            cone.SetPos((x, y, z))

        for cone in red_cones:
            x = (chrono.ChRandom() - .5) * cone_spread_x + cone_offset_x
            y = (chrono.ChRandom() - .5) * cone_spread_y + cone_offset_y
            z = terrain.GetHeight((x, y, 1000))
            cone.SetPos((x, y, z))



    # Create the ARTcar vehicle, set parameters, and initialize
    vehicle = veh.ARTcar()
    vehicle.SetContactMethod(contact_method)
    vehicle.SetChassisCollisionType(chassis_collision_type)
    vehicle.SetChassisFixed(False)
    vehicle.SetTireType(tire_model)
    vehicle.SetInitPosition(chrono.ChCoordsysD(initLoc, initRot))
    vehicle.SetTireStepSize(tire_step_size)
    vehicle.Initialize()


    vehicle.SetChassisVisualizationType(chassis_vis_type)
    vehicle.SetSuspensionVisualizationType(suspension_vis_type)
    vehicle.SetSteeringVisualizationType(steering_vis_type)
    vehicle.SetWheelVisualizationType(wheel_vis_type)
    vehicle.SetTireVisualizationType(tire_vis_type)

    # Create the terrain
    terrain = veh.RigidTerrain(vehicle.GetSystem())

    patch_mat = chrono.ChMaterialSurfaceNSC()
    patch_mat.SetFriction(0.9)
    patch_mat.SetRestitution(0.01) #-----check if mu, cr, and y is set similar to minfo

    # not right need to introduce point cloud -- not sure how to access this using the package_share_directory
    patch = terrain.AddPatch(patch_mat, chrono.CSYSNORM, chrono.GetChronoDataFile("autonomy-toolkit/me3038/rm3038_pt_cloud.obj"))  #chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.ChQuaternionD(1, 0, 0, 0))
    # patch.SetTexture(veh.GetDataFile("terrain/textures/tile4.jpg"), 200, 200)
    # patch.SetColor(chrono.ChColor(0.8, 0.8, 0.5))
    terrain.Initialize()

    # add in ME3038 room mesh
    room_mmesh = chrono.ChTriangleMeshConnected()
    room_mmesh.LoadWavefrontMesh(chrono.GetChronoDataFile("autonomy-toolkit/me3038/rm3038_pt_cloud.obj"), False, True)
    room_mmesh.Transform(chrono.ChVectorD(0, 0, 0), chrono.ChMatrix33D(1))

    room_trimesh_shape = chrono.ChTriangleMeshShape()
    room_trimesh_shape.SetMesh(room_mmesh)
    room_trimesh_shape.SetName("ME3038")
    room_trimesh_shape.SetMutable(False)

    room_mesh_body = chrono.ChBody()
    room_mesh_body.SetPos(chrono.ChVectorD(0, 0, 0))
    room_mesh_body.AddVisualShape(room_trimesh_shape)
    room_mesh_body.SetBodyFixed(True)

    vehicle.GetSystem().Add(room_mesh_body)


    if cones_from_file:
        AddConesFromFile()
    else:
        AddRandomCones(int(num_cones / 2), chrono.GetChronoDataFile("sensor/cones/green_cone.obj"), 2)
        AddRandomCones(int(num_cones / 2), chrono.GetChronoDataFile("sensor/cones/red_cone.obj"), 1)

    # === create sensors ===
    manager = sens.ChSensorManager(vehicle.GetSystem())
    manager.scene.AddPointLight(chrono.ChVectorF(100, 100, 100), chrono.ChColor(1, 1, 1), 5000)
    
    b = sens.Background()
    b.color_horizon = chrono.ChVectorF(.6, .7, .8)
    b.color_zenith = chrono.ChVectorF(.4, .5, .6)
    b.mode = sens.BackgroundMode_GRADIENT
    manager.scene.SetBackground(b)

    camera_pose = chrono.ChFrameD(chrono.ChVectorD(0.204, 0, 0.10018), chrono.Q_from_AngAxis(.2, chrono.ChVectorD(0, 1, 0)))
    width = 1280
    height = 720
    frame_rate = 30.0
    if create_semantic_maps:
        frame_rate = float(5)    # not sure about this
    fov = 1.396;  # 80 degree FOV camera)

    camera = sens.ChCameraSensor(
                vehicle.GetChassisBody(), # body camera is attached to
                frame_rate,                 # update rate in Hz
                camera_pose,                # offset pose
                width,                      # image width
                height,                     # image height
                fov,                        # FOV
                2)

    camera.SetName("Camera Sensor")
    c_window = float(0)
    camera.SetCollectionWindow(c_window)

    # camera.PushFilter(sens.ChFilterVisualize(640, 360))

    if save_sensor_data:
        camera.PushFilter(sens.ChFilterSave(sensor_data_dir + "cam1/"))

    camera.PushFilter(sens.ChFilterRGBA8Access())
    manager.AddSensor(camera)


    camera2 = sens.ChCameraSensor(
                patch.GetGroundBody(),  # body camera is attached to
                30,                      # update rate in Hz
                chrono.ChFrameD(chrono.ChVectorD(init_loc_x + 2, init_loc_y, 10), 
                chrono.Q_from_AngAxis(chrono.CH_C_PI_2, chrono.ChVectorD(0, 1, 0))),  # offset pose   ------ not sure what CH_C_PI_2 is
                1280,                                                           # image width
                720,                                                            # image height
                3.14 / 4,                                                       # FOV
                2)                                                              # super sample diameter
    camera2.SetName("Camera Sensor 2")
    # camera2.PushFilter(sens.ChFilterVisualize(1280, 720))
    if save_sensor_data:
        camera2.PushFilter(sens.ChFilterSave(sensor_data_dir + "cam2/"))
    manager.AddSensor(camera2)


    noise_model = sens.ChNoiseNone()
    imu_offset_pose = chrono.ChFrameD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngAxis(0, chrono.ChVectorD(1, 0, 0)))
    gps_offset_pose = chrono.ChFrameD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngAxis(0, chrono.ChVectorD(1, 0, 0)))
    gps_reference = chrono.ChVectorD(-89.400, 43.070, 260.0)

    # accelerometer
    acc = sens.ChAccelerometerSensor(vehicle.GetChassisBody(), 100, imu_offset_pose, noise_model)
    acc.SetName("IMU - Accelerometer")
    acc.PushFilter(sens.ChFilterAccelAccess())
    manager.AddSensor(acc)

    # gyroscope
    gyro = sens.ChGyroscopeSensor(vehicle.GetChassisBody(), 100, imu_offset_pose, noise_model)
    gyro.SetName("IMU - Gyroscope")
    gyro.PushFilter(sens.ChFilterGyroAccess())
    manager.AddSensor(gyro)

    # magnetometer
    mag = sens.ChMagnetometerSensor(vehicle.GetChassisBody(), 100, imu_offset_pose, noise_model, gps_reference)
    mag.SetName("IMU - Magnetometer")
    mag.PushFilter(sens.ChFilterMagnetAccess())
    manager.AddSensor(mag)

    # gps
    gps = sens.ChGPSSensor(vehicle.GetChassisBody(), 10, gps_offset_pose, gps_reference, noise_model)
    gps.SetName("GPS")
    gps.PushFilter(sens.ChFilterGPSAccess())
    manager.AddSensor(gps)

    # label the cones that were added to the scene with semantic information
    manager.ReconstructScenes()
    LabelConeAssets()
    manager.ReconstructScenes()

    # Create the vehicle Irrlicht interface

    vis = veh.ChWheeledVehicleVisualSystemIrrlicht()
    vis.SetWindowTitle('dart')
    vis.SetWindowSize(1280, 1024)
    vis.SetChaseCamera(trackPoint, 4.0, 0.5)
    vis.Initialize()
    vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
    vis.AddLightDirectional()
    vis.AddSkyBox()
    vis.AttachVehicle(vehicle.GetVehicle())


    driver_data = veh.vector_Entry([veh.DataDriverEntry(0.0, 0.0, 0.0, 0.0), 
                                    veh.DataDriverEntry(0.1, -1.0, 0.0, 0.0),
                                    veh.DataDriverEntry(0.5, -1.0, 0.7, 0.0),
                                    ])
    driver = veh.ChDataDriver(vehicle.GetVehicle(), driver_data)
    driver.Initialize()

    # Simulation loop
    realtime_timer = chrono.ChRealtimeStepTimer()
    
    
    render_step = 10
    step_number = 0
    while True:
        time = vehicle.GetSystem().GetChTime()

        # Draw scene
        if(step_number % render_step == 0):
            vis.BeginScene()
            vis.Render()
            vis.EndScene()

        # Get driver inputs
        driver_inputs = driver.GetInputs()

        # Update modules (process inputs from other modules)
        driver.Synchronize(time)
        terrain.Synchronize(time)
        vehicle.Synchronize(time, driver_inputs, terrain)
        vis.Synchronize(time, driver_inputs)

        # Advance simulation for one timestep for all modules
        driver.Advance(step_size)
        terrain.Advance(step_size)
        vehicle.Advance(step_size)
        vis.Advance(step_size)

        # Update sensor manager
        # Will render/save/filter automatically
        manager.Update()

        # Spin in place for real time to catch up
        realtime_timer.Spin(step_size)
        
        step_number = step_number + 1
    
    return 0       
    

# The path to the Chrono data directory containing various assets (meshes, textures, data files)
# is automatically set, relative to the default location of this demo.
# If running from a different directory, you must change the path to the data directory with: 
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "")
chrono.SetChronoDataPath(data_folder)
veh.SetDataPath(chrono.GetChronoDataPath() + 'vehicle/')

create_semantic_maps = False
save_sensor_data = False
sensor_data_dir = "sensor_output/"

num_cones = 100
cones_from_file = True
cone_path_file = "data/paths/cone_paths_0.csv"

cone_offset_x = 0
cone_offset_y = 0
cone_spread_x = 1.0
cone_spread_y = 1.0

throttle_scaling = .5 * abs(1400.0 - 1500.0) / (1980.0 - 1500.0) # based on motor_driver.py limits for safety
braking_scaling = abs(1600.0 - 1500.0) / (1980.0 - 1500.0)  # based on motor_driver.py limits for safety
steering_scaling = 1.0  # abs(1725.0 - 1500.0) / (1980.0 - 1500.0);  // based on motor_driver.py limits for safety

trackPoint = chrono.ChVectorD(0.0, 0.0, 1.75)

throttle = 0.0
braking = 0.0
steering = 0.0

red_cone_assets = list()
green_cone_assets = list()


red_cones = list()
green_cones = list()

# Initial vehicle location
init_loc_x = -2.5
init_loc_y = 0.5
init_angle_z = 1.57

initLoc = chrono.ChVectorD(init_loc_x, init_loc_y, 0.5)
initRot = chrono.Q_from_AngZ(init_angle_z)

# Visualization type for vehicle parts (PRIMITIVES, MESH, or NONE)
chassis_vis_type = veh.VisualizationType_PRIMITIVES
suspension_vis_type = veh.VisualizationType_PRIMITIVES
steering_vis_type = veh.VisualizationType_PRIMITIVES
wheel_vis_type = veh.VisualizationType_MESH
tire_vis_type = veh.VisualizationType_MESH

# Collision type for chassis (PRIMITIVES, MESH, or NONE)
chassis_collision_type = veh.CollisionType_NONE

# Type of tire model (RIGID, TMEASY)
tire_model = veh.TireModelType_TMEASY

# Rigid terrain -- not sure about this
terrainHeight = -.2339      # terrain height (FLAT terrain only)
terrainLength = 7.0  # size in X direction
terrainWidth = 7.0   # size in Y direction

# Contact method
contact_method = chrono.ChContactMethod_NSC
# contact_vis = False

# Flag to activate irrlicht
USE_IRRLICHT = False

# Simulation step sizes
step_size = 1e-3
tire_step_size = step_size

# Simulation end time
t_end = 1000

main()

