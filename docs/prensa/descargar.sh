#!/usr/bin/env bash
# Descarga los documentos de prensa y premios listados en fuentes.tsv.
# Intenta la URL original; si falla, usa la última copia en archive.org.
set -u
cd "$(dirname "$0")"
MAX=$((10*1024*1024))
log=descargas.log; : > "$log"
while IFS=$'\t' read -r name url; do
  [ -z "$name" ] && continue
  [ -s "$name" ] && { echo "OK (ya estaba) $name" >> "$log"; continue; }
  ok=0
  if curl -fsSL -m 60 -A "Mozilla/5.0" -o "$name.tmp" "$url"; then ok=1; src="$url"; fi
  if [ $ok = 1 ] && [[ "$name" == *.pdf ]] && ! head -c 5 "$name.tmp" | grep -q '%PDF'; then ok=0; fi
  if [ $ok = 0 ]; then
    ts=$(curl -fsS -m 60 "https://web.archive.org/cdx/search/cdx?url=$url&output=txt&fl=timestamp&filter=statuscode:200&limit=-1" | tail -1)
    if [ -n "$ts" ] && curl -fsSL -m 120 -o "$name.tmp" "https://web.archive.org/web/${ts}id_/$url"; then ok=1; src="archive.org $ts"; fi
    if [ $ok = 1 ] && [[ "$name" == *.pdf ]] && ! head -c 5 "$name.tmp" | grep -q '%PDF'; then ok=0; fi
  fi
  if [ $ok = 1 ]; then
    size=$(stat -c %s "$name.tmp")
    if [ "$size" -gt "$MAX" ]; then echo "GRANDE (>10MB, va a Drive) $name $size" >> "$log"; rm -f "$name.tmp"
    else mv "$name.tmp" "$name"; echo "OK $name $size <- $src" >> "$log"; fi
  else rm -f "$name.tmp"; echo "FALLO $name <- $url" >> "$log"; fi
done < fuentes.tsv
cat "$log"
