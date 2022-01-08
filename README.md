# Room Assistant Configurator (raCfg)

**I just tossed this together in an afternoon. No tests, just get it done.**

This tool assists with rapidly installing room assistant, and centerally managing mutliple cluster
peers from a cental location. For details on configurating room assistant, see:
https://github.com/mKeRix/room-assistant

# Compatibility

This was developed on a debian system. Should work on nearly any Unix/Linux system as it only uses Python,
Bash, and ssh.

## Details

There are 2 components to this package:
1) Scripted installation of room assistant into raspberry pis (or anything debian based really).
2) Configuration manager for a cluster of room assistants.
3) The target username is 'pi' as RA is designed to be installed on these.

Each component can be used independently.

This tool merges global room assistant settings with setting for individual peers
into a single file, sends that file to the room assistant peer, and restarts
the service.

For example, you may have settings for bluetooth, which are global, but each
peer will have its own name. Additionally, each peer can override a global
setting.

# Downloading this tool

Just clone this repository from https://github.com/tazzytazz/racfg

# Installing room assistant

This assumes a few new raspberry pi is waiting for us. This has been tested on a couple of pi's that have
been running for 3 years, and works just fine too. This also adds the system aliases 'll' and 'pico'. You're welcome.

1. (optional). Copy ssh keys to new peer:
   * ./copy_remote_ssh.sh 192.xx.xx.xx
2. Copy the installer files to remote:
   * ./copy_remote.sh 192.xx.xx.xx
3. ssh to the remote machine: ssh pi@192.xx.xx.xx  
4. On the new machine, change to 'room-assistant/installers'

## Phase 1:
(Pro Tip: After you start the room assistant, skip down to start creating the configuration files.)

For smaller raspberries, such as the Raspberry PI Zero, Zero W, Zero W 2, use a prebuilt NPM:

    ./install_rpi_slow.sh

For all others, such as Raspberry Pi 3, 4 (or 1 & 2 with a bluetooth dongle):

    ./install_rpi_fast.sh

## Phase 2:
After the raspberry pi reboots, complete the installation. SSH into the box and go back into the installers folder.

    ./install_finish.sh

## Cleanup

Remove the install files. While still connected to the remote peer, inside the installers folder, run:

    ./cleanup_remote.sh


# Configuration

There are 2 files that need to be created in the root directory of this tool.

* config.yml
  * see config.yml.example
  * contains the settings for this tool
  * settings for individual peers
  * modified versions of various integrations, that get expanded to room assistant style configurations.
  
* global.yml
  * Any contents you want merged into all peer configurations.
    
## config.yml

The 'raCfg' section is the configuration settings for this tool. See example file for settings.

### Implemented helpers

Addtional helpers mimic the RA original, but offers some additional settings to remove lots of
boiler plate typing.

* bluetoothLowEnergy, see room assistant doc for values. However, instead of allowlist + tagOverrides,
  this is combined into 'tags'. Just simply set whatever options per RA docs and the cfg tool will expand
  this into 'allowlist' and 'tagOverrides'.
  

### Peers

The heart of the config file. The details of each peer is listed here. Peers can override any global setting for
any section. Please see RA docs for the specific section / configuration option.  See the below example:

    peers:
      _defaults:
        cluster_weight: 5  # or just set in global.yml
      familypi:
        comment: RP4
        address: 10.133.144.10
        global_instanceName: "Family Room"
        cluster_weight: 1000
      denpi:
        comment: RPZW
        address: 10.133.144.11
        global_instanceName: "Den"
  
The formatting of the values is as follows: XXXX_YYYY
* XXXX = root level config section. Such as cluster, global, bluetoothLowEnergy, whatever high level settings are
  available in RA.
* YYYY = Setting name per RA docs.

The example of 'cluster_weight: 5' would be the same as putting this in global.yaml:

    cluster:
      weight: 5

#### _defaults

Values here are the exact same as putting them in global.yml. It's up to you where you want your configs.

#### raCfg values

There's a few values in the peers section that don't directly map to a RA setting.

* address - The ip / hostname of the peer. Used to build peers list for the cluster configuration.
* comment - Put peer comments here. Will be included at the top of each config file.

# raCfg order of operations

This tool creates local.yml output using various inputs and configuration. Here's the order settings
are created for each peer.

1. Load global settings (global.yml) 
2. Generate peer specific configurations.
3. Merge peer specific configs into global, over-riding global settings.
4. Send config file to peer as 'local.yml', and restart the service.
