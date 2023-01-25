import carla
import random
import time
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
count=0
#f = open("demofile2.txt", "a")
# Connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)
client.set_timeout(200.0)
world = client.get_world()
#spawnPoint=carla.Transform(carla.Location(x=-108,y=90, z=1),carla.Rotation(pitch=0.0, yaw=270.0, roll=0.000000))
spawnPoint=carla.Transform(carla.Location(x=45,y=-62, z=1),carla.Rotation(pitch=0.0, yaw=0.0, roll=0.000000))
#Processing
def processing(data):
    global count
    data=np.reshape(data, (int(data.shape[0] / 4), 4))
    for data1 in data:
        #f.write(str(data1))
        print(data1[0], data1[1])
        if 0 < data1[0] < 7:
            if -7 < data1[1] < 7:
                count = count + 1
                #print(data1[0], data1[1])
                if count > 2:
                    ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=10))
                    print("break")
        else:
            count = 0



# Get the blueprint library and filter for the vehicle blueprints
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle.bmw.*')

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()

ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), spawnPoint)

ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))

# --------------
# Add a new LIDAR sensor to my ego
# --------------
lidar_cam = None
lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
lidar_bp.set_attribute('channels',str(1))
lidar_bp.set_attribute('points_per_second',str(8000))
#lidar_bp.set_attribute('rotation_frequency',str(5.5))
lidar_bp.set_attribute('range',str(12))
lidar_bp.set_attribute('upper_fov',str(0))
lidar_bp.set_attribute('lower_fov',str(0))
lidar_location = carla.Location(0,0,2)
lidar_rotation = carla.Rotation(0,0,0)
lidar_transform = carla.Transform(lidar_location,lidar_rotation)
lidar_sen = world.spawn_actor(lidar_bp,lidar_transform,attach_to=ego_vehicle)
lidar_sen.listen(lambda point_cloud:processing(np.frombuffer(point_cloud.raw_data, dtype=np.dtype('f4'))))
#lidar_sen.listen(lambda point_cloud: point_cloud.save_to_disk('tutorial/new_lidar_output/%.6d.ply' % point_cloud.frame))

time.sleep(80)
#f.close()