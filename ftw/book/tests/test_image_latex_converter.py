from Products.ATContentTypes.interfaces.image import IATImage
from ftw.book.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IHTML2LaTeXConverter
from ftw.pdfgenerator.interfaces import ILaTeXLayout
from ftw.testing import MockTestCase
from simplelayout.base.interfaces import IBlockConfig
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class TestImageLaTeXView(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def create_mocks(self, image_layout, title,
                     description, uid):

        # mock is not yet in replay mode, so we use another layout dummy..
        layout_obj = self.create_dummy()
        alsoProvides(layout_obj, ILaTeXLayout)
        converter = getMultiAdapter((object(), object(), layout_obj),
                                    IHTML2LaTeXConverter)

        image = self.create_dummy(size=1)
        context = self.providing_stub([IATImage, IBlockConfig])
        request = self.create_dummy()
        layout = self.providing_mock([ILaTeXLayout])
        builder = self.mocker.mock()

        self.expect(layout.get_builder()).result(builder)
        self.expect(builder.add_file('%s_image.jpg' % uid, image))

        self.expect(layout.get_converter()).result(converter).count(0, None)
        self.expect(layout.use_package('graphicx'))
        self.expect(layout.use_package('wrapfig'))

        self.expect(context.getImage()).result(image).count(1, None)
        self.expect(context.image_layout).result(image_layout)
        self.expect(context.UID()).result(uid)
        self.expect(context.Title()).result(title)
        self.expect(context.description).result(description)

        return context, request, layout, converter

    def test_no_latex_with_no_image(self):
        request = self.create_dummy()
        layout = self.create_dummy()

        context = self.providing_stub([IATImage, IBlockConfig])
        self.expect(context.getImage()).result(object())
        self.expect(context.image_layout).result('no-image')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()
        self.assertEqual(latex, '')

    def test_latex_with_small_layout(self):
        context, request, layout, converter = self.create_mocks(
            'small', 'my title', 'my description', '123')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()

        self.assertEqual(
            latex,
            '\n'.join([
                    r'\begin{wrapfigure}{l}{0.25\textwidth}',
                    r'\begin{center}',
                    r'\includegraphics[width=0.25\textwidth]{123_image}',
                    r'\end{center}',
                    r'\caption{my title: my description}',
                    r'\end{wrapfigure}']))

    def test_latex_with_middle_layout(self):
        context, request, layout, converter = self.create_mocks(
            'middle', 'the title', 'the description', '3434')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()

        self.assertEqual(
            latex,
            '\n'.join([
                    r'\begin{wrapfigure}{l}{0.5\textwidth}',
                    r'\begin{center}',
                    r'\includegraphics[width=0.5\textwidth]{3434_image}',
                    r'\end{center}',
                    r'\caption{the title: the description}',
                    r'\end{wrapfigure}']))

    def test_latex_with_full_layout(self):
        context, request, layout, converter = self.create_mocks(
            'full', 'title', 'description', '12full')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()

        self.assertEqual(
            latex,
            '\n'.join([
                    r'\begin{figure}[htbp]',
                    r'\begin{center}',
                    r'\includegraphics[width=\textwidth]{12full_image}',
                    r'\end{center}',
                    r'\caption{title: description}',
                    r'\end{figure}']))

    def test_latex_with_middle_right_layout(self):
        context, request, layout, converter = self.create_mocks(
            'middle-right', 'title', 'description', '1mr')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()

        self.assertIn(r'\begin{wrapfigure}{r}{0.5\textwidth}', latex)
        self.assertIn(r'\includegraphics[width=0.5\textwidth]{1mr_image}',
                      latex)

    def test_latex_with_middle_small_layout(self):
        context, request, layout, converter = self.create_mocks(
            'small-right', 'title', 'description', '1sr')

        self.replay()

        view = getMultiAdapter((context, request, layout))
        latex = view.render()

        self.assertIn(r'\begin{wrapfigure}{r}{0.25\textwidth}', latex)
        self.assertIn(r'\includegraphics[width=0.25\textwidth]{1sr_image}',
                      latex)
