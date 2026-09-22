---
schema_version: 1
id: decision-self-funded-growth-budget
class: DECISION
title: Budget di crescita autofinanziato dagli incassi
status: current
event_at: 2026-09-22T11:20:00Z
recorded_at: 2026-09-22T11:20:00Z
owner: workGPTina
source_refs:
  - checkpoints/2026-09-22-zero-budget-fiverr-ready.md
supersedes: [decision-zero-budget-channel-strategy]
tags: [decision, budget, self-funded, risk-control]
---

Regola di Alberto: il capitale iniziale è EUR 0 e il budget aumenta incassando. Implementazione prudenziale v1: soltanto ricavi netti realmente `COLLECTED` possono alimentare il budget; `POTENTIAL`, `QUALIFIED`, `QUOTED`, `CONTRACTED` e `INVOICED` non contano. Fino al primo incasso nessuna spesa. Dopo ogni incasso, massimo 25% del netto cumulativo non già allocato diventa budget di crescita; almeno 75% resta non impegnato. Ogni spesa deve comunque avere scopo, costo massimo, metrica e autorizzazione applicabile. Rivalutare la percentuale dopo i primi tre incassi o EUR 300 netti cumulativi.

