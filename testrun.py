from debtwrapper import Client

client = Client('สำเนาของ ปลดหนี้ (Responses)', 'Form Responses 1', "cerds.json")

print(client.debt_list())