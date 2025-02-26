"""
Data models for Unsplash API responses
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .attribution import Attribution

@dataclass
class Urls:
    raw: str
    full: str
    regular: str
    small: str
    thumb: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'Urls':
        return cls(
            raw=data["raw"],
            full=data["full"],
            regular=data["regular"],
            small=data["small"],
            thumb=data["thumb"]
        )

@dataclass
class User:
    id: str
    username: str
    name: str
    portfolio_url: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    total_collections: int
    total_likes: int
    total_photos: int
    links: Dict

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(
            id=data["id"],
            username=data["username"],
            name=data["name"],
            portfolio_url=data.get("portfolio_url"),
            bio=data.get("bio"),
            location=data.get("location"),
            total_collections=data.get("total_collections", 0),
            total_likes=data.get("total_likes", 0),
            total_photos=data.get("total_photos", 0),
            links=data.get("links", {})
        )

@dataclass
class Photo:
    id: str
    created_at: datetime
    updated_at: datetime
    width: int
    height: int
    color: str
    blur_hash: Optional[str]
    downloads: Optional[int]
    likes: int
    liked_by_user: bool
    description: Optional[str]
    urls: Urls
    user: User

    def __post_init__(self):
        """Initialize the attribution after the dataclass is initialized"""
        self._attribution = Attribution(self)

    @property
    def attribution(self) -> Attribution:
        """Get attribution information for the photo"""
        return self._attribution

    @classmethod
    def from_dict(cls, data: Dict) -> 'Photo':
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")),
            width=data["width"],
            height=data["height"],
            color=data["color"],
            blur_hash=data.get("blur_hash"),
            downloads=data.get("downloads"),
            likes=data["likes"],
            liked_by_user=data["liked_by_user"],
            description=data.get("description"),
            urls=Urls.from_dict(data["urls"]),
            user=User.from_dict(data["user"])
        )

@dataclass
class Collection:
    id: str
    title: str
    description: Optional[str]
    published_at: datetime
    total_photos: int
    private: bool
    cover_photo: Optional[Photo]
    user: User

    @classmethod
    def from_dict(cls, data: Dict) -> 'Collection':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            published_at=datetime.fromisoformat(data["published_at"].replace("Z", "+00:00")),
            total_photos=data["total_photos"],
            private=data["private"],
            cover_photo=Photo.from_dict(data["cover_photo"]) if data.get("cover_photo") else None,
            user=User.from_dict(data["user"])
        )

@dataclass
class Topic:
    id: str
    slug: str
    title: str
    description: Optional[str]
    published_at: datetime
    updated_at: datetime
    total_photos: int
    links: Dict
    status: str
    owners: List[User]
    cover_photo: Optional[Photo]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Topic':
        return cls(
            id=data["id"],
            slug=data["slug"],
            title=data["title"],
            description=data.get("description"),
            published_at=datetime.fromisoformat(data["published_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")),
            total_photos=data["total_photos"],
            links=data["links"],
            status=data["status"],
            owners=[User.from_dict(user) for user in data["owners"]],
            cover_photo=Photo.from_dict(data["cover_photo"]) if data.get("cover_photo") else None
        )
