import web
from social_core.actions import do_auth, do_complete, do_disconnect

from .utils import load_strategy, psa

urls = (
    r"/login/(?P<backend>[^/]+)/?",
    "auth",
    r"/complete/(?P<backend>[^/]+)/?",
    "complete",
    r"/disconnect/(?P<backend>[^/]+)/?",
    "disconnect",
    r"/disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/?",
    "disconnect",
)


class BaseViewClass:
    def __init__(self, *args, **kwargs):
        self.session = web.web_session
        method = (web.ctx.method == "POST" and "post") or "get"
        self.strategy = load_strategy()
        self.data = web.input(_method=method)
        self.backend = None
        super().__init__(*args, **kwargs)

    def get_current_user(self):
        if not hasattr(self, "_user"):
            if self.session.get("logged_in"):
                self._user = self.strategy.get_user(  # fmt: skip
                    self.session.get("user_id")
                )
            else:
                self._user = None
        return self._user

    def login_user(self, user):
        self.session["logged_in"] = True
        self.session["user_id"] = user.id


class auth(BaseViewClass):
    def GET(self, backend):
        return self._auth(backend)

    def POST(self, backend):
        return self._auth(backend)

    @psa("/complete/%(backend)s/")
    def _auth(self, backend):
        return do_auth(self.backend)


class complete(BaseViewClass):
    def GET(self, backend, *args, **kwargs):
        return self._complete(backend, *args, **kwargs)

    def POST(self, backend, *args, **kwargs):
        return self._complete(backend, *args, **kwargs)

    @psa("/complete/%(backend)s/")
    def _complete(self, backend, *args, **kwargs):
        return do_complete(
            self.backend,
            login=lambda backend, user, social_user: self.login_user(user),
            user=self.get_current_user(),
            *args,
            **kwargs,
        )


class disconnect(BaseViewClass):
    @psa()
    def POST(self, backend, association_id=None):
        return do_disconnect(  # fmt: skip
            self.backend, self.get_current_user(), association_id
        )


app_social = web.application(urls, locals())
