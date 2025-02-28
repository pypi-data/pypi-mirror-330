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
