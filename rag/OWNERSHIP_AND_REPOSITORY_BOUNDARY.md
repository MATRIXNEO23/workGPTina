# Ownership e confine repository

`MATRIXNEO23/workGPTina` contiene memoria e infrastruttura operativa di workGPTina ed è l'unico target remoto di scrittura autorizzato.

`MATRIXNEO23/scodinzolina-conntinuity` appartiene a GPTina ed è **read-only**: lettura consentita quando pertinente; qualunque scrittura, inclusi branch, tag, issue, PR, commenti, workflow, release, artefatti e metadata, è vietata.

Permesso tecnico non significa consenso. Audit, urgenza o utilità non ampliano l'autorizzazione. Per agenti futuri: lettura cross-repo solo quando autorizzata; nessuna cross-write senza autorizzazione esplicita. Per GPTina il divieto è assoluto finché Alberto non modifica esplicitamente questa regola.

Ogni percorso mutante deve chiamare `rag/repo_guard.py` prima dell'operazione. Target diverso da `MATRIXNEO23/workGPTina` causa `ABORT` prima di una chiamata remota.
