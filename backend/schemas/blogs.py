from pydantic import BaseModel, Field


class BlogCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    excerpt: str | None = None
    content: str | None = None
    image: str | None = None
    category: str | None = Field(default=None, max_length=255)
    author: str | None = Field(default=None, max_length=255)


class BlogUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    excerpt: str | None = None
    content: str | None = None
    image: str | None = None
    category: str | None = Field(default=None, max_length=255)
    author: str | None = Field(default=None, max_length=255)
