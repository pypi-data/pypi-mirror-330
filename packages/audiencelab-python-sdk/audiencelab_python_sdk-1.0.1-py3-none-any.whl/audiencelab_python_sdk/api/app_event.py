class AppEvent:
    def __init__(self, api_client, event_data, user_data):
        self.api_client = api_client
        self.event_data = event_data
        self.user_data = user_data

    def send(self):
        # Check required fields in user_data.
        user_check = self.user_data.can_send_app_event() if hasattr(self.user_data, 'can_send_app_event') else True
        if isinstance(user_check, dict):
            if not user_check.get("status", True):
                raise ValueError(user_check.get("message", "User cannot send app event"))
        elif not user_check:
            raise ValueError("User cannot send app event")

        # Check that event_data is ready
        event_check = self.event_data.can_send()
        if not event_check.get("status", True):
            raise ValueError(event_check.get("message", "Event data is not ready"))

        event_json = self.event_data.to_json()

        # Build payload body
        body = {"type": event_json.get("type")}
        # Merge user event data
        if hasattr(self.user_data, 'get_app_event_data'):
            body.update(self.user_data.get_app_event_data())
        # Overwrite payload from event data
        body["payload"] = event_json.get("payload", {})

        # Perform POST request
        response = self.api_client.post(f"/webhook", json=body)
        return response.json() 