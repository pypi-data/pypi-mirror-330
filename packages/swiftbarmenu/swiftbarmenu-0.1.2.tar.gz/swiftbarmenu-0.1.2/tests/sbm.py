import sys

sys.path.append('.')
from src.swiftbarmenu import Menu

m = Menu('Test')
m.add_item('Item 1')
m.add_image('tests/images/parrot.png', 'Parrot')
item2 = m.add_item('Item 2', sep=True, checked=True)
item2.add_item('Subitem 1')
item2.add_item('Subitem 2')
m.add_link('Item 3', 'https://example.com', color='yellow')
m.add_item(':thermometer: Item 4', color='orange', sfcolor='black', sfsize=20)

m.dump()
