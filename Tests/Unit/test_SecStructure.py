from src.secStructure import *


def test_processData():
    pass


def test_createHeatMapColoring():
    pass


def test_createColorVector():
    pass


def test_createIntermediateTemplate():
    pass


def test_helpAddIBloop():
    pass


def test_element2dotbracket():
    # Test1 without multiloop
    elem_string1 = "EEESSSIIISSSBBBSSSHHHSSSSSSIIISSSEEE"
    dotbracket_string1 = "...(((...(((...(((...))))))...)))..."

    # Test2 with multiloop
    elem_string2 = "EESSIISSHHSSIISSMMSSBBSSHHSSSSEE"
    dotbracket_string2 = "..((..((..))..))..((..((..)))).."

    # Test 3 without loops
    elem_string3 = "EEEESSSSSSSSEEEE"
    dotbracket_string3 = "....(((())))...."

    # Test 5 with everything
    elem_string4 = "EEESSSIIISSSBBBSSSHHHSSSSSSIIISSSMMMSSSHHHSSSEEE"
    dotbracket_string4 = "...(((...(((...(((...))))))...)))...(((...)))..."

    # Execution
    db1 = []
    db1.extend(element2dotbracket(elem_string1, 3, 0, 20, True))
    db1.extend(element2dotbracket(elem_string1, 3, 21, len(elem_string1), False))
    db1 = ''.join(db1)

    db2 = []
    db2.extend(element2dotbracket(elem_string2, 2, 0, 9, True))
    db2.extend(element2dotbracket(elem_string2, 2, 10, 15, False))
    db2.extend(element2dotbracket(elem_string2, 2, 16, 23, True))
    db2.extend(element2dotbracket(elem_string2, 2, 24, len(elem_string2), False))
    db2 = ''.join(db2)

    db3 = []
    db3.extend(element2dotbracket(elem_string3, 4, 0, 7, True))
    db3.extend(element2dotbracket(elem_string3, 4, 8, len(elem_string3), False))
    db3 = ''.join(db3)

    db4 = []
    db4.extend(element2dotbracket(elem_string4, 3, 0, 20, True))
    db4.extend(element2dotbracket(elem_string4, 3, 21, 32, False))
    db4.extend(element2dotbracket(elem_string4, 3, 33, 38, True))
    db4.extend(element2dotbracket(elem_string4, 3, 39, len(elem_string4), False))
    db4 = ''.join(db4)

    # testing
    # assert db1 == dotbracket_string1
    # assert db2 == dotbracket_string2
    assert db3 == dotbracket_string3
    # assert db4 == dotbracket_string4
