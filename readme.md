Remote VMwareLibrary for Robot Framework
========================================
This python package is remote library for **Robot Framework**
that wraps around VMware utility called *vmrun*

vmrun command-line utility is for controling specific virtual machines, or teams of virtual machines.
The vmrun utility is available on any VMware product that includes the VIX API libraries, or when the libraries
are separately installed

#Requirements
To successfully install and run VMwareLibrary one needs to install following
software.

##vmrun
In order to use VMwareLibrary, one needs to install vmrun command line utility.
###Windows
On web page, one can find Automation Tools and SDKs - [VIX SDK for windows](https://my.vmware.com/web/vmware/free#desktop_end_user_computing/vmware_player/6_0|PLAYER-600-A|drivers_tools).
Download the sdk, and install it. Make sure that vmrun.exe is in PATH Environment variable and try _vmrun_ command.

    $ vmrun.exe
    >
    > vmrun version 7.1.5 build-491717
    >
    > Usage: vmrun [AUTHENTICATION-FLAGS] COMMAND [PARAMETERS]
    >
    >
    >
    > AUTHENTICATION-FLAGS
    > --------------------
    > These must appear before the command and any command parameters.
    >
    >    -h   (not needed for Workstation)
    >    -P   (not needed for Workstation)
    >    -T  (ws|server|server1|fusion|esx|vc|player)
    >      for example, use '-T server' for VMware Server 2.0
    >                   use '-T server1' for VMware Server 1.0
    >                   use '-T ws' for VMware Workstation
    >                   use '-T esx' for VMware ESX
    >                   use '-T vc' for VMware vCenter Server
    >    -u   (not needed for Workstation)
    >    -p   (not needed for Workstation)
    >    -vp 
    >    -gu 
    >    -gp 
    >
    >
    >
    > POWER COMMANDS           PARAMETERS           DESCRIPTION
    > --------------           ----------           -----------
    > start                    Path to vmx file     Start a VM or Team
    >                          [gui|nogui]
    >
    > stop                     Path to vmx file     Stop a VM or Team
    >                          [hard|soft]
    >
    > reset                    Path to vmx file     Reset a VM or Team
    >                          [hard|soft]
    >
    > suspend                  Path to vmx file     Suspend a VM or Team
    >                          [hard|soft]
    >
    > pause                    Path to vmx file     Pause a VM
    > ...

###Linux
Automation Tools and SDKs - [VIX SDK for linux32/64](https://my.vmware.com/web/vmware/free#desktop_end_user_computing/vmware_player/6_0|PLAYER-600-A|drivers_tools).
Download the sdk, and install it. Make sure that vmrun is in PATH variable and
try _vmrun_ command. Output should be same as for windows

##Python
One should have installed python 2.7.5

I didn't tested it on any other python version. 

##Robot Remote Server
In current available versions is the robot remote server integrated into
package. Since original package was intercepting standart output and one could
not log any other messages into standart ouput, I've made few changes that
would be nice to by integrated in original robot remote server package.

#Installation
One can install package by running command

    $ python setup.py install
    >
    > running install
    > running bdist_egg
    > running egg_info
    > creating robot_vmlib.egg-info
    > writing robot_vmlib.egg-info/PKG-INFO
    > writing top-level names to robot_vmlib.egg-info/top_level.txt
    > writing dependency_links to robot_vmlib.egg-info/dependency_links.txt
    > ...

Shortly after project is in stable version, it will be uploaded to pipy for
easy installation with distribute tools


For easy access in commandline of the new python command, one should have put
path/to/python/scripts in PATH variable.

#Usage

To start remote VMwareLibrary, use command _robot-vmlib_

    $ robot-vmlib -h
    > usage: robot-vmlib [-h] [-i IP] [-p PORT] [--vmpass VMPASS] [-c CONF_PATH]
    >
    > Robot Remote Server implementing VMware commands
    >
    > optional arguments:
    >   -h, --help            show this help message and exit
    >   -i IP, --ip IP
    >   -p PORT, --port PORT
    >   --vmpass VMPASS
    >   -c CONF_PATH, --config CONF_PATH

Example:

    $ robot-vmlib -i 127.0.0.1 -p 2347 --vmpass fake_pass -c vmware_server.cfg
    >
    > Robot Framework remote server at 127.0.0.1:2347 starting.

With VMware remote library up and running, try calling some commands from robot
testcase.

Each vmrun command needs as a first argument dictionary with information about
machine. Specifically it needs to have keys:

*   guest_user
*   guest_passwd
*   vmx

Example of usage in robot framework script

    *** Settings ***
    Suite Setup    Suite Setup
    Library    Remote    http://127.0.0.1:2347


    *** Keywords ***
    Suite Setup
        ${win7_32bit}=    Create Dictionary    vmx=\\path\\to\\Win_7_32_bit.vmx    guest_user=admin    guest_passwd=fake_pass
        Set Suite Variable    ${win7_32bit}

    *** Test Cases ***
    Try To Make New Snapshot
        Snapshot    ${win7_32bit}    new_snapshot_name

    Try To Revert To Snapshot
        Revert To Snapshot    ${win7_32bit}    init

    Try To Copy Files To Guest User
        Copy File From Host To Guest    ${win7_32bit}    C:\\test_file_on_host.txt    C:\\target_file_on_guest.txt

    Try To Run Application
        Run Applicatoin In Guest    ${win7_32bit}    -interactive    -activeWindow    C:\\windows\\system32\\notepad.exe


In order to execute vm command on the correct virtual machine, one have to
supply first argument which is dictionary.

    {
        "guest_user": "admin",
        "guest_passwd": "fake_pass",
        "vmx": "\\path\\to\\Win_7_32_bit.vmx"
    }

Where **guest_user** a user on virtual machine that we are trying to manage and
command that are supposed to run on virutal machine are executed under this
user. **guest\_passwd** is obviously password for this user. The **vmx** path
identifies virtual machine in VMware.
