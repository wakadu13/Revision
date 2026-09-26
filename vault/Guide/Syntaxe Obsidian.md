---
aliases: [Syntaxe, Aide]
tags: [guide, wiki/documentation]
auteur: ProjetPluri
---
Cette page montre la syntaxe Obsidian reconnue par le wiki.

## Liens internes

- Lien simple : [[Accueil]]
- Lien avec texte : [[Projet Pluri|voir le projet]]
- Lien vers un titre : [[Projet Pluri#Objectifs]]
- Lien vers un titre de cette page : [[#Intégrations]]
- Lien vers un bloc : [[Idées#^idee-cle]]
- Lien par alias : [[Aide]] pointe ici
- Lien Markdown classique : [le projet](../Projets/Projet%20Pluri.md)
- Page inexistante : [[Page à créer]]

## Intégrations

Une image, redimensionnée à 120 px :

![[logo.svg|120]]

Une section d'une autre note :

![[Projet Pluri#Objectifs]]

## Callouts

> [!note]
> Un callout simple, avec du **Markdown** et un lien [[Accueil]].

> [!warning] Attention
> Titre personnalisé.

> [!question]- Callout replié (cliquez)
> Contenu caché par défaut.

> [!example]+ Callouts imbriqués
> > [!success] Réussi
> > Un callout dans un callout.

## Mise en forme

==Texte surligné==, ~~texte barré~~, **gras**, *italique*, `code`.

Un commentaire invisible : %%ce texte n'apparaît pas%% (voir le fichier source).

Tags en ligne : #guide #wiki/documentation

### Tâches
- [x] Lire les fichiers `.md`
- [x] Afficher les liens `[[...]]`
- [ ] Écrire la documentation du projet

### Tableau
| Syntaxe | Rendu |
| --- | --- |
| `[[Page]]` | lien interne |
| `![[image.png]]` | image intégrée |
| `#tag` | tag cliquable |

### Formules
En ligne : $e^{i\pi} + 1 = 0$

$$
\int_0^1 x^2 \, dx = \frac{1}{3}
$$

### Code et diagrammes
```python
def bonjour(nom):
    return f"Bonjour {nom} #pas-un-tag [[pas un lien]]"
```

```mermaid
graph LR
    A[Fichier .md] --> B[Wiki Django]
    B --> C[Page web]
```

### Note de bas de page
Une affirmation sourcée[^1].

[^1]: La source en question.
