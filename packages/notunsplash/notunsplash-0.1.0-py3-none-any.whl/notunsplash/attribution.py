"""
Attribution handling for Unsplash photos
"""
from typing import Dict, Optional
from datetime import datetime

class Attribution:
    """Handles attribution requirements for Unsplash photos"""
    
    def __init__(self, photo):
        """Initialize attribution with a photo object"""
        self.photo = photo
    
    def get_html(self, css_class: Optional[str] = "unsplash-attribution") -> str:
        """Generate HTML attribution"""
        css_class_attr = f' class="{css_class}"' if css_class else ''
        return f"""
        <div{css_class_attr}>
            <p>
                Photo by <a href="https://unsplash.com/@{self.photo.user.username}">{self.photo.user.name}</a> on 
                <a href="https://unsplash.com/photos/{self.photo.id}">Unsplash</a>
            </p>
        </div>
        """.strip()
    
    def get_text(self) -> str:
        """Generate plain text attribution"""
        return f"""Photo by {self.photo.user.name} on Unsplash
Photographer: https://unsplash.com/@{self.photo.user.username}
Photo: https://unsplash.com/photos/{self.photo.id}"""
    
    def get_markdown(self) -> str:
        """Generate markdown attribution"""
        return f"Photo by [{self.photo.user.name}](https://unsplash.com/@{self.photo.user.username}) on [Unsplash](https://unsplash.com/photos/{self.photo.id})"
    
    def get_rst(self) -> str:
        """Generate reStructuredText attribution"""
        return f"Photo by `{self.photo.user.name} <https://unsplash.com/@{self.photo.user.username}>`_ on `Unsplash <https://unsplash.com/photos/{self.photo.id}>`_"
    
    @property
    def metadata(self) -> Dict:
        """Get complete metadata about the photo and attribution"""
        return {
            "photo_id": self.photo.id,
            "photographer_name": self.photo.user.name,
            "photographer_username": self.photo.user.username,
            "photographer_url": f"https://unsplash.com/@{self.photo.user.username}",
            "photo_url": f"https://unsplash.com/photos/{self.photo.id}",
            "description": self.photo.description,
            "unsplash_url": "https://unsplash.com",
            "creation_time": self.photo.created_at.isoformat(),
            "attribution_generated": datetime.now().isoformat()
        }
