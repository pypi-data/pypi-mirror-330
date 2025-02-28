# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class DonutChart(Component):
    """A DonutChart component.
DonutChart

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Additional elements rendered inside `PieChart` component.

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

- chartLabel (string | number; optional):
    Chart label, displayed in the center of the chart.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- clickData (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Click data.

- clickSeriesName (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Name of the series that was clicked.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data (list of dicts; required):
    Data used to render chart.

    `data` is a list of dicts with keys:

    - name (string; required)

    - value (number; required)

    - color (boolean | number | string | dict | list; required)

- data-* (string; optional):
    Wild card data attributes.

- display (boolean | number | string | dict | list; optional)

- endAngle (number; optional):
    Controls angle at which charts ends, `360` by default. Set to `0`
    to render the chart as semicircle.

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

- hoverData (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Hover data.

- hoverSeriesName (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Name of the series that is hovered.

- inset (string | number; optional)

- labelColor (boolean | number | string | dict | list; optional):
    Controls text color of all labels, by default depends on color
    scheme.

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

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- paddingAngle (number; optional):
    Controls padding between segments, `0` by default.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- pieChartProps (dict; optional):
    Props passed down to recharts `PieChart` component.

- pieProps (dict; optional):
    Props passed down to recharts `Pie` component.

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

- size (number; optional):
    Controls chart width and height, height is increased by 40 if
    `withLabels` prop is set. Cannot be less than `thickness`. `80` by
    default.

- startAngle (number; optional):
    Controls angle at which chart starts, `0` by default. Set to `180`
    to render the chart as semicircle.

- strokeColor (boolean | number | string | dict | list; optional):
    Controls color of the segments stroke, by default depends on color
    scheme.

- strokeWidth (number; optional):
    Controls width of segments stroke, `1` by default.

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

- thickness (number; optional):
    Controls thickness of the chart segments, `20` by default.

- tooltipAnimationDuration (number; optional):
    Tooltip animation duration in ms, `0` by default.

- tooltipDataSource (a value equal to: 'segment', 'all'; optional):
    Determines which data is displayed in the tooltip. `'all'` –
    display all values, `'segment'` – display only hovered segment.
    `'all'` by default.

- tooltipProps (dict; optional):
    Props passed down to `Tooltip` recharts component.

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

- withLabels (boolean; optional):
    Determines whether each segment should have associated label,
    `False` by default.

- withLabelsLine (boolean; optional):
    Determines whether segments labels should have lines that connect
    the segment with the label, `True` by default.

- withTooltip (boolean; optional):
    Determines whether the tooltip should be displayed when one of the
    section is hovered, `True` by default."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'DonutChart'
    Data = TypedDict(
        "Data",
            {
            "name": str,
            "value": typing.Union[int, float, numbers.Number],
            "color": typing.Any
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
        data: typing.Optional[typing.Sequence["Data"]] = None,
        withTooltip: typing.Optional[bool] = None,
        tooltipAnimationDuration: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        tooltipProps: typing.Optional[dict] = None,
        pieProps: typing.Optional[dict] = None,
        strokeColor: typing.Optional[typing.Any] = None,
        labelColor: typing.Optional[typing.Any] = None,
        paddingAngle: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        withLabels: typing.Optional[bool] = None,
        withLabelsLine: typing.Optional[bool] = None,
        thickness: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        size: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        strokeWidth: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        startAngle: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        endAngle: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        tooltipDataSource: typing.Optional[Literal["segment", "all"]] = None,
        chartLabel: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        pieChartProps: typing.Optional[dict] = None,
        clickData: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        hoverData: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        clickSeriesName: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        hoverSeriesName: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
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
        id: typing.Optional[typing.Union[str, dict]] = None,
        tabIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        loading_state: typing.Optional["LoadingState"] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'chartLabel', 'className', 'classNames', 'clickData', 'clickSeriesName', 'darkHidden', 'data', 'data-*', 'display', 'endAngle', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hoverData', 'hoverSeriesName', 'inset', 'labelColor', 'left', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'paddingAngle', 'pb', 'pe', 'pieChartProps', 'pieProps', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'size', 'startAngle', 'strokeColor', 'strokeWidth', 'style', 'styles', 'ta', 'tabIndex', 'td', 'thickness', 'tooltipAnimationDuration', 'tooltipDataSource', 'tooltipProps', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w', 'withLabels', 'withLabelsLine', 'withTooltip']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'chartLabel', 'className', 'classNames', 'clickData', 'clickSeriesName', 'darkHidden', 'data', 'data-*', 'display', 'endAngle', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hoverData', 'hoverSeriesName', 'inset', 'labelColor', 'left', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'paddingAngle', 'pb', 'pe', 'pieChartProps', 'pieProps', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'size', 'startAngle', 'strokeColor', 'strokeWidth', 'style', 'styles', 'ta', 'tabIndex', 'td', 'thickness', 'tooltipAnimationDuration', 'tooltipDataSource', 'tooltipProps', 'top', 'tt', 'unstyled', 'variant', 'visibleFrom', 'w', 'withLabels', 'withLabelsLine', 'withTooltip']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DonutChart, self).__init__(children=children, **args)
