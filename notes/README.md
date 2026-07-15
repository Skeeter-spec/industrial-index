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

## Standing rule

If a note can be replaced by a link, make it a link. The catalog is for links. This directory is for
the things that took someone a bad afternoon to learn.
