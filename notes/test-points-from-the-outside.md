# Test points from the outside, when the inside will not talk

**This page has no procedure in it, no signature, and no data.** It is a method, and it is the
companion to [Diagnose by deviation, not by symptom](diagnose-by-deviation.md). Read that one first.
This page only exists to attack the one exception that page admits defeat on.

## The exception

The method page is honest about its own scope, and this is the limit it names:

> You need test points, which means you need to have influenced the design, or gotten lucky. On
> somebody else's sealed product you are back to the symptom table.

That is a real limit and it covers most equipment most people touch. You did not design it. Nobody
who did design it works there anymore. It has no test points, no data interface worth the name, and
the controller cannot tell you anything useful about what it just did.

**The claim of this page is that the limit is smaller than it looks.** Not gone. Smaller.

## The thing nobody tells you

A machine is not one witness. It is many, and only one of them is the controller.

Every serious process has instruments hanging off it, because the process needed them to run at all.
Pumps. Lamps. Thermocouples on the chuck. Pressure sensing upstream and downstream. Mass flow
controllers. These are not there for your benefit and nobody thought of them as diagnostics. They are
there because the process does not work without them.

And here is the part that matters: **those instruments were never asked to keep the controller's
secrets.** They report what is physically happening, continuously, in current and in voltage and in
impulse response, whether or not the brain of the machine has anything to say about it.

So when the controller will not talk, the question is not "how do I make the controller talk." It is:

**Who else saw it?**

## Inside out, and outside in

The default way to instrument a machine is inside out. Go to the controller, ask it for its data,
take whatever it decides to give you, and be limited by what its designers, long retired, thought was
worth reporting at the time.

The other way is outside in. Ignore the controller. Go to the instruments, take the signal at the
physical layer, and build your own record of what the process actually did.

Outside in is worse in every respect except the ones that matter:

| | Inside out | Outside in |
|---|---|---|
| Effort | Low, if it works at all | High. You are building the thing. |
| Blessing | Vendor supported | Nobody's idea of standard practice |
| What you get | What the designer chose to expose | What you chose to observe |
| Works on a sealed legacy machine | Frequently not | Frequently yes |

The last two rows are the whole argument. **Inside out, the observables were chosen for you, by
someone who has never met your problem.** Outside in, you choose them. That is a real gain and it
survives even on machines where inside out works fine.

## Why this is not usually done, which is not the reason you think

It is not that it is hard. It is that **the interface is physical, and that filters people out.**

There is no port. There is no protocol. There is no document. There is a cable, and the cable is very
often a circular locking connector, twist on, quarter turn, the kind that the floor calls a military
style connector because that is the only name anyone ever used for it. Elsewhere it is ribbon. The
signal is a handful of conductors and you have to know which ones carry what before anything else can
begin.

That is not intellectually difficult. It is just outside the boundary of everybody's job. The
software people do not open panels and the panel people do not build loggers, so the work sits there
for years, in plain view, undone.

**A second reason, and it is the honest one: the people who do figure it out have every incentive to
keep it.** This kind of rig makes the person who built it the person you have to ask. That is worth
something to them and they are not wrong that it is worth something. Which is why there is almost
nothing written about this anywhere, and why this page exists.

## The method

The three moves from the method page still hold. What changes is where the test points come from.

### 1. The test points already exist, and nobody calls them that

You do not need to have influenced the design. You need to find which instruments are already on the
machine and which of them will give up a signal.

They will not be labelled as diagnostics. They are process equipment. Pumps, lamps, heaters, flow
control, pressure sensing, anything with a transducer in it. Each one is a witness to some part of
what happened, and collectively they can be a better witness than the controller, because there are
more of them and none of them is editorialising.

**What you get is analog, and that is a feature.** Current, voltage, an impulse response whose shape
depends on the sensor. This is below the digital layer, and below the digital layer nobody can
deprecate you, refuse your handshake, or tell you the field is reserved. The physics does not have a
firmware version.

### 2. You have to build the box, and the box is the price of admission

Something has to sit between those conductors and you, log what they are doing, and hand it onward in
a form a computer can use. That is a real build, it is custom to the process, and there is no
purchasing it.

This is the part that gets called rigged, usually by the person who built it. Worth separating two
things that get confused here: **the plumbing was improvised, the method was not.** Improvised
plumbing feeding a controlled before and after comparison is an experiment. Beautiful plumbing
feeding nothing is furniture.

### 3. Build the record, then find the difference

Which is the entire method page, and it does not change:

- Characterize the thing before the process runs.
- Log continuously while it runs.
- Characterize it again after.
- When one fails, go to the record. What was different? What did the instruments see?

Then the mapping, over time, from deviation to cause. **That mapping is the asset**, exactly as it is
on the bench, and exactly as much not publishable.

## Two preconditions, and the second one will bite you

The method page lists what it needs. Working outside in adds two more, and they are not optional.

### Matched instruments, or your comparison means nothing

Characterize before and after **with the same instrument.** If the before measurement comes from one
tool and the after measurement comes from another, then the difference you worked so hard to find
contains the process's difference and the instruments' difference, added together, with no way to
separate them afterward.

You will have built the whole record and poisoned the one comparison it existed to support. Then the
delta is not a finding. It is an artifact, and it is worse than no data because you will believe it.

This is the same rule the method page states about signatures, one level up: a signature is a fact
about a specific bench, so someone else's baseline is not yours. The instrument is part of the
measurement. Cross instruments and you are comparing against an educated guess again, which is the
exact failure this whole method exists to escape.

### Unambiguous identity of the unit under test, and you probably do not have it

Every window of logged signal has to belong to a specific physical unit, and you have to be certain
which. Not confident. Certain.

**In a semiconductor fab this is invisible, because it is infrastructure.** The wafer carries a
physical mark and a digital record, and every leg of the process reconfirms both. Ask someone who
works there how they solved unit tracking and the question will not parse, because it was never a
problem they had.

**Almost nowhere else is like this.** Take this method to a plant, a shop, a yard, a substation, and
the thing you are measuring has no serial, no digital record, and nothing reconfirming anything at
any step. The record still gets built. The deltas still get computed. They are simply attached to the
wrong unit, sometimes, and **nothing tells you.** No error, no alarm, no smell. Just a mapping that
is quietly part fiction, that you will trust, because you built it.

So: **establish identity before you build the record, because you cannot add it afterward.** Once the
data is logged against an ambiguous unit, the ambiguity is permanent. There is no cleanup pass. If
the units cannot be told apart with certainty, fix that first or do not start.

## When this does not apply

- **Nothing may be tappable.** Some machines are genuinely sealed to the point that the instruments
  are inside the sealed part too. Then this page is over.
- **It is a build, and builds have a payback period.** For a one off on equipment you will never see
  again, the symptom table is the correct tool and this is a hobby.
- **The plumbing is yours to own forever.** Vendor supported inside out gets vendor support. This gets
  you. Whoever builds it is who maintains it, and if that person leaves and wrote nothing down, the
  fab goes back to where it started. Write it down.
- **It says nothing about whether you are allowed to.** Opening panels and landing conductors on a
  logger is a decision about somebody's equipment and somebody's safety, and this page does not make
  it. It is not a field procedure. It does not tell you what to open, touch, or energize.

## Provenance

Written from this repo author's practice: an ask to bring Applied Materials P5000 platforms onto a
fab's supervisory layer, on which Ethernet was not an option because no board on any control panel
had it, and whose own controller was in any case very limited in usability.

The route taken was outside in. Signals were read from the process peripherals instead: vacuum pumps,
lamps, chuck temperature, showerhead pressure, chamber pressure, mass flow controllers. What those
peripherals give up is current, voltage, and impulse responses whose shape depends on the sensor,
mostly over circular locking connectors, some over ribbon. Custom logging modules, built per process,
collected it and passed it onward over Ethernet to a server. The wafer was characterized before and
after, with instrument matched to instrument, and wafer identity was never in question because a fab
gives you that for free.

The result was a record: what the wafer was, what the process physically did, what the wafer became.
When one failed, the question was answerable, because the difference was in the record.

**The mapping this produced is not published here and will not be.** It was produced on an employer's
equipment and it belongs to them, and it would not help you anyway: it is a fact about those tools,
those sensors, and that process. The method is portable. The fingerprints are not.

Nothing on this page is a field procedure.
