# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class PinInput(Component):
    """A PinInput component.
PinInput

Keyword arguments:

- id (string; optional):
    Base id used for all inputs. By default, inputs' ids are generated
    randomly.

- aria-* (string; optional):
    Wild card aria attributes.

- ariaLabel (string; optional):
    `aria-label` for the inputs.

- autoFocus (boolean; optional):
    If set, the first input is focused when component is mounted,
    `False` by default.

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

- disabled (boolean; optional):
    If set, `disabled` attribute is added to all inputs.

- display (boolean | number | string | dict | list; optional)

- error (boolean; optional):
    If set, adds error styles and `aria-invalid` attribute to all
    inputs.

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- flex (string | number; optional)

- form (string; optional):
    Hidden input `form` attribute.

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- gap (number; optional):
    Key of `theme.spacing` or any valid CSS value to set `gap` between
    inputs, numbers are converted to rem, `'md'` by default.

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- inputMode (a value equal to: 'none', 'text', 'tel', 'email', 'search', 'url', 'numeric', 'decimal'; optional):
    `inputmode` attribute, inferred from the `type` prop if not
    specified.

- inputType (boolean | number | string | dict | list; optional):
    Inputs `type` attribute, inferred from the `type` prop if not
    specified.

- inset (string | number; optional)

- left (string | number; optional)

- length (number; optional):
    Number of inputs, `4` by default.

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

- manageFocus (boolean; optional):
    Determines whether focus should be moved automatically to the next
    input once filled, `True` by default.

- mask (boolean; optional):
    Changes input type to `\"password\"`, `False` by default.

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

- mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
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

- name (string; optional):
    Hidden input `name` attribute.

- oneTimeCode (boolean; optional):
    Determines whether `autocomplete=\"one-time-code\"` attribute
    should be set on all inputs, `True` by default.

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- persisted_props (list of strings; optional):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; optional):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- pl (number; optional):
    PaddingLeft, theme key: theme.spacing.

- placeholder (string; optional):
    Inputs placeholder, `'○'` by default.

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
    `border-radius`, numbers are converted to rem,
    `theme.defaultRadius` by default.

- readOnly (boolean; optional):
    If set, the user cannot edit the value.

- right (string | number; optional)

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Controls inputs `width` and `height`, `'sm'` by default.

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

- type (boolean | number | string | dict | list; optional):
    Determines which values can be entered, `'alphanumeric'` by
    default.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (string; optional):
    Controlled component value.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'PinInput'
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
        name: typing.Optional[str] = None,
        form: typing.Optional[str] = None,
        gap: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        radius: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        size: typing.Optional[Literal["xs", "sm", "md", "lg", "xl"]] = None,
        autoFocus: typing.Optional[bool] = None,
        value: typing.Optional[str] = None,
        placeholder: typing.Optional[str] = None,
        manageFocus: typing.Optional[bool] = None,
        oneTimeCode: typing.Optional[bool] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        disabled: typing.Optional[bool] = None,
        error: typing.Optional[bool] = None,
        type: typing.Optional[typing.Any] = None,
        mask: typing.Optional[bool] = None,
        length: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        readOnly: typing.Optional[bool] = None,
        inputType: typing.Optional[typing.Any] = None,
        inputMode: typing.Optional[Literal["none", "text", "tel", "email", "search", "url", "numeric", "decimal"]] = None,
        ariaLabel: typing.Optional[str] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Union[typing.Any]] = None,
        hiddenFrom: typing.Optional[typing.Any] = None,
        visibleFrom: typing.Optional[typing.Any] = None,
        lightHidden: typing.Optional[bool] = None,
        darkHidden: typing.Optional[bool] = None,
        mod: typing.Optional[typing.Union[str, typing.Dict[typing.Union[str, float, int], typing.Any]]] = None,
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
        tabIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        loading_state: typing.Optional["LoadingState"] = None,
        persistence: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        persisted_props: typing.Optional[typing.Sequence[str]] = None,
        persistence_type: typing.Optional[Literal["local", "session", "memory"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'aria-*', 'ariaLabel', 'autoFocus', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'darkHidden', 'data-*', 'disabled', 'display', 'error', 'ff', 'flex', 'form', 'fs', 'fw', 'fz', 'gap', 'h', 'hiddenFrom', 'inputMode', 'inputType', 'inset', 'left', 'length', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'manageFocus', 'mask', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'name', 'oneTimeCode', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'right', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'value', 'variant', 'visibleFrom', 'w']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'aria-*', 'ariaLabel', 'autoFocus', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'darkHidden', 'data-*', 'disabled', 'display', 'error', 'ff', 'flex', 'form', 'fs', 'fw', 'fz', 'gap', 'h', 'hiddenFrom', 'inputMode', 'inputType', 'inset', 'left', 'length', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'manageFocus', 'mask', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'name', 'oneTimeCode', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'right', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'value', 'variant', 'visibleFrom', 'w']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PinInput, self).__init__(**args)
