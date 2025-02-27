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
