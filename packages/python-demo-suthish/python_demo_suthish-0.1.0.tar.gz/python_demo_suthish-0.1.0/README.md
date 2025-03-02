# Yonoma API Client

A Python client library for the Yonoma API that handles email marketing capabilities, contact management, and tagging functionality.

## Installation

```bash
pip install -r requirements.txt
```

## Features

- Contact Management
- List Management
- Tag Management

## Quick Start

```python
from yonoma import Lists, Tags, Contacts

# Initialize with your API key
api_key = "your_api_key"
lists = Lists(api_key)
tags = Tags(api_key)
contacts = Contacts(api_key)

# Create a list
new_list = lists.create_list(
    list_name="Newsletter Subscribers"
)

# Create a tag
new_tag = tags.create_tag(tag_name="VIP Customer")

# Create and tag a contact
contact = contacts.create_contact(
    email="user@example.com",
    name="John Doe"
)
contacts.label_contact(contact['id'], new_tag['id'])
```

## API Reference

### Lists

```python
# Get all lists
lists.list_lists()

# Create a list
lists.create_list(list_name="My List")

# Update a list
lists.update_list(list_id="123", data={"name": "Updated Name"})

# Retrieve a list
lists.retrieve_list(list_id="123")

# Delete a list
lists.delete_list(list_id="123")
```

### Tags

```python
# Get all tags
tags.list_tags()

# Create a tag
tags.create_tag(tag_name="VIP")

# Update a tag
tags.update_tag(tag_id="456", data={"name": "Premium"})

# Retrieve a tag
tags.retrieve_tag(tag_id="456")

# Delete a tag
tags.delete_tag(tag_id="456")
```

### Contacts

```python
# Create a contact
contacts.create_contact(
    email="user@example.com",
    status="John Doe",
)

# Unsubscribe a contact
contacts.unsubscribe_contact(contact_id="789")

# Label a contact with a tag
contacts.label_contact(contact_id="789", tag_id="456")

# Remove a tag from a contact
contacts.remove_tag(contact_id="789", tag_id="456")
```

## Error Handling

The API client will raise exceptions for various error cases:

```python
try:
    lists.create_list(name="My List")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## Configuration

The API client uses the following base configuration:

```python
BASE_URL = "http://localhost:8080"
VERSION = "v1"
```

## Project Structure

```plaintext
yonoma-api/
├── README.md
├── requirements.txt
├── setup.py
└── src/
    └── yonoma/
        ├── __init__.py
        ├── config.py
        ├── api_client.py
        ├── lists.py
        ├── tags.py
        └── contacts.py
```

## Development

1. Clone the repository
```bash
git clone https://github.com/SuthishTwinarcus/Demo-Python-Package.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run tests
```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@yourdomain.com or create an issue in the GitHub repository.

## Acknowledgments

- Based on the [Yonoma API Documentation](https://yonoma.io/api-reference/introduction)
- Thanks to all contributors

## Version History

- 0.1.0
    - Initial Release
    - Basic API functionality
    - List, Tag, and Contact management