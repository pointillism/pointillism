from pytest import fixture
from point.clients.gitcontent import GitContent
from point.models import User


class TestGitContent:
    @fixture
    def user(self):
        return User(git_token="123")

    def test_init(self, user):
        client = GitContent(user)
        dot = client.get('trevorgrayson', 'pointillism', 'master', '/example.dot')
        assert dot is not None
