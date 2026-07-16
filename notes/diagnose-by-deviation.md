# Diagnose by deviation, not by symptom

**For the engineer early enough in this to still choose their habits.** This page has no procedure in
it, no signature, and no data. It is a method, and the method is worth more than any of those.

## The thing nobody tells you

Every troubleshooting document you will ever read is organized the same way: symptom on the left,
cause on the right. The bus is silent, so check these six things. The drive faults on accel, so check
these four.

That structure has a hidden requirement, and the requirement is usually missing. **Symptom tables
assume somebody already did the characterization work.** They are the compressed output of a person
who once sat with the hardware, changed one thing at a time, and watched what the signal did. You are
reading their conclusions. On your hardware, in your plant, with your revision of the board, their
conclusions are an educated guess.

There is another way to work, and once you have seen it you cannot unsee how much time the first way
costs.

**Do not ask what the symptom means. Ask how this differs from known good, and what makes that
difference.**

## The method

Three moves. The order is the whole point, because the first one happens long before anything breaks.

### 1. Build the health check in, while you are building the thing

Test points, placed on purpose, so the board can be interrogated later without being taken apart or
guessed at. Control boards, power boards, communication boards, sensing boards: each one gets the
means to answer questions about itself.

This is the move that feels like it is not paying for itself, right up until the first failure.
Everyone else is deciding where to probe on hardware that was never designed to be probed, while
already under pressure, and the answer they get is one reading with nothing to compare it to.

### 2. Record what healthy looks like, BEFORE you need it

A signature from the test points while the board is behaving. That is it. That is the whole step, and
it is the one people skip, because nothing is wrong yet and it feels like filing paperwork about a
problem you do not have.

**A measurement of a broken thing tells you almost nothing on its own.** It is a number. It becomes
information the moment you have the same number from when it worked, because then it is a
*difference*, and a difference has a cause. Take the reading only after the failure and you have
bought yourself an afternoon of deciding whether what you are looking at is even abnormal.

The baseline is cheap while things work and unobtainable once they do not. That asymmetry is the
entire argument.

### 3. Trace differences back to causes, and keep the list

Then the real work: change things deliberately and watch what the signal does. Components, settings,
configurations, physical damage. Build up, over time, a mapping from *this deviation from base* to
*this cause*, including the distinction that costs the most to get wrong: **is this hardware or is
this software.**

That mapping is the asset. Not the fix, the mapping. A fix retires with the fault; the mapping
answers every future instance of it, and it gets better every time you use it.

## Why the roster is not in this repo, and why that is not a loss

The author of this repo has one. It is not published here, for two reasons, and the second is the one
that matters to you.

**First, and simply: characterization done for an employer belongs to that employer.** The knowledge
of how to do it is portable. The tables are not. That line is not a technicality, it is the deal.

**Second: it would not help you anyway.** A signature is a fact about a specific board, a specific
revision, a specific bench, a specific set of parts. Someone else's baseline is not your baseline,
and treating it as one puts you back to comparing your hardware against an educated guess, which is
the exact failure mode this method exists to escape.

**Which is the lesson, not a disclaimer.** The transferable part of this work was never the data. It
was always the habit: build the test points in, record the baseline while it is healthy, and write
down what you learn when you make it deviate. Nobody can hand you the roster. Everybody can start
theirs on the next board they touch.

## When this does not apply, and it is often

Honesty about scope, since a method oversold is a method that gets abandoned the first time it
disappoints.

- **You need test points, which means you need to have influenced the design, or gotten lucky.** On
  somebody else's sealed product you are back to the symptom table, and that is what the rest of this
  repo is for.
- **You need the baseline to exist.** If nobody recorded one while the equipment was healthy, this
  method does not start today. It starts on the next thing you build, or the next healthy unit you
  have access to.
- **It rewards patience up front and pays out later.** On a one off repair of something you will
  never see again, the symptom table is the correct tool and this is over engineering.

## Where this leaves the rest of the repo

Worth saying plainly, since it undercuts a page or two here: **the catalogued documents are symptom
tables**, and the notes are better symptom tables. Both are the second best way to work. They are
what you use when you did not, or could not, do the characterization. That is most of the time, which
is why they are here and why they are worth doing well.

But if you are early enough to choose: characterize. The document tells you what somebody else found
on their hardware. The baseline tells you what is true about yours.

## Provenance

This page is written from the practice of this repo's author: electronics prototype development and
board level characterization of communication boards and devices, taking hardware off tools to
characterize components and signal interactions, and building symptom to cause mappings traced back
to configuration and physical damage. Bench: function generator, oscilloscope, multimeter, LCR meter,
terminal, RF antennas.

The method is his to teach. The signatures are not his to publish, and are not published here.

**Nothing on this page is a field procedure.** It does not tell you where to probe, what to open, or
what to energize. It tells you when to write something down.
