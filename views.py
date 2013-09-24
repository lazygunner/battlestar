from flask.ext.mongoengine.wtf import model_form
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from models import Post, Comment
from baidu_pic import getDownloadLink
import markdown2
from flask import Markup
import re

posts = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):

    def get(self):
        posts = Post.objects.filter(show=True)
        return render_template('posts/list.html', posts=posts)

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

    def get_real_link(self, body):
        p = re.compile('!\[.*?\]\((http://pan.*?)\)')
        urls = p.findall(body)
        for url in urls:
            link = getDownloadLink(url)
            if link:
                real_link = link['link']
                n = re.compile(link)
                body = n.sub(real_link, body, 1)
        return body

 
    def get(self, slug):
        context = self.get_context(slug)
        md = markdown2.markdown(context['post'].body)
        md_body = Markup(md)
        
        context['post'].body = self.get_real_link(md_body)
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
        
	

posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
