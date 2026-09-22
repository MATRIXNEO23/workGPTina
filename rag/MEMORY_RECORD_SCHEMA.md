# Schema record lavorativo v1

Ogni record Markdown sotto `rag/records/**` ha front matter YAML e corpo leggibile. Campi obbligatori:

- `schema_version: 1`
- `id`: identificatore stabile univoco
- `class`: `PROJECT`, `EXPERIMENT`, `METHOD`, `ERROR`, `CUSTOMER_MARKET`, `ECONOMICS`, `DECISION`, `OPPORTUNITY`, `OPEN_LOOP`, `EVIDENCE`
- `title`
- `status`: `current`, `historical`, `superseded`, `invalidated`
- `event_at`: quando il fatto è avvenuto, ISO-8601
- `recorded_at`: quando è stato registrato, ISO-8601
- `owner: workGPTina`
- `source_refs`: lista non vuota di file/URL/commit/evidenze
- `supersedes`: lista di ID precedenti, anche vuota
- `tags`: lista

Una correzione crea un nuovo record e usa `supersedes`; non riscrive il precedente. `recorded_at` non può precedere `event_at` quando i valori hanno precisione confrontabile. Segreti e dati personali non necessari sono vietati.

