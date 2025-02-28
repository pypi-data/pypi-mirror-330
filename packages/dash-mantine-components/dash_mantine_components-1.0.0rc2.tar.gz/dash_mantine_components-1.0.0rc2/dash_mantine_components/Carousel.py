# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Carousel(Component):
    """A Carousel component.
Carousel

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    <Carousel.Slide /> components.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- active (number; default 0):
    The index of the current slide. Read only.  Use initialSlide to
    set the current slide.

- align (a value equal to: 'start', 'center', 'end'; optional):
    Determines how slides will be aligned relative to the container.
    `'center'` by default.

- aria-* (string; optional):
    Wild card aria attributes.

- autoScroll (boolean | number | string | dict | list; optional):
    Enables autoScroll with optional configuration.

- autoplay (boolean | number | string | dict | list; optional):
    Enables autoplay with optional configuration.

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

- containScroll (a value equal to: '', 'trimSnaps', 'keepSnaps'; optional):
    Clear leading and trailing empty space that causes excessive
    scrolling. Use `trimSnaps` to only use snap points that trigger
    scrolling or keepSnaps to keep them.

- controlSize (string | number; optional):
    Controls size of the next and previous controls, `26` by default.

- controlsOffset (number; optional):
    Controls position of the next and previous controls, key of
    `theme.spacing` or any valid CSS value, `'sm'` by default.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- display (boolean | number | string | dict | list; optional)

- dragFree (boolean; optional):
    Determines whether momentum scrolling should be enabled, `False`
    by default.

- draggable (boolean; optional):
    Determines whether the carousel can be scrolled with mouse and
    touch interactions, `True` by default.

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

- height (string | number; optional):
    Slides container `height`, required for vertical orientation.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- inViewThreshold (number; optional):
    Choose a fraction representing the percentage portion of a slide
    that needs to be visible in order to be considered in view. For
    example, 0.5 equals 50%.

- includeGapInSize (boolean; optional):
    Determines whether gap between slides should be treated as part of
    the slide size, `True` by default.

- initialSlide (number; default 0):
    Index of initial slide.

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

- loop (boolean; optional):
    Enables infinite looping. `True` by default, automatically falls
    back to `False` if slide content isn't enough to loop.

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

- nextControlIcon (a list of or a singular dash component, string or number; optional):
    Icon of the next control.

- opacity (boolean | number | string | dict | list; optional)

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    Carousel orientation, `'horizontal'` by default.

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

- previousControlIcon (a list of or a singular dash component, string or number; optional):
    Icon of the previous control.

- ps (number; optional):
    PaddingInlineStart, theme key: theme.spacing.

- pt (number; optional):
    PaddingTop, theme key: theme.spacing.

- px (number; optional):
    PaddingInline, theme key: theme.spacing.

- py (number; optional):
    PaddingBlock, theme key: theme.spacing.

- right (string | number; optional)

- skipSnaps (boolean; optional):
    Allow the carousel to skip scroll snaps if it is dragged
    vigorously. Note that this option will be ignored if the dragFree
    option is set to `True`, `False` by default.

- slideGap (number; optional):
    Key of theme.spacing or number to set gap between slides.

- slideSize (string | number; optional):
    Controls slide width based on viewport width, `'100%'` by default.

- slidesToScroll (number; optional):
    Number of slides that will be scrolled with next/previous buttons,
    `1` by default.

- speed (number; optional):
    Adjusts scroll speed when triggered by any of the methods. Higher
    numbers enables faster scrolling.

- style (boolean | number | string | dict | list; optional):
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

- type (a value equal to: 'media', 'container'; optional):
    Determines typeof of queries that are used for responsive styles,
    'media' by default.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing.

- withControls (boolean; optional):
    Determines whether next/previous controls should be displayed,
    True by default.

- withIndicators (boolean; optional):
    Determines whether indicators should be displayed, `False` by
    default.

- withKeyboardEvents (boolean; optional):
    Determines whether arrow key should switch slides, `True` by
    default."""
    _children_props = ['nextControlIcon', 'previousControlIcon']
    _base_nodes = ['nextControlIcon', 'previousControlIcon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'Carousel'
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
        active: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        controlSize: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        controlsOffset: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        slideSize: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        slideGap: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        orientation: typing.Optional[Literal["horizontal", "vertical"]] = None,
        height: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        align: typing.Optional[Literal["start", "center", "end"]] = None,
        slidesToScroll: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        includeGapInSize: typing.Optional[bool] = None,
        draggable: typing.Optional[bool] = None,
        dragFree: typing.Optional[bool] = None,
        loop: typing.Optional[bool] = None,
        speed: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        initialSlide: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        inViewThreshold: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        withControls: typing.Optional[bool] = None,
        withIndicators: typing.Optional[bool] = None,
        nextControlIcon: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        previousControlIcon: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        skipSnaps: typing.Optional[bool] = None,
        containScroll: typing.Optional[Literal["", "trimSnaps", "keepSnaps"]] = None,
        withKeyboardEvents: typing.Optional[bool] = None,
        autoplay: typing.Optional[typing.Any] = None,
        autoScroll: typing.Optional[typing.Any] = None,
        type: typing.Optional[Literal["media", "container"]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
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
        self._prop_names = ['children', 'id', 'active', 'align', 'aria-*', 'autoScroll', 'autoplay', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'containScroll', 'controlSize', 'controlsOffset', 'darkHidden', 'data-*', 'display', 'dragFree', 'draggable', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'height', 'hiddenFrom', 'inViewThreshold', 'includeGapInSize', 'initialSlide', 'inset', 'left', 'lh', 'lightHidden', 'loading_state', 'loop', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'nextControlIcon', 'opacity', 'orientation', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'previousControlIcon', 'ps', 'pt', 'px', 'py', 'right', 'skipSnaps', 'slideGap', 'slideSize', 'slidesToScroll', 'speed', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'variant', 'visibleFrom', 'w', 'withControls', 'withIndicators', 'withKeyboardEvents']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'active', 'align', 'aria-*', 'autoScroll', 'autoplay', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'containScroll', 'controlSize', 'controlsOffset', 'darkHidden', 'data-*', 'display', 'dragFree', 'draggable', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'height', 'hiddenFrom', 'inViewThreshold', 'includeGapInSize', 'initialSlide', 'inset', 'left', 'lh', 'lightHidden', 'loading_state', 'loop', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'nextControlIcon', 'opacity', 'orientation', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'previousControlIcon', 'ps', 'pt', 'px', 'py', 'right', 'skipSnaps', 'slideGap', 'slideSize', 'slidesToScroll', 'speed', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'variant', 'visibleFrom', 'w', 'withControls', 'withIndicators', 'withKeyboardEvents']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Carousel, self).__init__(children=children, **args)
