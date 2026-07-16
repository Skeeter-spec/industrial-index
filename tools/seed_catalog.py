#!/usr/bin/env python3
"""Write the initial catalog.csv.

    ./tools/seed_catalog.py            # refuses to clobber an existing catalog
    ./tools/seed_catalog.py --force

Run once, at scaffold time. Kept in the repo because the seed rows are a worked example of the
schema (including the ugly cases: unknown licenses, gated standards, a vendor that deleted the file),
and because hand writing CSV rows with commas in the titles is how you get an unparseable catalog.
csv.writer quotes correctly; a human typing between commas does not.

EVERY SEED ROW IS LOCATED ONLY. Not one of them has been opened by the person who wrote this file.
That is not a placeholder to fix later, it is the honest starting level, and the gate is fine with
it. What the gate is not fine with is a row claiming more than that.
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "catalog" / "catalog.csv"

COLUMNS = [
    "id", "title", "vendor", "doc_number", "revision", "revision_date", "category",
    "url", "archive_url", "license", "redistributable", "license_basis", "local_path", "sha256",
    "verified_level", "verified_date", "notes",
]

TODAY = "2026-07-15"

# archive_url is deliberately left empty on every seed row. tools/archive.py fills it, and until it
# does, gate.sh reports these rows as unfinished. Pre filling a snapshot URL that was never taken
# would be a fabricated citation of the cheapest kind: a plausible string in a URL shaped column.
ROWS = [
    dict(
        id="modbus-org-application-protocol-v1-1b3",
        title="MODBUS Application Protocol Specification",
        vendor="modbus.org", doc_number="n/a", revision="V1.1b3", revision_date="2012-04-26",
        category="protocols",
        url="https://www.modbus.org/file/secure/modbusprotocolspecification.pdf",
        license="unknown", redistributable="no",
        notes="The function code and exception code reference. The one protocol spec that is free, "
              "canonical, and short enough to actually read. WARNING: the URL no longer encodes the "
              "version, so modbus.org can ship a new revision at this exact path. The V1.1b3 in "
              "this row is UNVERIFIED against the file. This is the cites rev C links rev A case.",
    ),
    dict(
        id="modbus-org-serial-line-v1-02",
        title="MODBUS over Serial Line Specification and Implementation Guide",
        vendor="modbus.org", doc_number="n/a", revision="V1.02", revision_date="2006-12-20",
        category="protocols",
        url="https://www.modbus.org/file/secure/modbusoverserial.pdf",
        license="unknown", redistributable="no",
        notes="RTU framing, timing, termination, biasing. Where the answer to most RS485 will not "
              "talk problems actually lives. Version agnostic URL, same caveat as the application "
              "protocol row.",
    ),
    dict(
        id="modbus-org-tcp-implementation-guide-v1-0b",
        title="MODBUS Messaging on TCP/IP Implementation Guide",
        vendor="modbus.org", doc_number="n/a", revision="V1.0b", revision_date="2006-10-24",
        category="protocols",
        url="https://www.modbus.org/file/secure/messagingimplementationguide.pdf",
        license="unknown", redistributable="no",
        notes="MBAP header, unit id against slave id, connection handling. Version agnostic URL, "
              "same caveat as the application protocol row.",
    ),
    dict(
        id="nist-sp-800-82r3",
        title="Guide to Operational Technology (OT) Security",
        vendor="NIST", doc_number="SP 800-82r3", revision="r3", revision_date="2023-09-28",
        category="standards",
        url="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf",
        license="public domain (US government work)", redistributable="yes",
        notes="The OT security reference that is not behind a paywall, unlike IEC 62443. US "
              "government work, so this one can actually be mirrored here.",
    ),
    dict(
        id="osha-1910-147",
        title="The control of hazardous energy (lockout/tagout)",
        vendor="OSHA", doc_number="29 CFR 1910.147", revision="n/a", revision_date="",
        category="safety",
        url="https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
        license="public domain (US government work)", redistributable="yes",
        notes="The regulation itself, not a vendor's summary of it. Free, quotable, and the actual "
              "legal text behind every LOTO procedure.",
    ),
    dict(
        id="rpi-rp2040-datasheet",
        title="RP2040 Datasheet",
        vendor="Raspberry Pi Ltd", doc_number="n/a", revision="n/a", revision_date="",
        category="silicon",
        url="https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf",
        license="CC BY-SA 4.0", redistributable="yes",
        notes="Rare case of a chip datasheet under an open license. Verify the license notice inside "
              "the PDF before trusting this row's redistributable=yes.",
    ),
    dict(
        id="rpi-bcm2711-peripherals",
        title="BCM2711 ARM Peripherals",
        vendor="Raspberry Pi Ltd", doc_number="n/a", revision="n/a", revision_date="",
        category="silicon",
        url="https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf",
        license="unknown", redistributable="no",
        notes="The SoC behind the Pi 4. Register level detail that the Pi documentation site "
              "summarizes and loses.",
    ),
    dict(
        id="espressif-esp32-s3-trm",
        title="ESP32-S3 Technical Reference Manual",
        vendor="Espressif Systems", doc_number="n/a", revision="n/a", revision_date="",
        category="silicon",
        url="https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf",
        license="unknown", redistributable="no",
        notes="Revision moves without the URL changing, which is exactly the case verified_level "
              "exists to catch.",
    ),
    dict(
        id="oasis-mqtt-v5-0",
        title="MQTT Version 5.0",
        vendor="OASIS", doc_number="mqtt-v5.0", revision="5.0", revision_date="2019-03-07",
        category="protocols",
        url="https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html",
        license="unknown", redistributable="no",
        notes="The base spec under Sparkplug. Read the OASIS IPR terms before flipping "
              "redistributable.",
    ),
    dict(
        id="eclipse-sparkplug-3-0-0",
        title="Sparkplug Specification",
        vendor="Eclipse Foundation", doc_number="n/a", revision="3.0.0", revision_date="2022-11-17",
        category="protocols",
        url="https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf",
        license="unknown", redistributable="no",
        notes="What makes MQTT usable for plant data: birth and death certificates, state "
              "management, the topic namespace.",
    ),
    dict(
        id="odva-cip-networks-library",
        title="The CIP Networks Library (EtherNet/IP)",
        vendor="ODVA", doc_number="n/a", revision="n/a", revision_date="",
        category="protocols",
        url="https://www.odva.org/technology-standards/key-technologies/ethernet-ip/",
        license="proprietary, purchase required", redistributable="no",
        level="GATED, UNREAD",
        notes="Landing page only. The spec itself is sold and it is expensive. Cite it by number, "
              "paraphrase structure, never reproduce. A GATED, UNREAD row is still a useful row: it "
              "tells a reader the document exists, what it covers, and what it costs.",
    ),
    dict(
        id="nfpa-free-access",
        title="NFPA Free Access to codes and standards",
        vendor="NFPA", doc_number="n/a", revision="n/a", revision_date="",
        category="standards",
        url="https://www.nfpa.org/codes-and-standards/free-access",
        license="proprietary, read only viewer", redistributable="no",
        level="GATED, UNREAD",
        notes="How to legally read NFPA 70, 70E, and 79 for free. A pointer to a viewer, not a "
              "document. Never mirror anything reached through it.",
    ),
]


def main():
    if OUT.exists() and "--force" not in sys.argv:
        print(f"refusing to clobber {OUT.relative_to(ROOT)} (pass --force)")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        for r in ROWS:
            row = {c: "" for c in COLUMNS}
            src = dict(r)
            # A row may override the default level. Gated documents are not LOCATED ONLY: nobody
            # located their content, only their price.
            level = src.pop("level", "LOCATED ONLY")
            row.update(src)
            row["archive_url"] = ""
            row["verified_level"] = level
            row["verified_date"] = TODAY
            w.writerow(row)
    print(f"wrote {len(ROWS)} rows to {OUT.relative_to(ROOT)}")
    print("No row is above LOCATED ONLY and none has a snapshot. gate.sh will say so.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
