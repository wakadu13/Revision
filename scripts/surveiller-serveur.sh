#!/usr/bin/env bash
# Surveille le wiki sur le serveur (Linux, Raspberry Pi) : si l'adresse de statut
# ne répond pas, l'incident est noté dans le journal système (journalctl -t
# wiki-surveillance), une notification part sur le téléphone (ntfy, si un sujet est
# configuré) et le conteneur peut être relancé. Une seule notification par panne,
# une autre quand le wiki répond de nouveau.
#
# Réglages (variables d'environnement, toutes facultatives) :
#   WIKI_STATUT_URL  adresse testée (défaut : http://127.0.0.1:8000/api/status/)
#   WIKI_NTFY        sujet ntfy.sh à prévenir, ou adresse complète d'un serveur ntfy.
#                    Choisir un nom difficile à deviner : qui le connaît lit les alertes
#                    (elles ne contiennent que « le wiki ne répond pas »). Sur le téléphone,
#                    application ntfy, s'abonner au même sujet.
#   WIKI_RELANCE     commande lancée à chaque échec, par ex.
#                    "docker compose --project-directory /home/pi/deploy restart web"
#
# Toutes les 5 minutes avec cron (crontab -e) :
#   */5 * * * * WIKI_NTFY=projetpluri-alertes-a1b2c3 /home/pi/ProjetPluri/ProjetPluri/scripts/surveiller-serveur.sh
#
# Depuis l'extérieur (le Pi lui-même peut être éteint ou sans réseau), un moniteur
# gratuit comme UptimeRobot sur https://wiki.airhiterofprovence.fr/api/status/
# complète ce script.
set -u

url="${WIKI_STATUT_URL:-http://127.0.0.1:8000/api/status/}"
etat_dir="${XDG_STATE_HOME:-$HOME/.local/state}"
etat="$etat_dir/wiki-surveillance.etat"
mkdir -p "$etat_dir"
precedent="$(cat "$etat" 2>/dev/null || echo ok)"

journal() { logger -t wiki-surveillance -- "$1" 2>/dev/null || echo "$(date '+%F %T') $1" >&2; }

prevenir() {
  [ -n "${WIKI_NTFY:-}" ] || return 0
  local cible="$WIKI_NTFY"
  case "$cible" in http://*|https://*) ;; *) cible="https://ntfy.sh/$cible" ;; esac
  curl -fsS --max-time 15 -H "Title: ProjetPluri" -H "Priority: $2" -H "Tags: $3" -d "$1" "$cible" >/dev/null \
    || journal "notification impossible vers $cible"
}

if raison="$(curl -fsS --max-time 10 -o /dev/null "$url" 2>&1)"; then
  if [ "$precedent" = "panne" ]; then
    journal "le wiki répond de nouveau ($url)"
    prevenir "Le wiki répond de nouveau." default white_check_mark
  fi
  echo ok > "$etat"
  exit 0
fi

raison="$(printf '%s' "$raison" | tr '\n' ' ' | sed 's/^curl: //')"
journal "le wiki ne répond pas ($url) : $raison"
if [ "$precedent" != "panne" ]; then
  prevenir "Le wiki ne répond pas : $raison" high warning
fi
echo panne > "$etat"

if [ -n "${WIKI_RELANCE:-}" ]; then
  journal "relance : $WIKI_RELANCE"
  sh -c "$WIKI_RELANCE" >/dev/null 2>&1 || journal "la relance a échoué"
fi
exit 1
