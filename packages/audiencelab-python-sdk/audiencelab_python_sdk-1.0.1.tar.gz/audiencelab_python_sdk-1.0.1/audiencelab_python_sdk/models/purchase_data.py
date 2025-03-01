class PurchaseData:
    def __init__(self):
        self.data = {"type": "purchase", "payload": {}}

    def set_item_id(self, item_id):
        if not isinstance(item_id, str):
            raise ValueError("Invalid input type for item_id")
        self.data["payload"]["item_id"] = item_id
        return self

    def set_item_name(self, item_name):
        if not isinstance(item_name, str):
            raise ValueError("Invalid input type for item_name")
        self.data["payload"]["item_name"] = item_name
        return self

    def set_value(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Invalid input type for value")
        self.data["payload"]["value"] = value
        return self

    def set_currency(self, currency):
        if not isinstance(currency, str):
            raise ValueError("Invalid input type for currency")
        self.data["payload"]["currency"] = currency
        return self

    def set_status(self, status):
        self.data["payload"]["status"] = status
        return self

    def can_send(self):
        payload = self.data["payload"]
        required = ["item_id", "item_name", "value"]
        missing = [field for field in required if field not in payload]
        if missing:
            return {"status": False, "message": f"Missing fields: {', '.join(missing)}"}
        return {"status": True, "message": "Ready to send"}

    def to_json(self):
        return self.data 