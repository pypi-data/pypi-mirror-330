# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Button(Component):
    """A Button component.
Button

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Button content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- autoContrast (boolean; optional):
    Determines whether button text color with filled variant should
    depend on `background-color`. If luminosity of the `color` prop is
    less than `theme.luminosityThreshold`, then `theme.white` will be
    used for text color, otherwise `theme.black`. Overrides
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

- color (boolean | number | string | dict | list; optional):
    Key of `theme.colors` or any valid CSS color, `theme.primaryColor`
    by default.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- disabled (boolean; optional):
    Indicates disabled state.

- display (boolean | number | string | dict | list; optional)

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- flex (string | number; optional)

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fullWidth (boolean; optional):
    Determines whether button should take 100% width of its parent
    container, `False` by default.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- gradient (dict; optional):
    Gradient configuration used when `variant=\"gradient\"`, default
    value is `theme.defaultGradient`.

    `gradient` is a dict with keys:

    - from (string; required)

    - to (string; required)

    - deg (number; optional)

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- inset (string | number; optional)

- justify (boolean | number | string | dict | list; optional):
    Sets `justify-content` of `inner` element, can be used to change
    distribution of sections and label, `'center'` by default.

- left (string | number; optional)

- leftSection (a list of or a singular dash component, string or number; optional):
    Content displayed on the left side of the button label.

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loaderProps (dict; optional):
    Props added to the `Loader` component (only visible when `loading`
    prop is set).

    `loaderProps` is a dict with keys:

    - size (number; optional):
        Controls `width` and `height` of the loader. `Loader` has
        predefined `xs`-`xl` values. Numbers are converted to rem.
        Default value is `'md'`.

    - color (boolean | number | string | dict | list; optional):
        Key of `theme.colors` or any valid CSS color, default value is
        `theme.primaryColor`.

    - type (a value equal to: 'bars', 'dots', 'oval'; optional):
        Loader type, key of `loaders` prop, default value is `'oval'`.

    - children (a list of or a singular dash component, string or number; optional):
        Overrides default loader with given content.

    - className (string; optional):
        Class added to the root element, if applicable.

    - style (optional):
        Inline style added to root component element, can subscribe to
        theme defined on MantineProvider.

    - hiddenFrom (boolean | number | string | dict | list; optional):
        Breakpoint above which the component is hidden with `display:
        none`.

    - visibleFrom (boolean | number | string | dict | list; optional):
        Breakpoint below which the component is hidden with `display:
        none`.

    - lightHidden (boolean; optional):
        Determines whether component should be hidden in light color
        scheme with `display: none`.

    - darkHidden (boolean; optional):
        Determines whether component should be hidden in dark color
        scheme with `display: none`.

    - mod (string; optional):
        Element modifiers transformed into `data-` attributes, for
        example, `{ 'data-size': 'xl' }`, falsy values are removed.

    - m (number; optional):
        Margin, theme key: theme.spacing.

    - my (number; optional):
        MarginBlock, theme key: theme.spacing.

    - mx (number; optional):
        MarginInline, theme key: theme.spacing.

    - mt (number; optional):
        MarginTop, theme key: theme.spacing.

    - mb (number; optional):
        MarginBottom, theme key: theme.spacing.

    - ms (number; optional):
        MarginInlineStart, theme key: theme.spacing.

    - me (number; optional):
        MarginInlineEnd, theme key: theme.spacing.

    - ml (number; optional):
        MarginLeft, theme key: theme.spacing.

    - mr (number; optional):
        MarginRight, theme key: theme.spacing.

    - p (number; optional):
        Padding, theme key: theme.spacing.

    - py (number; optional):
        PaddingBlock, theme key: theme.spacing.

    - px (number; optional):
        PaddingInline, theme key: theme.spacing.

    - pt (number; optional):
        PaddingTop, theme key: theme.spacing.

    - pb (number; optional):
        PaddingBottom, theme key: theme.spacing.

    - ps (number; optional):
        PaddingInlineStart, theme key: theme.spacing.

    - pe (number; optional):
        PaddingInlineEnd, theme key: theme.spacing.

    - pl (number; optional):
        PaddingLeft, theme key: theme.spacing.

    - pr (number; optional):
        PaddingRight, theme key: theme.spacing.

    - bd (string | number; optional):
        Border.

    - bg (boolean | number | string | dict | list; optional):
        Background, theme key: theme.colors.

    - c (boolean | number | string | dict | list; optional):
        Color.

    - opacity (boolean | number | string | dict | list; optional)

    - ff (boolean | number | string | dict | list; optional):
        FontFamily.

    - fz (number; optional):
        FontSize, theme key: theme.fontSizes.

    - fw (boolean | number | string | dict | list; optional):
        FontWeight.

    - lts (string | number; optional):
        LetterSpacing.

    - ta (boolean | number | string | dict | list; optional):
        TextAlign.

    - lh (number; optional):
        LineHeight, theme key: lineHeights.

    - fs (boolean | number | string | dict | list; optional):
        FontStyle.

    - tt (boolean | number | string | dict | list; optional):
        TextTransform.

    - td (string | number; optional):
        TextDecoration.

    - w (string | number; optional):
        Width, theme key: theme.spacing.

    - miw (string | number; optional):
        MinWidth, theme key: theme.spacing.

    - maw (string | number; optional):
        MaxWidth, theme key: theme.spacing.

    - h (string | number; optional):
        Height, theme key: theme.spacing.

    - mih (string | number; optional):
        MinHeight, theme key: theme.spacing.

    - mah (string | number; optional):
        MaxHeight, theme key: theme.spacing.

    - bgsz (string | number; optional):
        BackgroundSize.

    - bgp (string | number; optional):
        BackgroundPosition.

    - bgr (boolean | number | string | dict | list; optional):
        BackgroundRepeat.

    - bga (boolean | number | string | dict | list; optional):
        BackgroundAttachment.

    - pos (boolean | number | string | dict | list; optional):
        Position.

    - top (string | number; optional)

    - left (string | number; optional)

    - bottom (string | number; optional)

    - right (string | number; optional)

    - inset (string | number; optional)

    - display (boolean | number | string | dict | list; optional)

    - flex (string | number; optional)

    - classNames (dict; optional):
        Adds class names to Mantine components.

    - styles (boolean | number | string | dict | list; optional):
        Mantine styles API.

    - unstyled (boolean; optional):
        Remove all Mantine styling from the component.

    - variant (string; optional):
        variant.

- loading (boolean; optional):
    Determines whether the `Loader` component should be displayed over
    the button.

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

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

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
    Key of `theme.radius` or any valid CSS value to set
    `border-radius`, `theme.defaultRadius` by default.

- right (string | number; optional)

- rightSection (a list of or a singular dash component, string or number; optional):
    Content displayed on the right side of the button label.

- size (boolean | number | string | dict | list; optional):
    Controls button `height`, `font-size` and horizontal `padding`,
    `'sm'` by default.

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
    Width, theme key: theme.spacing."""
    _children_props = ['leftSection', 'rightSection', 'loaderProps.children']
    _base_nodes = ['leftSection', 'rightSection', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Button'
    Gradient = TypedDict(
        "Gradient",
            {
            "from": str,
            "to": str,
            "deg": NotRequired[typing.Union[int, float, numbers.Number]]
        }
    )

    LoaderProps = TypedDict(
        "LoaderProps",
            {
            "size": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "color": NotRequired[typing.Any],
            "type": NotRequired[Literal["bars", "dots", "oval"]],
            "children": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "className": NotRequired[str],
            "style": NotRequired[typing.Union[typing.Any]],
            "hiddenFrom": NotRequired[typing.Any],
            "visibleFrom": NotRequired[typing.Any],
            "lightHidden": NotRequired[bool],
            "darkHidden": NotRequired[bool],
            "mod": NotRequired[typing.Union[str]],
            "m": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "my": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mx": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ms": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "me": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ml": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "p": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "py": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "px": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ps": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pe": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pl": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "bd": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bg": NotRequired[typing.Any],
            "c": NotRequired[typing.Any],
            "opacity": NotRequired[typing.Any],
            "ff": NotRequired[typing.Any],
            "fz": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fw": NotRequired[typing.Any],
            "lts": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "ta": NotRequired[typing.Any],
            "lh": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fs": NotRequired[typing.Any],
            "tt": NotRequired[typing.Any],
            "td": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "w": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "miw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "maw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "h": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mih": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mah": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgsz": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgp": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgr": NotRequired[typing.Any],
            "bga": NotRequired[typing.Any],
            "pos": NotRequired[typing.Any],
            "top": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "left": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bottom": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "right": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "inset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "display": NotRequired[typing.Any],
            "flex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "classNames": NotRequired[dict],
            "styles": NotRequired[typing.Any],
            "unstyled": NotRequired[bool],
            "variant": NotRequired[str]
        }
    )

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
        size: typing.Optional[typing.Any] = None,
        color: typing.Optional[typing.Any] = None,
        justify: typing.Optional[typing.Any] = None,
        leftSection: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        rightSection: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        fullWidth: typing.Optional[bool] = None,
        radius: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        gradient: typing.Optional["Gradient"] = None,
        disabled: typing.Optional[bool] = None,
        loading: typing.Optional[bool] = None,
        loaderProps: typing.Optional["LoaderProps"] = None,
        autoContrast: typing.Optional[bool] = None,
        n_clicks: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        tabIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        loading_state: typing.Optional["LoadingState"] = None,
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
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'aria-*', 'autoContrast', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'color', 'darkHidden', 'data-*', 'disabled', 'display', 'ff', 'flex', 'fs', 'fullWidth', 'fw', 'fz', 'gradient', 'h', 'hiddenFrom', 'inset', 'justify', 'left', 'leftSection', 'lh', 'lightHidden', 'loaderProps', 'loading', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'n_clicks', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'right', 'rightSection', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'autoContrast', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'color', 'darkHidden', 'data-*', 'disabled', 'display', 'ff', 'flex', 'fs', 'fullWidth', 'fw', 'fz', 'gradient', 'h', 'hiddenFrom', 'inset', 'justify', 'left', 'leftSection', 'lh', 'lightHidden', 'loaderProps', 'loading', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'n_clicks', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'right', 'rightSection', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Button, self).__init__(children=children, **args)
