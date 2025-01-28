"""
Kano Device Interface Module

This module provides functionality to discover and interact with Kano BLE devices.
It enables scanning for devices, connecting to them, and reading their characteristics.
"""

from bleak import BleakScanner, BleakClient
import asyncio

async def discover_devices():
    """
    Scan for available BLE devices and find Kano devices.
    
    Returns:
        str: The address of the first found Kano device, or None if no devices found
    """
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if(device.name != None and device.name.startswith("Kano")):
            print(f"Device: {device.name}, Address: {device.address}")
            return device.address
    print("No Kano devices found..... is it on?")
    return None

async def discover_details(address):
    """
    Connect to a Kano device and discover its services and characteristics.
    
    Args:
        address (str): The BLE address of the device to connect to
    """
    print(f"Attempting to connect to {address}...")
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address} successfully!")

            # Discover services and characteristics
            print("Discovering services...")
            services = await client.get_services()
            # Iterate through each service
            for service in services:
                print(f"\nService: {service.uuid} Description: ({service.description})")
                # Iterate through characteristics in each service
                for serchar in service.characteristics:
                    print(f"--Characteristic: {serchar.uuid}, Properties: {serchar.properties}, Desc: {serchar.description})")

                    # If characteristic is readable, get its value
                    if 'read' in serchar.properties :
                        value = await client.read_gatt_char(serchar.uuid)
                        print(f"----Value: {serchar.uuid}: {value}")
        else:
            print("Failed to connect to the device.")

async def stream_ir_sensor(address):
    """
    Stream IR sensor data from a Kano device.
    
    Args:
        address (str): The BLE address of the device to stream from
    """
    print(f"Attempting to connect to {address}...")
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address} successfully!")

            #ir_sensor_characteristic_uuid represents the characteristic uuid for the IR sensor data
            ir_sensor_characteristic_uuid = "11a70201-f691-4b93-a6f4-0968f5b648f8"

            while client.is_connected:
                value = await client.read_gatt_char(ir_sensor_characteristic_uuid)
                
                yield value
                
        else:
            print("Failed to connect to the device.")

async def process_ir_sensor_data(address):
    """
    Process IR sensor data from a Kano device.
    
    Args:
        address (str): The BLE address of the device to process data from
    """
    async for value in stream_ir_sensor(address):
        #If the button is 'towards you' North (N) [0] is furthest away, East (E) [1] is to the right, South (S) [2] is closest, West (W) [3] is to the left
        #The value is a 4 byte array with each byte representing the strength of the signal 255 with zero reflection to 0 with maximum reflection
        print(f"IR Array: N{value[0]:03}-E{value[1]:03}-S{value[2]:03}-W{value[3]:03}")
        

async def writesensor(address, serchar, value, read):
    """
    Write a value to a specific characteristic of a Kano device and optionally read it back.
    
    Args:
        address (str): The BLE address of the device
        serchar (str): The UUID of the characteristic to write to
        value (bytearray): The value to write to the characteristic
        read (bool): Whether to read the characteristic value back after writing
    """
    print(f"Attempting to connect to {address}...")
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address} successfully!")

            # Write the value to the specified characteristic
            await client.write_gatt_char(serchar, value)
            print(f"array: {value}")

            # If read is True, read the value back from the characteristic
            if read:
                value = await client.read_gatt_char(serchar)
                print(f"array: {value}")
        else:
            print("Failed to connect to the device.")

async def blastwrite(address, serchar, read):
    """
    Write incrementing values to the device characteristic.
    
    Args:
        address (str): The BLE address of the device
    """
    print(f"Attempting to connect to {address}...")
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address} successfully!")
            value = bytearray([0x00])
            while client.is_connected:
                
                value[0] = (value[0] + 1) % 256
                await client.write_gatt_char(serchar, value)
                print(f"array: {value}")

                if read:
                    value = await client.read_gatt_char(serchar)
                    print(f"array: {value}")
        else:
            print("Failed to connect to the device.")



async def main():
    # Step 1: Discover devices
    kano_device = await discover_devices()

    if kano_device is None:

        return
    
    #await discover_details(kano_device)

    await process_ir_sensor_data(kano_device)


    #await writesensor(kano_device, "11a70301-f691-4b93-a6f4-0968f5b648f8", bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'), True)
    #await writesensor(kano_device, "11a70302-f691-4b93-a6f4-0968f5b648f8", bytearray(b'\xFF'), False)
    #await blastwrite(kano_device, "11a70304-f691-4b93-a6f4-0968f5b648f8", True)



if __name__ == "__main__":
    asyncio.run(main())
