# Simulation setup

This is the Step 2 baseline for the tabletop simulator. The project uses Ubuntu 24.04 in WSL2, ROS 2 Jazzy, and Gazebo Harmonic. ROS and Gazebo are installed as Ubuntu packages inside the WSL distribution. The repository holds the world, bridge configuration, and launch file; it does not vendor either installation.

## Storage layout on this workstation

| Location | Purpose |
| --- | --- |
| `Z:\WSL\Ubuntu-24.04\ext4.vhdx` | Ubuntu filesystem, ROS/Gazebo packages, apt cache, ROS logs, and Linux user files |
| `Z:\Robotics-AI-Agent` | Project source, ROS workspace, and ignored build output |
| `Z:\Robotics-AI-Agent\ros2_ws\src\vortiqo_gazebo` | Project-owned tabletop world, camera bridge, and launch file |

The other installed WSL distributions were left untouched. The new distribution has an `ojas2` user with local passwordless sudo for development. Windows and WSL platform components may use small amounts of system-drive space; the Ubuntu virtual disk and large packages are on Z.

## Recreate the environment

On Windows with WSL2 available, install a new Ubuntu 24.04 distribution on a drive with enough space. Replace the path if your drive is different:

```powershell
wsl --install --distribution Ubuntu-24.04 --location 'Z:\WSL\Ubuntu-24.04'
wsl --distribution Ubuntu-24.04
```

Complete Ubuntu's first-launch user setup. The remaining commands run inside that Ubuntu terminal. The ROS apt source package version used here was `1.3.0` on 2026-10-03; use the current version from the [ROS apt source releases](https://github.com/ros-infrastructure/ros-apt-source/releases) if this file becomes stale.

```bash
sudo apt update
sudo apt install -y ca-certificates curl software-properties-common gnupg locales
sudo add-apt-repository -y universe
sudo locale-gen en_US.UTF-8

curl -fL -o /tmp/ros2-apt-source.deb \
  https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.3.0/ros2-apt-source_1.3.0.noble_all.deb
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update
sudo apt install -y --no-install-recommends \
  ros-jazzy-desktop ros-jazzy-ros-gz \
  ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers \
  ros-jazzy-gz-ros2-control-demos \
  python3-colcon-common-extensions python3-rosdep build-essential
sudo rosdep init
rosdep update
```

The [Gazebo compatibility guide](https://gazebosim.org/docs/harmonic/ros_installation/) identifies Jazzy and Harmonic as the supported pairing. Installing `ros-jazzy-ros-gz` pulls the matching Gazebo vendor packages from the ROS repository. The controller package connects Gazebo joints to ROS 2 control; the demos are used only for the setup check.

## Build and launch the project world

From Windows PowerShell, you can start the simulation using the project wrapper. It builds the ROS package, loads the ROS and workspace environments, and launches Gazebo inside Ubuntu on WSL:

```powershell
.\scripts\launch_sim.ps1
```

Add `-Headless` to run Gazebo without its GUI:

```powershell
.\scripts\launch_sim.ps1 -Headless
```

Do not run `python tabletop.launch.py` from Windows. This file is a ROS 2 launch description, not a standalone Python program; it needs ROS's Python packages and environment, which exist inside the Ubuntu WSL distribution.

In Ubuntu, change to this repository's ROS workspace. This workstation mounts the Z drive at `/mnt/z`:

```bash
source /opt/ros/jazzy/setup.bash
cd /mnt/z/Robotics-AI-Agent/ros2_ws
colcon build --packages-select vortiqo_gazebo
source install/setup.bash
ros2 launch vortiqo_gazebo tabletop.launch.py
```

Use `headless:=true` at the end of the launch command to omit the Gazebo window. The world contains a table, two movable blocks, and a fixed RGB-D camera. It is a sensor and graphics baseline; an arm and gripper will be added in the manipulation milestone.

In a second Ubuntu terminal, inspect the ROS outputs:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic list
ros2 topic echo /table_camera/image --once --field width
ros2 topic echo /table_camera/depth_image --once --field encoding
ros2 topic echo /table_camera/camera_info --once --field width
ros2 topic echo /clock --once --field clock.sec
```

Expected camera topics are `/table_camera/image`, `/table_camera/depth_image`, and `/table_camera/camera_info`. The depth image encoding is `32FC1`. The current RGB image is 640 by 480 pixels. These messages travel from Gazebo Transport through `ros_gz_bridge` into ROS 2.

## Check joint control separately

The project world does not yet contain a selected robot. The installed controller demo checks the same Gazebo-to-ROS control path that the future arm will use:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch gz_ros2_control_demos cart_example_position.launch.py gz_args:=-s
```

In a second terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 control list_controllers
ros2 topic echo /joint_states --once --field position
ros2 run gz_ros2_control_demos example_position
ros2 topic echo /joint_states --once --field position
ros2 topic echo /tf --once
```

The cart joint begins at position `1.0`. The demo sends a trajectory toward `0.0`; its action should succeed, and `/joint_states` and `/tf` should reflect the new position. Stop the launch before starting the tabletop world again.

## Verified on this workstation

- Ubuntu 24.04.5 LTS runs in a WSL2 distribution whose registered base path is `Z:\WSL\Ubuntu-24.04`.
- ROS environment reports `jazzy`; `gz sim --versions` reports `8.15.0` (Gazebo Harmonic).
- WSL sees the NVIDIA RTX 4060 Laptop GPU, and Gazebo's server and GUI launched under WSLg.
- The project world built with `colcon` and published RGB, depth, camera info, and clock messages. A captured RGB frame visibly showed the table and both blocks.
- The controller demo loaded active joint state and trajectory controllers. Its action succeeded and moved the cart from `1.0` to approximately `0.0`; `/tf` published the cart transform.

The next milestone is selecting and integrating an arm, gripper, controllers, and motion planning into the project world. SAM3 remains in its separate Windows Python environment until the perception integration milestone.
