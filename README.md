# Arch ros package monitor

This tooling helps getting an overview of a ROS distribution inside AUR. On execution it creates
three lists:
 * **Missing packages** shows all packages present in the ROS distribution but not inside AUR.
 * **Outdated packages** shows all packages present in the ROS distribution and inside AUR, but
   where the AUR version isn't the same as the one from the ROS distribution
 * **Outofsync packages** shows all packages where the AUR version isn't the same as the one
   from the Github repository inside the ros-<distro>-arch organization. Packages from that list
   probably also show up in the **Outdated packages** list.

For each list each item is printed with all found versions. If the package is found to be installed
on the current system, the installed version is printed, as well.

Each of the lists above can be hidden, as well as the output can be restricted to installed packages
only. See `./check_distro.py --help` for more information.
