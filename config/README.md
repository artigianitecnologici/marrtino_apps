# docker configuration

Follow instructions in [docker folder](https://bitbucket.org/iocchi/marrtino_apps/src/master/docker/)



# udev configuration

Copy file `80-marrtino.rules` in `/etc/udev/rules.d/`

Check Vendor and Product IDs of your devices with command `lsusb`

Edit  `/etc/udev/rules.d/80-marrtino.rules` if needed

Restart the system and enjoy!

# system_watchdog configuration

To start docker containers at boot, copy file `system_watchdog` in
`/etc/init.d`

Edit `/etc/init.d/system_watchdog` if needed (`user` and `dir` info)

Enable the service

    sudo systemctl enable system_watchdog

Start the service

    sudo systemctl start system_watchdog

Restart the system and enjoy!

# orazio configuration




# MARRtino firmware parameters configuration #

NOTE: Instructions have been updated for 2018 firmware. 
If you have 2017 firmware, please use the scripts named with 2017
or refer to previous checkout ```19c4c221f81e2414651aceeba900ca3a0c66988e``` of this repository.

## Scripted version ##


* to upload firmware parameters from file to Arduino


        ./uploadfirmwareparams.bash [marrtino2019|pka03|ln298|arduino]


* to download firmware parameters from Arduino to file


        cat download_config.script | rosrun srrg2_orazio orazio -serial-device /dev/orazio 



Note: change file names in the .script files if needed.



## Manual version ##


* Download

        rosrun srrg2_orazio orazio -serial-device /dev/orazio
        orazio> fetch system_params
        orazio> fetch joint_params[0]
        orazio> fetch joint_params[1]
        orazio> fetch joint_params[2]
        orazio> fetch joint_params[3]
        orazio> fetch drive_params
        orazio> fetch sonar_params
        orazio> request system_params
        orazio> request joint_params[0]
        orazio> request joint_params[1]
        orazio> request joint_params[2]
        orazio> request joint_params[3]
        orazio> request drive_params
        orazio> request sonar_params
        orazio> save_config XXX_firmware_params.cfg
        orazio> quit


* Upload

        rosrun srrg2_orazio orazio -serial-device /dev/orazio
        orazio> load_config XXX_firmware_params.cfg
        orazio> send system_params
        orazio> send joint_params[0]
        orazio> send joint_params[1]
        orazio> send joint_params[2]
        orazio> send joint_params[3]
        orazio> send drive_params
        orazio> send sonar_params
        orazio> store system_params
        orazio> store joint_params[0]
        orazio> store joint_params[1]
        orazio> store joint_params[2]
        orazio> store joint_params[3]
        orazio> store drive_params
        orazio> store sonar_params
        orazio> quit

# SD config script


    usage: sdconfig.py [-h] [-imagefile IMAGEFILE] [-ssid SSID] [-channel CHANNEL]
                       [-password PASSWORD] [-hostname HOSTNAME]
                       op device

    MARRtino SD config

    positional arguments:
      op                    [read, write, check, set, speed]
      device                device name (e.g.: /dev/mmcblk0)

    optional arguments:
      -h, --help            show this help message and exit
      -imagefile IMAGEFILE  image file prefix (e.g., raspi3b_marrtino_2.0)
      -ssid SSID            Wlan SSID
      -channel CHANNEL      Wlan channel
      -password PASSWORD    Wlan password
      -hostname HOSTNAME    host name

Notes:

* Script must be run with `sudo` privileges

* Check device name with `dmesg`

* Read and write not available for version 4 SD cards (use balenaEtcher to flash an SD card)

* If files `system_config.yaml` or `autostart.yaml` are not present, copy from templates

    cd home/marrtino/src/marrtino_apps
    cp docker/system_config_template.yaml system_config.yaml
    cp start/autostart_template.yaml autostart.yaml


* Edit `system_config.yaml` or `autostart.yaml` in `home/marrtino/src/marrtino_apps` to configure startup docker containers and functionalities

    cd home/marrtino/src/marrtino_apps
    nano system_config.yaml
    nano autostart.yaml

* To setup `system_config` and `autostart` for ROSITA robot, use

    cd home/marrtino/src/marrtino_apps/bin
    ./setup_rosita.bash

* Use `git pull` in `home/marrtino/src/marrtino_apps` to update `marrtino_apps`


