from .api_client import APIClient

class Contacts(APIClient):
    def create_contact(self, email, name=None, custom_fields=None):
        data = {
            "email": email,
            "name": name,
            "custom_fields": custom_fields
        }
        return self.post("contacts", data)
    
    def unsubscribe_contact(self, contact_id):
        return self.post(f"contacts/{contact_id}/unsubscribe")
    
    def label_contact(self, contact_id, tag_id):
        return self.post(
            f"contacts/{contact_id}/tags",
            {"tag_id": tag_id}
        )
    
    def remove_tag(self, contact_id, tag_id):
        return self.post(f"contacts/{contact_id}/tags/{tag_id}/remove")