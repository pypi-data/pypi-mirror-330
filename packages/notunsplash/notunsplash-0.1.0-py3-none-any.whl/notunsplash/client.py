"""
Unsplash API Client
"""
import requests
from typing import Optional, Dict, List, Union
from urllib.parse import urlencode
from .models import Photo, Collection, User, Topic
from .errors import UnsplashError, UnsplashAuthError

class Unsplash:
    """Main client class for interacting with the Unsplash API"""
    
    BASE_URL = "https://api.unsplash.com"
    OAUTH_URL = "https://unsplash.com/oauth"
    
    def __init__(
        self, 
        access_key: str, 
        secret_key: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        bearer_token: Optional[str] = None
    ):
        """
        Initialize the Unsplash client
        
        Args:
            access_key: Your Unsplash API access key
            secret_key: Your Unsplash API secret key (optional, only needed for write operations)
            redirect_uri: OAuth redirect URI (optional, needed for user authentication)
            scope: List of OAuth scopes (optional, needed for user authentication)
            bearer_token: User's OAuth bearer token (optional, needed for authenticated requests)
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.scope = scope or []
        self.bearer_token = bearer_token
        
        self.session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self):
        """Set the appropriate authentication header"""
        if self.bearer_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.bearer_token}"
            })
        else:
            self.session.headers.update({
                "Authorization": f"Client-ID {self.access_key}"
            })
        self.session.headers.update({"Accept-Version": "v1"})

    def get_auth_url(self) -> str:
        """
        Get the OAuth authorization URL for user authentication
        
        Returns:
            str: Authorization URL that the user should visit
        """
        if not self.redirect_uri:
            raise UnsplashAuthError("redirect_uri is required for authentication")
            
        params = {
            "client_id": self.access_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scope)
        }
        return f"{self.OAUTH_URL}/authorize?{urlencode(params)}"

    def get_bearer_token(self, auth_code: str) -> Dict[str, str]:
        """
        Exchange authorization code for bearer token
        
        Args:
            auth_code: Authorization code received from OAuth redirect
            
        Returns:
            dict: Token response containing access_token, refresh_token, etc.
        """
        if not self.secret_key:
            raise UnsplashAuthError("secret_key is required for authentication")
            
        data = {
            "client_id": self.access_key,
            "client_secret": self.secret_key,
            "redirect_uri": self.redirect_uri,
            "code": auth_code,
            "grant_type": "authorization_code"
        }
        
        response = requests.post(f"{self.OAUTH_URL}/token", data=data)
        if not response.ok:
            raise UnsplashAuthError(f"Failed to get bearer token: {response.text}")
            
        token_data = response.json()
        self.bearer_token = token_data["access_token"]
        self._set_auth_header()
        return token_data

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make a request to the Unsplash API"""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        
        if not response.ok:
            raise UnsplashError(f"API request failed: {response.status_code} - {response.text}")
            
        return response.json()

    def get_photo(self, photo_id: str) -> Photo:
        """Get a single photo by ID"""
        data = self._request("GET", f"/photos/{photo_id}")
        return Photo.from_dict(data)

    def list_photos(self, page: int = 1, per_page: int = 10, order_by: str = "latest") -> List[Photo]:
        """List photos with optional pagination"""
        data = self._request("GET", "/photos", params={
            "page": page,
            "per_page": per_page,
            "order_by": order_by
        })
        return [Photo.from_dict(item) for item in data]

    def search_photos(self, query: str, page: int = 1, per_page: int = 10) -> Dict[str, Union[int, List[Photo]]]:
        """Search for photos"""
        data = self._request("GET", "/search/photos", params={
            "query": query,
            "page": page,
            "per_page": per_page
        })
        return {
            "total": data["total"],
            "total_pages": data["total_pages"],
            "results": [Photo.from_dict(item) for item in data["results"]]
        }

    def get_random_photo(self) -> Photo:
        """Get a random photo"""
        data = self._request("GET", "/photos/random")
        return Photo.from_dict(data)

    def get_user(self, username: str) -> User:
        """Get a user's public profile"""
        data = self._request("GET", f"/users/{username}")
        return User.from_dict(data)

    def get_collection(self, collection_id: str) -> Collection:
        """Get a single collection"""
        data = self._request("GET", f"/collections/{collection_id}")
        return Collection.from_dict(data)

    def list_collections(self, page: int = 1, per_page: int = 10) -> List[Collection]:
        """List collections"""
        data = self._request("GET", "/collections", params={
            "page": page,
            "per_page": per_page
        })
        return [Collection.from_dict(item) for item in data]

    def get_topic(self, topic_id_or_slug: str) -> Topic:
        """Get a single topic"""
        data = self._request("GET", f"/topics/{topic_id_or_slug}")
        return Topic.from_dict(data)

    def list_topics(self, page: int = 1, per_page: int = 10, order_by: str = "featured") -> List[Topic]:
        """List topics"""
        data = self._request("GET", "/topics", params={
            "page": page,
            "per_page": per_page,
            "order_by": order_by
        })
        return [Topic.from_dict(item) for item in data]

    def track_download(self, photo_id: str) -> None:
        """Track a photo download"""
        self._request("GET", f"/photos/{photo_id}/download")

    def like_photo(self, photo_id: str) -> Dict:
        """Like a photo on behalf of the authenticated user"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to like photos")
        return self._request("POST", f"/photos/{photo_id}/like")

    def unlike_photo(self, photo_id: str) -> Dict:
        """Remove like from a photo on behalf of the authenticated user"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to unlike photos")
        return self._request("DELETE", f"/photos/{photo_id}/like")

    def get_user_collections(self, username: str, page: int = 1, per_page: int = 10) -> List[Collection]:
        """Get collections created by a user"""
        data = self._request("GET", f"/users/{username}/collections", params={
            "page": page,
            "per_page": per_page
        })
        return [Collection.from_dict(item) for item in data]

    def create_collection(self, title: str, description: Optional[str] = None, private: bool = False) -> Collection:
        """Create a new collection"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to create collections")
        
        data = {
            "title": title,
            "description": description,
            "private": private
        }
        response = self._request("POST", "/collections", json=data)
        return Collection.from_dict(response)

    def update_collection(self, collection_id: str, title: Optional[str] = None, 
                         description: Optional[str] = None, private: Optional[bool] = None) -> Collection:
        """Update an existing collection"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to update collections")
            
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if private is not None:
            data["private"] = private
            
        response = self._request("PUT", f"/collections/{collection_id}", json=data)
        return Collection.from_dict(response)

    def delete_collection(self, collection_id: str) -> None:
        """Delete a collection"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to delete collections")
        self._request("DELETE", f"/collections/{collection_id}")

    def add_photo_to_collection(self, collection_id: str, photo_id: str) -> Dict:
        """Add a photo to a collection"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to modify collections")
        return self._request("POST", f"/collections/{collection_id}/add", json={"photo_id": photo_id})

    def remove_photo_from_collection(self, collection_id: str, photo_id: str) -> Dict:
        """Remove a photo from a collection"""
        if not self.bearer_token:
            raise UnsplashAuthError("Authentication required to modify collections")
        return self._request("DELETE", f"/collections/{collection_id}/remove", json={"photo_id": photo_id})
