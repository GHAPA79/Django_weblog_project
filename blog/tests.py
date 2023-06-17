from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post


class BlogPostTest(TestCase):
    @classmethod  # Use Decorator
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')
        cls.post1 = Post.objects.create(
            title='post1',
            text='this is the description.',
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0],
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='this is the description!',
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0]
        )

    def test_post_model_str_title(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'this is the description.')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_posts_list_contents_on_blog_list_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_post_details_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_details_url_by_name(self):
        response = self.client.get(reverse('post_details', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_blog_details_page(self):
        response = self.client.get(reverse('post_details', args=[self.post1.id]))
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_details', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_posts_list_template_is_correct(self):
        response = self.client.get(reverse('posts_list'))
        self.assertTemplateUsed(response, 'blog/posts_list.html')

    def test_post_details_template_is_correct(self):
        response = self.client.get(reverse('post_details', args=[self.post1.id]))
        self.assertTemplateUsed(response, 'blog/post_details.html')

    def test_login_template_is_correct(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, "registration/login.html")

    def test_extends_base_template_use_in_posts_list_blog_html(self):
        response = self.client.get(reverse('posts_list'))
        self.assertTemplateUsed(response, '_base.html')
        self.assertTemplateUsed(response, 'blog/posts_list.html')

    def test_extends_base_template_use_in_post_details_blog_html(self):
        response = self.client.get(reverse('post_details', args=[self.post1.id]))
        self.assertTemplateUsed(response, '_base.html')
        self.assertTemplateUsed(response, 'blog/post_details.html')

    def test_draft_post_not_show_in_posts_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1)
        self.assertNotContains(response, self.post2)

    def test_post_create_view(self):
        response = self.client.post(reverse('create_post'), {
            'title': 'some title',
            'text': 'this post is created',
            'status': 'pub',
            'author': self.post1.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'some title'),
        self.assertEqual(Post.objects.last().text, 'this post is created'),
        self.assertEqual(Post.objects.last().status, 'pub'),
        self.assertEqual(Post.objects.last().author, self.post1.author),

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'post2 updated',
            'text': 'this text is updated',
            'status': 'pub',
            'author': self.post2.author.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post2 updated')
        self.assertEqual(Post.objects.last().text, 'this text is updated')
        self.assertEqual(Post.objects.last().status, 'pub')
        self.assertEqual(Post.objects.last().author, self.post2.author)

    def test_post_delete_view(self):
        response = self.client.post(reverse('delete_post', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)
