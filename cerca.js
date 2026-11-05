// Ricerca locale nell'elenco dei caduti: nessun server, nessun cookie, nessun tracking.
// Filtra i <li> di #elenco-caduti per testo libero e per stato.
(() => {
  const input = document.querySelector("#cerca-caduti");
  const stato = document.querySelector("#filtro-stato");
  const list = document.querySelector("#elenco-caduti");
  if (!input || !list) return;

  const items = [...list.querySelectorAll("li")];
  const esito = document.querySelector("#cerca-esito");
  const empty = document.querySelector("#nessun-caduto");
  const totale = items.length;

  const norm = (s = "") =>
    s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  const aggiorna = () => {
    const q = norm(input.value.trim());
    const st = stato ? stato.value : "";
    let visibili = 0;

    for (const li of items) {
      const testo = li.dataset.cerca || li.textContent;
      const ok =
        (!q || norm(testo).includes(q)) &&
        (!st || li.dataset.stato === st);
      li.hidden = !ok;
      if (ok) visibili += 1;
    }

    if (esito) {
      esito.textContent =
        q || st ? `${visibili} di ${totale} nominativi` : `${totale} nominativi`;
    }

    if (empty) {
      empty.hidden = visibili !== 0;
      if (visibili === 0) {
        const parti = [];
        if (q) parti.push(`«${input.value.trim()}»`);
        if (st) parti.push(`stato «${st}»`);
        empty.textContent = `Nessun risultato per ${parti.join(" e ")}.`;
      }
    }
  };

  input.addEventListener("input", aggiorna);
  if (stato) stato.addEventListener("change", aggiorna);
  aggiorna();
})();
