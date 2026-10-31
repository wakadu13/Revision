"""Adresse IP du visiteur, pour django-axes (blocage après 5 mots de passe faux).

Derrière un proxy, REMOTE_ADDR est celle du proxy (127.0.0.1 avec Caddy) : tous
les visiteurs auraient la même et un inconnu pourrait bloquer n'importe quel
compte. On ne lit pour autant que des adresses impossibles à falsifier :
- derrière Cloudflare (DJANGO_CLOUDFLARE=1) : CF-Connecting-IP, que Cloudflare
  réécrit toujours ;
- derrière un proxy (DJANGO_BEHIND_PROXY=1) : la dernière adresse de
  X-Forwarded-For, celle qu'a vue notre proxy ; le visiteur ne peut qu'ajouter
  des adresses avant elle.
"""

import ipaddress

from django.conf import settings


def _adresse(valeur):
    try:
        return str(ipaddress.ip_address(valeur.strip()))
    except ValueError:
        return None


def ip_client(request):
    meta = request.META
    if settings.CLOUDFLARE:
        ip = _adresse(meta.get("HTTP_CF_CONNECTING_IP", ""))
        if ip:
            return ip
    if settings.BEHIND_PROXY:
        ip = _adresse(meta.get("HTTP_X_FORWARDED_FOR", "").split(",")[-1])
        if ip:
            return ip
    return meta.get("REMOTE_ADDR")
