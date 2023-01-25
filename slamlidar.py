import rplidar
import numpy as np
from slam import SLAM

# Connect to RPLIDAR
lidar = rplidar.RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.start()

# Create SLAM object
slam = SLAM()

# Initialize map
slam.initialize_map(500, 500, 0.1)

try:
    for scan in lidar.iter_scans():
        # Get lidar data
        angles = np.array([scan[i][1] for i in range(len(scan))])
        distances = np.array([scan[i][2] for i in range(len(scan))])

        # Update SLAM with lidar data
        slam.update(angles, distances)

        # Get current map
        map = slam.get_map()

finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
