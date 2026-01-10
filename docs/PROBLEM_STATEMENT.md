# WinGuard – Problem Statement (Long Form)

> This document expands the README’s problem statement into a deeper, story-style explanation.
> It’s written for judges, reviewers, and stakeholders who want the *why* before the *how*.

---

## 1) Context: where this problem lives

Across many parts of India, there are villages that sit close to forests and wildlife corridors. In regions near Uttarakhand’s forest boundaries (and similar geographies across the country), the “border” between settlement and jungle is not a hard line on a map — it’s a daily experience.

Fields often meet forest edges.

Footpaths that children use in the morning can become animal routes at night.

A narrow road can be the fastest way home for a farmer — and also the same route an elephant herd uses to cross from one patch of forest to another.

This overlap is the heart of Human–Wildlife Conflict (HWC): **humans and wildlife are sharing space without sharing intent**.

---

## 2) A story you can picture (and why seconds matter)

Imagine a typical evening.

The temperature drops. Lights come on in small homes and shops. People finish work, return from fields, or step out for routine tasks:

- checking crops,
- fetching water,
- walking to a neighbor’s house,
- moving livestock,
- closing gates.

Now imagine a sensor triggers near the forest boundary.

A camera frame is captured.

At this moment, the village does not need “a lot of data.”

The village needs an answer.

The answer must be fast, and it must be correct.

Because the next few minutes decide whether:

- people go back inside safely,
- someone goes out to confirm and takes a risk,
- a response team is notified early enough to prevent escalation,
- a false alarm wastes time and trust.

This is not a lab problem. This is a decision problem.

---

## 3) What people face today

### 3.1 Alerts without clarity

Many deployments rely on motion/PIR sensors, basic CCTV setups, or manual watch systems.

They are good at producing a trigger:

- “something moved”
- “motion detected”

But they are not good at producing the decision:

- “it’s an elephant herd”
- “it’s a bear”
- “it’s a human”
- “it’s nothing important”

When the system cannot label the event, the burden shifts to people.

People become the classifier.

And classification is slow in the dark.

### 3.2 False alarms and alarm fatigue

A large number of motion triggers are not wildlife:

- wind moving branches,
- insects close to the lens,
- shadows from passing vehicles,
- small animals,
- pets,
- people walking normally.

When alerts are frequently wrong, the community stops responding quickly.

This is “alarm fatigue.”

And alarm fatigue is dangerous, because the one alert that matters can get ignored.

### 3.3 Slow verification loops

Even if a camera is available, verification is often manual:

- someone must open a feed,
- someone must watch and interpret,
- someone must decide whether to alert others.

That time cost is not just “latency.”

It is exposure.

The longer uncertainty exists, the more likely someone steps out to check.

### 3.4 No audit trail, no learning

Many incidents end as rumors or unstructured messages:

- “There was an elephant last night.”
- “Someone saw a bear near the boundary.”

Without:

- a saved image,
- a timestamp,
- a location/camera identifier,
- a label/species estimate,
- a confidence score,

there is no reliable way to:

- analyze patterns,
- allocate resources,
- measure whether interventions worked,
- improve the monitoring system over time.

### 3.5 Edge constraints (power and connectivity)

Remote installations face:

- unstable power,
- limited bandwidth,
- limited internet uptime,
- hardware cost constraints.

Always-on cloud streaming is expensive and not robust in these settings.

This pushes the design toward *edge intelligence*:

- detect locally,
- transmit only what matters,
- store evidence and metadata.

---

## 4) Why the problem is hard

### 4.1 The environment is not “clean data”

Real scenes include:

- poor lighting,
- occlusion,
- rain/fog,
- cluttered foliage,
- moving shadows,
- low-resolution frames,
- motion blur.

### 4.2 The output must be actionable

A system that outputs “animal” is better than nothing, but still not enough.

Different species imply different risk and different response:

- **Elephant** near crops may require a fast community alert and boundary response.
- **Bear** sightings may require different safety guidance.

Even within the same “animal” category, the actions are not the same.

### 4.3 Confidence matters

Overconfident wrong labels can be worse than uncertainty.

A good system should:

- output confidence,
- degrade gracefully,
- say `unknown` when it is not sure.

### 4.4 A trigger is not an event

A sensor trigger is a hint.

An event is a record.

An event must include:

- evidence (image),
- metadata (timestamp, camera id),
- interpretation (label/species),
- uncertainty (confidence),
- storage (database).

---

## 5) WinGuard’s problem statement (refined)

**Problem:** Villages close to forests need a reliable, low-latency way to convert sensor/camera signals into high-confidence wildlife incidents, so that people can respond safely and authorities can track patterns — but existing solutions either produce too many false alarms, require manual verification, or fail under edge constraints.

**Goal:** Build an AI-powered monitoring pipeline that:

1. Detects whether the frame contains a human or an animal.
2. If an animal is present, classifies the likely species.
3. Outputs confidence-aware results (unknown if unsure).
4. Logs every meaningful incident with image + metadata.
5. Supports edge-friendly operation (efficient, practical, auditable).

---

## 6) Stakeholders and what they need

### 6.1 Villagers

Need:

- fewer false alarms,
- clear alerts with simple labels,
- fast decisions at night,
- reduced risk of stepping out to verify.

### 6.2 Forest department / response teams

Need:

- incident logs with evidence,
- timestamps and camera identifiers,
- pattern analysis (when/where/which species),
- better prioritization (high-confidence events first).

### 6.3 Researchers / conservation planners

Need:

- consistent records,
- fewer “anecdotal only” reports,
- data for corridor understanding and mitigation planning.

---

## 7) Success criteria (what “working” means)

A prototype is successful when it can:

- reduce false alerts compared to motion-only triggers,
- label `human` vs `animal` reliably,
- classify common target species when visible,
- store every detection event for audit,
- run without depending on constant internet.

---

## 8) Scope boundaries (what this repo focuses on)

This repository currently focuses on:

- inference pipeline (YOLO + species classifier),
- event logging in a local database,
- a simple API (`POST /detect`).

Planned future work (mentioned in README):

- tracking (DeepSORT/ByteTrack),
- cross-camera re-ID,
- zone-based alert escalation,
- dashboard/analytics.

---

## 9) Why “Decision Support System” is the right frame

WinGuard is designed as an Intelligent Decision Support System (DSS) because:

- sensors provide *signals*,
- AI provides *interpretation*,
- the system must provide *decisions* backed by evidence.

This framing matters because it guides the product:

- accuracy is important,
- but so is trust,
- so is logging,
- so is explainability at the level of “what/when/where.”

---

## 10) Next sections

For implementation details, continue with:

- [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/API.md](API.md)
- [docs/HARDWARE.md](HARDWARE.md)
