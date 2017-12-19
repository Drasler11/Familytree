#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users


from models import Member


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))




class MainHandler(BaseHandler):
     def get(self):
         return self.render_template("intro.html")

class SignInHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            signed_in = True
            logout_url = users.create_logout_url("/")
            params = {"signed_in": signed_in, "logout_url": logout_url, "user": user}

        else:
            signed_in = False
            login_url = users.create_login_url("/")

            params = {"signed_in": signed_in, "login_url": login_url, "user": user}

        return self.render_template("user_sign_in.html", params=params)


class AddNewHandler(BaseHandler):

    def get(self):
        return self.render_template("add_new.html")


class AddedNewHandler(BaseHandler):
    def post(self):
        added_member = self.request.get("full_name")
        return self.write("/added_member")


class MembersListHandler(BaseHandler):
    def get(self):
        return self.render_template("members_list.html")


class IndividualsHandler(BaseHandler):
    def get(self, member_id):
            member = Member.get_by_id(int(member_id))

            params = {"member": member}

            return self.render_template("individual_member.html", params=params)


class EditMemberHandler(BaseHandler):
    def get(self, member_id):
        member = Member.get_by_id(int(member_id))

        params = {"member": member}

        return self.render_template("edit_member.html", params=params)

    def post(self, member_id):
        member = Member.get_by_id(int(member_id))

        new_input = self.request.get("input")

        member.input = new_input
        member.put()

        return self.redirect_to("members_list")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/user_sign_in', SignInHandler),
    webapp2.Route('/add_new', AddNewHandler),
    webapp2.Route('/added_member', AddedNewHandler),
    webapp2.Route('/members_list', MembersListHandler),
    webapp2.Route('/individual_member', IndividualsHandler),
    webapp2.Route('/member/<member_id:\d+>/edit', EditMemberHandler)
], debug=True)
