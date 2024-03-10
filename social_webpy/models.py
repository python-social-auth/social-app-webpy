"""Flask SQLAlchemy ORM models for Social Auth"""
import web

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

from social_core.utils import setting_name, module_member
from social_sqlalchemy.storage import SQLAlchemyUserMixin, \
                                      SQLAlchemyAssociationMixin, \
                                      SQLAlchemyNonceMixin, \
                                      SQLAlchemyCodeMixin, \
                                      SQLAlchemyPartialMixin, \
                                      BaseSQLAlchemyStorage


class SocialBase(DeclarativeBase):
    pass


UID_LENGTH = web.config.get(setting_name('UID_LENGTH'), 255)
User = module_member(web.config[setting_name('USER_MODEL')])


class WebpySocialBase(object):
    @classmethod
    def _session(cls):
        return web.db_session


class UserSocialAuth(WebpySocialBase, SQLAlchemyUserMixin, SocialBase):
    """Social Auth association model"""
    uid: Mapped[str] = mapped_column(String(UID_LENGTH))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id),
                                         nullable=False, index=True)
    user: Mapped["User"] = relationship(User, backref='social_auth')

    @classmethod
    def username_max_length(cls):
        return User.__table__.columns.get('username').type.length

    @classmethod
    def user_model(cls):
        return User


class Nonce(WebpySocialBase, SQLAlchemyNonceMixin, SocialBase):
    """One use numbers"""
    pass


class Association(WebpySocialBase, SQLAlchemyAssociationMixin, SocialBase):
    """OpenId account association"""
    pass


class Code(WebpySocialBase, SQLAlchemyCodeMixin, SocialBase):
    """Mail validation single one time use code"""
    pass


class Partial(WebpySocialBase, SQLAlchemyPartialMixin, SocialBase):
    """Partial pipeline storage"""
    pass


class WebpyStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code
    partial = Partial
