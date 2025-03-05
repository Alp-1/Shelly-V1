![shelly-banner](https://github.com/user-attachments/assets/eb581776-ccef-45be-9879-fe92661eba2b)

SHELLY is an ultra-low-cost amphibious legged robot developed for the Biologically Inspired Robotics module at the University of Southampton. The platform was designed for biome surveying across the land-water boundary, with turtle-inspired gaits for both land and aquatic locomotion.

The robot uses two repurposed electric screwdriver motors driving four 1-DOF legs through a GT2 belt and pulley system, housed in a 3D-printed PLA body waterproofed with acetone smoothing, epoxy coating, a dual-trench rubber gasket seal, and a vaseline wax shaft mechanism. Control is provided via a Flutter web interface hosted on a Raspberry Pi 3B+, with a Pi Camera Module 3 NoIR for live streaming on land and mission recording underwater. The total system cost was approximately £220.

Contributions to hardware design, sensor integration, and on-device development are not reflected in the commit history.

> **Note:** Some files are not publicly available due to university policy. Some links may also be broken as a result of migration.

## System Architecture

```
Flutter UI (browser)
├── Land mode: WASD / arrow buttons
│     → GET /land?query=forward
│     → backend.py sets Controller flags
│     → controlLoop() checks flags
│     → movement_functions_ground: hardcoded differential PWM
│     → pigpio.set_servo_pulsewidth()
│
├── Water mode: drag-drop mission builder
│     → GET /water?commands=Forward,100,Left,20,...
│     → backend.py sets Controller.mission_array
│     → controlLoop() iterates mission_array
│     → np.linspace angle trajectory arrays (sinusoidal sweep)
│     → movement_functions: PID angle tracking per motor
│     → pigpio.set_servo_pulsewidth()
│
└── Settings: sliders
      → GET /settings?speed=2&quality=50...
      → backend.py sets speed_mode, camera controls
```

## Gaits

On land, the robot employs a gait in which the legs on either side operate 180 degrees out of phase. This configuration allows one side of the robot to lift while the other side supports the body weight, reducing the impact stress on the structure during movement.

In water, the system uses a restricted flapping motion, avoiding full rotations to prevent counterproductive forces. The legs perform synchronized limited-arc movements defined by sinusoidal angle trajectories (e.g. 30-150-30 degrees for forward), with PID controllers tracking the setpoints via AS5600 magnetic encoders. Different trajectory profiles produce different movements (forward, up/down, turning), and the mission builder allows sequencing these into timed mission plans executed without WiFi connectivity underwater.

## Sensors

- 2x AS5600 magnetic encoders (12-bit, I2C via RP2040 Pico over serial)
- BNO085 9-DOF IMU (heading for ground mode PID correction)
- Pi Camera Module 3 NoIR (live stream on land, recording underwater)

## Unit Pamphlet

![Pamphlet](https://github.com/user-attachments/assets/1aca5fb8-ff1d-41e5-8dca-10b2439dd2c5)
