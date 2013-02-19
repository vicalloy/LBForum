# -*- coding: UTF-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsBaseCase(TestCase):
    fixtures = ['test_lbforum.json']


class ViewsSimpleTest(ViewsBaseCase):

    def test_index(self):
        resp = self.client.get(reverse('lbforum_index'))
        self.assertEqual(resp.status_code, 200)

    def test_recent(self):
        resp = self.client.get(reverse('lbforum_recent'))
        self.assertEqual(resp.status_code, 200)

    def test_forum(self):
        resp = self.client.get(reverse('lbforum_forum', args=("notexistforum", )))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(reverse('lbforum_forum', args=("forum", )))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('lbforum_forum', args=("forum", "topictype", )))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('lbforum_forum', args=("forum", "topictype", "good")))
        self.assertEqual(resp.status_code, 200)

    def test_topic(self):
        resp = self.client.get(reverse('lbforum_topic', args=(1, )))
        self.assertEqual(resp.status_code, 200)

    def test_lang_js(self):
        resp = self.client.get(reverse('lbforum_lang_js'))
        self.assertEqual(resp.status_code, 200)
