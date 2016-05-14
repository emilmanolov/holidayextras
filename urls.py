import web
from controllers import user

url_map = web.UrlMap([
    (r'/user/', user.User),
    (r'/user/(?P<user_id>\d+)', user.User),
])
