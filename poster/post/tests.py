
# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory

from post.api import list_create_posts, get_update_delete_post, list_create_comment, get_update_delete_comment, \
    list_create_post_comment, get_update_delete_post_comment
from post.models import Post, Comment


class PostsTest(APITestCase):
    """ Test module for Puppy model """

    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        Post.objects.create(
            title='Prvi post', content='test', owner=self.user)
        Post.objects.create(
            title='Drugi post', content='tt', owner=self.user)

    def test_list_posts(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/')
        response = list_create_posts(request)
        first_post = response.data[0]
        second_post = response.data[1]
        self.assertEquals('Prvi post', first_post['title'])
        self.assertEquals('test', first_post['content'])
        self.assertEquals(1, first_post['owner'])

        self.assertEquals('Drugi post', second_post['title'])

    def test_create_post(self):
        factory = APIRequestFactory()
        request = factory.post('/posts/', {'title': 'Test post', 'content': 'tt'})
        request.user = self.user
        response = list_create_posts(request)
        self.assertEquals(3, response.data['id'])
        self.assertEquals('Test post', response.data['title'])
        self.assertEquals('tt', response.data['content'])
        self.assertEquals(1, response.data['owner'])

        post = Post.objects.get(id=3)
        self.assertEquals('Test post', post.title)
        self.assertEquals('tt', post.content)


class PostsIdTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        Post.objects.create(
            title='Prvi post', content='test', owner=self.user)

    def test_get_post(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/1')
        response = get_update_delete_post(request, 1)
        self.assertEquals('Prvi post', response.data['title'])
        self.assertEquals('test', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_put_post(self):
        factory = APIRequestFactory()
        request = factory.put('/posts/1', {'title': 'Updateani post', 'content': 'test', 'owner': 1})
        response = get_update_delete_post(request, 1)
        self.assertEquals('Updateani post', response.data['title'])
        self.assertEquals('test', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_delete_post(self):
        factory = APIRequestFactory()
        request = factory.delete('/posts/1')
        response = get_update_delete_post(request, 1)
        self.assertEquals(0, len(Post.objects.all()))


class CommentsTest(APITestCase):
    """ Test module for Puppy model """

    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        post = Post.objects.create(
            title='Prvi post', content='test', owner=self.user)
        Comment.objects.create(
            post=post, content='prvi komentar', owner=self.user)
        Comment.objects.create(
            post=post, content='drugi komentar', owner=self.user)

    def test_list_comments(self):
        factory = APIRequestFactory()
        request = factory.get('/comments/')
        response = list_create_comment(request)
        first_comment = response.data[0]
        second_comment = response.data[1]
        self.assertEquals('prvi komentar', first_comment['content'])
        self.assertEquals(1, first_comment['owner'])

        self.assertEquals('drugi komentar', second_comment['content'])

    def test_create_comment(self):
        factory = APIRequestFactory()
        request = factory.post('/comments/', {'post': 1, 'content': 'tt'})
        request.user = self.user
        response = list_create_comment(request)
        self.assertEquals(3, response.data['id'])
        self.assertEquals('tt', response.data['content'])
        self.assertEquals(1, response.data['owner'])

        comment = Comment.objects.get(id=3)
        self.assertEquals('tt', comment.content)


class CommentsIdTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        post = Post.objects.create(
            title='Prvi post', content='test', owner=self.user)
        Comment.objects.create(
            post=post, content='tt', owner=self.user
        )

    def test_get_comment(self):
        factory = APIRequestFactory()
        request = factory.get('/comments/1')
        response = get_update_delete_comment(request, 1)
        self.assertEquals(1, response.data['post'])
        self.assertEquals('tt', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_put_comment(self):
        factory = APIRequestFactory()
        request = factory.put('/comment/1', {'post': 1, 'content': 'test', 'owner': 1})
        response = get_update_delete_comment(request, 1)
        self.assertEquals('test', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_delete_comment(self):
        factory = APIRequestFactory()
        request = factory.delete('/comments/1')
        response = get_update_delete_comment(request, 1)
        self.assertEquals(0, len(Comment.objects.all()))


class PostCommentsTest(APITestCase):
    """ Test module for Puppy model """

    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        post = Post.objects.create(
            title='Prvi post', content='test', owner=self.user)
        Comment.objects.create(
            post=post, content='prvi komentar', owner=self.user)
        Comment.objects.create(
            post=post, content='drugi komentar', owner=self.user)

    def test_list_post_comments(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/1/comments')
        response = list_create_post_comment(request, 1)
        first_comment = response.data[0]
        second_comment = response.data[1]
        self.assertEquals(1, first_comment['post'])
        self.assertEquals('prvi komentar', first_comment['content'])
        self.assertEquals(1, first_comment['owner'])

        self.assertEquals(1, second_comment['post'])
        self.assertEquals('drugi komentar', second_comment['content'])

    def test_create_post_comment(self):
        factory = APIRequestFactory()
        request = factory.post('/posts/1/comments', {'post': 1, 'content': 'tt'})
        request.user = self.user
        response = list_create_post_comment(request, 1)
        self.assertEquals(1, response.data['post'])
        self.assertEquals(3, response.data['id'])
        self.assertEquals('tt', response.data['content'])
        self.assertEquals(1, response.data['owner'])

        comment = Comment.objects.get(id=3)
        self.assertEquals('tt', comment.content)


class PostCommentsIdTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='tin', password='tin')
        post = Post.objects.create(
            title='Prvi post', content='test', owner=self.user)
        Comment.objects.create(
            post=post, content='tt', owner=self.user
        )

    def test_get_post_comment(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/1/comments/1')
        response = get_update_delete_post_comment(request, 1, 1)
        self.assertEquals(1, response.data['post'])
        self.assertEquals('tt', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_put_post_comment(self):
        factory = APIRequestFactory()
        request = factory.put('/posts/1/comment/1', {'post': 1, 'content': 'test', 'owner': 1})
        response = get_update_delete_post_comment(request, 1, 1)
        self.assertEquals('test', response.data['content'])
        self.assertEquals(1, response.data['owner'])

    def test_delete_post_comment(self):
        factory = APIRequestFactory()
        request = factory.delete('posts/1/comments/1')
        response = get_update_delete_post_comment(request, 1, 1)
        self.assertEquals(0, len(Comment.objects.all()))
