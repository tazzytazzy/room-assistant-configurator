#!/usr/bin/env python
"""
Merges global.yml and config.yml to create various local.yml for each room assistant peer node. It then
sends the configuration file to peer, and restarts the room assistant service.

See README.md file for details.
"""
import math
import os
import time
import yaml


def mergeDicts(dict1, dict2):
    """ Just a wrapper around _mergeDicts to hide the generator. """
    return dict(_mergeDicts(dict1, dict2))


def _mergeDicts(dict1, dict2):
    """ Recursively merge dictionaries. Taken from here: https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries """
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_mergeDicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


# Read the configuration files. Who needs error handling?
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

with open('global.yml', 'r') as file:
    globalData = yaml.safe_load(file)


def getRaCfg(name, default):
    """ Gets a config attribute, if not set, return the default. """
    if 'raCfg' in config:
        if name in config['raCfg'] and isinstance(config['raCfg'][name], bool):
            return config['raCfg'][name]
    return default


shutdownPeersOnSync = getRaCfg('shutdownPeersOnSync', False)
restartServices = getRaCfg('restartServices', True)
restartSleepTime = getRaCfg('restartSleepTime', 10)

if 'peers' not in config:
    raise KeyError("Error: No 'peers' in config file. Must have peers!")

# Load default values for each peer. It's the same as putting the values in global.yml
peerDefaults = config.pop('_defaults', None)
if peerDefaults is None:
    peerDefaults = {}


peersRaw = {}   # Store raw peer data here.
peersData = {}  # Properly parsed data. Ready to be merged with global.yml data.
# peerAddressesRaw = {}

globalKeys = globalData.keys()

# Find system wide port number for clustering.
clusterPort = 6425
hasClustering = False
if 'cluster' in globalData:
    hasClustering = True
    if 'port' in globalData['cluster']:
        clusterPort = globalData['cluster']['port']


if 'bluetoothLowEnergy' in config:
    tagOverrides = config['bluetoothLowEnergy'].pop('tags', None)
    if 'bluetoothLowEnergy' not in config:
        config['bluetoothLowEnergy'] = {'allowlist': []}
    if 'allowlist' not in config:
        config['bluetoothLowEnergy']['allowlist'] = []

    if tagOverrides is not None:
        # allowlist = []
        config['bluetoothLowEnergy']['tagOverrides'] = tagOverrides
        for tag, data in tagOverrides.items():
            config['bluetoothLowEnergy']['allowlist'].append(tag)

    if 'bluetoothLowEnergy' not in globalData:
        globalData['bluetoothLowEnergy'] = {}
    globalData['bluetoothLowEnergy'] = mergeDicts(globalData['bluetoothLowEnergy'], config['bluetoothLowEnergy'])
    # print(globalData)

peersAddressList = []  # A list of all peers and their address:port

for peerName, raw in config['peers'].items():
    """ 
    Build peerData from peerRaw data. This allows overriding global.yml settings for all peers
    or individual peers. You choose if you want it in global.yml or in _defaults inside config.yml
    """
    if peerName == '_defaults':
        continue
    peersData[peerName] = {}
    peersRaw[peerName] = mergeDicts(peerDefaults, raw)

    # For each top level global item, lets add some additional data for this peer.
    for gKey in globalKeys:
        peersData[peerName][gKey] = {}
        res = {key: val for key, val in peersRaw[peerName].items()
               if key.startswith(f'{gKey}_')}
        if len(res) == 0:
            continue
        for resKey, resData in res.items():
            peersData[peerName][gKey][resKey.split('_')[1]] = resData

    peerClusterPort = clusterPort
    if 'cluster' in peersData[peerName]:
        if 'port' in peersData[peerName]['cluster']:
            peerClusterPort = peersData[peerName]['cluster']['port']
        peersData[peerName]['cluster']['port'] = peerClusterPort
    else:
        peersData[peerName]['cluster'] = {'port': peerClusterPort}
    peersAddressList.append(f"{peersRaw[peerName]['address']}:{peersData[peerName]['cluster']['port']}")


#
# Update / Force various globalData settings.

if 'quorum' not in globalData['cluster']:  # Should have a quorum value.
    globalData['cluster']['quorum'] = int(math.ceil((len(peersAddressList)+1)/2))
else:
    if globalData['cluster']['quorum'] > len(peersAddressList):
        raise Exception("quorum value manually set, but it's higher than peer count. Please math better.")

if 'autoDiscovery' not in globalData['cluster']:  # Should have a quorum value.
    globalData['cluster']['autoDiscovery'] = false


#############################################
# Time to publish the files.
#
# Files are saved in ./dist folder for review, and is used by rsync to copy the file over.
#############################################

# Shutting down all the peers has caused issues, not recommended, but it's here.
if shutdownPeersOnSync:
    restartServices = True
    print("\nStopping all Room Assistant peers.")
    for peerName, data in peersData.items():
        print(
            f"Stopping peer: {peerName} - {peersRaw[peerName]['address']} - '{peersRaw[peerName]['global_instanceName']}'")

        stream = os.popen(f"ssh pi@{peersRaw[peerName]['address']} sudo systemctl stop room-assistant.service")
        output = stream.read()
        if len(output):
            print(output)

timestamp = time.ctime()  # Ex: 'Mon Oct 18 13:35:29 2020'
for peerName, data in peersData.items():
    try:
        os.mkdir('dist')
    except FileExistsError:
        pass
    data = mergeDicts(globalData, data)  # Using global data as the base, merge in peer data for final data..
    data['cluster']['peerAddresses'] = peersAddressList

    textOut = f"#\n# This file was auto generated at {timestamp}\n" \
              f"# *** Modifications to this file may be lost. ***\n#\n# {peerName} - {peersRaw[peerName]['address']} - '{peersRaw[peerName]['global_instanceName']}'\n" \
              f"#\n"
    if "comment" in peersRaw[peerName]:
        textOut += f"# {peersRaw[peerName]['comment']}\n#\n"
    textOut += "\n\n"
    textOut += yaml.dump(data)

    with open(f'dist/{peerName}.yml', 'w') as file:
        file.write(textOut)

    print(f"Sending config file to: {peerName} -{ peersRaw[peerName]['address']} - '{peersRaw[peerName]['global_instanceName']}")
    stream = os.popen(f"./sync_config_file.sh {peerName} {peersRaw[peerName]['address']}")
    output = stream.read()
    if len(output):
        print(output)

    # print(f"restarting service: ssh pi@{peersRaw[peerName]['address']} sudo systemctl restart room-assistant.service")
    stream = os.popen(f"ssh pi@{peersRaw[peerName]['address']} sudo systemctl restart room-assistant.service")
    output = stream.read()
    if len(output):
        print(output)
    time.sleep(restartSleepTime)
