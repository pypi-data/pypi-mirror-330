from .api_client import APIClient

class Lists(APIClient):
    def list_lists(self):
        return self.get("lists")
    
    def create_list(self, name, description=None):
        data = {"name": name, "description": description}
        return self.post("lists", data)
    
    def update_list(self, list_id, data):
        return self.post(f"lists/{list_id}", data)
    
    def retrieve_list(self, list_id):
        return self.get(f"lists/{list_id}")
    
    def delete_list(self, list_id):
        return self.post(f"lists/{list_id}/delete")