# Copyright policy and takedown

## The short version

This repo is an index. It links to documents on their publishers' own servers and adds original
notes about them. It hosts a small number of documents directly, and only where the publisher's
license grants redistribution in words that can be quoted.

If you are a rights holder and something here is wrong, open an issue or email
`scholarkeaton@protonmail.com`. **It comes down first and gets discussed after.** No argument, no
delay, no request that you prove ownership beyond identifying yourself and the document.

## What this repo will not do

- Host a document whose license does not clearly permit it.
- Treat "free to download" as permission to republish. It is a price, not a license.
- Reproduce the tables, figures, or clauses of a sold standard. IEC, ISO, IEEE, UL, and NFPA
  documents are cited by number and described in scope. Their content stays with them.
- Route around a paywall or a login. A gated document is catalogued as `GATED, UNREAD`, which is an
  honest and useful row: it tells a reader the document exists, what it covers, and what it costs.
- Mirror something reached through a free access viewer. Read only access is not a distribution
  grant, and that distinction is the entire deal those viewers offer.

## How the boundary is enforced

Not by good intentions, because this repo gets worked on at 1am and good intentions keep bad hours.

- `mirrors/` is gitignored. A document file must be force added on purpose to be publishable.
- `tools/check_mirrors.py` starts from the filesystem, not the catalog, and fails on any tracked
  file that no catalog row has cleared. Starting from the catalog would only ever find rows, and the
  dangerous file is precisely the one no row mentions.
- `redistributable=yes` requires a named license. The checker rejects `unknown`, `free`, `free to
  download`, and the rest of the phrases that mean "I did not check."
- Every mirrored file's sha256 is recorded. If a publisher swaps rev A for rev B at the same URL
  under different terms, the hash mismatch fails the gate rather than silently republishing content
  under a license that no longer applies.

## Wayback snapshots

Rows link to Internet Archive snapshots. Those snapshots are made by, and hosted by, the Internet
Archive, and are subject to its policies. This repo records the URL of a snapshot; it does not host
the snapshot. Rights holders who want a snapshot removed should contact the Internet Archive, and if
you tell us it is gone the row will be updated to say so.

## Safety

This repo indexes documents about equipment that kills people.

Nothing here is a field procedure, an engineered study, or a substitute for the actual document.
The notes exist to help you find and understand the right document, not to replace reading it.
No summary in this repo should decide what anyone wears, touches, opens, or energizes.

That is the same line drawn in `power-service-toolbox`, and it is drawn here for the same reason: a
wrong number in that category burns a person.
