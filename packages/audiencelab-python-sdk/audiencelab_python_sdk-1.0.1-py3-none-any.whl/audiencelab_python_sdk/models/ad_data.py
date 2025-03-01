class AdData:
    def __init__(self):
        self.data = {"type": "ad", "payload": {}}

    def set_ad_id(self, ad_id):
        if not isinstance(ad_id, str):
            raise ValueError("Invalid input type for ad_id")
        self.data["payload"]["ad_id"] = ad_id
        return self

    def set_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Invalid input type for name")
        self.data["payload"]["name"] = name
        return self

    def set_source(self, source):
        if not isinstance(source, str):
            raise ValueError("Invalid input type for source")
        self.data["payload"]["source"] = source
        return self

    def set_watch_time(self, watch_time):
        if not isinstance(watch_time, (int, float)):
            raise ValueError("Invalid input type for watch time")
        self.data["payload"]["watch_time"] = watch_time
        return self

    def set_reward(self, reward):
        self.data["payload"]["reward"] = reward
        return self

    def set_media_source(self, media_source):
        self.data["payload"]["media_source"] = media_source
        return self

    def set_channel(self, channel):
        self.data["payload"]["channel"] = channel
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

    def can_send(self):
        # require at least ad_id, name, and source
        payload = self.data["payload"]
        required = ["ad_id", "name", "source"]
        missing = [field for field in required if field not in payload]
        if missing:
            return {"status": False, "message": f"Missing fields: {', '.join(missing)}"}
        return {"status": True, "message": "Ready to send"}

    def to_json(self):
        return self.data 