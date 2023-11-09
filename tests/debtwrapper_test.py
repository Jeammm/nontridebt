from debtwrapper import Client
from pytest import fixture

@fixture
def debt_keys():
    # Responsible only for returning the test data
    return ['Timestamp', 'ชื่อเจ้าหนี้', 'ชื่อบิล', 'พ้ง', 'เว็บ',
              'อู๋', 'ป้อง']

def test_debt_list(debt_keys):
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    data = client.debt_list()

    if len(data) > 0 :
        assert isinstance(data, list)
        assert set(debt_keys).issubset(data[0].keys())

def test_add_debt():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.add_debt({
      'ชื่อเจ้าหนี้': 'อู๋',
      'ชื่อบิล': 'yayayayayayyaya',
      'พ้ง': 4000,
      'เว็บ': 40000,
      'อู๋': 67,
      'ป้อง': 2
    })

    assert response["updates"]["updatedCells"] == 7

def test_add_debt_not_full():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.add_debt({
      'ชื่อเจ้าหนี้': 'อู๋',
      'ชื่อบิล': 'just one',
      'เว็บ': 4000,
    })

    assert response["updates"]["updatedCells"] == 7

def test_add_debt_not_sorted():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.add_debt({
      'ชื่อเจ้าหนี้': 'อู๋',
      'ชื่อบิล': 'not sorted',
      'อู๋': 67,
      'เว็บ': 4000,
      'พ้ง': 4000,
    })

    assert response["updates"]["updatedCells"] == 7

def test_check_debt():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.check_debt('เว็บ');

    assert response["borrower"] == "เว็บ"
    assert isinstance(response["amount"], dict)

def test_check_debt_2():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.check_debt('พ้ง');

    assert response["borrower"] == "พ้ง"
    assert isinstance(response["amount"], dict)

def test_check_debt_3():
    client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1')
    response = client.check_debt();

    assert response["message"]
