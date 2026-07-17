# What arrived, not what you did

**The triage order on a new install is the opposite of the one that works everywhere else.**

On a running machine you suspect what changed, and what changed is usually what you touched. That
order is correct and it is earned, because the machine ran yesterday. Yesterday is a baseline. It is
the whole reason [Diagnose by deviation](diagnose-by-deviation.md) works.

On a new install there is no yesterday. Nothing has ever run. So the instinct to suspect your own
work is not a diagnostic method at all, it is a habit borrowed from a situation that does not apply,
and it will cost you weeks.

Invert it. **The parts you touched are the only parts you have first hand knowledge of. The parts
that arrived are the unverified ones.** They are unverified precisely because they arrived labelled
as verified, which is exactly why nobody looks at them.

## Where this came from

A new tool, being built out and integrated. Communications, power, the physical arms, and the tie in
to the fab supervisory layer. One chamber's pedestal and wafer lift would not answer a ping and would
not talk.

Weeks went into validating every variable. Control boards. Cables. Power sources. Logic. Software
configuration. All of it under an assumption that arrived with the crate: the tool had passed
functionality testing at the previous build facility. That assumption did not sit in the background.
It defined the search. If the tool was good when it shipped, and it is not good now, then the fault
is something I did while commissioning and integrating it.

The fault was not something I did. It was a control switch, seen at two in the morning after saying
the thing you say at two in the morning.

## Why every method available had already failed

This one is told in full because it is the clearest of the four, not because it is the only one. It
is worth the page because the switch was not subtle. It was undocumented, and undocumented defeats a
documentation based method by construction. Four paths, four dead ends:

**The drawings could not find it.** The device was improvised. It smoothed out the wafer lift
movement and somebody had added it. It was never on a drawing, so reading the source documents, which
is the correct first move and the one this whole repo is organised around, was structurally incapable
of finding it. The drawing was not wrong. The drawing was describing a different machine than the one
in the room.

**The measurement could not find it, and it failed by being right.** Power to the lift measured good.
That reading was true. Power was present. What was not visible is that the improvised device sat last
in the path from the power source to the lift, so the honest sentence "power to the lift is good" was
really "power reaches the device that feeds the lift." A correct measurement, a false conclusion, and
nothing in the measurement to warn you, because the instrument was never wrong. Only the label on it
was. **This is the failure that gets called a good result and closed.**

**The inherited validation could not find it.** It passed somewhere else. The switch on the device was
misconfigured, and it was misconfigured when it arrived.

**Looking could not find it.** The one affordance that would have made the device discoverable is that
it is supposed to be visible from outside the tool. It had been crammed up underneath, near the
chamber structure, by whoever put it there.

## The real lesson is about the baseline you were handed

[Diagnose by deviation](diagnose-by-deviation.md) needs a record of healthy taken before you need it.
A new install has none. That is the honest version of the problem and it is survivable, because a
person who knows they have no baseline goes and builds one.

The trap is that a new install does not hand you nothing. **It hands you a fiction.** Somebody else's
validation, performed at a facility you were not standing in, witnessed by nobody you can ask,
arriving stamped as complete. That is not an absent baseline. It is a false one, and a false baseline
is worse than no baseline in the one way that matters: it draws a box, you search inside the box, and
the box is not where the fault is.

**An inherited verification is not a verification.** It is a claim that somebody checked something,
somewhere, once. It is the weakest link in any chain of reasoning you build on top of it, and it is
invisible, because unlike every other weak link it arrives already labelled done. This repo exists for
the same reason: a row that says `LOCATED ONLY` and a confident bullet with a working link look
identical to a reader, and they are worth wildly different amounts. That previous build facility
handed over a `TRACED`. It was a `LOCATED ONLY` wearing the label. The README says the person who
finds out is a tech standing in front of the equipment. That is what this page is.

## The order, and exactly how far it is earned

**All five steps were paid for, across four installs.** The story above is told in full because one
story teaches better than a tally, but it is not the sample. The order comes from four new tool
installs that failed final testing, across plasma, CVD, and etch, and the fault was a different class
each time: a bad component, a bad configuration, and, more than once, documentation that did not match
the machine in the room. Four installs, three failure classes, one order that survived all of them.

That is why this page does not carry the hedge [RS485 will not talk](rs485-will-not-talk.md) carries.
That page states plainly that its triage order was reasoned from the specification rather than chased
on a live bus, because it was. This order was chased, four times, and it earned the right to be stated
without the qualifier. The distinction between those two pages is the distinction this whole repo runs
on: a claim says how far it was actually verified, and neither says more than that.

1. **Ask what you are assuming, and where that assumption came from.** If the answer is "it was
   tested before it got here," you have found an unverified claim sitting underneath every other step
   you are about to take. Write it down as a claim, not as a fact.
2. **Suspect what arrived before what you did.** Your own work is the part you watched happen.
3. **Ask what a correct reading would look like if the fault were downstream of where you measured.**
   "Power is present" is a fact about the point of the probe, never about the load. Know what is last
   in the path, and know it from the machine rather than from the drawing.
4. **Assume the machine has been modified and the modification is not written down.** On custom or
   field modified gear this is the normal case, not the exotic one. Any device you can see and cannot
   find on a drawing outranks everything on the drawing.
5. **Go look at the hardware, physically, from the primary build up.** Last resort in the order that
   works on a running machine. Not last here.

## What this page does not say

It does not say skip the documents. Reading the source documents is still the first move and it is
right almost every time. This page is about the residue: the case where the documents are correct and
the machine does not match them, which no amount of reading resolves, because the disagreement is not
in the reading.

It does not name the tool, the vendor, or the facility. The improvisation matters. The logo does not.

It is not a procedure and it decides nothing about what anyone opens, touches, or energizes. It is an
order of suspicion, which is a thing you carry in your head before you pick up a meter.
