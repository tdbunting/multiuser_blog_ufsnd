from app.handlers.base import BlogHandler

class LogoutHandler(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')
