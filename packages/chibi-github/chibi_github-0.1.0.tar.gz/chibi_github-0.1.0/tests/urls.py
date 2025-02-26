from unittest import TestCase, skip
from chibi_github.urls import base_url, user_repos, repo_pull


@skip( 'old and dead' )
class Test_base_url( TestCase ):
    def setUp( self ):
        super().setUp()
        self.url = base_url

    def test_should_return_200( self ):
        response = self.url.get()
        self.assertEqual( response.status_code, 200 )
        self.assertTrue( response.native )


@skip( 'old and dead' )
class Test_user_repos_url( Test_base_url ):
    def setUp( self ):
        super().setUp()
        self.url = user_repos.format( username='dem4ply' )

    def test_should_return_200( self ):
        response = self.url.get()
        self.assertEqual( response.status_code, 200 )
        self.assertTrue( response.native )


@skip( 'old and dead' )
class Test_repos_pull_url( Test_base_url ):
    def setUp( self ):
        super().setUp()
        self.url = repo_pull.format( username='dem4ply', repo='chibi' )

    def test_should_return_200( self ):
        response = self.url.get()
        self.assertEqual( response.status_code, 200 )
