import pytest
from textx import metamodel_for_language


@pytest.fixture
def mm():
    return metamodel_for_language('ladsl')


def test_create_site(mm):

    model = '''
    create development site 34/77
    geoaggregates 34/17, 34/78
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.site.ko == 34 and t.site.id == 77

    assert len(t.geoaggregates) == 2
    g = t.geoaggregates[1]
    assert g.ko == 34 and g.id == 78


def test_apply_site(mm):

    model = '''
    apply development site 34/77
    '''

    m = mm.model_from_str(model)

    assert len(m.transactions) == 1
    t = m.transactions[0]
    assert t.site.ko == 34 and t.site.id == 77
