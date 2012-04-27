from simplelayout.types.common.interfaces import IPage
from zope.interface import Interface


class IBook(Interface):
    """Book marker interface.
    """


class IChapter(IPage):
    """Chapter marker interface.
    """


class IHTMLBlock(Interface):
    """HTMLBlock marker interface.
    """

class IRemark(Interface):
    """Remark marker interface.
    """

class IAddRemarkLayer(Interface):
    """ Request layer interface, provided if we select to show remarks in
    the pdf export wizard
    """

class IWithinBookLayer(Interface):
    """Request layer interface, automatically provided by request
    when traversing over book.
    """


class ILaTeXCodeInjectionEnabled(Interface):
    """Enables LaTeX code injection for admins on
    book-objects (chapters, SL-paragraphs).
    """

class ILaTeXInjectionController(Interface):
    """This adapter controlls LaTeX injection and providing methods for
    retrieving the current injection state, such as the current column
    layout.
    """

    def __init__(layout):
        """Adapts an ``ILaTeXLayout``. The current state is stored as
        annotation on the layout.
        """

    def is_twocolumn_layout():
        """Returns ``True`` when the current rendering position is in two
        column layout, otherwise ``False``.
        """

    def use_twocolumns():
        """Switches the current rendering position to two column layout. The
        followed content will be in two columns until it switched back to
        one column mode.
        """

    def use_onecolumn():
        """Switches the current rendering position to one column layout.
        """
