from .api_client import APIClient

class Tags(APIClient):
    def list_tags(self):
        return self.get("tags")
    
    def create_tag(self, name):
        return self.post("tags", {"name": name})
    
    def update_tag(self, tag_id, data):
        return self.post(f"tags/{tag_id}", data)
    
    def retrieve_tag(self, tag_id):
        return self.get(f"tags/{tag_id}")
    
    def delete_tag(self, tag_id):
        return self.post(f"tags/{tag_id}/delete")