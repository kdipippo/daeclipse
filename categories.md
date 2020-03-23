Maybe this is too complicated. What if the list just gets simplified as a list of checkboxes: select all that apply. And then that decides the flags.

----
`all` is a default True flag.
Each artwork has a `media` and a `subject`. Choosing a deeper selection means that the parent categories get inherited.

For example, a `f2u icon of Miku` will result in the categories list, `f2u > icon > pixel, miku > vocaloid, all`.

### All
```mermaid
graph TD;
  all
```

### Media
```mermaid
graph TD;
  digital

  pixel
  pixel --> icon
  icon --> f2u
  icon --> p2u
  icon --> commission_info

  adopts

  comics
```

### Subject
```mermaid
graph TD;
  animals

  humans

  vocaloid
  vocaloid --> group
  vocaloid --> miku
  vocaloid --> ia
  vocaloid --> rin
  vocaloid --> len
  vocaloid --> luka
  vocaloid --> meiko
  vocaloid --> kaito
  vocaloid --> gumi

  yugioh

  pokemon
```
