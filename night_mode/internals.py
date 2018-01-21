import re
from PyQt5 import QtCore
from abc import abstractmethod, ABCMeta
from inspect import isclass
from types import MethodType

from anki.hooks import wrap
from anki.lang import _
from aqt.utils import showWarning


try:
    from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
    from_utf8 = lambda s: s


def alert(info):
    showWarning(_(info))


class PropertyDescriptor:
    def __init__(self, value=None):
        self.value = value

    def __get__(self, obj, obj_type):
        return self.value(obj)

    def __set__(self, obj, value):
        self.value = value


class css(PropertyDescriptor):
    is_css = True


def abstract_property(func):
    return property(abstractmethod(func))


def snake_case(camel_case):
    return re.sub('(?!^)([A-Z]+)', r'_\1', camel_case).lower()


class AbstractRegisteringType(ABCMeta):

    def __init__(cls, name, bases, attributes):
        super().__init__(name, bases, attributes)

        if not hasattr(cls, 'members'):
            cls.members = set()

        cls.members.add(cls)
        cls.members -= set(bases)


class SnakeNameMixin:

    @property
    def name(self):
        """Nice looking internal identifier."""

        return snake_case(
            self.__class__.__name__
            if hasattr(self, '__class__')
            else self.__name__
        )


class MenuAction(SnakeNameMixin, metaclass=AbstractRegisteringType):

    def __init__(self, app):
        self.app = app

    @abstract_property
    def label(self):
        """Text to be shown on menu entry.

        Use ampersand ('&') to set that the following
        character as a menu shortcut for this action.

        Use double ampersand ('&&') to display '&'.
        """
        pass

    @property
    def checkable(self):
        """Add 'checked' sign to menu item when active"""
        return False

    @property
    def shortcut(self):
        """Global shortcut for this menu action.

        The shortcut should be given as a string, like:
            shortcut = 'Ctrl+n'
        """
        return None

    @abstractmethod
    def action(self):
        """Callback for menu entry clicking/selection"""
        pass

    @property
    def is_checked(self):
        """Should the menu item be checked (assuming that checkable is True)"""
        return bool(self.value)


def singleton_creator(old_creator):
    def one_to_rule_them_all(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = old_creator(cls)
        return cls.instance
    return one_to_rule_them_all


class SingletonMetaclass(AbstractRegisteringType):

    def __init__(cls, name, bases, attributes):
        super().__init__(name, bases, attributes)

        # singleton
        cls.instance = None
        old_creator = cls.__new__
        cls.__new__ = singleton_creator(old_creator)


class RequiringMixin:

    require = set()
    dependencies = {}

    def __init__(self, app):
        for requirement in self.require:
            instance = requirement(app)
            key = instance.name
            self.dependencies[key] = instance

    def __getattr__(self, attr):
        if attr in self.dependencies:
            return self.dependencies[attr]


class Setting(RequiringMixin, SnakeNameMixin, metaclass=SingletonMetaclass):

    def __init__(self, app):
        RequiringMixin.__init__(self, app)
        self.default_value = self.value
        self.app = app

    @abstract_property
    def value(self):
        """Default value of a setting"""
        pass

    def on_load(self):
        """Callback called after loading of initial value"""
        pass

    def on_save(self):
        pass

    def reset(self):
        if hasattr(self, 'default_value'):
            self.value = self.default_value


def decorate_or_call(operator):
    def outer_decorator(method_or_value):
        if callable(method_or_value):
            method = method_or_value

            def decorated(*args, **kwargs):
                return operator(method(*args, **kwargs))
            return decorated
        else:
            return operator(method_or_value)
    return outer_decorator


@decorate_or_call
def style_tag(some_css):
    return '<style>' + some_css + '</style>'


@decorate_or_call
def percent_escaped(text):
    return text.replace('%', '%%')


class StylerMetaclass(AbstractRegisteringType):
    """
    Makes classes: singletons, work with:
        wraps,
        appends_in_night_mode,
        replaces_in_night_mode
    decorators
    """

    def __init__(cls, name, bases, attributes):
        super().__init__(name, bases, attributes)

        # singleton
        cls.instance = None
        old_creator = cls.__new__
        cls.__new__ = singleton_creator(old_creator)

        # additions and replacements
        cls.additions = {}
        cls.replacements = {}

        target = attributes.get('target', None)

        def callback_maker(wrapper):
            def raw_new(*args, **kwargs):
                return wrapper(cls.instance, *args, **kwargs)
            return raw_new

        for key, attr in attributes.items():

            if key == 'init':
                key = '__init__'
            if hasattr(attr, 'wraps'):

                if not target:
                    raise Exception(f'Asked to wrap "{key}" but target of {name} not defined')

                original = getattr(target, key)

                if type(original) is MethodType:
                    original = original.__func__

                new = wrap(original, callback_maker(attr), attr.position)

                # for classes, just add the new function, it will be bound later,
                # but instances need some more work: we need to bind!
                if not isclass(target):
                    new = MethodType(new, target)

                cls.replacements[key] = new

            if hasattr(attr, 'appends_in_night_mode'):
                if not target:
                    raise Exception(f'Asked to replace "{key}" but target of {name} not defined')
                cls.additions[key] = attr
            if hasattr(attr, 'replaces_in_night_mode'):
                if not target:
                    raise Exception(f'Asked to replace "{key}" but target of {name} not defined')
                cls.replacements[key] = attr

            # TODO: invoke and cache css?
            if hasattr(attr, 'is_css'):
                pass


def wraps(method=None, position='after'):
    """Decorator for methods extending Anki QT methods.

    Args:
        method: a function method to be wrapped
        position: after, before or around
    """

    if not method:
        def wraps_inner(func):
            return wraps(method=func, position=position)
        return wraps_inner

    method.wraps = True
    method.position = position

    return method


class appends_in_night_mode(PropertyDescriptor):
    appends_in_night_mode = True


class replaces_in_night_mode(PropertyDescriptor):
    replaces_in_night_mode = True


def move_args_to_kwargs(original_function, args, kwargs):
    args = list(args)

    import inspect

    signature = inspect.signature(original_function)
    i = 0
    for name, parameter in signature.parameters.items():
        if i >= len(args):
            break
        if parameter.default is not inspect._empty:
            value = args.pop(i)
            kwargs[name] = value
        else:
            i += 1
    return args, kwargs
