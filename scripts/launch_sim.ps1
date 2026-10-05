[CmdletBinding()]
param(
    [switch]$Headless
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$driveLetter = $repoRoot.Substring(0, 1).ToLowerInvariant()
$repoPathFromDriveRoot = $repoRoot.Substring(2).Replace('\', '/')
$repoLinux = "/mnt/$driveLetter$repoPathFromDriveRoot"
$workspaceLinux = "$repoLinux/ros2_ws"
$quotedWorkspace = "'" + $workspaceLinux.Replace("'", "'\''") + "'"
$headlessArgument = if ($Headless) { ' headless:=true' } else { '' }

$linuxCommand = "source /opt/ros/jazzy/setup.bash && cd $quotedWorkspace && colcon build --packages-select vortiqo_gazebo && source install/setup.bash && ros2 launch vortiqo_gazebo tabletop.launch.py$headlessArgument"

& wsl.exe --distribution Ubuntu-24.04 -- bash -lc $linuxCommand
exit $LASTEXITCODE
