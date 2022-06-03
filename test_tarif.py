from tarif_assurance import tarif


def test_1():
    assert  tarif(26,6,6,0) == 'bleu'
def test_2():
    assert  tarif(26,6,4,0) == 'vert'
def test_3():
    assert  tarif(26,1,6,0) == 'vert'
def test_4():
    assert  tarif(26,1,4,0) == 'orange'
def test_5():
    assert  tarif(23,4,6,0) == 'vert'
def test_6():
    assert  tarif(23,4,4,0) == 'orange'
def test_7():
    assert  tarif(23,1,6,0) == 'orange'
def test_8():
    assert  tarif(23,1,1,0) == 'rouge'
def test_9():
    assert  tarif(26,4,6,1) == 'vert'
def test_10():
    assert  tarif(26,4,4,1) == 'orange'
def test_11():
    assert  tarif(26,1,6,1) == 'orange'
def test_12():
    assert  tarif(28,1,4,1) == 'rouge'
def test_13():
    assert  tarif(23,4,6,1) == 'orange'
def test_14():
    assert  tarif(23,4,4,1) == 'rouge'
def test_15():
    assert  tarif(22,1,6,1) == 'refus'
def test_16():
    assert  tarif(22,1,4,1) == 'refus'
def test_17():
    assert  tarif(26,4,6,2) == 'orange'
def test_18():
    assert  tarif(30,4,2,2) == 'rouge'
def test_19():
    assert  tarif(30,1,6,2) == 'refus'
def test_20():
    assert  tarif(30,1,2,2) == 'refus'
def test_21():
    assert  tarif(22,4,6,2) == 'refus'
def test_22():
    assert  tarif(22,4,4,2) == 'refus'
def test_23():
    assert  tarif(22,1,6,2) == 'refus'
def test_24():
    assert  tarif(22,1,4,2) == 'refus'
def test_25():
    assert  tarif(26,4,6,3) == 'refus'
def test_26():
    assert  tarif(26,4,4,3) == 'refus'
def test_27():
    assert  tarif(28,1,8,3) == 'refus'
def test_28():
    assert  tarif(26,1,3,3) == 'refus'
def test_29():
    assert  tarif(24,3,6,3) == 'refus'
def test_30():
    assert  tarif(24,3,4,3) == 'refus'
def test_31():
    assert  tarif(24,1,6,3) == 'refus'
def test_32():
    assert  tarif(24,1,2,3) == 'refus'








