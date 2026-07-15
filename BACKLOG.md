# Backlog

**This is a wishlist, not a claim.** Nothing here has been checked. Nothing here has a URL. A line in
this file means "this document probably exists and would be worth having," which is the weakest
possible statement and is stated weakly on purpose.

It lives in a separate file from `catalog/catalog.csv` for that reason. Seeding the catalog with six
hundred empty rows would produce a catalog that is 98 percent unverified stubs, which reads to any
visitor as an abandoned project, because that is what it would be. A row enters the catalog when it
has a real URL and a real verification level. Until then it lives here, where it is honest.

## The order of work

Depth first, one domain at a time. Breadth is what makes this a link dump.

The first domains are the ones where the author can check a document against **ground truth** rather
than against other documents: hands on the power chain, LOTO certified and recertified every six
months, 70E trained through the apprenticeship, a proprietary PLC built and running, install level
networking. In those areas a wrong manual is detectable. Everywhere else, only the manual's own
confidence is visible, and that is exactly the condition where a catalog quietly fills up with
plausible garbage.

| Order | Domain | Why here |
|---|---|---|
| 1 | `protocols` | Modbus, EtherNet/IP, and the serial layer are free, canonical, short, and checkable. Best value per hour in the whole list, and it is where the tribal knowledge is worst. |
| 2 | `power-distribution` | The author's ground truth. Nobody else's automation doc repo has switchgear, UPS, ATS, and protective relays in it. This is the differentiator. |
| 3 | `plc-control` | The largest and most searched. Also the most link rotted, so the snapshot machinery earns its keep. |
| 4 | `standards` | Mostly `CITED, UNREAD` and `GATED, UNREAD` rows plus scope notes. Low effort, high value, because "which standard even governs this" is the actual question people have. |
| 5+ | everything else | Only once the first four are worth linking to. |

---

## protocols

- Modbus RTU and TCP: application protocol, serial line guide, TCP implementation guide **(seeded)**
- EtherNet/IP and CIP, CIP Safety, CIP Motion (ODVA, sold, cite by number)
- PROFIBUS DP and PROFINET, PROFIsafe (PI)
- EtherCAT, EtherCAT slave controller documentation (ETG)
- CANopen, DeviceNet, J1939, CAN FD, ISO 11898
- IO-Link (IEC 61131-9) and IODD specification
- OPC UA parts 1 through 14, plus companion specs. Legacy OPC DA and HDA
- MQTT 3.1.1 and 5.0 **(5.0 seeded)**, Sparkplug B **(seeded)**
- BACnet MS/TP and BACnet IP, LonWorks, KNX, DALI
- DNP3, IEC 60870-5-101 and 104, IEC 61850 (substation, ties directly to power-distribution)
- HART, WirelessHART, FOUNDATION Fieldbus, the 4 to 20 mA loop and the HART overlay
- Serial physical layer: RS232, RS422, RS485, TIA/EIA-485 biasing and termination
- Ethernet: IEEE 802.3, VLANs, PoE 802.3af/at/bt, TSN 802.1Q series, PTP IEEE 1588
- Wireless: LoRaWAN, Zigbee, BLE, ISA100.11a, private 5G for industrial
- SEMI E4, E5, E30, E37 (SECS/GEM) if fabs ever become relevant

## power-distribution

- Switchgear and switchboards, LV and MV: Eaton, Square D, ABB, Siemens, GE
- Motor control centers: CENTERLINE 2100 and 2500, Eaton Freedom, Siemens tiastar
- Breakers and trip units: molded case, insulated case, power breakers, Micrologic, Digitrip, Entelliguard
- Protective relays: SEL 751, SEL 751A, SEL 311, Basler, Beckwith, ABB REF and REM
- Transformers: dry type, cast resin, K factor, liquid filled, taps and impedance
- UPS: Vertiv Liebert, Schneider Galaxy, Eaton 93PM, Mitsubishi. Battery systems, VRLA, lithium, BMS
- Static transfer switches, automatic transfer switches, tie breakers
- Generators and paralleling: Caterpillar, Cummins, Kohler, Woodward, ASCO
- Data center: PDUs, RPPs, busway (Starline, Universal Electric), overhead bus
- Power monitoring: PowerLogic ION, PowerMonitor 5000, Eaton PXM, Fluke and Dranetz analyzers
- Grounding and bonding, ground grid, isolated ground, SPD
- Harmonics, VFD line reactors, drive isolation transformers, active filters
- Power factor correction and capacitor banks
- Commissioning: NETA ATS and MTS scope (reference only, never reproduce), IR, TTR, DLRO, injection

## plc-control

**Rockwell**: ControlLogix 1756 (controllers, I/O, comms, redundancy), CompactLogix 5380 and 5069,
MicroLogix, Micro800, SLC 500 and PLC-5 legacy, GuardLogix and safety I/O, Studio 5000, RSLogix 500
and 5, RSLinx, FactoryTalk View SE and ME, FactoryTalk Historian, PowerFlex 4, 40, 525, 753, 755,
Kinetix, PanelView Plus and 5000, Stratix, POINT I/O, FLEX I/O, ArmorBlock

**Siemens**: S7-1200, S7-1500, ET200SP and ET200MP, S7-300 and S7-400 legacy, TIA Portal, STEP 7
classic, WinCC all editions, WinCC OA, SIMATIC HMI, PCS 7, PCS neo, SINAMICS G120, G130, S120,
MICROMASTER legacy, SCALANCE, F CPUs

**Others**: Schneider Modicon M221, M241, M251, M580, Quantum, Control Expert, Altivar, Magelis.
Beckhoff TwinCAT 2 and 3, EL and EP terminals. Mitsubishi FX, Q, iQ-R, iQ-F, GX Works2 and 3, GOT,
FR drives. Omron NX, NJ, CJ, CS, Sysmac Studio, CX-Programmer. ABB AC500, Automation Builder,
ACS355, ACS580, ACS880. Emerson PACSystems RX3i, RSTi, Proficy. WAGO 750 and PFC200, e!COCKPIT.
Phoenix Contact PLCnext. Codesys runtime and IDE (underlies half the vendors above).
AutomationDirect Productivity, CLICK, Do-more (unusually well documented and freely available).
Keyence KV, IDEC, Delta, Unitronics, Red Lion. Safety: Pilz PNOZ and PSS, Sick Flexi Soft, Banner
XS26

## standards

- IEC 61131-3 (PLC languages), IEC 61499
- ISA-88 (batch), ISA-95 (integration), ISA-101 (HMI), ISA-18.2 (alarm management)
- ISA/IEC 62443 series (OT security). NIST SP 800-82 **(seeded, and the free one)**
- IEC 61508, IEC 61511 (SIL)
- ISO 13849-1 (PL), ISO 12100, IEC 62061
- ISO 10218-1 and 2, ISO/TS 15066, ANSI/RIA R15.06
- NFPA 79, NFPA 70 (NEC), NFPA 70E, NFPA 72, NFPA 110. Free access viewer **(seeded)**
- IEC 60204-1
- UL 508A, UL 61010, UL 60947, UL 61800-5-1
- IPC-2221 and 2222, IPC-A-610, IPC-7351, J-STD-001
- IEEE 519, IEEE 1584, IEEE 142, IEEE 3007 series, IEEE C37
- NEMA 250 against IEC 60529 IP ratings, NEMA ICS
- Hazardous locations: NEC 500 to 506, ATEX, IECEx, Class/Division against Zone
- CE, Machinery Directive 2006/42/EC and the Machinery Regulation, UKCA
- ISO 9001, IATF 16949, AS9100
- FDA 21 CFR Part 11, GAMP 5, ISPE guides
- OSHA 1910.147 **(seeded)**, 1910.212, 1910.333

## silicon

- STM32 F0, F1, F4, G4, H7, U5: reference manuals, datasheets, app notes, CubeMX
- ESP32, ESP32-S3 **(seeded)**, C3, C6: TRMs, ESP-IDF, hardware design guidelines
- Microchip PIC, AVR and ATmega, MPLAB
- TI MSP430, C2000 (motor control), Sitara AM335x and AM62x
- NXP i.MX 6, 8, 9, Kinetis, S32K
- Renesas RA, RX, RL78. Nordic nRF52, nRF53, nRF54
- RP2040 **(seeded)**, RP2350, BCM2711 **(seeded)**, BCM2712
- FPGA: AMD 7 Series, Artix, Zynq 7000, UltraScale. Intel Cyclone IV, V, 10. Lattice iCE40, ECP5
- Rockchip RK3568 and RK3588, Allwinner H6
- Analog: op amps, instrumentation amps, delta sigma ADCs for metering, isolation amps AMC1301 and AMC1311
- Digital isolators ADuM and Si86xx, optocouplers 4N35 and PC817, gate drive optos HCPL-3120
- Power semis: IGBT, SiC, GaN, IPM modules (Infineon, Wolfspeed, onsemi, Mitsubishi), SCR, bridges
- Gate drivers, desat protection, snubber design notes
- PMICs, LDOs, buck and boost, isolated DC/DC
- Current sensing: ACS712, ACS37002, shunt plus amp, Rogowski, CTs
- RS485 transceivers MAX485, SN65HVD72, THVD. CAN TJA1050, MCP2551, MCP2515
- Ethernet PHYs LAN8720, KSZ8863. Industrial ASICs netX, ERTEC, EtherCAT ET1100
- Memory: NOR flash, eMMC, EEPROM, DDR3 and DDR4, FRAM. RTCs, watchdogs, supervisors
- Sensor front ends: MAX31855, MAX31856, MAX31865, HX711. MEMS IMUs for vibration

## instrumentation

- Pressure and DP: Rosemount 3051, E+H Cerabar, Yokogawa EJA, Siemens Sitrans
- Flow: magnetic, coriolis, vortex, ultrasonic, turbine, thermal mass
- Level: radar, guided wave, ultrasonic, capacitance, float
- Temperature: RTD PT100 and PT1000, thermocouple types J, K, T, E, N, R, S, B, wells, transmitters
- Presence: inductive, capacitive, photoelectric, ultrasonic, magnetic. Banner, Sick, Keyence,
  Pepperl+Fuchs, Turck, IFM
- Vision: Cognex In-Sight and DataMan, Keyence CV and IV, Basler. Lighting and lens selection
- Barcode, 2D code, RFID and NFC (industrial UHF)
- Load cells, weighing controllers, torque sensors
- Valves and actuators: Fisher DVC6200, Emerson, Rotork, Belimo
- Pneumatics: SMC, Festo, Parker. Valve manifolds and IO-Link
- Gas and flame detection. Calibration: Fluke process calibrators, NIST traceability

## robotics-motion

- FANUC (R-30iB, KAREL, TP), ABB (IRC5, OmniCore, RAPID), KUKA (KRC4, KRL), Yaskawa Motoman,
  Universal Robots (URScript, e-Series), Kawasaki, Epson, Staubli, Doosan, Techman
- ROS and ROS 2, MoveIt, ros2_control
- Servo drives and motors, stepper drivers, torque and inertia matching
- Encoders: incremental, absolute, SSI, BiSS-C, EnDat, resolvers, Hiperface
- PLCopen Motion Control function blocks, cam, gearing, electronic line shaft
- Linear motion: ball screws, rails, gantries. THK, Bosch Rexroth, Igus
- AGV and AMR platforms, safety scanners (Sick, Hokuyo)
- End of arm tooling, grippers (Schunk, Robotiq), vacuum

## software-scada

- Ignition by Inductive Automation (excellent free docs, plus the Exchange)
- AVEVA System Platform and InTouch, AVEVA PI System
- Kepware KEPServerEX, Matrikon, Softing
- Node-RED and industrial nodes
- Grafana, InfluxDB, TimescaleDB, Telegraf
- Docker, Kubernetes and K3s at the edge, Balena
- Linux (Debian, Yocto, Buildroot), RTOS (FreeRTOS, Zephyr, QNX, VxWorks, PREEMPT_RT)
- PostgreSQL, SQL Server, SQLite for edge logging
- MES and OEE: Tulip, MachineMetrics, SAP ME, Critical Manufacturing
- CMMS: Fiix, Limble, UpKeep, IBM Maximo
- PLC version control: Copia, Octoplant, git strategies for L5X and XML exports
- Simulation: Emulate3D, Factory IO, Simulink and Simscape, Visual Components
- ECAD: EPLAN Electric P8, AutoCAD Electrical, SolidWorks Electrical, KiCad, Altium
- Panel design and UL 508A build practice

## safety

- Light curtains, safety laser scanners, safety mats, two hand controls
- E-stops, cable pull, interlocks, guard locking (Euchner, Fortress, Schmersal)
- Safety relays and safety I/O, muting
- LOTO devices and procedures, energy isolation, stored energy
- Risk assessment templates, safety circuit examples (categories, PL, SIL)

## maintenance

- Vibration analysis, ISO 10816 and 20816 severity, bearing fault frequencies
- Thermography (Fluke, FLIR), acceptance criteria, ultrasound
- Oil analysis, lubrication charts, grease compatibility
- Bearings (SKF, Timken), belts and sheaves, couplings, alignment, gearboxes
- Bolt torque and tension tables
- FMEA, RCM, MTBF and MTTR, criticality ranking
- Spares strategy and obsolescence tracking

---

## Original notes to write (`notes/`)

These are the reason to visit. Everything above is a link somebody else could have found.

- Which document do I actually need. A router, because finding the doc is the real problem
- ~~RS485 will not talk: a decision tree~~ **WRITTEN**, `notes/rs485-will-not-talk.md`. **Its triage
  order is owed and is Keaton's to pay.** The routing is anchored to pages of the spec. The ORDER is
  reasoned from the document rather than from having chased it on a live bus, and it is labelled as a
  first cut in the page itself. Three questions the page asks out loud and cannot answer:
  - **Is polarization the answer four times in five?** Then it moves to the top and stops being a row
    in a table.
  - **What fails that the spec never describes?** The spec documents a correct bus. It does not
    document the ways real ones break.
  - **Which vendors sit on which side of the 19200 baud timer split?** Above 19200 the spec stops
    scaling t1.5 and t3.5 and recommends fixed values, so two correct implementations disagree and
    drop frames only at high baud. **Nobody publishes that table.** This repo could own it and it
    would likely be the single most valuable page here.
- Profinet drops: a decision tree
- VFD faults on acceleration: a decision tree
- Vendor fault code indexes with diagnosis notes
- Startup and commissioning checklists
- Panel build conventions, wire color and numbering schemes
- Retrofit playbooks: PLC-5 to CompactLogix, and friends
- A glossary translating between the electrician, controls, and IT vocabularies for the same thing
- Obsolescence watch: what got deleted from which vendor library and when

## Where the hard to find documents live

- Rockwell Literature Library, Siemens SIOS, Schneider Download Center and Green Book, ABB Library,
  Mitsubishi FA, Omron eData
- Bitsavers and archive.org for discontinued and pre 2005 equipment
- The Wayback Machine for dead vendor pages
- Public.Resource.Org for standards incorporated by reference into US law
- NIST, DOE, EPRI, OSHA eTools, NREL
- PLCTalk forum and r/PLC file threads, often the only surviving copy of an obsolete manual
- Distributors: AutomationDirect, Galco, Radwell, which frequently host manuals the OEM deleted
- Used equipment listings, for nameplate and wiring diagram photos
