"""Flask SQLAlchemy ORM models for Social Auth"""

import web
from social_core.utils import module_member, setting_name
from social_sqlalchemy.storage import (
    BaseSQLAlchemyStorage,
    SQLAlchemyAssociationMixin,
    SQLAlchemyCodeMixin,
    SQLAlchemyNonceMixin,
    SQLAlchemyPartialMixin,
    SQLAlchemyUserMixin,
)
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class SocialBase(DeclarativeBase):
    pass


UID_LENGTH = web.config.get(setting_name("UID_LENGTH"), 255)
User = module_member(web.config[setting_name("USER_MODEL")])


class WebpySocialBase:
    @classmethod
    def _session(cls):
        return web.db_session


class UserSocialAuth(WebpySocialBase, SQLAlchemyUserMixin, SocialBase):
    """Social Auth association model"""

    uid: Mapped[str] = mapped_column(String(UID_LENGTH))
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id), nullable=False, index=True
    )
    user: Mapped["User"] = relationship(User, backref="social_auth")

    @classmethod
    def username_max_length(cls):
        return User.__table__.columns.get("username").type.length

    @classmethod
    def user_model(cls):
        return User


class Nonce(WebpySocialBase, SQLAlchemyNonceMixin, SocialBase):
    """One use numbers"""


class Association(WebpySocialBase, SQLAlchemyAssociationMixin, SocialBase):
    """OpenId account association"""


class Code(WebpySocialBase, SQLAlchemyCodeMixin, SocialBase):
    """Mail validation single one time use code"""


class Partial(WebpySocialBase, SQLAlchemyPartialMixin, SocialBase):
    """Partial pipeline storage"""


class WebpyStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code
    partial = Partial
