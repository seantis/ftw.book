from ftw.book.interfaces import ILaTeXCodeInjectionEnabled
from ftw.book.interfaces import ILaTeXInjectionController
from ftw.book.interfaces import IWithinBookLayer
from ftw.book.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.pdfgenerator.layout.baselayout import BaseLayout
from plone.mocktestcase import MockTestCase
from zope.component import getAdapter
from zope.component import queryAdapter
from zope.interface import directlyProvides
from zope.interface.verify import verifyClass


class TestInjectionAwareConvertObject(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        super(TestInjectionAwareConvertObject, self).setUp()

        context = self.create_dummy()
        request = self.create_dummy()
        directlyProvides(request, IWithinBookLayer)
        builder = self.create_dummy()

        self.layout = BaseLayout(context, request, builder)

    def test_not_injected_without_interface(self):
        obj = self.mocker.mock()
        self.expect(obj.Schema()).count(0)

        self.replay()

        self.assertEqual(self.layout.render_latex_for(obj), '')

    def test_injected_with_interface(self):
        latex_pre_code = 'INJECTED PRE LATEX CODE'
        latex_post_code = 'INJECTED POST LATEX CODE'

        obj_dummy = self.create_dummy()
        directlyProvides(obj_dummy, ILaTeXCodeInjectionEnabled)
        obj = self.mocker.proxy(obj_dummy, spec=None)
        schema = self.mocker.mock()
        self.expect(obj.Schema()).result(schema).count(2)

        self.expect(schema.getField('preLatexCode').get(obj)).result(
            latex_pre_code)
        self.expect(schema.getField('postLatexCode').get(obj)).result(
            latex_post_code)

        self.expect(obj.getPhysicalPath()).result(
            ['', 'myobj']).count(3)  # 3 = pre + post + assertion below

        self.replay()
        latex = self.layout.render_latex_for(obj)

        self.assertIn(latex_pre_code, latex)
        self.assertIn(latex_post_code, latex)
        self.assertIn('/'.join(obj.getPhysicalPath()), latex)

    def test_bad_schemaextender_state(self):
        # sometimes the field can not be retrieved. We do nothing and we
        # don't fail in this case.
        obj_dummy = self.create_dummy()
        directlyProvides(obj_dummy, ILaTeXCodeInjectionEnabled)
        obj = self.mocker.proxy(obj_dummy, spec=None)
        schema = self.mocker.mock()
        self.expect(obj.Schema()).result(schema).count(2)

        # pre latex: field not found
        self.expect(schema.getField('preLatexCode')).result(None)

        # post latex: field value is empty
        self.expect(schema.getField('postLatexCode').get(obj)).result('')

        self.replay()
        latex = self.layout.render_latex_for(obj)

        self.assertEqual(latex.strip(), '')


class TestLaTeXInjectionController(MockTestCase):

    def setUp(self):
        super(TestLaTeXInjectionController, self).setUp()

        context = self.create_dummy()
        request = self.create_dummy()
        directlyProvides(request, IWithinBookLayer)
        builder = self.create_dummy()

        self.layout = BaseLayout(context, request, builder)

    def test_component_is_registered(self):
        self.replay()
        component = queryAdapter(self.layout, ILaTeXInjectionController)

        self.assertNotEquals(component, None)
        verifyClass(ILaTeXInjectionController, type(component))

    def test_columns_defaults_to_onecolumn(self):
        self.replay()
        controller = getAdapter(self.layout, ILaTeXInjectionController)
        self.assertFalse(controller.is_twocolumn_layout())

    def test_columns_layout_switching_is_persistent(self):
        self.replay()

        controller = getAdapter(self.layout, ILaTeXInjectionController)
        self.assertFalse(controller.is_twocolumn_layout())
        controller.use_twocolumns()
        self.assertTrue(controller.is_twocolumn_layout())

        controller = getAdapter(self.layout, ILaTeXInjectionController)
        self.assertTrue(controller.is_twocolumn_layout())
        controller.use_onecolumn()
        self.assertFalse(controller.is_twocolumn_layout())
