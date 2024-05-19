from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Song Translation Document Class
# Define the SongTranslation Document class
class SongTranslation(BaseModel):
    song_name: str
    artist_names: str
    is_published: bool
    similarity_score: Optional[float] = None
    error: Optional[str] = None
    target_language: str
    date_created: datetime = datetime.now

    class Settings:
        name = "song_translations"
