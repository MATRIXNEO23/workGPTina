# Runbook canonico di salvataggio e recovery

## Modello

Git contiene fonti canoniche: record, evidenze, checkpoint, micro-checkpoint, live context e router narrativi. `rag/index/.projection-generations/`, SQLite, JSONL e puntatore attivo sono proiezioni locali ignorate da Git.

## Salvataggio

1. Rileggi HEAD remoto, live, ultimo micro e ultimo checkpoint.
2. Per lavoro lungo/rischioso crea un micro preflight.
3. Crea fonti append-only conformi allo schema; le correzioni usano `supersedes`.
4. Aggiorna coerentemente live, checkpoint e router.
5. Verifica il target con `python rag/repo_guard.py MATRIXNEO23/workGPTina`.
6. Crea un commit candidato locale pulito.
7. Esegui verifier, build, unit test, retrieval, resilienza e cold start.
8. Rileggi HEAD remoto; se è avanzato riconcilia senza force e ripeti i gate interessati.
9. Pubblica soltanto in fast-forward e verifica commit/tree/CI remoti.

## Recovery

Seguire l'entrypoint live-first. Se le proiezioni mancano o sono corrotte, non correggerle a mano: rigenerarle con `python rag/work_memory.py build`. Il puntatore viene sostituito atomicamente soltanto dopo JSONL, metadata e SQLite completi e coerenti.

Una procedura è riuscita solo se record correnti e superseded restano recuperabili, puntatori esistono, working tree resta pulito, cold start individua la next action e nessuna mutazione può raggiungere GPTina.

