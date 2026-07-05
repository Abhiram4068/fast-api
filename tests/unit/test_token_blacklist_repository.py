from datetime import datetime, timedelta, timezone

from app.repositories.token_blacklist_repository import TokenBlacklistRepository


def _future(days: int = 1) -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=days)


def _past(days: int = 1) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def test_token_is_not_blacklisted_by_default(db_session):
    repo = TokenBlacklistRepository(db_session)

    assert repo.is_blacklisted("some.jwt.token") is False


def test_blacklist_token_is_then_detected(db_session):
    repo = TokenBlacklistRepository(db_session)
    token = "header.payload.signature"

    repo.blacklist_token(token=token, expires_at=_future())

    assert repo.is_blacklisted(token) is True


def test_different_token_is_not_flagged(db_session):
    repo = TokenBlacklistRepository(db_session)
    repo.blacklist_token(token="token.a", expires_at=_future())

    assert repo.is_blacklisted("token.b") is False


def test_blacklist_prunes_expired_entries(db_session):
    repo = TokenBlacklistRepository(db_session)

    # Insert an already-expired entry directly via session
    from app.models.token_blacklist import TokenBlacklist

    expired_entry = TokenBlacklist(token="expired.token", expires_at=_past())
    db_session.add(expired_entry)
    db_session.commit()

    # Now blacklist a new (valid) token — this triggers lazy pruning
    repo.blacklist_token(token="fresh.token", expires_at=_future())

    # The expired entry should have been deleted
    assert repo.is_blacklisted("expired.token") is False
    # The new entry must still be present
    assert repo.is_blacklisted("fresh.token") is True
