from rplidar import RPLidar

def main():
    lidar = RPLidar('/dev/ttyUSB0')


    info = lidar.get_info()
    print(info)

    health = lidar.get_health()
    print(health)

    for i, scan in enumerate(lidar.iter_scans()):
        print('%d: Got %d measurments' % (i, len(scan)))
        createData(scan)
        if i > 10:
            break

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

def createData(data):
    for daten  in data:
        print(daten)


main()
