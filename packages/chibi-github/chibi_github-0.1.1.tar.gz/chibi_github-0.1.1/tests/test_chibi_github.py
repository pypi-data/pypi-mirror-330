#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vcr_unittest import VCRTestCase

from chibi_github import Github_api
from chibi_github.chibi_github import Github_api_inner


class Test_chibi_github( VCRTestCase ):
    def setUp( self ):
        super().setUp()

    def test_should_wort( self ):
        api = Github_api()
        api.login()
        self.assertTrue( api )

    def test_me_should_return_user_data( self ):
        api = Github_api()
        api.login()
        result = api.me.get()
        self.assertTrue( result )
        self.assertIsInstance( result.native, dict )

    def test_me_should_return_name_login( self ):
        api = Github_api()
        api.login()
        result = api.me.get()
        self.assertTrue( result )
        self.assertIn( 'name', result.native  )
        self.assertTrue( result.native.name )
        self.assertIn( 'login', result.native )
        self.assertTrue( result.native.login )


class Test_chibi_github_login( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.api = Github_api()
        self.api.login()
        self.assertTrue( self.api )

    def build_message_error_from_github( self, response ):
        message = response.native.get( 'message' )
        errors = response.native.get( 'errors' )
        if errors:
            messages = "\n".join( ( e.message for e in errors ) )
            return (
                f"\n{message}\n"
                f"{messages}\n"
                f"{response.native.documentation_url}"
            )
        return message


class Test_chibi_github_me( Test_chibi_github_login ):
    def test_me_should_return_user_data( self ):
        result = self.api.me.get()
        self.assertTrue( result )
        self.assertIsInstance( result.native, dict )

    def test_me_should_return_name_login( self ):
        result = self.api.me.get()
        self.assertTrue( result )
        self.assertIn( 'name', result.native  )
        self.assertTrue( result.native.name )
        self.assertIn( 'login', result.native )
        self.assertTrue( result.native.login )


class Test_chibi_github_repo( Test_chibi_github_login ):
    def test_should_can_list_repo_of_user( self ):
        result = self.api.me.repos.get()
        self.assertTrue( result )
        self.assertIsInstance( result.native, list )

    def test_all_repos_should_have_name( self ):
        result = self.api.me.repos.get()
        self.assertTrue( result )
        for repo in result.native:
            self.assertIn( 'name', repo )
            self.assertIn( 'clone_url', repo )
            self.assertIn( 'url', repo )

    def test_repo_url_should_be_a_api_inner( self ):
        result = self.api.me.repos.get()
        self.assertTrue( result )
        for repo in result.native:
            self.assertIsInstance( repo.url, Github_api_inner )


class Test_chibi_github_repo_create( Test_chibi_github_login ):
    def test_create_without_data_should_fail( self ):
        result = self.api.me.repos.create()
        self.assertFalse( result )

    def test_create_and_delete_should_work( self ):
        result = self.api.me.repos.create(
            name='__test__chibi_github',
            description=(
                'repositorio de prueba para las pruebas de chibi_github' ),
            private=False,
        )
        self.assertEqual(
            result.status_code, 201,
            self.build_message_error_from_github( result ) )
        self.assertTrue( result.ok )
        self.assertTrue( result )

        repo = result.native
        self.assertIn( 'name', repo )
        self.assertIn( 'clone_url', repo )
        self.assertIn( 'url', repo )
        self.assertIsInstance( repo.url, Github_api_inner )

        result = repo.url.delete()
        self.assertEqual( result.status_code, 204 )
        self.assertTrue( result.ok )
        self.assertTrue( result )
