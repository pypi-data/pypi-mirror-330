# NotUnsplash Python SDK

A Python wrapper for the [Unsplash API](https://unsplash.com/documentation) that makes it easy to interact with Unsplash's services programmatically.

## Features

- Simple and intuitive interface for the Unsplash API
- Full OAuth authentication support
- Type hints for better IDE integration
- Comprehensive error handling
- Support for all major Unsplash API endpoints
- Proper rate limit handling
- Automatic image download tracking

## Installation

```bash
pip install notunsplash
```

Or install from source:

```bash
git clone https://github.com/yourusername/notunsplash-python-sdk.git
cd notunsplash-python-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
from notunsplash import Unsplash

# Initialize with your access key
client = Unsplash(access_key="your_access_key")

# Get a random photo
photo = client.get_random_photo()
print(f"Photo by {photo.user.name}: {photo.urls.regular}")

# Search for photos
results = client.search_photos("nature", page=1, per_page=10)
for photo in results["results"]:
    print(f"Photo ID: {photo.id}, Likes: {photo.likes}")

# Get a user's profile
user = client.get_user("username")
print(f"Total photos: {user.total_photos}")
```

### Authentication

For actions that require user authentication (like liking photos or managing collections), you'll need to use OAuth:

```python
# Initialize with OAuth credentials
client = Unsplash(
    access_key="your_access_key",
    secret_key="your_secret_key",
    redirect_uri="your_redirect_uri",
    scope=["public", "write_likes", "write_collections"]
)

# Get the authorization URL
auth_url = client.get_auth_url()
print(f"Visit this URL to authorize: {auth_url}")

# After user authorizes and you get the code from the redirect
token_data = client.get_bearer_token("authorization_code_from_redirect")

# Now you can use authenticated endpoints
# Like a photo
client.like_photo("photo_id")
```

## Available Methods

### Photos

- `get_photo(photo_id)`: Get a single photo
- `list_photos(page=1, per_page=10, order_by="latest")`: List photos
- `search_photos(query, page=1, per_page=10)`: Search photos
- `get_random_photo()`: Get a random photo
- `track_download(photo_id)`: Track a photo download
- `like_photo(photo_id)`: Like a photo (requires authentication)
- `unlike_photo(photo_id)`: Unlike a photo (requires authentication)

### Collections

- `get_collection(collection_id)`: Get a single collection
- `list_collections(page=1, per_page=10)`: List collections
- `get_user_collections(username, page=1, per_page=10)`: Get a user's collections
- `create_collection(title, description=None, private=False)`: Create a collection (requires authentication)
- `update_collection(collection_id, title=None, description=None, private=None)`: Update a collection (requires authentication)
- `delete_collection(collection_id)`: Delete a collection (requires authentication)
- `add_photo_to_collection(collection_id, photo_id)`: Add a photo to a collection (requires authentication)
- `remove_photo_from_collection(collection_id, photo_id)`: Remove a photo from a collection (requires authentication)

### Users

- `get_user(username)`: Get a user's public profile

### Topics

- `get_topic(topic_id_or_slug)`: Get a single topic
- `list_topics(page=1, per_page=10, order_by="featured")`: List topics

## Attribution

Unsplash requires proper attribution for all photos. This SDK makes it easy to generate correct attribution in multiple formats:

```python
from notunsplash import Unsplash

# Initialize client and get a photo
client = Unsplash(access_key="your_access_key")
photo = client.get_random_photo()

# Get attribution in different formats
# HTML
html_attribution = photo.attribution.get_html()
print(html_attribution)
# <div class="unsplash-attribution">
#     <p>
#         Photo by <a href="https://unsplash.com/@photographer">John Smith</a> on 
#         <a href="https://unsplash.com/photos/abc123">Unsplash</a>
#     </p>
# </div>

# Plain text
text_attribution = photo.attribution.get_text()
print(text_attribution)
# Photo by John Smith on Unsplash
# Photographer: https://unsplash.com/@photographer
# Photo: https://unsplash.com/photos/abc123

# Markdown
md_attribution = photo.attribution.get_markdown()
print(md_attribution)
# Photo by [John Smith](https://unsplash.com/@photographer) on [Unsplash](https://unsplash.com/photos/abc123)

# reStructuredText
rst_attribution = photo.attribution.get_rst()
print(rst_attribution)
# Photo by `John Smith <https://unsplash.com/@photographer>`_ on `Unsplash <https://unsplash.com/photos/abc123>`_

# Get complete metadata
metadata = photo.attribution.metadata
print(metadata)
# {
#     "photo_id": "abc123",
#     "photographer_name": "John Smith",
#     "photographer_username": "photographer",
#     "photographer_url": "https://unsplash.com/@photographer",
#     "photo_url": "https://unsplash.com/photos/abc123",
#     "description": "A beautiful landscape",
#     "unsplash_url": "https://unsplash.com",
#     "creation_time": "2025-02-25T21:52:18-06:00",
#     "attribution_generated": "2025-02-25T22:00:23-06:00"
# }

### Customizing HTML Attribution

You can customize the CSS class used in HTML attribution:

```python
# Custom CSS class
html_attribution = photo.attribution.get_html(css_class="my-custom-attribution")

# No CSS class
html_attribution = photo.attribution.get_html(css_class=None)
```

## Examples

### Blog Post Generator

Create a markdown blog post with Unsplash images and proper attribution:

```python
from notunsplash import Unsplash
from datetime import datetime

client = Unsplash(access_key="your_access_key")

# Search for coffee-related photos
photos = client.search_photos("coffee brewing", per_page=2)

# Generate markdown blog post
post = "# Coffee Brewing - A Photo Journey\n\n"

for photo in photos.entries:
    # Add photo with markdown attribution
    post += f"![{photo.description or 'Coffee photo'}]({photo.urls.regular})\n\n"
    post += f"_{photo.attribution.get_markdown()}_\n\n"

# Save the blog post
with open("coffee_blog.md", "w") as f:
    f.write(post)
```

### Social Media Gallery

Create a responsive HTML gallery with proper attribution:

```python
from notunsplash import Unsplash

client = Unsplash(access_key="your_access_key")

# Get photos from a nature collection
collections = client.search_collections("nature", per_page=1)
collection = collections.entries[0]
photos = client.get_collection_photos(collection.id, per_page=4)

# Generate HTML gallery
html = """
<div class="gallery">
"""

for photo in photos.entries:
    html += f"""
    <div class="image-card">
        <img src="{photo.urls.regular}" alt="{photo.description or 'Nature photo'}">
        {photo.attribution.get_html(css_class="gallery-attribution")}
    </div>
    """

html += "</div>"

# Save the gallery
with open("nature_gallery.html", "w") as f:
    f.write(html)
```

For more detailed examples, check out the `examples` directory:
- `blog_post_generator.py`: Complete blog post generator with image metadata
- `social_media_gallery.py`: Responsive image gallery with styled attribution
- `real_estate_images.py`: Real estate listing image management

## Data Models

The SDK uses dataclasses to represent Unsplash resources:

- `Photo`: Represents a photo with properties like `id`, `urls`, `user`, etc.
- `Collection`: Represents a collection of photos
- `User`: Represents a user profile
- `Topic`: Represents a topic
- `Urls`: Represents photo URLs (raw, full, regular, small, thumb)

## Error Handling

The SDK provides custom exceptions for better error handling:

```python
from notunsplash.errors import UnsplashError, UnsplashAuthError

try:
    client.like_photo("photo_id")
except UnsplashAuthError:
    print("Authentication required!")
except UnsplashError as e:
    print(f"An error occurred: {e}")
```

## Rate Limiting

The Unsplash API has rate limits:
- Demo applications: 50 requests per hour
- Production applications: 5000 requests per hour

The rate limit status is returned in the response headers:
- `X-Ratelimit-Limit`: Total requests allowed per hour
- `X-Ratelimit-Remaining`: Remaining requests for the hour

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Unsplash team for providing an excellent API
