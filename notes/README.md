# notes/

Original content. **This is the reason to visit.**

The catalog is a manifest, and a good one, but the links in it are a commodity: anyone with a search
engine and a free afternoon can find the Rockwell literature library. Nobody is going to star a repo
for that, and more importantly nobody is going to be helped by it at 2am, because the problem was
never that the manual is hard to find. The problem is knowing which manual, which section, and what
the manual does not say.

That is what goes here, and it is the part that cannot be scraped, generated, or bookmarked.

## What belongs

- **Routers.** "Which document do I actually need." The highest value page in the repo and the one
  that only exists if someone has already had the problem.
- **Decision trees.** RS485 will not talk. Profinet drops. VFD faults on accel. The shape of these is
  a triage order, and the order comes from having been wrong about it before.
- **Gotchas the manual omits.** The reason the answer to most RS485 problems is in the serial line
  spec's biasing and timing sections rather than in the device manual you were reading.
- **Retrofit playbooks.** PLC-5 to CompactLogix and its friends. What breaks, what surprises you.
- **The translation glossary.** An electrician, a controls engineer, and an IT admin have three names
  for the same thing and each assumes the other two are talking about something else. Writing that
  table down is worth more than it sounds.
- **Obsolescence watch.** What got deleted from which vendor library and when. This one compounds:
  every entry is a document that is now only reachable through this repo's snapshot column.

## What does not belong

- Anything reproduced from a copyrighted document. Write it longhand from understanding, or cite it
  and link it. See [POLICY.md](../POLICY.md).
- Standards tables. Not paraphrased, not "just the structure," not IEC, ISO, IEEE, UL, or NFPA.
- Anything that reads as a field procedure. These notes help you find and understand the right
  document. They do not replace reading it, and nothing here should decide what anyone wears,
  touches, opens, or energizes.

## What is here now

- **[Diagnose by deviation, not by symptom](diagnose-by-deviation.md)**. The method page. Build the
  health check in, record what healthy looks like before you need it, and trace differences back to
  causes. Read this one first: it explains why everything else in this directory is the second best
  way to work, and why that is still worth doing well.
- **[RS485 will not talk](rs485-will-not-talk.md)**. A router into the serial line spec, including
  the words that spec does not use for the things it covers.
- **[Modbus TCP: the unit id is not the slave id, except when it is](modbus-tcp-unit-id.md)**. The
  field the spec repurposes rather than removes.
- **[What arrived, not what you did](what-arrived-not-what-you-did.md)**. The second exception the
  method page concedes, and the one it never names. Deviation needs a record of healthy taken before
  you need it, and a new install has none, because nothing has ever run. Worse: it does not hand you
  nothing, it hands you a fiction. Somebody else's validation, performed at a facility you were not
  standing in, arriving stamped complete. A false baseline draws the search box, and the fault is
  outside the box. Includes the four paths an undocumented modification defeats by construction, one
  of which fails by producing a correct measurement.
- **[Test points from the outside, when the inside will not talk](test-points-from-the-outside.md)**.
  The companion to the method page, and an attack on the one exception that page concedes: on a sealed
  legacy machine with no test points and a controller that will not talk, you are supposed to be back
  to the symptom table. You are not. The process instruments are test points nobody designed as test
  points, they report in current and voltage below the digital layer, and they never needed the
  controller's permission. Includes the two preconditions that decide whether the record you build is
  a finding or a fiction.

## Standing rule

If a note can be replaced by a link, make it a link. The catalog is for links. This directory is for
the things that took someone a bad afternoon to learn.

## The line on other people's work

Characterization done for an employer belongs to that employer. **The method is portable, the tables
are not.** Nothing here publishes a signature, a fingerprint, or a symptom table produced on someone
else's payroll, and nothing here ever will.

That is not only a legal boundary, it is a technical one. A signature is a fact about a specific
board, a specific revision, and a specific bench. Someone else's baseline is not yours, and using it
as one is the exact mistake the method exists to avoid. So the constraint and the pedagogy point the
same way, which is the tell that the line is drawn in the right place.
