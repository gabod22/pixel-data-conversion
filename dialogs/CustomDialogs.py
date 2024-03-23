# dialogs
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from modules.backend_connection import save_computer
import re
from modules.helpers import convert_size
import asyncio
import json


class CustomDialog(QDialog):
    def __init__(self, title, message):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(message)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class RegisterComputerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("¿Desea registrar la computadora?")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        messageLabel = QLabel(
            "La computadora no está registrada, si desea registrar la computadora, de click en ok")
        self.layout.addWidget(messageLabel)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class RegisterFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Colocar el Pixel-ID")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(lambda: asyncio.run(self.save()))
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.pixelid = QLineEdit()
        self.layout.addWidget(self.pixelid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    async def save(self):
        pixelidText = self.pixelid.text()
        cpu_model = re.search(
            "i\d-\d{4}[A-Z]", self.parent.system_info["cpu"]["brand_raw"]).group()
        ram = str(convert_size(self.parent.system_info["virtual_memory"]
                  ["total"])) + " " + self.parent.system_info["memories"][0]["Tipo"]

        # self.parent.system_info["bios"]["Version"]

        model = self.parent.system_info["computer_system"]["Model"]
        service_tag = self.parent.system_info["bios"]["SerialNumber"]
        # Add all Disks to table
        specs = {
                "gpus": str(self.parent.system_info['gpus']),
                "cpu": cpu_model,
                "ram": ram,
                "disks": str(self.parent.system_info['disks']),
            }
        computer = {
            "service_tag": service_tag,
            "internal_id": pixelidText,
            "specs": json.dumps(specs),
            "model": model,
        }
        # print(json.encoder(str(computer)))
        (response, r) = await save_computer(computer=computer)
        if response.status == 200 or response.status == 201 :
            self.parent.this_computer = json.loads(r)
            self.accept()
            if "warn" in r:
                print(r)