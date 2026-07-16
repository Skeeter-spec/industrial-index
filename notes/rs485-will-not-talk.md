# RS485 will not talk

**This is a router, not a procedure.** It tells you which document and which page answers the
symptom in front of you. It does not tell you what to wire, what to set, or what to touch. Every
number you actually need lives in the document this page sends you to, and it stays there on
purpose: a value retyped into a note is a value that can be retyped wrong, and this one ends in
somebody's hands on a terminal block.

Everything below was read at modbus.org's own PDF. Page numbers are that file's own pages.

## The two documents

Most people debug this with one document and it is the wrong one.

| You are holding | It answers |
|---|---|
| The device manual | Its address, its baud and parity, whether **this** device needs polarization, and how many of it the bus tolerates. |
| **MODBUS over Serial Line, V1.02** (`modbus-org-serial-line-v1-02`) | The bus itself. Framing, timing, termination, polarization, grounding, length, device count. |

The split is not incidental, it is in the spec by design. The spec says each device **must** be
documented to state whether it needs line polarization and whether it can provide it. So the spec
tells you polarization exists and what it does, and only the manual tells you if yours wants it.
Read one document and you get half an answer, which is worse than none because it feels like a whole
one.

The serial line spec is free and it is 44 pages. That is a short afternoon and it is the highest
leverage afternoon available to anyone who works on these buses.

## Start here: the words are wrong

**This is the single biggest time sink in that document and it is why this page exists.**

You will search the PDF for the thing you are looking for, get **zero hits**, and conclude the spec
does not cover it. The spec covers it. It calls it something else.

| Your word | The spec's word | Where |
|---|---|---|
| biasing, idle state resistors, fail safe | **polarization** | 3.4.6, p.28 |
| timing, character gap, dead time | **t1.5** and **t3.5** | 2.5.1.1, p.13 |
| termination, end resistor | line termination, **LT** | 3.4.5, p.27 |
| stub, spur, drop | **derivation** | 3.4.3, p.27 |
| A and B, plus and minus | **D0** and **D1** | 3.3.2, p.22 |
| how many can I hang on it | unit load, devices without repeater | 3.4.1, p.27 |
| the message shape | MODBUS frame description | 2.3, p.8 (RTU specifically: 2.5.1, p.13) |

Grep that PDF for "biasing" and you get nothing. It is on page 28, under polarization, and it is
probably your problem.

**And one false friend, which is worse than an absent word.** Search for "turnaround" and you *will*
get a hit, on p.10. It is not the character gap you were looking for. In this spec **turnaround
delay** is the delay the master observes after a broadcast, so that slaves can finish processing
before the next request. A word that is present and means something else does not announce itself the
way a word with zero hits does. If you want the character gap, it is t1.5 and t3.5 on p.13.

## Route by symptom

Pick the row that matches what you are actually seeing. The point of splitting these is that they
send you to different places, and the most common wasted afternoon is treating all of them as one
undifferentiated "it does not work."

| What you see | Where the answer lives |
|---|---|
| **Nothing at all, from anything.** No device on the bus responds. | Physical first, per above. D0 and D1 identity and orientation, 3.3.2 p.22. Grounding arrangements, 3.4.4 p.27. Rarely subtle, and it is the one that costs the least to rule out. |
| **One device silent, the rest fine.** | Not a bus problem. That device's manual: address, baud, parity. Addressing rules and what addresses are legal are 2.2, p.8. |
| **Two devices answer at once, or one address behaves strangely.** | Duplicate address. Addressing rules, 2.2, p.8. |
| **CRC errors, garbage, partial frames.** | The bus is carrying signal and corrupting it. First rule out the free one: 2.5 p.12 requires the transmission mode **and the serial port parameters** to match on every device on the line, so one device at the wrong parity or baud is a bus wide symptom with a single device cause. Then the physical: termination 3.4.5 p.27, grounding 3.4.4 p.27. |
| **Half the bus is RTU and something is ASCII.** | 2.5, p.12. RTU is mandatory, ASCII is an option, and they do not mix on one line. |
| **Works on the bench, fails in the plant.** | Grounding 3.4.4 p.27, then polarization 3.4.6 p.28. The bench has no noise and an undriven line is defenceless against it, which is the entire reason polarization is in the spec. |
| **Works at 9600, fails at 38400 or above.** | **Read the remark at the bottom of p.13 before anything else.** See below, this one is a trap. |
| **Worked with three devices, broke when you added more.** | Device count and unit load 3.4.1 p.27, and note that polarization itself costs you devices, 3.4.6 p.28. Then length and derivations 3.4.3 p.27. |
| **First character lost or mangled, intermittently.** | Polarization, 3.4.6, p.28. An undriven idle line does not hold a defined state. |
| **You are writing the driver and the CRC never matches.** | 2.5.1.2, p.14. Check the byte order it specifies against the byte order you assumed. |

## Three traps the device manual will not warn you about

These are structural. They are in the spec, they are not in your device manual, and each one
produces a fault that looks like something else.

### 1. Polarization belongs at exactly one place on the bus

The spec is explicit: where polarization is needed it is implemented at **one location for the whole
serial bus**, and other devices **must not** implement any. Section 3.4.6, p.28.

Now look at the hardware. Vendors put a bias or termination DIP switch on **every** device, because
any one of them might be the one that provides it. Nothing on the device says "only one of these may
be on." A reasonable person wiring twelve devices flips twelve switches, because each device's
manual, read alone, says the switch is how you enable the thing the bus needs.

The result is a bus that is technically biased twelve times over, degrades as you add devices, and
reads as a noise or cable problem.

### 2. Polarization costs you devices, and termination changes with it

Two couplings that are easy to miss because they live one paragraph apart from the things they
affect:

- The maximum device count on a polarized bus is **lower** than on an unpolarized one, stated at the
  end of 3.4.6, p.28. So "it broke when I added the ninth device" can be a consequence of a decision
  made about resistors at commissioning.
- The spec's preferred line termination arrangement is **different** when polarization is present,
  3.4.5, p.28. Terminate as if it is not polarized, then polarize, and you have quietly left the
  arrangement the spec recommends.

### 3. Above 19200 baud, t3.5 is not what you think it is

This is the best one in the document and it is a **remark at the bottom of p.13**, not a heading.

Below and at 19200 baud, the inter frame and inter character delays are defined in **character
times**, so they scale with baud rate. Above 19200, the spec says respecting that literally costs too
much CPU, and recommends **fixed values instead**, which do not scale at all.

So there are two defensible readings of the same spec, and above 19200 baud they disagree. A vendor
who scales and a vendor who uses the fixed value will interoperate perfectly at 9600 and start
dropping frames at 38400, where each end is enforcing a different idea of where the frame ended. It
presents as a cable problem, a noise problem, or a "that device is junk" problem. It is none of
those. It is two correct implementations of one paragraph.

**If the bus works at 9600 and fails at 38400, read that remark before you buy cable.**

## What this page is missing, and it is the important part

The routing above is anchored: every claim on it traces to a page of the spec that was read at
modbus.org, not at a mirror and not from memory.

**The triage order is not, and this section exists to keep saying so.** It is reasoned from the
document, not from having been wrong about it in a plant at 2am, and that is exactly the ingredient
the `notes/` standing rule asks for and the only one reading cannot supply. A real order comes from
what actually turns out to be the culprit and how often.

This page was briefly published with an order claimed as practiced. It was not. The claim came from
answering a multiple choice question rather than from an account of what happened, which is a way of
manufacturing agreement and not a way of learning anything. It has been withdrawn. That failure is
worth leaving on the record here, because it is the same failure the `verified_level` column exists
to catch: a confident statement whose evidence nobody looked at.

Still open, and stated rather than guessed at:

- **What is the real order?** If polarization is the answer four times in five, it belongs at the top
  and not in the middle of a table.
- **What fails that the spec never describes?** The spec documents a correct bus. It does not
  document the ways real ones break, and that gap is where a page like this earns its keep.
- **Which vendors sit on which side of the 19200 split?** Nobody publishes this. It stays open rather
  than invented, because a fabricated interoperability table would be worse than the silence it
  replaced.

Corrections from anyone who has actually chased this are worth more than the page is. Open an issue.

## Sources

| Row | Level |
|---|---|
| `modbus-org-serial-line-v1-02` | `TRACED`. Sections 2.2, 2.5.1, 2.5.1.1, 2.5.1.2, 3.3.2, 3.4.1 to 3.4.6 read at modbus.org 2026-07-15. |

Nothing on this page is reproduced from that document. It is a map of it. The spec is free, it is 44
pages, and if you are debugging one of these buses you should be reading it rather than this.

Nothing on this page is reproduced from that document. It is a map of it. The spec is free, it is 44
pages, and if you are debugging one of these buses you should be reading it rather than this.
