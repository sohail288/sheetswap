from unittest import mock, TestCase
from app.controllers.items.controllers import index, create
from app.tests.test_base import AppTest
from flask import url_for
from models import Item

@mock.patch('app.controllers.items.controllers.flash')
@mock.patch('app.controllers.items.controllers.request')
@mock.patch('app.controllers.items.controllers.render_template')
@mock.patch('app.controllers.items.controllers.g')
class ItemControllerUnitTests(TestCase):

    @mock.patch('app.controllers.items.controllers.url_for')
    @mock.patch('app.controllers.items.controllers.redirect')
    @mock.patch('app.controllers.items.controllers.Item')
    @mock.patch('app.controllers.items.controllers.CreateItemForm')
    @mock.patch('app.decorators.g')
    @mock.patch('app.controllers.items.controllers.Sheetmusic')
    def test_create_item__redirects_to_item_page(self,
                                                 Sheetmusic,
                                                 decG,
                                                 Form,
                                                 Item,
                                                 redirect,
                                                 g,
                                                 render_template,
                                                 request,
                                                 url_for,
                                                 flash):
        Form.return_value=Form()
        Sheetmusic.query.filter_by().one = mock.MagicMock(return_value=Sheetmusic())
        decG.user = 'user'
        request.method= mock.PropertyMock(return_value='POST')
        form = Form(request.form)
        form.validate = mock.MagicMock(return_value=True)

        create()
        flash.assert_called_with('You just made a new item!', 'success')
        redirect.assert_called_with('items.index', item_id=2)


    @mock.patch('app.controllers.items.controllers.Item')
    def test_item_index__calls_correct_render_template_arguments(self,
                                                                 Item,
                                                                 g,
                                                                 render_template,
                                                                 request,
                                                                 flash):

        return_item = Item(id=1)
        Item.query.filter_by().one_or_none = mock.MagicMock(return_value=return_item)
        index(1)
        render_template.assert_called_with('items/view_item.html', item=return_item)


    @mock.patch('app.controllers.items.controllers.Item')
    @mock.patch('app.controllers.items.controllers.redirect')
    @mock.patch('app.controllers.items.controllers.url_for')
    def test_item_index_redirects_when_item_is_not_available(self,
                                                            url_for,
                                                            redirect,
                                                            Item,
                                                            g,
                                                            render_template,
                                                            request,
                                                            flash):
        Item.query.filter_by().one_or_none = mock.MagicMock(return_value=None)
        index(1)
        url_for.assert_called_with('main.dashboard')
        flash.assert_called_with('That item does not exist!')

        g.user = None
        index(1)
        url_for.assert_called_with('main.index')
        redirect.assert_called_with(url_for('main.index'))


class ItemControllerContextTests(AppTest):

    def test_get_request_for_an_available_sheetmusic_gives_item_page(self):
        item_to_be_examined = Item.query.filter_by(id=1).one()
        response = self.client.get(url_for('items.index', item_id=1))
        self.assertEqual(response.status_code, 200, 'Make sure the database is seeded')

        self.assertIn(item_to_be_examined.sheetmusic.title, response.get_data(as_text=True))




