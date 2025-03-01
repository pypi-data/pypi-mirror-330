# swiftbarmenu

✨ Easy menu building for [SwiftBar](https://swiftbar.app/) (... and [xbar](https://xbarapp.com/)).

**Transform this...**

```python
from swiftbarmenu import Menu

m = Menu('My menu')
m.add_item('Item 1')
item2 = m.add_item('Item 2', sep=True, checked=True)
item2.add_item('Subitem 1')
item2.add_item('Subitem 2')
m.add_link('Item 3', 'https://example.com', color='yellow')
m.add_item(':thermometer: Item 4', color='orange', sfcolor='black', sfsize=20)

m.dump()
```

**Into this...**

![Swiftbarmenu Screenshot](https://raw.githubusercontent.com/sdelquin/swiftbarmenu/main/images/swiftbarmenu.png)

## Installation

```console
pip install swiftbarmenu
```

Check out [uv](https://docs.astral.sh/uv/)!

## Usage

Check out the features through basic examples below.

### Basic menu

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_item('Item 1')
Item 1
>>> m.add_item('Item 2')
Item 2
>>> m.dump()
My menu
---
Item 1
Item 2
```

Added items are instances of `MenuItem`:

```pycon
>>> from swiftbarmenu import MenuItem

>>> m = Menu('My menu')
>>> item = m.add_item('Item 1')
>>> isinstance(item, MenuItem)
True
>>> item.text
'Item 1'
```

### Multiple header

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_header('Header 2')
Header 2
>>> m.add_header('Header 3')
Header 3
>>> m.dump()
My menu
Header 2
Header 3
---
```

### Add parameters

You can add multiple [parameters](https://github.com/swiftbar/SwiftBar?tab=readme-ov-file#parameters):

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> item = m.add_item('Item 1', color='orange', size=18, checked=True)
>>> item
Item 1|color=orange size=18 checked=True

>>> m.dump()
My menu
---
Item 1|color=orange size=18 checked=True

>>> item.text
'Item 1'
>>> item.params
{'color': 'orange', 'size': 18, 'checked': True}
>>>
```

### Add links

```python
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_link('GitHub', 'https://github.com')
GitHub|href=https://github.com
>>> m.dump()
My menu
---
GitHub|href=https://github.com
```

It's actually a shortcut for:

```pycon
>>> m.add_item('GitHub', href='https://github.com')
GitHub|href=https://github.com
```

### Nested items

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> item1 = m.add_item('Item 1')
>>> item1.add_item('Item 1.1')
Item 1.1
>>> item1.add_item('Item 1.2')
Item 1.2
>>> item1.add_item('Item 1.3')
Item 1.3
>>> m.dump()
My menu
---
Item 1
-- Item 1.1
-- Item 1.2
-- Item 1.3
```

### Swift icons

You can add [SF Symbols](https://developer.apple.com/sf-symbols/) using `:symbol:`

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_item('Sunny! :sun.max:')
Sunny! :sun.max:
>>> m.add_item('Cloudy! :cloud.rain:', sfcolor='blue')
Cloudy! :cloud.rain:|sfcolor=blue
>>> m.dump()
My menu
---
Sunny! :sun.max:
Cloudy! :cloud.rain:|sfcolor=blue
```

The parameter `sfcolor` only colorizes _sf symbols_.  
Search _sf symbols_ [here](https://hotpot.ai/free-icons).

### Add images

It's pretty simple to add an image (**using path not base64**) to a menu item:

```pycon
>>> from src.swiftbarmenu import Menu

>>> m = Menu('My menu')

>>> m.add_image('tests/images/parrot.png', 'Parrot')
Parrot|image=iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAJZlWElmTU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAExAAIAAAARAAAAWodpAAQAAAABAAAAbAAAAAAAAABgAAAAAQAAAGAAAAABd3d3Lmlua3NjYXBlLm9yZwAAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAA4+VmVAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAWRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIj4KICAgICAgICAgPHhtcDpDcmVhdG9yVG9vbD53d3cuaW5rc2NhcGUub3JnPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqyyWIhAAACL0lEQVQ4Eb1TXUiTURh+ztn2bW7OmGa2DAIpt8ogRxS0q6Ifbyy88MIuEoIgUOznIop+WAWSlGHSTdBVN10s6C6Tlo0i+5EULFhQ68fSOecmubl92/fz9m06ZrHVXS8cznue93le3vc95wD/NpaApeYLYCpGZcXAPDazfXdr+ZrVJ3UNTofu2/eg7uvEQfZ8MJSPZ3f98kPBJ5bY2txltgp9ZC3Hu+YmsESiUuDsEHYN9hZ4RRLceIJagQynfcFVHY2j62EbTyFwqdvLjx2pd9bVTS0XZ/3fWuh/hQpZxFOjGa6EAqyYMqHlphsVcb7nx8O74xvs9sifCXge8BC4kkG/YIIrk9RKk7WV0iOjUjAZ148UE2e1uRl0+1AlPMJ1ZkR7fB6ILVQjGnbguJ/9XDvHO9inAQ0tbrkWLpzYcipkcvQOiW5EpVpY5JXomnyG+tTwyxc23T0DIQ2oUUllYUlSwjqJR8fS6Xm/3y8zELF9h/uuTNt3nuPVNWiqHEHDzOjbhfH3iZjZ6OYK6VUVcwCZGGNlinZQFDVGoJAsqUdzFfQccFsjnXcet22c2OGKDMSASSdzeSO3O9uc2hAkbZyzekG2iKroIKK9pNJ+znhjWlZalm6B+Pmx0OuLVfe3GeLJs2zzmavFO15EPR4Pt00HNqVFdXYRaaWyB2+8PgpcFunzrXV/E5eIEcsEetrpw7XhEoSS8NI7YGQAfdRYQyWZJQKFvyBRAEZZG9h/tl+8ztuKYW6OWAAAAABJRU5ErkJggg==
```

It's actually a shortcut for:

```pycon
>>> m.add_item('Parrot', image='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAJZlWElmTU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAExAAIAAAARAAAAWodpAAQAAAABAAAAbAAAAAAAAABgAAAAAQAAAGAAAAABd3d3Lmlua3NjYXBlLm9yZwAAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAA4+VmVAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAWRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIj4KICAgICAgICAgPHhtcDpDcmVhdG9yVG9vbD53d3cuaW5rc2NhcGUub3JnPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqyyWIhAAACL0lEQVQ4Eb1TXUiTURh+ztn2bW7OmGa2DAIpt8ogRxS0q6Ifbyy88MIuEoIgUOznIop+WAWSlGHSTdBVN10s6C6Tlo0i+5EULFhQ68fSOecmubl92/fz9m06ZrHVXS8cznue93le3vc95wD/NpaApeYLYCpGZcXAPDazfXdr+ZrVJ3UNTofu2/eg7uvEQfZ8MJSPZ3f98kPBJ5bY2txltgp9ZC3Hu+YmsESiUuDsEHYN9hZ4RRLceIJagQynfcFVHY2j62EbTyFwqdvLjx2pd9bVTS0XZ/3fWuh/hQpZxFOjGa6EAqyYMqHlphsVcb7nx8O74xvs9sifCXge8BC4kkG/YIIrk9RKk7WV0iOjUjAZ148UE2e1uRl0+1AlPMJ1ZkR7fB6ILVQjGnbguJ/9XDvHO9inAQ0tbrkWLpzYcipkcvQOiW5EpVpY5JXomnyG+tTwyxc23T0DIQ2oUUllYUlSwjqJR8fS6Xm/3y8zELF9h/uuTNt3nuPVNWiqHEHDzOjbhfH3iZjZ6OYK6VUVcwCZGGNlinZQFDVGoJAsqUdzFfQccFsjnXcet22c2OGKDMSASSdzeSO3O9uc2hAkbZyzekG2iKroIKK9pNJ+znhjWlZalm6B+Pmx0OuLVfe3GeLJs2zzmavFO15EPR4Pt00HNqVFdXYRaaWyB2+8PgpcFunzrXV/E5eIEcsEetrpw7XhEoSS8NI7YGQAfdRYQyWZJQKFvyBRAEZZG9h/tl+8ztuKYW6OWAAAAABJRU5ErkJggg==')
```

> 💡 16x16 pixels is a nice size for menu images.

### Add separators

A separator is a thin long line on the menu:

```pycon
>>> from swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_item('Item 1')
Item 1
>>> m.add_item('Item 2', sep=True)
Item 2
>>> m.add_item('Item 3')
Item 3
>>> m.dump()
My menu
---
Item 1
---
Item 2
Item 3
```

You can explicitly add a separator using:

```pycon
>>> m.add_sep()
---
```

### Access header and body

Within the menu, you can access the header and the body:

```pycon
>>> from src.swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_header('Header 2')
Header 2
>>> m.add_header('Header 3')
Header 3

>>> m.add_item('Item 1')
Item 1
>>> m.add_item('Item 2')
Item 2

>>> m.header
[My menu, Header 2, Header 3]
>>> m.body
[Item 1, Item 2]
```

You can also access items inside header and body:

```pycon
>>> from swiftbarmenu import MenuItem

>>> m.header[0]
My menu
>>> isinstance(m.header[0], MenuItem)
True

>>> m.body[1]
Item 2
>>> isinstance(m.body[1], MenuItem)
True
```

Even with nested items:

```pycon
>>> from src.swiftbarmenu import Menu

>>> m = Menu('My menu')

>>> item1 = m.add_item('Item 1')
>>> item1.add_item('Item 1.1')
Item 1.1
>>> item1.add_item('Item 1.2')
Item 1.2
>>> item1.add_item('Item 1.3')
Item 1.3

>>> item1[2]
Item 1.3
```

### Clear items

You can clear whole menu:

```pycon
>>> from src.swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> m.add_header('Header 2')
Header 2
>>> m.add_header('Header 3')
Header 3
>>> m.add_item('Item 1')
Item 1
>>> m.add_item('Item 2')
Item 2

>>> m
My menu
Header 2
Header 3
---
Item 1
Item 2

>>> m.clear()
>>> m

>>> m.header
[]
>>> m.body
[]
```

You can also clear nested items for a certain item:

```pycon
>>> from src.swiftbarmenu import Menu

>>> m = Menu('My menu')
>>> item1 = m.add_item('Item 1')
>>> item1.add_item('Item 1.1')
Item 1.1
>>> item1.add_item('Item 1.2')
Item 1.2
>>> item1.add_item('Item 1.3')
Item 1.3

>>> m
My menu
---
Item 1
-- Item 1.1
-- Item 1.2
-- Item 1.3

>>> item1.clear()

>>> m
My menu
---
Item 1
```

## Changelog

Releases use [Semantic Versioning](https://semver.org/) (`<major>.<minor>.<patch>`).

## 0.1.2

Released 2025-02-28

- Add feature to include images using path.

## 0.1.1

Released 2025-02-27

- Fixes menus with no header.

## 0.1.0

Released 2025-02-26

- First release.
