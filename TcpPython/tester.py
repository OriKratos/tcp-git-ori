from Kratos.KratosProtocol import KratosProtocol
from TCPClient.TCPClient import TCPClient

# יצירת לקוח TCP
client = TCPClient(host="127.0.0.1", port=65432)
client.connect()

# יצירת פרוטוקול Kratos
protocol = KratosProtocol(client)

# שליחת Frame לדוגמה
frame = {
    "preamble": 0x0054,
    "command": 0x101,
    "dataLength": 0,
    "data": "",
    "checksum": 0xFFFF
}
protocol.send_frame(frame)

# קבלת תשובה מהשרת
response_frame = protocol.receive_frame()
print(response_frame)

# סגירת הלקוח
client.close()

