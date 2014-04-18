from flask.ext.mongoengine.wtf import model_form
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from models import Post, Comment
import markdown2
from flask import Markup
import re

posts = Blueprint('posts', __name__, template_folder='templates')

class DefaultView(MethodView):

    def get(self):
        return redirect('/page/1')

class ListView(MethodView):

    def get(self, page_id=1):
        #posts = Post.objects.filter(show=True)
        paginated_posts = Post.objects(show=True).paginate(int(page_id), per_page=5)
        return render_template('posts/list.html', posts=paginated_posts)

class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        md = markdown2.markdown(context['post'].body)
        context['post'].body = Markup(md)
        return render_template('posts/detail.html', **context)
    
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')
        
        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))
        return render_template('posts/detail.html', **context)
        
	

posts.add_url_rule('/page/<page_id>', view_func=ListView.as_view('list'))
posts.add_url_rule('/', view_func=DefaultView.as_view('default'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
