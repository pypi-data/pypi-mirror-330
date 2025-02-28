# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class LoadingOverlay(Component):
    """A LoadingOverlay component.
LoadingOverlay

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

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

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- display (boolean | number | string | dict | list; optional)

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

- inset (string | number; optional)

- left (string | number; optional)

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loaderProps (dict; optional):
    Props passed down to `Loader` component.

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

- overlayProps (dict; optional):
    Props passed down to `Overlay` component.

    `overlayProps` is a dict with keys:

    - backgroundOpacity (number; optional):
        Controls overlay `background-color` opacity 0–1, disregarded
        when `gradient` prop is set, `0.6` by default.

    - color (boolean | number | string | dict | list; optional):
        Overlay `background-color`, `#000` by default.

    - blur (string | number; optional):
        Overlay background blur, `0` by default.

    - gradient (string; optional):
        Changes overlay to gradient. If set, `color` prop is ignored.

    - zIndex (string | number; optional):
        Overlay z-index, `200` by default.

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        border-radius, `0` by default.

    - children (a list of or a singular dash component, string or number; optional):
        Content inside overlay.

    - center (boolean; optional):
        Determines whether content inside overlay should be vertically
        and horizontally centered, `False` by default.

    - fixed (boolean; optional):
        Determines whether overlay should have fixed position instead
        of absolute, `False` by default.

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

- top (string | number; optional)

- transitionProps (dict; optional):
    Props passed down to `Transition` component, `{ transition:
    'fade', duration: 0 }` by default.

    `transitionProps` is a dict with keys:

    - keepMounted (boolean; optional):
        If set element will not be unmounted from the DOM when it is
        hidden, `display: none` styles will be applied instead.

    - transition (boolean | number | string | dict | list; optional):
        Transition name or object.

    - duration (number; optional):
        Transition duration in ms, `250` by default.

    - exitDuration (number; optional):
        Exit transition duration in ms, `250` by default.

    - timingFunction (string; optional):
        Transition timing function, `theme.transitionTimingFunction`
        by default.

    - mounted (boolean; required):
        Determines whether component should be mounted to the DOM.

- tt (boolean | number | string | dict | list; optional):
    TextTransform.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (string; optional):
    variant.

- visible (boolean; optional):
    Determines whether the overlay should be visible, `False` by
    default.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing.

- zIndex (string | number; optional):
    Controls overlay `z-index`, `400` by default."""
    _children_props = ['loaderProps.children', 'overlayProps.children']
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'LoadingOverlay'
    TransitionProps = TypedDict(
        "TransitionProps",
            {
            "keepMounted": NotRequired[bool],
            "transition": NotRequired[typing.Any],
            "duration": NotRequired[typing.Union[int, float, numbers.Number]],
            "exitDuration": NotRequired[typing.Union[int, float, numbers.Number]],
            "timingFunction": NotRequired[str],
            "mounted": bool
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

    OverlayProps = TypedDict(
        "OverlayProps",
            {
            "backgroundOpacity": NotRequired[typing.Union[int, float, numbers.Number]],
            "color": NotRequired[typing.Any],
            "blur": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "gradient": NotRequired[str],
            "zIndex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "children": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "center": NotRequired[bool],
            "fixed": NotRequired[bool],
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
        transitionProps: typing.Optional["TransitionProps"] = None,
        loaderProps: typing.Optional["LoaderProps"] = None,
        overlayProps: typing.Optional["OverlayProps"] = None,
        visible: typing.Optional[bool] = None,
        zIndex: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
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
        self._prop_names = ['id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'darkHidden', 'data-*', 'display', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'inset', 'left', 'lh', 'lightHidden', 'loaderProps', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'overlayProps', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'transitionProps', 'tt', 'unstyled', 'variant', 'visible', 'visibleFrom', 'w', 'zIndex']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'darkHidden', 'data-*', 'display', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'inset', 'left', 'lh', 'lightHidden', 'loaderProps', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'overlayProps', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'transitionProps', 'tt', 'unstyled', 'variant', 'visible', 'visibleFrom', 'w', 'zIndex']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LoadingOverlay, self).__init__(**args)
