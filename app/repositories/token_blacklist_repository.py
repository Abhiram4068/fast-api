from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.token_blacklist import TokenBlacklist


class TokenBlacklistRepository:
    def __init__(self, db: Session):
        self.db = db

    def blacklist_token(self, token: str, expires_at: datetime) -> None:
        """
        Persists a token to the blacklist.
        Also prunes all rows whose expires_at is in the past (lazy cleanup)
        so the table never grows unboundedly.
        """
        # Prune expired entries first
        now = datetime.now(timezone.utc)
        self.db.query(TokenBlacklist).filter(TokenBlacklist.expires_at < now).delete()

        entry = TokenBlacklist(token=token, expires_at=expires_at)
        self.db.add(entry)
        self.db.commit()

    def is_blacklisted(self, token: str) -> bool:
        """Returns True if the token has been revoked."""
        return (
            self.db.query(TokenBlacklist)
            .filter(TokenBlacklist.token == token)
            .first()
        ) is not None
