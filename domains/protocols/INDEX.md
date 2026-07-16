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

That paragraph was written before anyone here had opened the spec, and reading it end to end proved
it right and then immediately showed why it is not enough: **the spec does not contain the words
"timing" or "biasing."** Biasing is polarization, p.28. Timing is t1.5 and t3.5, p.13. Go looking for
the sections named above and the document tells you they do not exist.

→ **[RS485 will not talk](../../notes/rs485-will-not-talk.md)** routes the symptom to the page: the
vocabulary table, the false friend that costs more than the missing words, and the three traps the
device manual will not warn you about.

→ **[Modbus TCP: the unit id is not the slave id, except when it is](../../notes/modbus-tcp-unit-id.md)**
covers the field the spec repurposes rather than removes, the byte order that reverses between the
two Modbus documents, and why "works from my laptop, not from the PLC" is usually not a network
problem.

## Reading order

1. Serial line spec, for the physical layer and RTU framing. Most field problems are here.
2. Application protocol spec, for function codes and exception codes. This is the one to keep open.
   Note that this holds for TCP too: the TCP guide describes an envelope and defers the function
   codes right back to this document, so it is the spec you want open regardless of transport.
3. TCP implementation guide, only when you are actually doing Modbus TCP. The MBAP header and the
   unit id against slave id distinction are the parts that bite.

<!-- BEGIN GENERATED: catalog. Do not hand edit. Regenerate: ./tools/build_indexes.py -->

| Document | Vendor | Rev | Verified | Mirror |
|---|---|---|---|---|
| [RS-485 Design and install best practices: Guidelines for successful communication](https://library.e.abb.com/public/19382ad529ef49f0803e1ec89fbbf6b3/LVD-EOTKN121U-EN_RS-485designandinstallbestpractices_REVA.pdf) | ABB | A | `LOCATED ONLY` | link only |
| [RS-422 & RS-485 Applications eBook: A Practical Guide To Using RS-422 and RS-485 Serial Interfaces](https://advdownload.advantech.com/productfile/Downloadfile3/1+3FD+0/RS422-RS485%20ApplicationNote_4218wp%20ebook.pdf) | Advantech (B+B SmartWorx) | 2.0 | `LOCATED ONLY` | link only |
| [GEM Introduction - SECS-II, GEM aka SECS/GEM Communication Protocols](https://secsgem.eu/) ([snapshot](https://web.archive.org/web/20260716221625/https://secsgem.eu/)) | Agileo Automation |  | `LOCATED ONLY` | link only |
| [MODBUS RTU Functions and Addressing Modes](https://cdn.automationdirect.com/static/manuals/t1kmodbusm/ch3.pdf) ([snapshot](https://web.archive.org/web/20260716212026/https://cdn.automationdirect.com/static/manuals/t1kmodbusm/ch3.pdf)) | AutomationDirect |  | `LOCATED ONLY` | link only |
| [HSMS - SEMI E37 High-Speed SECS Message Services](https://www.cimetrix.com/hsms) ([snapshot](https://web.archive.org/web/20260716221450/https://www.cimetrix.com/hsms)) | Cimetrix Incorporated |  | `LOCATED ONLY` | link only |
| [Introduction to the SEMI Standards: SECS/GEM](https://41260.fs1.hubspotusercontent-na2.net/hub/41260/file-14039401-pdf/docs/cimetrix_secs_gem_stds_wp_jan_2012.pdf?t=1440107137689) ([snapshot](https://web.archive.org/web/20260716221319/https://41260.fs1.hubspotusercontent-na2.net/hub/41260/file-14039401-pdf/docs/cimetrix_secs_gem_stds_wp_jan_2012.pdf?t=1440107137689)) | Cimetrix Incorporated |  | `LOCATED ONLY` | link only |
| [Schneider Electric Modicon Modbus Protocol](https://www.cisa.gov/news-events/ics-advisories/icsa-17-101-01) ([snapshot](https://web.archive.org/web/20260716212036/https://www.cisa.gov/news-events/ics-advisories/icsa-17-101-01)) | CISA (Cybersecurity and Infrastructure Security Agency) |  | `LOCATED ONLY` | link only |
| [Sparkplug Specification](https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf) ([snapshot](https://web.archive.org/web/20260715162455/https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf)) | Eclipse Foundation | 3.0.0 | `LOCATED ONLY` | link only |
| [HSMS vs SECS-I : Transport Protocols in Semiconductor](https://www.einnosys.com/hsms-vs-secs-i-protocols-semiconductor/) ([snapshot](https://web.archive.org/web/20260716220949/https://www.einnosys.com/hsms-vs-secs-i-protocols-semiconductor/)) | einnosys |  | `LOCATED ONLY` | link only |
| [Enhanced Receiver Failsafe Implementation In Dual Protocol SP339 and XR34350 Serial Transceivers](https://www.maxlinear.com/appnote/ani-22.pdf) | Exar Corporation (now MaxLinear) |  | `LOCATED ONLY` | link only |
| [FreeModbus API Documentation](https://www.embedded-solutions.at/files/freemodbus-v1.6-apidoc/main.html) ([snapshot](https://web.archive.org/web/20260716215957/https://www.embedded-solutions.at/files/freemodbus-v1.6-apidoc/main.html)) | FreeMODBUS project (open source, Christian Walter) | 1.6 | `LOCATED ONLY` | link only |
| [SECS/GEM Interface Manual -- Disclaimer](https://secs-docs.gathertech.com.tw/legal/disclaimer/) ([snapshot](https://web.archive.org/web/20260716221510/https://secs-docs.gathertech.com.tw/legal/disclaimer/)) | GatherTech | GST-SGM-REF-2026 | `LOCATED ONLY` | link only |
| [Stream 1 - Equipment Status (SECS/GEM Interface Manual)](https://secs-docs.gathertech.com.tw/messages/stream01/) ([snapshot](https://web.archive.org/web/20260716220930/https://secs-docs.gathertech.com.tw/messages/stream01/)) | GatherTech |  | `LOCATED ONLY` | link only |
| [go-secs: A library that implements SECS-II/HSMS/SML in Go](https://github.com/arloliu/go-secs) ([snapshot](https://web.archive.org/web/20260716221154/https://github.com/arloliu/go-secs)) | go-secs project (open source) |  | `LOCATED ONLY` | link only |
| [SECS/GEM | Ignition User Manual](https://www.docs.inductiveautomation.com/docs/8.1/ignition-modules/secs-gem) ([snapshot](https://web.archive.org/web/20260716221708/https://www.docs.inductiveautomation.com/docs/8.1/ignition-modules/secs-gem)) | Inductive Automation | 8.1 | `LOCATED ONLY` | link only |
| [KIGEM Automation Software Reference Manual](https://download.tek.com/manual/KIGEM-901-01B_Sep_2019.pdf) ([snapshot](https://web.archive.org/web/20260716220914/https://download.tek.com/manual/KIGEM-901-01B_Sep_2019.pdf)) | Keithley Instruments | Rev. B | `LOCATED ONLY` | link only |
| [libmodbus API Reference](https://libmodbus.org/reference/) ([snapshot](https://web.archive.org/web/20260716215832/https://libmodbus.org/reference/)) | libmodbus project (open source, Stephane Raimbault et al.) |  | `LOCATED ONLY` | link only |
| [RS-485 Advanced Fail-Safe Feature Application Note](https://www.maxlinear.com/appnote/an_291.pdf) | MaxLinear | 01 | `LOCATED ONLY` | link only |
| [RS-485 Transceivers in Fieldbus Networks Application Note](https://www.maxlinear.com/appnote/rs-485%20transceivers%20in%20fieldbus%20networks%20application%20note_300anr00.pdf) | MaxLinear | 00 | `LOCATED ONLY` | link only |
| [Conformance Test Specification for Modbus TCP](http://www.modbus.org/docs/MBConformanceTestSpec_v3.0.pdf) ([snapshot](https://web.archive.org/web/20250313004744/https://modbus.org/docs/MBConformanceTestSpec_v3.0.pdf)) | Modbus Organization, Inc. | Version 3.0 | `LOCATED ONLY` | link only |
| [MODBUS/TCP Security Protocol Specification](https://www.modbus.org/file/secure/modbussecurityprotocol.pdf) ([snapshot](https://web.archive.org/web/20260716211853/https://www.modbus.org/file/secure/modbussecurityprotocol.pdf)) | Modbus Organization, Inc. | v36 | `LOCATED ONLY` | link only |
| [MODBUS Application Protocol Specification](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf) ([snapshot](https://web.archive.org/web/20260715154556/https://www.modbus.org/file/secure/modbusprotocolspecification.pdf)) | modbus.org | V1.1b3 | `TRACED` | link only |
| [MODBUS Messaging on TCP/IP Implementation Guide](https://www.modbus.org/file/secure/messagingimplementationguide.pdf) ([snapshot](https://web.archive.org/web/20260712095147/https://www.modbus.org/file/secure/messagingimplementationguide.pdf)) | modbus.org | V1.0b | `TRACED` | link only |
| [MODBUS over Serial Line Specification and Implementation Guide](https://www.modbus.org/file/secure/modbusoverserial.pdf) ([snapshot](https://web.archive.org/web/20260601051038/https://www.modbus.org/file/secure/modbusoverserial.pdf)) | modbus.org | V1.02 | `TRACED` | link only |
| [Modicon Modbus Protocol Reference Guide](http://www.modbus.org/docs/PI_MBUS_300.pdf) ([snapshot](https://web.archive.org/web/20250825041232/https://www.modbus.org/docs/PI_MBUS_300.pdf)) | Modicon (Schneider Electric predecessor) | Rev. J | `LOCATED ONLY` | link only |
| [Industrial Protocols User's Guide](https://www.moxa.com/getmedia/048873ee-468f-4e61-80c6-dfd7eabc44d7/moxa-industrial-protocols-users-guide-v6.2.pdf) ([snapshot](https://web.archive.org/web/20260716212019/https://www.moxa.com/getmedia/048873ee-468f-4e61-80c6-dfd7eabc44d7/moxa-industrial-protocols-users-guide-v6.2.pdf)) | Moxa Inc. | Version 6.2 | `LOCATED ONLY` | link only |
| [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) ([snapshot](https://web.archive.org/web/20260715162441/https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html)) | OASIS | 5.0 | `LOCATED ONLY` | link only |
| [The CIP Networks Library (EtherNet/IP)](https://www.odva.org/technology-standards/key-technologies/ethernet-ip/) | ODVA |  | `GATED, UNREAD` | link only |
| [High-Level Overview of Equipment Communication during Semiconductor Fabrication](https://www.pdf.com/high-level-overview-of-equipment-communication-during-semiconductor-fabrication/) ([snapshot](https://web.archive.org/web/20260716221646/https://www.pdf.com/high-level-overview-of-equipment-communication-during-semiconductor-fabrication/)) | PDF Solutions |  | `LOCATED ONLY` | link only |
| [hsms package - github.com/arloliu/go-secs/hsms - Go Packages](https://pkg.go.dev/github.com/arloliu/go-secs/hsms) ([snapshot](https://web.archive.org/web/20260716221220/https://pkg.go.dev/github.com/arloliu/go-secs/hsms)) | pkg.go.dev (Google) |  | `LOCATED ONLY` | link only |
| [Usage of Generic Equipment Model (E30 Standard) for Semiconductor Equipment and Materials International (SEMI) robotization instrument](https://www.primescholarslibrary.org/articles/usage-of-generic-equipment-model-e30-standard-for-semiconductor-equipment-and-materials-international-semi-robotization-.pdf) ([snapshot](https://web.archive.org/web/20260716221731/https://www.primescholarslibrary.org/articles/usage-of-generic-equipment-model-e30-standard-for-semiconductor-equipment-and-materials-international-semi-robotization-.pdf)) | Prime Scholars Library | Vol. 8 (3) | `LOCATED ONLY` | link only |
| [PyModbus documentation](https://pymodbus.readthedocs.io/en/stable/) | pymodbus project (open source) | 3.14.0 | `LOCATED ONLY` | link only |
| [External Fail-Safe Biasing of RS-485 Networks](https://www.renesas.com/www/doc/application-note/an1986.pdf) | Renesas Electronics (Intersil legacy line) | 1.00 | `LOCATED ONLY` | link only |
| [secs4java8: This library is SEMI-SECS-communicate implementation on Java8](https://github.com/kenta-shimizu/secs4java8) ([snapshot](https://web.archive.org/web/20260716221302/https://github.com/kenta-shimizu/secs4java8)) | secs4java8 project (open source) |  | `LOCATED ONLY` | link only |
| [secs4net: SECS-II/HSMS-SS/GEM implementation on .NET](https://github.com/mkjeff/secs4net) ([snapshot](https://web.archive.org/web/20260716221239/https://github.com/mkjeff/secs4net)) | secs4net project (open source) |  | `LOCATED ONLY` | link only |
| [bparzella/secsgem: Simple Python SECS/GEM implementation](https://github.com/bparzella/secsgem) ([snapshot](https://web.archive.org/web/20260716221119/https://github.com/bparzella/secsgem)) | secsgem project (open source) |  | `LOCATED ONLY` | link only |
| [secsgem](https://secsgem.readthedocs.io/) ([snapshot](https://web.archive.org/web/20260716221103/https://secsgem.readthedocs.io/en/latest/)) | secsgem project (open source) | 0.3.0 | `LOCATED ONLY` | link only |
| [secsgem Documentation Release 0.0.3](https://secsgem.readthedocs.io/_/downloads/en/v0.0.3/pdf/) ([snapshot](https://web.archive.org/web/20260716221143/https://secsgem.readthedocs.io/_/downloads/en/v0.0.3/pdf/)) | secsgem project (open source) | 0.0.3 | `LOCATED ONLY` | link only |
| [Specification for High-Speed SECS Message Services (HSMS) Generic Services](https://store-us.semi.org/products/e03700-semi-e37-high-speed-secs-message-services-hsms-generic-services) ([snapshot](https://web.archive.org/web/20260716162118/https://store-us.semi.org/products/e03700-semi-e37-high-speed-secs-message-services-hsms-generic-services)) | SEMI | SEMI E37-0222 | `GATED, UNREAD` | link only |
| [Specification for SEMI Equipment Communications Standard 1 Message Transfer (SECS-I)](https://store-us.semi.org/products/e00400-semi-e4-specification-for-semi-equipment-communications-standard-1-message-transfer-secs-i) ([snapshot](https://web.archive.org/web/20260716161816/https://store-us.semi.org/products/e00400-semi-e4-specification-for-semi-equipment-communications-standard-1-message-transfer-secs-i)) | SEMI | SEMI E4-0923 | `GATED, UNREAD` | link only |
| [Specification for SEMI Equipment Communications Standard 2 Message Content (SECS-II)](https://store-us.semi.org/products/e00500-semi-e5-specification-for-semi-equipment-communications-standard-2-message-content-secs-ii) ([snapshot](https://web.archive.org/web/20260716161934/https://store-us.semi.org/products/e00500-semi-e5-specification-for-semi-equipment-communications-standard-2-message-content-secs-ii)) | SEMI | SEMI E5-0725 | `GATED, UNREAD` | link only |
| [Specification for the Generic Model for Communications and Control of Manufacturing Equipment (GEM)](https://store-us.semi.org/products/e03000-semi-e30-specification-for-the-generic-model-for-communications-and-control-of-manufacturing-equipment-gem) ([snapshot](https://web.archive.org/web/20260716162040/https://store-us.semi.org/products/e03000-semi-e30-specification-for-the-generic-model-for-communications-and-control-of-manufacturing-equipment-gem)) | SEMI | SEMI E30-0526 | `GATED, UNREAD` | link only |
| [How to Isolate Signal and Power for an RS-485 System](https://www.ti.com/lit/ab/slla416d/slla416d.pdf) | Texas Instruments | D | `LOCATED ONLY` | link only |
| [Interface Circuits for TIA/EIA-232-F](https://www.ti.com/lit/an/slla037a/slla037a.pdf) ([snapshot](https://web.archive.org/web/20260716220120/https://www.ti.com/lit/an/slla037a/slla037a.pdf)) | Texas Instruments | A | `LOCATED ONLY` | link only |
| [RS-422 and RS-485 Standards Overview and System Configurations](https://www.ti.com/lit/an/slla070d/slla070d.pdf) ([snapshot](https://web.archive.org/web/20260716220108/https://www.ti.com/lit/an/slla070d/slla070d.pdf)) | Texas Instruments | D | `LOCATED ONLY` | link only |
| [The RS-485 Design Guide](https://www.ti.com/lit/an/slla272d/slla272d.pdf) ([snapshot](https://web.archive.org/web/20260716220112/https://www.ti.com/lit/an/slla272d/slla272d.pdf)) | Texas Instruments | D | `LOCATED ONLY` | link only |
| [AN-1057 Ten Ways to Bulletproof RS-485 Interfaces](https://www.ti.com/lit/an/snla049b/snla049b.pdf) | Texas Instruments (originally National Semiconductor, AN-1057) | B | `LOCATED ONLY` | link only |
| [FAILSAFE Biasing of Differential Buses](https://www.ti.com/lit/an/snla031/snla031.pdf) ([snapshot](https://web.archive.org/web/20260716220132/https://www.ti.com/lit/an/snla031/snla031.pdf)) | Texas Instruments (originally National Semiconductor, AN-847) |  | `LOCATED ONLY` | link only |
| [Securing Semiconductor Manufacturing (TXOne whitepaper, June 2024)](https://media.txone.com/prod/uploads/2024/06/Securing-Semiconductor-Manufacturing-TXOne-WP-2024.pdf) ([snapshot](https://web.archive.org/web/20260417193412/https://media.txone.com/prod/uploads/2024/06/Securing-Semiconductor-Manufacturing-TXOne-WP-2024.pdf)) | TXOne Networks |  | `LOCATED ONLY` | link only |
| [Conformance Test Policy for the Modbus/TCP Conformance Test Laboratory](https://web.eecs.umich.edu/~modbus/documents/Conformance_Test_Policy_2_0.pdf) ([snapshot](https://web.archive.org/web/20260716215743/https://web.eecs.umich.edu/~modbus/documents/Conformance_Test_Policy_2_0.pdf)) | University of Michigan Modbus/TCP Conformance Test Laboratory | Version 2.0 | `LOCATED ONLY` | link only |

<!-- END GENERATED: catalog. -->
