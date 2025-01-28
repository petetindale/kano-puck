# kano-puck

Making use of a Kano puck.

My son bought a Star Wars Kano Coding Kit from a school fair, only to find that Kano had gone bust.
To bring it back to life, I wrote this little Python script.

Note: this leverages Bleak Python [Bleak Documentation](https://bleak.readthedocs.io/en/latest/index.html)

## Kano Star Wars Device

### Interesting characteristic UUIDs

- `11a70201-f691-4b93-a6f4-0968f5b648f8` is the main IR sensor returning a byte array `[0] == North, [1] == East, [2] == South, [3] == West`

### Extract from device BLE data

```text
Service: 11a70100-f691-4b93-a6f4-0968f5b648f8 Description: (Unknown)
--Characteristic: 11a70101-f691-4b93-a6f4-0968f5b648f8, Properties: ['read'], Desc: Unknown)
----Value: 11a70101-f691-4b93-a6f4-0968f5b648f8: bytearray(b'Kano Computing')
--Characteristic: 11a70102-f691-4b93-a6f4-0968f5b648f8, Properties: ['read'], Desc: Unknown)
----Value: 11a70102-f691-4b93-a6f4-0968f5b648f8: bytearray(b'1.1.1')
--Characteristic: 11a70103-f691-4b93-a6f4-0968f5b648f8, Properties: ['read'], Desc: Unknown)
----Value: 11a70103-f691-4b93-a6f4-0968f5b648f8: bytearray(b'0')
--Characteristic: 11a70104-f691-4b93-a6f4-0968f5b648f8, Properties: ['read'], Desc: Unknown)
----Value: 11a70104-f691-4b93-a6f4-0968f5b648f8: bytearray(b'1')

Service: 11a70200-f691-4b93-a6f4-0968f5b648f8 Description: (Unknown)
--Characteristic: 11a70201-f691-4b93-a6f4-0968f5b648f8, Properties: ['read', 'notify'], Desc: Unknown)
----Value: 11a70201-f691-4b93-a6f4-0968f5b648f8: bytearray(b'\xff\xff\xff\xff')

Service: 11a70300-f691-4b93-a6f4-0968f5b648f8 Description: (Unknown)
--Characteristic: 11a70301-f691-4b93-a6f4-0968f5b648f8, Properties: ['read', 'write'], Desc: Unknown)
----Value: 11a70301-f691-4b93-a6f4-0968f5b648f8: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
--Characteristic: 11a70302-f691-4b93-a6f4-0968f5b648f8, Properties: ['write'], Desc: Unknown)
--Characteristic: 11a70303-f691-4b93-a6f4-0968f5b648f8, Properties: ['read', 'notify'], Desc: Unknown)
----Value: 11a70303-f691-4b93-a6f4-0968f5b648f8: bytearray(b'\x17')
--Characteristic: 11a70304-f691-4b93-a6f4-0968f5b648f8, Properties: ['read', 'write'], Desc: Unknown)
----Value: 11a70304-f691-4b93-a6f4-0968f5b648f8: bytearray(b'\x19')

Service: 0000fe59-0000-1000-8000-00805f9b34fb Description: (Nordic Semiconductor ASA)
--Characteristic: 8ec90003-f315-4f60-9fb8-838830daea50, Properties: ['write', 'indicate'], Desc: Buttonless DFU)
```
