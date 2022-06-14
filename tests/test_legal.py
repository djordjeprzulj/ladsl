import pytest
from textx import metamodel_for_language


@pytest.fixture
def mm():
    return metamodel_for_language('ladsl')


def test_transfer(mm):

    model = '''
    transfer
       from party1
       parcel 23/101
       share 1/1
       to party1
       share 1/1
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t._from[0] == 'party1'
    assert (t.from_share[0].nom, t.from_share[0].den) == (1, 1)
    assert (t.to_share[0].nom, t.to_share[0].den) == (1, 1)


def test_transfer_multi(mm):

    model = '''
    transfer
       from party11, party12
       parcel 23/101
       share 1/2, 1/2
       to party21, party22
       share 1/3, 2/3
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert len(t._from) == len(t.to) == 2
    assert t._from[0] == 'party11'
    assert (t.from_share[0].nom, t.from_share[0].den) == (1, 2)
    assert (t.to_share[0].nom, t.to_share[0].den) == (1, 3)


def test_update_party_1(mm):
    model = '''
    update
        party party1
        firstName "Marko"
        lastName  "Marković"
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.party == 'party1'
    assert t.first_name == 'Marko'
    assert t.last_name == 'Marković'


def test_update_party_2(mm):
    model = '''
    update
        party party1
        name "Neka firma"
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.party == 'party1'
    assert t.name == 'Neka firma'


def test_update_party_3(mm):
    model = '''
    update
        party party1
        address "Neka nova adresa"
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.party == 'party1'
    assert t.address == 'Neka nova adresa'


def test_update_parcelpart_1(mm):
    model = '''
    update
        parcel 34/101/2
        landUse liv1
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.parcel.ko == 34
    assert t.parcel.parcel == 101
    assert t.parcel.part == 2
    assert t.land_use == 'liv1'


def test_update_right(mm):
    model = '''
    update
        building 34/101/2
        right
          mortgage 45000.00 7%
        party party1
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.building.ko == 34
    assert t.building.parcel == 101
    assert t.building.building == 2
    assert t.right.ammount == 45000
    assert t.right.percent == 7


def test_create_building(mm):
    model = '''
    create
        building 34/101/2
        party party1, party2
        share 1/3, 2/3
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.building.ko == 34
    assert t.building.parcel == 101
    assert t.building.building == 2
    assert t.party == ['party1', 'party2']
    assert t.share[0].nom == 1
    assert t.share[0].den == 3
