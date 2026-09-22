# Checklist di esecuzione

## Preflight

- confermare repository, branch, HEAD e autorizzazione;
- verificare target con il guardrail;
- registrare scope, budget tempo e operazioni vietate;
- lavorare in clone isolato; nessun force-push;
- controllare presenza accidentale di segreti senza registrarne il valore.

## Audit read-only

- inventario ricorsivo di codice, documentazione, workflow, release e artefatti;
- mappa branch/tag/commit rilevanti;
- ricostruzione della catena `fonte → build → test → artefatto`;
- esecuzione riproducibile dei verifier consentiti;
- distinzione `VERIFIED / PARTIAL / MISSING / CONTRADICTED / UNKNOWN`;
- ricerca di stato corrente, vecchie strategie, tentativi falliti e next action;
- verifica che cache e database derivati non sostituiscano le fonti.

## Correzione opzionale

- una sola causa circoscritta concordata;
- candidato locale, test prima della pubblicazione;
- nessuna espansione silenziosa dello scope;
- commit non distruttivo e verifica remota.

## Consegna

- HEAD e prove;
- diagnosi con livello di confidenza;
- cosa è stato modificato e cosa no;
- comandi di verifica;
- rischi residui;
- next action economicamente sensata.

