# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Alert(Component):
    """An Alert component.
Alert

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- autoContrast (boolean; optional):
    Determines whether text color with filled variant should depend on
    `background-color`. If luminosity of the `color` prop is less than
    `theme.luminosityThreshold`, then `theme.white` will be used for
    text color, otherwise `theme.black`. Overrides
    `theme.autoContrast`.

- bd (string | number; optional):
    Border.

- bg (boolean | number | string | dict | list; optional):
    Background, theme key: theme.colors.

- bga (boolean | number | string | dict | list; optional):
    BackgroundAttachment.

- bgp (string | number; optional):
    BackgroundPosition.

- bgr (boolean | number | string | dict | list; optional):
    BackgroundRepeat.

- bgsz (string | number; optional):
    BackgroundSize.

- bottom (string | number; optional)

- c (boolean | number | string | dict | list; optional):
    Color.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- closeButtonLabel (string; optional):
    Close button `aria-label`.

- color (boolean | number | string | dict | list; optional):
    Key of `theme.colors` or any valid CSS color, default value is
    `theme.primaryColor`.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- display (boolean | number | string | dict | list; optional)

- duration (number; optional):
    Duration in milliseconds after which the Alert dismisses itself.

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- flex (string | number; optional)

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- hide (boolean; default False):
    Whether to hide the alert.

- icon (a list of or a singular dash component, string or number; optional):
    Icon displayed next to the title.

- inset (string | number; optional)

- left (string | number; optional)

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

    - component_name (string; required):
        Holds the name of the component that is loading.

- lts (string | number; optional):
    LetterSpacing.

- m (number; optional):
    Margin, theme key: theme.spacing.

- mah (string | number; optional):
    MaxHeight, theme key: theme.spacing.

- maw (string | number; optional):
    MaxWidth, theme key: theme.spacing.

- mb (number; optional):
    MarginBottom, theme key: theme.spacing.

- me (number; optional):
    MarginInlineEnd, theme key: theme.spacing.

- mih (string | number; optional):
    MinHeight, theme key: theme.spacing.

- miw (string | number; optional):
    MinWidth, theme key: theme.spacing.

- ml (number; optional):
    MarginLeft, theme key: theme.spacing.

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- mr (number; optional):
    MarginRight, theme key: theme.spacing.

- ms (number; optional):
    MarginInlineStart, theme key: theme.spacing.

- mt (number; optional):
    MarginTop, theme key: theme.spacing.

- mx (number; optional):
    MarginInline, theme key: theme.spacing.

- my (number; optional):
    MarginBlock, theme key: theme.spacing.

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- pl (number; optional):
    PaddingLeft, theme key: theme.spacing.

- pos (boolean | number | string | dict | list; optional):
    Position.

- pr (number; optional):
    PaddingRight, theme key: theme.spacing.

- ps (number; optional):
    PaddingInlineStart, theme key: theme.spacing.

- pt (number; optional):
    PaddingTop, theme key: theme.spacing.

- px (number; optional):
    PaddingInline, theme key: theme.spacing.

- py (number; optional):
    PaddingBlock, theme key: theme.spacing.

- radius (number; optional):
    Key of `theme.radius` or any valid CSS value to set border-radius,
    `theme.defaultRadius` by default.

- right (string | number; optional)

- style (optional):
    Inline style added to root component element, can subscribe to
    theme defined on MantineProvider.

- styles (boolean | number | string | dict | list; optional):
    Mantine styles API.

- ta (boolean | number | string | dict | list; optional):
    TextAlign.

- tabIndex (number; optional):
    tab-index.

- td (string | number; optional):
    TextDecoration.

- title (a list of or a singular dash component, string or number; optional):
    Alert title.

- top (string | number; optional)

- tt (boolean | number | string | dict | list; optional):
    TextTransform.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing.

- withCloseButton (boolean; optional):
    Determines whether close button should be displayed, `False` by
    default."""
    _children_props = ['title', 'icon']
    _base_nodes = ['title', 'icon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Alert'
    LoadingState = TypedDict(
        "LoadingState",
            {
            "is_loading": bool,
            "prop_name": str,
            "component_name": str
        }
    )

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        radius: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        color: typing.Optional[typing.Any] = None,
        title: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        icon: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        withCloseButton: typing.Optional[bool] = None,
        closeButtonLabel: typing.Optional[str] = None,
        autoContrast: typing.Optional[bool] = None,
        duration: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        hide: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Union[typing.Any]] = None,
        hiddenFrom: typing.Optional[typing.Any] = None,
        visibleFrom: typing.Optional[typing.Any] = None,
        lightHidden: typing.Optional[bool] = None,
        darkHidden: typing.Optional[bool] = None,
        mod: typing.Optional[typing.Union[str]] = None,
        m: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        my: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mx: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mt: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mb: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ms: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        me: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ml: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mr: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        p: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        py: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        px: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pt: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pb: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ps: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pe: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pl: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pr: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        bd: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bg: typing.Optional[typing.Any] = None,
        c: typing.Optional[typing.Any] = None,
        opacity: typing.Optional[typing.Any] = None,
        ff: typing.Optional[typing.Any] = None,
        fz: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        fw: typing.Optional[typing.Any] = None,
        lts: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        ta: typing.Optional[typing.Any] = None,
        lh: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        fs: typing.Optional[typing.Any] = None,
        tt: typing.Optional[typing.Any] = None,
        td: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        w: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        miw: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        maw: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        h: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        mih: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        mah: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgsz: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgp: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgr: typing.Optional[typing.Any] = None,
        bga: typing.Optional[typing.Any] = None,
        pos: typing.Optional[typing.Any] = None,
        top: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        left: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bottom: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        right: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        inset: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        display: typing.Optional[typing.Any] = None,
        flex: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        classNames: typing.Optional[dict] = None,
        styles: typing.Optional[typing.Any] = None,
        unstyled: typing.Optional[bool] = None,
        variant: typing.Optional[str] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        tabIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        loading_state: typing.Optional["LoadingState"] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'aria-*', 'autoContrast', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'closeButtonLabel', 'color', 'darkHidden', 'data-*', 'display', 'duration', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hide', 'icon', 'inset', 'left', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'right', 'style', 'styles', 'ta', 'tabIndex', 'td', 'title', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w', 'withCloseButton']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'autoContrast', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'closeButtonLabel', 'color', 'darkHidden', 'data-*', 'display', 'duration', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hide', 'icon', 'inset', 'left', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'right', 'style', 'styles', 'ta', 'tabIndex', 'td', 'title', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w', 'withCloseButton']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Alert, self).__init__(children=children, **args)
