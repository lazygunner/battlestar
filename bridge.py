#coding=utf-8
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from auth import requires_auth
from models import Post, Comment

bridge = Blueprint('bridge', __name__, template_folder='templates')

class List(MethodView):
    decorators = [requires_auth]
    cls = Post

    def get(self):
        posts = self.cls.objects.all()
        return render_template('bridge/list.html', posts=posts)

class Detail(MethodView):
    decorateors = [requires_auth]

    def get_context(self, slug=None):
        form_cls = model_form(Post, exclude=('created_at', 'comments', 'show'))

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)

        else:
            post = Post()
            form = form_cls(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('bridge/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.save()

            return redirect(url_for('bridge.index'))
        return render_template('bridge/detail.html', **context)



class Display(MethodView):
    #decorateors = [requires_auth]
              
	def get(self, slug):
		post = Post.objects.get_or_404(slug=slug)

		context = {
            "post": post,
            "create": slug is None
        }
		if post:
			post.show = not post.show
			post.save()
			return redirect(url_for('bridge.index'))
		else:
			render_template('bridge/detail.html', **context)
		


bridge.add_url_rule('/bridge/', view_func=List.as_view('index'))
bridge.add_url_rule('/bridge/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
bridge.add_url_rule('/bridge/<slug>/', view_func=Detail.as_view('edit'))
bridge.add_url_rule('/bridge/display/<slug>/', view_func=Display.as_view('display'))
