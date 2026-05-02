# Traitre.exe

Soumission Python pour le defi du dilemme du prisonnier a trois joueurs sur 250 tours.

La strategie commence par collaborer, repond aux trahisons recentes, revient a la collaboration apres quelques tours calmes et trahit dans les derniers tours.

## Prerequis

- Python 3.9 ou plus recent
- Aucune dependance externe

## Execution rapide

Interface visuelle :

Ouvrez `index.html` dans un navigateur.

Windows :

```powershell
py traitre.py simulate
```

GNU/Linux :

```bash
python3 traitre.py simulate
```

La simulation par defaut lance `Traitre.exe` contre `donnant-donnant` et `rancunier` pendant 250 tours.

## Mode action

Le mode `action` lit un etat JSON et imprime uniquement la prochaine action : `collaborer` ou `trahir`.

Exemple Windows :

```powershell
@'
{
  "self": "Traitre.exe",
  "players": ["Traitre.exe", "Alice", "Bob"],
  "total_rounds": 250,
  "history": [
    {"actions": {"Traitre.exe": "collaborer", "Alice": "collaborer", "Bob": "trahir"}}
  ]
}
'@ | py traitre.py action
```

Exemple GNU/Linux :

```bash
python3 traitre.py action <<'JSON'
{
  "self": "Traitre.exe",
  "players": ["Traitre.exe", "Alice", "Bob"],
  "total_rounds": 250,
  "history": [
    {"actions": {"Traitre.exe": "collaborer", "Alice": "collaborer", "Bob": "trahir"}}
  ]
}
JSON
```

## Format JSON attendu

```json
{
  "self": "Traitre.exe",
  "players": ["Traitre.exe", "Alice", "Bob"],
  "total_rounds": 250,
  "history": [
    {
      "actions": {
        "Traitre.exe": "collaborer",
        "Alice": "trahir",
        "Bob": "collaborer"
      }
    }
  ]
}
```

Les actions acceptees sont flexibles : `collaborer`, `cooperer`, `C`, `trahir`, `traitre`, `D`, etc. La sortie canonique demeure `collaborer` ou `trahir`.

## Simulations personnalisees

```bash
python3 traitre.py simulate --rounds 250 --players traitre cooperateur mefiant
python3 traitre.py simulate --rounds 250 --players traitre aleatoire donnant-donnant --seed 42
```

Strategies incluses pour les tests locaux :

- `traitre`
- `cooperateur`
- `mefiant`
- `donnant-donnant`
- `rancunier`
- `aleatoire`

## Tests

Windows :

```powershell
py -m unittest test_traitre.py
```

GNU/Linux :

```bash
python3 -m unittest test_traitre.py
```
