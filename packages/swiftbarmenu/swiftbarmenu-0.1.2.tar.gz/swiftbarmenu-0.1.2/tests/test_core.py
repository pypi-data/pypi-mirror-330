import pytest

from src.swiftbarmenu import Menu, MenuItem

# ==============================================================================
# HEADER
# ==============================================================================


def test_single_header(capsys):
    m = Menu('Header')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
""".lstrip()
    )


def test_multiple_headers(capsys):
    m = Menu('Header')
    m.add_header('Header 2')
    m.add_header('Header 3')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
Header 2
Header 3
---
""".lstrip()
    )


def test_header_with_params(capsys):
    m = Menu('Header')
    m.add_header('Header 2', color='red', font='Helvetica')
    m.add_header('Header 3', color='blue', font='Arial')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
Header 2|color=red font=Helvetica
Header 3|color=blue font=Arial
---
""".lstrip()
    )


def test_add_header_fails_when_contains_sep():
    m = Menu('Header')
    with pytest.raises(ValueError) as err:
        m.add_header('Header 2', sep=True)
    assert str(err.value) == 'Header cannot have sep=True'


def test_get_header():
    m = Menu('Header')
    m.add_header('Header 2')
    m.add_header('Header 3')
    assert m.header[0].text == 'Header'
    assert m.header[1].text == 'Header 2'
    assert m.header[2].text == 'Header 3'


def test_add_header_returns_menuitem():
    m = Menu('Header')
    header = m.add_header('Header 2')
    assert isinstance(header, MenuItem)


def test_clear_header():
    m = Menu('Header')
    m.add_header('Header 2')
    m.add_header('Header 3')
    m.clear()
    assert m.header == []


def test_menu_fails_when_no_header():
    m = Menu()
    m.add_item('Item 1')
    m.add_item('Item 2')
    with pytest.raises(ValueError) as err:
        m.dump()
    assert str(err.value) == 'Menu must have a header'


# ==============================================================================
# BODY
# ==============================================================================


def test_add_items(capsys):
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Item 1
Item 2
""".lstrip()
    )


def test_add_items_with_params(capsys):
    m = Menu('Header')
    m.add_item('Item 1', color='red', font='Helvetica')
    m.add_item('Item 2', color='blue', font='Arial')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Item 1|color=red font=Helvetica
Item 2|color=blue font=Arial
""".lstrip()
    )


def test_add_items_with_sep(capsys):
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2', sep=True)
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Item 1
---
Item 2
""".lstrip()
    )


def test_add_nested_items(capsys):
    m = Menu('Header')
    m.add_item('Item 1')
    item2 = m.add_item('Item 2')
    m.add_item('Item 3')
    item2.add_item('Item 2.1')
    item2.add_item('Item 2.2')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Item 1
Item 2
-- Item 2.1
-- Item 2.2
Item 3
""".lstrip()
    )


def test_add_link(capsys):
    m = Menu('Header')
    m.add_link('Google', 'https://www.google.com')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Google|href=https://www.google.com
""".lstrip()
    )


def test_add_link_with_params(capsys):
    m = Menu('Header')
    m.add_link('Google', 'https://www.google.com', color='red', font='Helvetica')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Google|href=https://www.google.com color=red font=Helvetica
""".lstrip()
    )


def test_str():
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2')
    assert str(m) == 'Header\n---\nItem 1\nItem 2'


def test_repr():
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2')
    assert repr(m) == 'Header\n---\nItem 1\nItem 2'


def test_get_body():
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2')
    assert m.body[0].text == 'Item 1'
    assert m.body[1].text == 'Item 2'


def test_get_item():
    m = Menu('Header')
    item1 = m.add_item('Item 1')
    item1.add_item('Item 1.1')
    item1.add_item('Item 1.2')
    assert item1[0].text == 'Item 1.1'
    assert item1[1].text == 'Item 1.2'


def test_add_item_returns_menuitem():
    m = Menu()
    item = m.add_item('Item')
    assert isinstance(item, MenuItem)


def test_clear_body():
    m = Menu('Header')
    m.add_item('Item 1')
    m.add_item('Item 2')
    m.clear()
    assert m.body == []


def test_clear_nested_items():
    m = Menu('Header')
    item1 = m.add_item('Item 1')
    item1.add_item('Item 1.1')
    item1.add_item('Item 1.2')
    item1.clear()
    assert item1.items == []


def test_add_image(capsys):
    m = Menu('Header')
    m.add_image('tests/images/parrot.png', 'Parrot')
    m.dump()
    output = capsys.readouterr()
    assert (
        output.out
        == """
Header
---
Parrot|image=iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAJZlWElmTU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAExAAIAAAARAAAAWodpAAQAAAABAAAAbAAAAAAAAABgAAAAAQAAAGAAAAABd3d3Lmlua3NjYXBlLm9yZwAAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAA4+VmVAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAWRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIj4KICAgICAgICAgPHhtcDpDcmVhdG9yVG9vbD53d3cuaW5rc2NhcGUub3JnPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqyyWIhAAACL0lEQVQ4Eb1TXUiTURh+ztn2bW7OmGa2DAIpt8ogRxS0q6Ifbyy88MIuEoIgUOznIop+WAWSlGHSTdBVN10s6C6Tlo0i+5EULFhQ68fSOecmubl92/fz9m06ZrHVXS8cznue93le3vc95wD/NpaApeYLYCpGZcXAPDazfXdr+ZrVJ3UNTofu2/eg7uvEQfZ8MJSPZ3f98kPBJ5bY2txltgp9ZC3Hu+YmsESiUuDsEHYN9hZ4RRLceIJagQynfcFVHY2j62EbTyFwqdvLjx2pd9bVTS0XZ/3fWuh/hQpZxFOjGa6EAqyYMqHlphsVcb7nx8O74xvs9sifCXge8BC4kkG/YIIrk9RKk7WV0iOjUjAZ148UE2e1uRl0+1AlPMJ1ZkR7fB6ILVQjGnbguJ/9XDvHO9inAQ0tbrkWLpzYcipkcvQOiW5EpVpY5JXomnyG+tTwyxc23T0DIQ2oUUllYUlSwjqJR8fS6Xm/3y8zELF9h/uuTNt3nuPVNWiqHEHDzOjbhfH3iZjZ6OYK6VUVcwCZGGNlinZQFDVGoJAsqUdzFfQccFsjnXcet22c2OGKDMSASSdzeSO3O9uc2hAkbZyzekG2iKroIKK9pNJ+znhjWlZalm6B+Pmx0OuLVfe3GeLJs2zzmavFO15EPR4Pt00HNqVFdXYRaaWyB2+8PgpcFunzrXV/E5eIEcsEetrpw7XhEoSS8NI7YGQAfdRYQyWZJQKFvyBRAEZZG9h/tl+8ztuKYW6OWAAAAABJRU5ErkJggg==
""".lstrip()
    )
