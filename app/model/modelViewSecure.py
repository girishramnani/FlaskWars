from flask.ext.admin.contrib.sqla.view import ModelView
from flask.ext.login import current_user

class SecureView(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.if_admin() :
            return False
        return True
