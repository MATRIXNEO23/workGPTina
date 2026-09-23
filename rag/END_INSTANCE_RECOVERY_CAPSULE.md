# Capsula canonica di fine istanza

Prima di terminare ogni istanza:

1. registrare il micro-checkpoint finale e un checkpoint completo;
2. aggiornare i record durevoli di decisioni, errori, risultati e open loop;
3. aggiornare stato del progetto, artefatti, prove, live context e relativa prossima azione;
4. distinguere chiaramente ciò che è remoto, solo locale o soltanto discusso;
5. eseguire verifica, build, test, pubblicazione fast-forward e controllo HEAD/CI secondo il runbook;
6. consegnare ad Alberto un prompt autosufficiente conforme a `rag/END_INSTANCE_HANDOFF_PROMPT_TEMPLATE.md`, con repository, HEAD remoto, puntatori esatti, stato corrente, vincoli, blocchi e prossima azione.

Il prompt di recovery non sostituisce il salvataggio: va prodotto solo dopo aver salvato e verificato lo stato canonico. Non inserirvi segreti.
