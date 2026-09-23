# Protocollo live

Il live context è una piccola proiezione del presente, non la storia definitiva. I micro-checkpoint sono append-only e registrano delta reali: progetto o esperimento nuovo/cambiato, risultato, ricavo/costo significativo, decisione, opportunità qualificata, errore, cliente, pricing, blocco, milestone o preflight rischioso.

Regola del proprietario: durante il lavoro attivo creare un micro-checkpoint almeno ogni 3–5 scambi utente/assistente, anche quando serve soltanto a consolidare i delta accumulati. Crearlo immediatamente dopo ogni passo importante, decisione, blocco, modifica esterna, risultato o cambio di stato. Non creare un micro per ogni messaggio se non esiste un delta utile.

Quando nasce un progetto operativo con artefatti propri, creare una cartella canonica dedicata sotto `projects/<project-id>/` e mantenerne un file di stato. Le decisioni vanno registrate anche come record durevoli; non devono vivere soltanto nel checkpoint o nella chat. Non salvare password, OTP, token, cookie o altri segreti.

Un checkpoint pieno consolida lo stato complessivo dopo milestone, cambio fase, accumulo di delta o fine istanza. Dopo ogni modifica: verificare schema e puntatori, mantenere gli storici, aggiornare live/Fast Recall/Current Context solo se il presente cambia.
