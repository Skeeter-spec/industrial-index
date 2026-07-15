# Modbus TCP: the unit id is not the slave id, except when it is

**This is a router, not a procedure.** It says which document and which page answers the thing in
front of you. The field layouts, byte counts and encodings live in the spec and stay there: this page
does not retype them, because a retyped byte count is a byte count that can be retyped wrong.

Everything below was read at modbus.org's own PDF, `modbus-org-tcp-implementation-guide-v1-0b`,
V1.0b, October 24 2006. Page numbers are that file's own.

## The one sentence

Modbus TCP is the same application protocol as Modbus RTU with a different envelope. Function codes,
register semantics and exception codes do not change, so **the spec you actually want open most of
the time is the Application Protocol spec**, not this one. This one only explains the envelope.

| You want | Read |
|---|---|
| Function codes, exception codes, register model | Application Protocol spec (`modbus-org-application-protocol-v1-1b3`). The TCP guide says so itself on p.2 and defers to it. |
| The MBAP header, the unit id, port 502, connections | This guide. |
| Why the serial bus will not talk | The serial line spec, and [RS485 will not talk](rs485-will-not-talk.md). |

## The unit id, which is the whole point of this page

On serial, the first byte of the frame is the slave address, and it is how one device on a shared
wire knows the message is for it. On TCP, the device already has an IP address, so that job is done
and the address byte looks redundant.

It is not removed. It is **repurposed**, and the spec is specific about what into: the slave address
field is replaced by a one byte **Unit Identifier** in the MBAP header, and its stated purpose is
routing **through** something. Bridges, routers, and gateways that sit on one IP address and front
**multiple independent Modbus end units** need a way to say which one. That is the unit id. Read it
on p.5 and p.6, where the spec calls it intra system routing and gives the gateway to serial case as
the typical one.

So which value do you send?

- **Through a gateway to a serial device**: the unit id is the serial slave address. This is the case
  the field is designed for and the case where it behaves exactly as you would hope.
- **Straight to a native TCP device**: the field has no job. The spec gives it a purpose that does
  not apply, and does not tell you what a device with nothing to route to should do with it.

**That silence is the entire problem, and it is not a defect in your setup.** The spec defines the
field's purpose, not the behaviour of a device for which that purpose is vacuous. Implementations
therefore differ, legitimately, and a device that ignores the unit id and a device that demands a
particular one are both reading the same document. Which one yours is belongs in its manual, not
here, and that split is why "it works from my laptop but not from the PLC" is usually a unit id
disagreement rather than a network problem.

The client's obligation is stated plainly and is worth knowing: the client sets it, and the server
**must return the same value** in the response, p.6.

## Traps that are in the spec and not in your device manual

### 1. The header is big endian, and the serial CRC is not

The MBAP fields are **big endian**, said once, as a one line remark at the bottom of p.6.

Now hold that next to the serial line spec, where the RTU CRC goes out **low byte first** (serial
spec 2.5.1.2, p.14). Same protocol family, two documents, opposite byte orders, each stated in
passing. If you have written both an RTU driver and a TCP driver you have met this, and if you have
written one and are now writing the other, this paragraph is the one to remember.

### 2. The length field counts the unit id

The length field is a byte count of what follows it, and the spec says explicitly that this
**includes the Unit Identifier**, p.5.

The unit id is easy to think of as part of the header rather than part of the payload, because it is
physically in the header. Count it the way it looks and you are off by one, on every single frame,
which presents as a parser that works until it does not.

### 3. Port 502 is registered, and the connection is meant to stay open

Port 502, p.6.

Connection management is section 4.2, p.9 to p.13, and the part that surprises people is on p.13:
the connection is meant to be **held open** for the duration of the communications, and a client may
have several transactions outstanding at once without waiting for the previous one to finish. That is
what the transaction identifier in the header is for, p.5: pairing responses to requests when more
than one is in flight.

A client that opens a connection, does one read, and closes it will work, and will also produce a
device that runs out of sockets, a switch that logs constant churn, and latency nobody can explain.
The spec is describing a persistent connection. Treating Modbus TCP like a series of one shot
requests is a design choice being made by accident.

## What is owed on this page

**Solid.** Every claim traces to a page of the guide, read at modbus.org.

**Owed, and it is the same shape as the gap on the RS485 page:** the spec does not say what a native
TCP device should do with a unit id it cannot route, so implementations differ. **Which devices want
1, which want 255, which ignore it entirely, and which reject the frame** is a real fact, it is
knowledge held only by people who have connected to them, and nobody publishes the table.

The repo's author has run Modbus TCP in the field, so that table is buildable here and is not
guessed at in the meantime. If you have fought this on specific hardware, open an issue: a device
name and what it wanted is a complete contribution.

## Sources

| Row | Level |
|---|---|
| `modbus-org-tcp-implementation-guide-v1-0b` | `TRACED`. Sections 1.1, 3.1.3, 3.2, 4.2 read at modbus.org 2026-07-15. |
| `modbus-org-serial-line-v1-02` | `TRACED`. 2.5.1.2 read for the CRC byte order comparison. |

Nothing here is reproduced from those documents. This is a map of them. Both are free and short, and
if you are writing a driver you should be reading them rather than this.
