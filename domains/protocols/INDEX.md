# protocols

Industrial networks and the physical layers under them. **First domain by design**: the free specs
here are canonical, short enough to actually read, and the tribal knowledge around them is the worst
in the trade, which is where an index earns its keep.

Everything above the marker is written by hand. The table below it is generated from
`catalog/catalog.csv`, so it cannot drift from the catalog. Notes are the reason to be here; the
table is just the manifest.

## Two things worth knowing before you open any of these

**The modbus.org URLs no longer encode the version.** The application protocol spec now lives at
`/file/secure/modbusprotocolspecification.pdf`, with no `V1_1b3` in the path, so the organization can
ship a new revision at the identical URL and nothing in a link based bookmark would notice. The old
versioned `/docs/Modbus_Application_Protocol_V1_1b3.pdf` style URLs are dead, which means every blog
post, forum answer, and quoted citation pointing at them is now a 404. This is the whole argument for
the `revision`, `verified_level`, and `archive_url` columns in one example.

**RS485 will not talk is usually not a device problem.** The answer is disproportionately in the
serial line spec's framing, timing, termination, and biasing sections rather than in the manual of the
device that is failing to talk, which is the manual everyone reads first. Failing idle bias is the
classic: the bus floats, the first character gets eaten, and every device reports a framing error
while every device is configured correctly.

## Reading order

1. Serial line spec, for the physical layer and RTU framing. Most field problems are here.
2. Application protocol spec, for function codes and exception codes. This is the one to keep open.
3. TCP implementation guide, only when you are actually doing Modbus TCP. The MBAP header and the
   unit id against slave id distinction are the parts that bite.

<!-- BEGIN GENERATED: catalog. Do not hand edit. Regenerate: ./tools/build_indexes.py -->

| Document | Vendor | Rev | Verified | Mirror |
|---|---|---|---|---|
| [Sparkplug Specification](https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf) ([snapshot](https://web.archive.org/web/20260715162455/https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf)) | Eclipse Foundation | 3.0.0 | `LOCATED ONLY` | link only |
| [MODBUS Application Protocol Specification](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf) ([snapshot](https://web.archive.org/web/20260715154556/https://www.modbus.org/file/secure/modbusprotocolspecification.pdf)) | modbus.org | V1.1b3 | `TRACED` | link only |
| [MODBUS Messaging on TCP/IP Implementation Guide](https://www.modbus.org/file/secure/messagingimplementationguide.pdf) ([snapshot](https://web.archive.org/web/20260712095147/https://www.modbus.org/file/secure/messagingimplementationguide.pdf)) | modbus.org | V1.0b | `TRACED` | link only |
| [MODBUS over Serial Line Specification and Implementation Guide](https://www.modbus.org/file/secure/modbusoverserial.pdf) ([snapshot](https://web.archive.org/web/20260601051038/https://www.modbus.org/file/secure/modbusoverserial.pdf)) | modbus.org | V1.02 | `TRACED` | link only |
| [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) | OASIS | 5.0 | `LOCATED ONLY` | link only |
| [The CIP Networks Library (EtherNet/IP)](https://www.odva.org/technology-standards/key-technologies/ethernet-ip/) | ODVA |  | `GATED, UNREAD` | link only |

<!-- END GENERATED: catalog. -->
