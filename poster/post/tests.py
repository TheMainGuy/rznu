
# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory

from post.api import list_create_posts, get_update_delete_post
from post.models import Post


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

