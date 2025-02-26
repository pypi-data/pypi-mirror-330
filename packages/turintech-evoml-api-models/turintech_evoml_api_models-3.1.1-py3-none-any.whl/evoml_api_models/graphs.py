"""Gathering all models related to graphs. Those models are used by two main
components:
- visualiser:
    creating graphs about datasets and columns
- optimisation components:
    creating graphs about machine learning models and their performance
"""
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import datetime
from typing import List, Tuple, Any, Generic, TypeVar, Optional, Union, Dict
from enum import Enum

# ---------------------------------------------------------------------------- #
# Dependencies
from pydantic.v1 import BaseModel, validator, Field
from pydantic.v1.generics import GenericModel

# ---------------------------------------------------------------------------- #
# Module
from .utils import KeyValuePair, NameWeightPair
from .utils import to_highcharts_matrix
from .utils import AxisMetadata, check_metadata_contains_key

# ──────────────────────────────────────────────────────────────────────────── #
# Info for Fields portion of graph


class FieldOptions(BaseModel):
    """
    If type of GraphField is select, provides information on a signle
    option that can be selected from for that GraphField

    Inputs:
        value (Any):
            Value corresponding to the option
        label (str):
            Label that the user sees for the option
    """

    value: Any
    label: str


class GraphFields(BaseModel):
    """
    Provides information for an optional argument of a Graph

    Inputs:
        name (str):
            Name of the optional argument
        label (str):
            Label which the user sees for the optional argument
        value (Any):
            Original value of the optional argument from the Graph
        type (str):
            Type of optional argument. Can be "select", "boolean" or "number"
        options (Optional[List[FieldOptions]]):
            If type is select, provides possible choices for the optional argument
    """

    name: str
    label: str
    value: Any
    type: str
    options: Optional[List[FieldOptions]]


# ──────────────────────────────────────────────────────────────────────────── #
# Info for Context portion of graph


class ColumnContext(BaseModel):
    """
    Provides context of a column

    Inputs:
        name (str):
            Name of column
        index (int):
            Index of column
    """

    name: str
    index: int


class GraphContext(BaseModel):
    """
    Provides information on the context from which a graph was generated

    Inputs:
        generatedBy (str):
            String corresponding to the function used to generate the Graph
    """

    generatedBy: str

    class Config:
        extra = "allow"


# ──────────────────────────────────────────────────────────────────────────── #
# Library specific graphs, converted using the .converter module
class ConvertedGraph(BaseModel):
    """Graphs converted from the generic Graph model to fit a specific display
    library, indicated by the 'type' field.

    Inputs:
        type (str):
            Type of converted graph
        data (Any):
            Information of converted graph
        description (Optional[str]):
            Description of converted graph
        graphFields (Optional[List[GraphFields]]):
            Contains information needed for optional arguments of the converted graph
        context (Optional[GraphContext]):
            Contains information on the context from which the converted graph was made


    """

    type: str
    data: Any
    description: Optional[str]
    graphFields: Optional[List[GraphFields]]
    context: Optional[GraphContext]


class HighchartsGraph(ConvertedGraph):
    """Converted graph targeting specifically the javascript library Highcharts"""

    @validator("type")
    def is_highcharts(cls, t):
        if t != "highcharts":
            raise ValueError('type must be "highcharts"')
        return t


class DataTableGraph(ConvertedGraph):
    """Converted graph targeting custom css"""

    @validator("type")
    def is_data_table(cls, t):
        if t != "dataTable":
            raise ValueError('type must be "dataTable"')
        return t


# ──────────────────────────────────────────────────────────────────────────── #
# Definition for pairs info from smart pair selection
class AIGraphPairsFeature(BaseModel):
    """
    Contains information on a feature for AI Graph Pairs

    Inputs:
        name (str):
            Name of feature
        columnIndex (int):
            Column index of feature
        detectedType (str):
            Data type of feature
    """

    name: str
    columnIndex: int
    detectedType: str


class AIGraphPairsMetrics(BaseModel):
    """
    Contains information on a metric used for AI Graph Pairs

    Inputs:
        id (str):
            ID of metric
        name (str):
            Name of metric which will be displayed
        description (Optional[str]):
            Description of metric
    """

    id: str
    name: str
    description: Optional[str]


class AIGraphPairsData(BaseModel):
    """
    Contains information on a pairs and its scores from AI Graph Pairs

    Inputs:
        featureOne (AIGraphPairsFeature):
            Information of the first part of the pair
        featureTwo (AIGraphPairsFeature):
            Information of the second part of the pair
        scores (dict):
            A dictionary of scores, with the keys being the metrics being
            measured and the values being the values of that metric
            for the pair in question
    """

    featureOne: AIGraphPairsFeature
    featureTwo: AIGraphPairsFeature
    scores: dict


class AIGraphPairs(BaseModel):
    """
    Contains information needed to produce the AI Graph Pairs.

    Inputs:
        pairs (List[AIGraphPairsData]]):
            Gives information on the pairs and its scores of the AI Graph Pairs
        metrics (List[AIGraphPairsMetrics]):
            Gives information on the metrics used for the AI Graph Pairs
        description (Optional[str]):
            Provides description of the AI Graph Pairs process
    """

    pairs: List[AIGraphPairsData]
    metrics: List[AIGraphPairsMetrics]
    description: Optional[str]


# ──────────────────────────────────────────────────────────────────────────── #
# Info for DataTables


class DataTableColumn(BaseModel):
    """
    Information on a column of a data table

    Inputs:
        name (str):
            Name of column
        id (str):
            ID of column for reference in dataSource section of table
    """

    name: str
    id: str


class DataTable(BaseModel):
    """
    Information needed to make a data table

    Inputs:
        columns (List[DataTableColumn]):
            List of information on the columns of the table
        dataSource (List[dict]):
            List of RowData of the table
            @TODO make model of RowData in dataSource since they have same structure
    """

    columns: List[DataTableColumn]
    dataSource: List[dict] = []


# ──────────────────────────────────────────────────────────────────────────── #
check_metadata_categories = lambda x: check_metadata_contains_key(x, "categories")


# Defining the different graph type enums here.
class GraphType(str, Enum):
    timeseriesLineChart = "timeseriesLineChart"
    acfPlot = "acfPlot"
    barChart = "barChart"
    matrix = "matrix"
    confusionMatrix = "confusionMatrix"
    heatMap = "heatMap"
    histogram = "histogram"
    linePlot = "linePlot"
    linearRegressionPlot = "linearRegressionPlot"
    pieChart = "pieChart"
    parallelPlot = "parallelPlot"
    scatterPlot = "scatterPlot"
    stockPlot = "stockPlot"
    surface3d = "surface3d"
    table = "table"
    dataTable = "dataTable"
    dendogram = "dendogram"
    cornerPlot = "cornerPlot"
    rocCurve = "rocCurve"
    precisionRecallCurve = "precisionRecallCurve"
    wordCloud = "wordCloud"
    boxPlot = "boxPlot"
    violinPlot = "violinPlot"
    boxViolinPlot = "boxViolinPlot"
    correlationPlot = "correlationPlot"
    calendarPlot = "calendarPlot"
    geolocationPlot = "geolocationPlot"
    multiWordCloud = "multiWordCloud"
    multiHistAndLine = "multiHistAndLine"
    columnChart = "columnChart"
    KDE = "KDE"
    Waterfall = "waterfall"
    lineHistogram = "lineHistogram"
    timelineReport = "timelineReport"
    aggregationBarChart = "aggregationBarChart"
    aucCurve = "aucCurve"


class GraphDataType(str, Enum):
    histogram = "histogram"
    bar = "bar"
    column = "column"
    line = "line"
    spline = "spline"
    area = "area"
    areaspline = "areaspline"
    boxplot = "boxplot"
    scatter = "scatter"
    heatmap = "heatmap"
    wordcloud = "wordcloud"
    waterfall = "waterfall"
    timeline = "timeline"
    errorbar = "errorbar"


class SingleColumn(BaseModel):
    """
    Provides model for a single-column Graph

    Inputs:
        title (Optional[str]):
            Title of Graph
        subtitle (Optional[str]):
            Subtitle of Graph
        columnName (Optional[str]):
            Column name of columns used for Graph
        columnIndex (Optional[int]):
            Column index of column used for Graph
        chartSize (Optional[Tuple[Optional[float],Optional[float]]]):
            Provides information on the (height, width) of the Graph

    """

    title: Optional[str]
    subtitle: Optional[str]
    columnName: Optional[str]
    columnIndex: Optional[int]
    chartSize: Optional[Tuple[Optional[float], Optional[float]]]


class MultiColumn(BaseModel):
    """
    Provides model for a multi-column Graph

    Inputs:
        title (Optional[str]):
            Title of Graph
        subtitle (Optional[str]):
            Subtitle of Graph
        columnNames (Optional[List[str]]):
            List of column names of columns used for Graph
        columnIndices (Optional[List[int]]):
            List of column indices of columns used for Graph
        chartSize (Optional[Tuple[Optional[float],Optional[float]]]):
            Provides information on the (height, width) of the Graph

    """

    title: Optional[str]
    subtitle: Optional[str]
    columnNames: Optional[List[str]]
    columnIndices: Optional[List[int]]
    chartSize: Optional[Tuple[Optional[float], Optional[float]]]


class Matrix(BaseModel):
    """
    Model for a matrix of data for Graph. Data given is converted from
    a pure matrix form to a list of [x,y,value] of the matrix.
    (see to_highcharts_matrix)

    Inputs:
        title (Optional[str]):
            Title of Graph
        subtitle (Optional[str]):
            Subtitle of Graph
        data (List[List[float]]):
            Data given in matrix form, the value in the matrix corresponding
            to the value in the list of lists given
        matrixLabel (Optional[str]):
            Label of matrix. Provides information on what kind of matrix is given.
        chartSize (Optional[Tuple[Optional[float],Optional[float]]]):
            Provides information on the (height, width) of the Graph

    """

    # Used to represent a matrix of values
    # Data is a matrix/ list of lists where each sublist represents a row
    title: Optional[str]
    subtitle: Optional[str]
    data: List[List[float]]
    matrixLabel: Optional[str]
    chartSize: Optional[Tuple[Optional[float], Optional[float]]]

    # Convert Matrix to a format that can be used by HighCharts
    # validators
    # _convert_matrix = validator("data", allow_reuse=True)(to_highcharts_matrix)


class MarkerData(SingleColumn):
    """
    Information needed for marker of data

    Inputs:
        radius (Optional[int]):
            Radius of marker
        fillColor (Optional[str]):
            Color of marker
    """

    radius: Optional[int]
    fillColor: Optional[str]


class GenericGraphData(BaseModel):
    """
    Generic model for a series entered into the graph. This will take in
    the name of the series, the type of graph the series takes (e.g. scatter, line),
    and the data within the series. The data is not defined within this model,
    but should be defined in any class that inherits from this class.

    Inputs:
        name (str):
            Name of the series in question.
        type (str):
            Type of the series in question.
        zIndex (Optional[int]):
            Determines the order the series appears in when stacked on each other in the graph
            (index along the z-axis)
    """

    name: str
    type: GraphDataType
    zIndex: Optional[int]


class ScatterPlotData(GenericGraphData):
    """
    Model for a scatter plot series. Takes in all arguments from GenericGraphData,
    but can also be provided with marker information, additionalInfo (for use in tooltips),
    and a tooltip key dictionary. The data provided must be in the form of a list of tuples,
    with each tuple being length 2.

    Inputs:
        data (List[Tuple[Any, Any]]):
            Data needed for the scatter plot.
        marker (Optional[MarkerData]):
            Information on the marker of the scatter plot.
        additionalInfo (Optional[List[dict])):
            Any additional info needed for tooltip/data labels. Must be formatted
            as a list of dictionaries, each dictionary in the list being a key value
            pair of the additional info for the corresponding point.
        tooltipFormat (Optional[str]):
            Tooltip format to use for series.
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given.

    """

    data: List[Tuple[Any, Any]]
    marker: Optional[MarkerData]
    additionalInfo: Optional[List[dict]]
    tooltipFormat: Optional[str]
    tooltipKeyDict: Optional[Dict[str, str]]

    @validator("data")
    def check_len(cls, v):
        for i in v:
            if len(i) != 2:
                raise ValueError("Data point should have x and y values only")
        return v

    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != "scatter":
            raise ValueError(f"Type must be scatter, but type was {v}")
        return v


class LineData(GenericGraphData):
    """
    Model for a line plot series. Takes in all arguments from GenericGraphData,
    but can also be provided with series description, dash style, marker information,
    color, and ability to disable tooltip and legend. The data provided must be in
    the form of a list of tuples, with each tuple being length 2.

    Inputs:
        data (List[Tuple[Any, Any]]):
            Data needed for the line plot.
        seriesDescription (Optional[str]):
            Provides the tooltip for this series. If not given, uses the
            converter default.
        zIndex (Optional[int]):
            Provides the z index of the series
        dashStyle (Optional[str]):
            Dash style of the line. Can be chosen from the following:
                'Solid'
                'ShortDash'
                'ShortDot'
                'ShortDashDot'
                'ShortDashDotDot'
                'Dot'
                'Dash'
                'LongDash'
                'DashDot'
                'LongDashDot'
                'LongDashDotDot'
        marker (Optional[MarkerData]):
            Information on the marker of the line plot.
        disableTooltip (bool):
            Whether or not to disable tooltip of graph. Defaults to False.
        color (Optional[str]):
            Color of the series. Can provide string name of color (eg red), or color hash.
        disableLegend (Optional[bool]):
            Whether or not to disable the sereies from showing up in the legend.
            Defaults to False.
        additionalInfo (Optional[List[dict])):
            Any additional info needed for tooltip/data labels. Must be formatted
            as a list of dictionaries, each dictionary in the list being a key value
            pair of the additional info for the corresponding point.
    """

    data: List[Union[Tuple[Any, Any], List[float]]]
    seriesDescription: Optional[str]
    zIndex: Optional[int]
    dashStyle: Optional[str]
    marker: Optional[MarkerData]
    disableTooltip: bool = False
    tooltip: Optional[Dict]
    color: Optional[str]
    visible: bool = True
    disableLegend: bool = False
    additionalInfo: Optional[List[dict]]

    @validator("data")
    def check_len(cls, v):
        # if len(v) != 2:
        #     raise ValueError('Should provide 2 points for line')
        for i in v:
            if len(i) != 2:
                raise ValueError("Data point should have x and y values only")
        return v

    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v not in ["line", "spline", "area", "areaspline"]:
            raise ValueError(f"Type must be line or spline, but type was {v}")
        return v


class ErrorBarData(GenericGraphData):
    """
    Model for an error bar series. Error bar series MUST be provided with
    an accompanying BarChartData if used. Data must contain a list of lists
    with each list containing the minimum and maximum values of the error bar
    in that order. Each of the lists of min/max values corresponds to a single
    bar in the accompanying BarChartData.

    Inputs:
        Data (List[List[float]]):
            Data containing a list of lists with each list containing the minimum and
            maximum values of the error bar in that order. Each of the lists of min/max
            values corresponds to a single bar in the accompanying BarChartData.
    """

    data: List[List[float]]

    @validator("data")
    def check_len(cls, v):
        for i in v:
            if len(i) != 2:
                raise ValueError("Data point should have min and max values only")
        return v


class BarChartData(GenericGraphData):
    """
    Model for a bar chart series. Takes in all arguments from GenericGraphData,
    but can also be provided with additionalInfo (for use in tooltips),
    and color. The data provided must be in the form of a list of floats,
    with each item in the list being the length of the barchart (can be negative,
    in which case it goes below the axis).

    Inputs:
        data (List[float]):
            Data needed for the bar chart.
        additionalInfo (Optional[List[dict])):
            Any additional info needed for tooltip/data labels. Must be formatted
            as a list of dictionaries, each dictionary in the list being a key value
            pair of the additional info for the corresponding point.
        color (Optional[str]):
            Color for the bar chart. If not given, uses converter default.

    """

    data: List[float]
    additionalInfo: Optional[List[dict]]
    color: Optional[str]


class StackEnum(str, Enum):
    """
    Stacking options for BarChart.
    Null does not stack barchart
    Normal stacks barcharts from different series but on the same label together
    Percent acts as normal but stacks them as a percentage instead
    """

    null = "null"
    normal = "normal"
    percent = "percent"


class BarChart(SingleColumn):
    """
    Information needed for making a barchart.

    Inputs:
        labels (List[str]):
            A list of labels to be used for the bar chart.
        type (str):
            Type of the graph. Can be "bar" or "column".
        stacking (Optional[StackEnum]):
            Stacking method for the barchart. Defaults to "null"
        data (List[BarChartData]):
            A list of bar chart series to be graphed. The length of all the data within
            each of the BarChartData must match the length of the labels.
            e.g. [{'name:'A','data':[1,5,2]},{'name:'B','data'::[3,1,7]}]
            for the labels ['label1','label2','label3'].
        errorBarData (Optional[List[ErrorBarData]]):
            A list of error bar data series to be graphed. The length of errorBarData
            must match the length of data, with each errorBarData corresponding to
            a series in data (based on the order listed).
        dataToPercent (bool):
            Whether or not to convert to percent. Default to False.
            @TODO to be deprecated
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        legendTitle (Optional[str]):
            Title of the legend
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
            @TODO deprecated for now, but should be reenabled
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
            @TODO enabled for now, but should be deprecated
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
    """

    # labels (number of categories)
    labels: List[str]
    type: str = "bar"
    stacking: Optional[StackEnum]
    data: List[BarChartData]
    errorBarData: Optional[List[ErrorBarData]]
    dataToPercent: bool = False
    xAxis: AxisMetadata = None
    yAxis: AxisMetadata = None
    legendTitle: Optional[str]
    tooltipFormat: Optional[str]
    tooltipKeyDict: Optional[Dict[str, str]]
    # Whether to show grid lines
    showGridLines: bool = False
    # Max number of series to show (if given)
    maxVisible: Optional[int]


class ColumnChart(SingleColumn):
    """
    Information needed for making a column chart.

    Inputs:
        labels (List[str]):
            A list of labels to be used for the column chart.
        stacking (Optional[StackEnum]):
            Stacking method for the column chart. Defaults to "null"
        data (List[BarChartData]):
            A list of bar chart series to be graphed. The length of all the data within
            each of the BarChartData must match the length of the labels.
            e.g. [{'name:'A','data':[1,5,2]},{'name:'B','data'::[3,1,7]}]
            for the labels ['label1','label2','label3'].
        errorBarData (Optional[List[ErrorBarData]]):
            A list of error bar data series to be graphed. The length of errorBarData
            must match the length of data, with each errorBarData corresponding to
            a series in data (based on the order listed).
        dataToPercent (bool):
            Whether or not to convert to percent. Default to False.
            @TODO to be deprecated
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        legendTitle (Optional[str]):
            Title of the legend
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
            @TODO deprecated for now, but should be reenabled
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
            @TODO enabled for now, but should be deprecated
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        inverted (bool):
            Whether or not to swap x and y axes. Defaults to false.
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
    """

    # labels (number of categories)
    labels: List[str]
    stacking: Optional[StackEnum]
    data: List[BarChartData]
    xAxis: AxisMetadata = None
    yAxis: AxisMetadata = None
    legendTitle: str = None
    tooltipFormat: str = None
    tooltipKeyDict: Optional[Dict[str, str]]
    # Whether to show grid lines
    showGridLines: bool = False
    # Whether to invert graph to be horizontal instead
    inverted: bool = False
    # Max number of series to show (if given)
    maxVisible: Optional[int]


class ConfusionMatrix(Matrix):
    """
    Information needed for making a confusion matrix. Takes same inputs as Matrix,
    but needs additional info on class labels.

    Inputs:
        classLabels (Union[List[str],List[float]]):
            Labels to use for both the x and y axes of the confusion matrix.


    """

    # Labels to use for both x and y axes could be integers not just str
    classLabels: Union[List[str], List[float]]


class HeatMap(Matrix):
    """
    Information needed for making a heatmap. Takes same inputs as Matrix,
    but needs x/y axes. Can also provide additional metadata for the heatmap.

    Inputs:
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        additionalInfo (Optional[List[dict])):
            Any additional info needed for tooltip/data labels. Must be formatted
            as a list of dictionaries, each dictionary in the list being a key value
            pair of the additional info for the corresponding point.
        dataLabels (bool):
            Decides whether to have the count of the heatmap show in its grid.
            Defaults to false.
        borderWidth (float):
            Width of the border between grids for the heatmap. Defaults to 0.25.
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    xAxis: AxisMetadata

    # Similarly it is the same for the yAxis
    # The categories provided are used for labelling top to bottom in the visualisation
    yAxis: AxisMetadata

    # Heatmap additional info
    additionalInfo: Optional[List[List[dict]]]

    # Heatmap metadata
    # Enabling data labels
    dataLabels: bool = False
    # Checking border width
    borderWidth: float = 0.025
    # Tooltip format
    tooltipFormat: Optional[str]
    # Dictionary for setting the tooltip
    tooltipKeyDict: Optional[Dict[str, str]]

    # validators
    _check_xAxis_for_categories = validator("xAxis", allow_reuse=True)(
        check_metadata_categories
    )
    _check_yAxis_for_categories = validator("yAxis", allow_reuse=True)(
        check_metadata_categories
    )


class CorrelationPlot(Matrix):
    """
    Information needed for making a correlation plot. Takes same inputs as Matrix,
    but needs x/y axes.

    Inputs:
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
    """

    xAxis: AxisMetadata

    # Similarly it is the same for the yAxis
    # The categories provided are used for labelling top to bottom in the visualisation
    yAxis: AxisMetadata

    # validators
    _check_xAxis_for_categories = validator("xAxis", allow_reuse=True)(
        check_metadata_categories
    )
    _check_yAxis_for_categories = validator("yAxis", allow_reuse=True)(
        check_metadata_categories
    )


class HistogramData(GenericGraphData):
    """
    Model for a histogram plot series. Takes in all arguments from GenericGraphData,
    but also needs information on the histogram bins.
    The data provided must be in the form of a list of tuples,
    with each tuple being length 2.

    Inputs:
        data (List[Tuple[Any, Any]]):
            Data needed for the histogram. The first value being the midpoint of the bin
            for a particular bin, the second value being the number of entries in that bin.
        zIndex (Optional[int]):
            If given, provides the ordering of this histogram on the graph in terms of
            layers. This does not affect the order of this histogram in the legend.
        bins (List[float]):
            A list of the bin edges of the histogram
        additionalInfo (Optional[List[dict])):
            Any additional info needed for tooltip/data labels. Must be formatted
            as a list of dictionaries, each dictionary in the list being a key value
            pair of the additional info for the corresponding point.
    """

    data: List[Tuple[Any, Any]]
    zIndex: Optional[int]
    # List of bin edges
    bins: List[float] = Field(..., min_items=2)
    additionalInfo: Optional[List[dict]]

    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != "histogram":
            raise ValueError(f"Type must be histogram, but type was {v}")
        return v


class Histogram(SingleColumn):
    """
    Information needed for making a histogram.

    Inputs:
        data (List[Union[HistogramData,LineData]]):
            Data needed for the histogram. Line data will be for a density plot
            shown with the histogram.
        anomaliesScatter (Optional[ScatterPlotData]):
            If given, has series information on the scatter plot of the anomalies
            of the histogram data.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        legendTitle (Optional[str]):
            Title of the legend
        bins (Optional[List[float]]):
            A list of the bin edges of the histogram
            @TODO no longer optional
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        integerBins (bool):
            Whether to force tooltip bin edges to be integers.

    For more reference consult the js fiddle example https://jsfiddle.net/Bastss/qhpom1ck/
    """

    # List of HistogramData instances for data after removing anomalies
    data: List[Union[HistogramData, LineData]]
    # ScatterPlotData instance for anomalous data, centered around the midpoint of the highest bin
    anomaliesScatter: Optional[List[ScatterPlotData]]
    # store any metadata for x axis here.
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis
    yAxis: AxisMetadata
    # Title of legend
    legendTitle: str = None
    # List of bin edges
    bins: Optional[List[float]]
    # Max visible at start
    maxVisible: Optional[int] = 2
    # Whether to show grid lines
    showGridLines: bool = False
    # Tooltip format
    tooltipFormat: Optional[str]
    # Dictionary for setting the tooltip
    tooltipKeyDict: Optional[Dict[str, str]]
    # Whether to force tooltip bin edges to be integers
    integerBins: bool = False


class LineHistogram(SingleColumn):
    """
    Information needed for making a line histogram (specific graph with both line plots
    and histogram plots, each type taking its own y-axis).

    Inputs:
        histogramData (List[HistogramData]):
            Data needed for the histogram portion of the graph.
        lineData (List[LineData]):
            Data needed for the line portion of the graph.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (List[AxisMetadata]):
            Information on the multiple yAxis of the graph. First one should
            be the y-axis for the line data, second one should be the y-axis
            for the histogram data.
        anomaliesScatter (Optional[ScatterPlotData]):
            If given, has series information on the scatter plot of the anomalies
            of the kde plot data.
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        integerBins (bool):
            Whether to force tooltip bin edges to be integers.

    For more reference consult the js fiddle example https://jsfiddle.net/Bastss/qhpom1ck/
    """

    # List of HistogramData instances for data after removing anomalies
    histogramData: List[HistogramData]
    # List of lineData instances
    lineData: List[LineData]
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis, except need two axis
    # 1st one listed is for lineData, second is for histogramData
    yAxis: List[AxisMetadata]
    # ScatterPlotData instance for anomalous data, centered around the midpoint of the highest bin
    anomaliesScatter: Optional[List[ScatterPlotData]]
    maxVisible: Optional[int]
    # Whether to show grid lines
    showGridLines: bool = False
    # Whether to force tooltip bin edges to be integers
    integerBins: bool = False


class KDE(SingleColumn):
    """
    Information needed for making a kde plot.

    Inputs:
        data (List[HistogramData]):
            Data needed for the kde plot.
        anomaliesScatter (Optional[ScatterPlotData]):
            If given, has series information on the scatter plot of the anomalies
            of the kde plot data.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        legendTitle (Optional[str]):
            Title of the legend
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        shadeArea (Optional[bool])
            Whether or not to shade area under kde. Defaults to false
    """

    # List of HistogramData instances for data after removing anomalies
    data: List[LineData]
    # ScatterPlotData instance for anomalous data, centered around the midpoint of the highest bin
    anomaliesScatter: Optional[List[ScatterPlotData]]
    # store any metadata for x axis here.
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis
    yAxis: AxisMetadata
    legendTitle: str = None
    maxVisible: Optional[int] = 2
    # Whether to show grid lines
    showGridLines: bool = False
    # Tooltip format
    tooltipFormat: Optional[str]
    # Tooltip header format
    tooltipHeaderFormat: Optional[str]
    # Whether or not to use a shared tooltip
    sharedTooltip: bool = False
    # Boolean stating whether to shade area underneath
    shadeArea: bool = False
    # Set plot options (if tooltip is not complete)
    plotOptions: Optional[dict]


class LineType(str, Enum):
    line = "line"
    spline = "spline"
    area = "area"
    areaspline = "areaspline"


class LineGraph(SingleColumn):
    """
    Information needed for making a line graph.

    Inputs:
        data (List[Union[LineData,ScatterPlotData]]):
            Data needed for the line graph.
        labels (Optional[str]):
            If given, provides label information for the x-axis of the graph
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        anomaliesData (Optional[ScatterPlotData]):
            If given, provides the data for anomalies of violin plot as a
            scatter plot on the graph.
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given

    """

    data: List[Union[LineData, ScatterPlotData]]
    labels: Optional[List[str]]  # If given, gives labels to use on the x-axis
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis
    yAxis: AxisMetadata
    maxVisible: Optional[int]
    # Whether to show grid lines
    showGridLines: bool = False
    # Data on anomalies
    anomaliesData: Optional[ScatterPlotData]
    # Tooltip Format
    tooltipFormat: Optional[str]
    # Dictionary for setting the tooltip
    tooltipKeyDict: Optional[Dict[str, str]]
    # Line type to use for graph
    lineType: LineType = LineType.line
    # Set plot options (if provided for more extensive chart creation)
    plotOptions: Optional[dict]


class CalendarOptions(str, Enum):
    single_year = "single_year"
    year_month = "year_month"


class CalendarData(BaseModel):
    date: datetime.datetime
    cat_frequencies: List[int]


class CalendarPlot(MultiColumn):
    """ Information needed to make a calendar plot

    Inputs:
        calendar_type (CalendarOptions):
            An element from CalendarOptions enum determining what kind of
            calendar to plot.
        categories (List[str]):
            A list of categories of the categorical variable.
            Note: the order of categories must be identical to the order of
            value counts within each ColumnData's cat_frequencies list.
        data (List[CalendarData]):
            Data needed for the calendar graph.
            Note: cat_frequencies must be of the same length as categories. If
            a category is not present at a date it must be 0. Order of values
            must match the order of categories.
        years_to_visualise (List[int]):
            List of years to visualise. Automatically sorted through the
            validator.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph.
        yAxis (AxisMetadata):
            Information on the yAxis of the graph.

    """
    calendar_type: CalendarOptions
    categories: List[str]
    data: List[CalendarData]
    years_to_visualise: List[int]
    xAxis: AxisMetadata
    yAxis: AxisMetadata

    @validator("data")
    def categories_and_cat_frequencies_size_match(cls, v, values):
        for data_point in v:
            if len(data_point.cat_frequencies) != len(values["categories"]):
                raise ValueError("Lists lengths don't match, need a frequency count"
                                 " for each category")
        return v

    @validator("years_to_visualise")
    def num_of_years_matches_calendar_type(cls, v, values):
        if values["calendar_type"] == CalendarOptions.single_year and len(v) != 1:
            raise ValueError(f"1 year is required to visualise 'single_year'"
                             f" type calendar, got {len(v)} years")
        if values["calendar_type"] == CalendarOptions.year_month and not 2 <= len(v) <= 15:
            raise ValueError(f"2 to 15 years required to visualise 'year_month'"
                             f" type calendar, got {len(v)} years")
        return v

    @validator("years_to_visualise")
    def sort_years_to_visualise(cls, v):
        # Automatically sort years to visualise
        return sorted(v)


class ACFPlot(SingleColumn):
    """
    Information needed for making an autocorrelation plot.

    Inputs:
        data (List[Union[LineData,ScatterPlotData]]):
            Data needed for the line graph.
        labels (Optional[str]):
            If given, provides label information for the x-axis of the graph
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    # Data of series (combined)
    data: List
    # Labels of graph
    labels: Optional[List[str]]
    # Information about axis
    xAxis: AxisMetadata
    yAxis: AxisMetadata
    # Add plotOptions
    plotOptions: Optional[dict]


class LinearRegressionPlot(SingleColumn):
    """
    CURRENTLY UNUSED
    """

    data: List[Tuple[Any, Any]]  # (x,y)
    plotLabels: Tuple[str, str]  # Labels for the axes of the plot.
    dataLabels: List[str]  # A label for each data point in data
    linearCoefficents: Tuple[float, float]  # Coefficents m and c in y = mx + c


class PieChart(SingleColumn):
    """
    CURRENTLY UNUSED
    """

    labels: List[str]  # Labels for each section of the pie chart
    sizes: List[float]  # fractional size of each label, sum should be 1.


class ScatterPlot(SingleColumn):
    """
    Information needed for making a scatter plot.

    Inputs:
        data (List[Union[ScatterPlotData,LineData]]):
            Data needed for the scatter plot.
        anomaliesData (Optional[ScatterPlotData]):
            If given, has series information on the scatter plot of the anomalies
            of the scatter plot data.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    # List of ScatterPlotData instances or LineData instances
    data: List[Union[ScatterPlotData, LineData]]
    # ScatterPlotData instances for which tuples are marked as anomalous in data
    anomaliesData: Optional[ScatterPlotData]
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis
    yAxis: AxisMetadata
    # Tooltip Format
    tooltipFormat: Optional[str]
    # Dictionary for setting the tooltip
    tooltipKeyDict: Optional[Dict[str, str]]


class MapBubbleData(BaseModel):
    # Highcharts key referencing map's region
    hc_key: str
    # Value set to that region
    z: int


class MapPointData(BaseModel):
    # Latitude - Longitude pair of coordinates
    lat: float
    lon: float


class GeoData(BaseModel):
    map_bubbles: List[MapBubbleData]
    # Optional as we will only visualise this if we have less than 1000 points
    map_points: Optional[List[MapPointData]] = None


class GeoLocationPlot(SingleColumn):
    # Data of MapBubble locations for regions and potentially (if less than
    # 1000 points) MapPoints scatter coordinates
    data: GeoData
    # map selected to be plotted on (link to Highcharts map collections)
    map_link: str
    # Name used for the label
    name_label: str


class StockChart(SingleColumn):
    """
    CURRENTLY UNUSED
    """

    data: List[Tuple[Any, Any]]  # Data (timestamp,value)
    plotLabels: Tuple[str, str]  # Labels for each axes x,y of the plot
    # Index locations for which tuples are marked as anomalous in data
    anomaliesLines: List[int]


class Surface3DPlot(SingleColumn):
    """
    CURRENTLY UNUSED
    """

    data: List[Tuple[Any, Any, Any]]  # Data (x,y,z)
    plotLabels: Tuple[str, str, str]
    # Index locations for which tuples are marked as anomalous in data
    anomaliesLines: List[int]


class Table(SingleColumn):
    """
    CURRENTLY UNUSED
    """

    columnHeaders: List[str]  # Columns for the table
    rowHeaders: Optional[List[str]]  # Optional row headers
    # List of data in each column. Length of data = len(row_headers)
    data: List[List[Any]]
    columnsNames: List[str]
    columnsIndexes: List[int]


class OptimalThresholdData(SingleColumn):
    """
    Information on a point that is on the optimal threshold of an AUC Curve

    Inputs:
        name (str):
            Name of statistic for which this point is optimal
        index (int):
            Index of this optimal point (in list of points for AUC Curve)
        threshold (float):
            Threshold of this point (in an AUC context)
    """

    name: str
    index: int
    threshold: float


class AUCData(GenericGraphData):
    """
    Model for a AUC line series. Takes in all arguments from GenericGraphData,
    but also needs information on the aucScore, thresholds, optimalThresholds,
    and label proportions.
    The data provided must be in the form of a list of tuples,
    with each tuple being length 2.

    Inputs:
        data (List[Tuple[float, float]]):
            Data needed for the AUC Curve.
        aucScore (float):
            AUC Score of the AUC Curve.
        thresholds (List[float]):
            List of positive probability thresholds for each of the points in
            the data for the AUC curve. Must be same length as data.
        optimalThresholds (Optional[List[OptimalThresholdData]]):
            List of points which are optimal thresholds for the AUC curve given.
            Can have more than 1 depending on the metric for which you want to be optimal.
        labelProportion (Optional[float]):
            The proportion of true positives for AUC curve given.

    """

    # Area-Under-Curve score (between 0 and 1)
    aucScore: float

    # Info on the optimal thresholds of the AUC curve
    optimalThresholds: Optional[List[OptimalThresholdData]]

    # Info on the thresholds of the AUC curve
    thresholds: Optional[List[float]]

    # Info on class proportion
    labelProportion: Optional[float]

    # Additional info on AUC data
    additionalInfo: Optional[List[dict]]

    # zipped values of x-axis values (x) to y-axis values (y)
    # In the case of ROC, values of false positive (fp) to true positive (tp)
    # e.g [(fp_1,tp_1),(fp_2,tp_2),...,(fp_n,tp_n)]
    data: List[Tuple[float, float]]


class MultiClassROCCurve(SingleColumn):
    """
    Information needed for making an ROC Curve.

    Inputs:
        data (List[AucData]):
            Data needed for the ROC Curve.
        showBaselines (bool):
            Whether or not to show reference line for ROC Curve. Defaults to True.
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    # ROC Curve with Multiple classes e.g. Random Forest and NN
    data: List[AUCData]
    showBaselines: bool = True
    maxVisible: Optional[int]
    tooltipFormat: Optional[str]
    tooltipKeyDict: Optional[Dict[str, str]]
    # Whether to show grid lines
    showGridLines: bool = False


class MultiClassPrecisionRecallCurve(SingleColumn):
    """
    Information needed for making a Precision-Recall (PR) Curve.

    Inputs:
        data (List[AucData]):
            Data needed for the PR Curve.
        showBaselines (bool):
            Whether or not to show reference line for PR Curve. Defaults to True.
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    # Precision-Recall Curve with Multiple classes e.g. Random Forest and NN
    data: List[AUCData]
    showBaselines: bool = True
    maxVisible: Optional[int]
    tooltipFormat: Optional[str]
    tooltipKeyDict: Optional[Dict[str, str]]
    # Whether to show grid lines
    showGridLines: bool = False


class AUCCurve(SingleColumn):
    """
    Information needed for making an AUC Curve.

    Inputs:
        data (List[AucData]):
            Data needed for the ROC Curve.
        baselines (bool):
            List of baselines to show
        showGridLines (bool):
            Whether or not to show the grid lines of the data. Defaults to False
        maxVisible (Optional[int]):
            If given, only displays up to maxVisible series on the graph to start
            (other series are still able to be shown by clicking on their name in
            the legend)
        tooltipFormat (Optional[str]):
            Formatting of tooltip for each series
        tooltipKeyDict (Optional[Dict[str,str]]):
            A key value dictionary to be converted to a tooltip for the series,
            with the key on the column on the left and the value on the column
            on the right. Only used if tooltipFormat not given
    """

    # AUC Curve with Multiple classes e.g. Random Forest and NN
    data: List[AUCData]
    baselines: Optional[List[LineData]]
    xAxis: AxisMetadata
    yAxis: AxisMetadata
    maxVisible: Optional[int]
    tooltipFormat: Optional[str]
    tooltipKeyDict: Optional[Dict[str, str]]


class WaterfallData(SingleColumn):
    """
    Data needed for a single point on the waterfall plot

    Inputs:
        name (str):
            Name of waterfall point. Will appear in x-axis
        y (Optional[int]):
            The change in the waterfall graph for this pont.
            Should not be given if isIntermediateSum or isSum is True
        isIntermediateSum (bool):
            Whether or not this pont is an intermediate sum. Defaults to False.
        isSum (bool):
            Whether or not this point is a sum. Defaults to False.
        isStart (bool):
            Whether or not this point is a start point. Defaults to False.
    """

    # Data to be used for waterfall graph
    name: str
    y: Optional[int]
    isIntermediateSum: bool = False
    isSum: bool = False
    isStart: bool = False


class WaterfallTooltip(BaseModel):
    """
    Information regarding different parts of the Waterfall graph

    Inputs:
        start (Optional[str]):
            Tooltip for a start point in the Waterfall graph
        increase (Optional[str]):
            Tooltip for an increase in the Waterfall graph
        decrease (Optional[str]):
            Tooltip for a decrease in the Waterfall graph
        unchanged (Optional[str]):
            Tooltip for a change of 0 in the Waterfall graph
        sum (Optional[str]):
            Tooltip for a sum point in the Waterfall graph
        intermediateSum (Optional[str]):
            Tooltip for an intermediate sum point in the Waterfall graph
    """

    start: Optional[str]
    increase: Optional[str]
    decrease: Optional[str]
    unchanged: Optional[str]
    sum: Optional[str]
    intermediateSum: Optional[str]


class Waterfall(SingleColumn):
    """
    Graph Model for Waterfall Plot

    Inputs:
        xAxis (AxisMetaData):
            Information needed for the xAxis
        yAxis (AxisMetaData):
            Information needed for the yAxis
        data (List[WaterfallData]):
            List containing he points of the waterfall plot.
        tooltip (WaterfallTooltip):
            Information regarding the tooltips of various parts of the Waterfall graph
    """

    xAxis: AxisMetadata
    yAxis: AxisMetadata
    data: List[WaterfallData]
    tooltip: Optional[WaterfallTooltip]


class WordCloud(SingleColumn):
    """
    Data needed for word cloud.

    Inputs:
        data (List[NameWeightPair[int]]):
            A list of dictionaries with the name and weight of each word for
            the wordcloud.
    """

    # Data is a list of maps containing names of words and their weight/frequency
    # e.g [{name:'Lorem',weight:4},{name:'Ipsum',weight:1},{name:'fermentum',weight:'2}]
    data: List[NameWeightPair[int]]


class MultiWordCloud(SingleColumn):
    """Currently Unused"""

    # Data is a list of maps containing names of words and their weight/frequency
    # e.g [{name:'Lorem',weight:4},{name:'Ipsum',weight:1},{name:'fermentum',weight:'2}]
    data: List[List[NameWeightPair[int]]]
    labels: List[str]


class DendogramCluster(BaseModel):
    """Currently Unused"""

    # A list of class names in a cluster
    cluster: List[str]


class Dendogram(MultiColumn):
    """Currently Unused"""

    # List of Tuples which are (Cluster A, Cluster B, Distance between Cluster)
    clusterDistances: List[Tuple[DendogramCluster, DendogramCluster, float]]


class CornerPlot(MultiColumn):
    """Currently Unused"""

    # Used to view correlations between numerical samples/data
    # For an example of what a corner plot looks like consult the results
    # section in https://emcee.readthedocs.io/en/latest/tutorials/line/
    dimensions: int
    # As many data sample rows as there are dimensions
    dataSamples: List[List[float]]
    # How many sigma contour levels to plot, e.g. 1, 2 or 3 sigma.
    sigma_contour_levels: int
    # columnNames no longer optional
    columnNames: List[str]


class BoxPlotParams(GenericGraphData):
    """Model for a boxplot plot series. Takes in all arguments from GenericGraphData,
    but also needs other parameters for calculating the boxplot.

    Inputs:
        min (float):
            Minimum of data of boxplot
        max (float):
            Minimum of data of boxplot
        min (float):
            Minimum of data of boxplot
        lower_quartile (float):
            Lower quartile of data of boxplot
        median (float):
            Median of data of boxplot
        upper_quartile (float):
            Upper quartile of data of boxplot
        mean (float):
            Mean of data of boxplot
    """

    # Parameters required to define a box plot
    min: float
    max: float
    lower_quartile: float
    median: float
    upper_quartile: float
    mean: Optional[float]


class BoxPlot(SingleColumn):
    """
    Information needed for making a boxplot.

    Inputs:
        data (List[BoxPlotParams]):
            Data needed for the boxplot
        showMeanScatter (bool):
            Whether to show the means of each boxplot as a point on the boxplot.
        overallMean (Optional[float]):
            If given, provides overall mean of data needed to show it as a
            line on the boxplot
        showMeanLine (bool):
            Whether to show overall mean as a line on the boxplot.
            Defaults to False.
        roundAmount (Optional[int]):
            If given, uses this to round data in the TABLE tooltip (quantiles,
            min, max, median, but NOT the mean dot tooltip). If not provided,
            it is inferred.
        anomaliesData (Optional[ScatterPlotData]):
            If given, provides the data for anomalies of boxplot as a scatter
            plot on the graph.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph
        yAxis (AxisMetadata):
            Information on the yAxis of the graph
        datetime_tooltip (Optional[str]):
            If provided box plot will be generated with axis and tooltips
            adjusted to display data in this specific date-time format.

    """

    # Data is a list of BoxPlotModels
    # Only ever instantiate this with list size 1 if you want a single box plot
    data: List[BoxPlotParams]
    # Whether to show scatterplot of category means
    showMeanScatter: bool = False
    # If given, show overall mean as a line on the boxplot
    overallMean: Optional[float]
    showMeanLine: bool = False
    # If given, uses this to round in the TABLE tooltip (quantiles, not the
    # mean dot tooltip)
    roundAmount: Optional[int]
    # Data on anomalies
    anomaliesData: Optional[ScatterPlotData]
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly it is the same for the yAxis
    yAxis: AxisMetadata
    # If a datetime tooltip is passed then the converter will assume that the
    # numerical data passed is in unix time and will convert axis and tooltips
    # to the format provided.
    datetime_tooltip: Optional[str]


class ViolinPlot(SingleColumn):
    """Information needed for making a violin plot.

    Inputs:
        data (Dict[str, List]):
            Data needed for the violin plot, tooltips, and additional lines.
        showMedianLine (bool):
            Whether to show median, lower and upper quartile lines as a line
            on the violin plot. Defaults to False.
        anomaliesData (Optional[ScatterPlotData]):
            If given, provides the data for anomalies of violin plot as a
            scatter plot on the graph.
        xAxis (AxisMetadata):
            Information on the xAxis of the graph.
        yAxis (AxisMetadata):
            Information on the yAxis of the graph.

    """
    # Data is a dictionary consisting of lists of numeric values:
    data: Dict[str, List]
    # Whether to show the median, lower and upper quartile lines inside the violin plot.
    showMedianLine: bool = False
    # Data on anomalies
    anomaliesData: Optional[ScatterPlotData]
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly, it is the same for the yAxis
    yAxis: AxisMetadata


class BoxViolinPlot(MultiColumn):
    """ Information needed for making a box violin plot.

    Inputs:
        data_violin (Dict[str, List[tuple]]):
            Violin data with corresponding category names.
        data_box (List[BoxPlotParams]):
            Box plot data.
        anomaliesData (Optional[ScatterPlotData]):
            Data of anomalies.
        showMeanScatter (bool):
            Whether to show scatter plot of category mean values.
            Defaults to False.
        xAxis (AxisMetadata):
            Axis metadata, must at least contain "title" field.
        yAxis (AxisMetadata):
            Axis metadata, must at least contain "title" field.
        roundAmount (Optional[float]):
            Round amount determining by how much to round values (for the
            tooltip).

    """
    # Dictionary of lists of violin plots
    # Format is 'category name': list of data
    data_violin: Dict[str, List[tuple]]
    # List of boxplots parameters to plot
    data_box: List[BoxPlotParams]
    # Data on anomalies
    anomaliesData: Optional[ScatterPlotData]
    # Whether to show scatterplot of category means
    showMeanScatter: bool = False
    # Must at minimum contain {title':'title of xAxis'} - default is no title
    xAxis: AxisMetadata
    # Similarly, it is the same for the yAxis
    yAxis: AxisMetadata
    # If given, uses this to round in the tooltip
    roundAmount: Optional[float]


class ParallelPlot(MultiColumn):
    """Currently Unused, will be for global anomalies visualisation"""
    # Format of data is 'row_index': [int value for each column]
    inliers: Dict[int, List[float]]
    outliers: Dict[int, List[float]]
    # Must contain categories field filled with column names
    xAxis: AxisMetadata
    # One AxisMetadata per column
    yAxis: List[AxisMetadata]


class HistAndLine(MultiColumn):
    """Currently Unused"""

    histData: HistogramData
    lineData: List[LineData]
    xAxis: AxisMetadata
    yAxis: AxisMetadata


class TimelineStep(BaseModel):
    """Currently Unused"""

    name: str
    description: str
    duration: Optional[float]
    information: List[str]


class TimelineReport(BaseModel):
    """Currently Unused"""

    name: str
    data: List[TimelineStep]
    duration: Optional[float]


class GraphDescription(BaseModel):
    """
    Information needed for graph description

    Inputs:
        html (str):
            HTML string representation of graph description.
    """

    html: str


# Mapping from GraphType to appropriate model
graph_to_class = {
    GraphType.timeseriesLineChart: LineGraph,
    GraphType.acfPlot: ACFPlot,
    GraphType.barChart: BarChart,
    GraphType.aggregationBarChart: BarChart,
    GraphType.confusionMatrix: ConfusionMatrix,
    GraphType.heatMap: HeatMap,
    GraphType.histogram: Histogram,
    GraphType.linePlot: LineGraph,
    GraphType.linearRegressionPlot: LinearRegressionPlot,
    GraphType.pieChart: PieChart,
    GraphType.scatterPlot: ScatterPlot,
    GraphType.stockPlot: StockChart,
    GraphType.surface3d: Surface3DPlot,
    GraphType.table: Table,
    GraphType.dataTable: DataTable,
    GraphType.dendogram: Dendogram,
    GraphType.wordCloud: WordCloud,
    GraphType.cornerPlot: CornerPlot,
    GraphType.rocCurve: MultiClassROCCurve,
    GraphType.precisionRecallCurve: MultiClassPrecisionRecallCurve,
    GraphType.parallelPlot: ParallelPlot,
    GraphType.aucCurve: AUCCurve,
    GraphType.boxPlot: BoxPlot,
    GraphType.violinPlot: ViolinPlot,
    GraphType.boxViolinPlot: BoxViolinPlot,
    GraphType.correlationPlot: CorrelationPlot,
    GraphType.calendarPlot: CalendarPlot,
    GraphType.geolocationPlot: GeoLocationPlot,
    GraphType.multiWordCloud: MultiWordCloud,
    GraphType.multiHistAndLine: HistAndLine,
    GraphType.columnChart: ColumnChart,
    GraphType.KDE: KDE,
    GraphType.Waterfall: Waterfall,
    GraphType.lineHistogram: LineHistogram,
    GraphType.timelineReport: TimelineReport,
}
# ──────────────────────────────────────────────────────────────────────────── #
GraphT = TypeVar("GraphT", *graph_to_class.values())


class Graph(GenericModel, Generic[GraphT]):
    """Format to package a generic graph with it's type and content separaterly

    Inputs:
        type (GraphType):
            Type of graph (used to find appropriate model from graphs.py)
        graphJson (GraphT):
            Contains the information of the Graph in the form of one of the
            models in graphs.py
        description (Optional[GraphDescription]):
            Contains information of the ddescription of the graph
        graphFields (Optional[List[GraphFields]]):
            Contains information needed for optional arguments of the Graph
        context (Optional[GraphContext]):
            Contains information on the context from which the graph was made

    """

    type: GraphType
    graphJson: GraphT
    description: Optional[GraphDescription]
    graphFields: Optional[List[GraphFields]]
    context: Optional[GraphContext]


# ──────────────────────────────────────────────────────────────────────────── #
__all__ = [
    "ACFPlot",
    "AIGraphPairs",
    "AUCCurve",
    "AUCData",
    "BarChart",
    "BoxPlot",
    "BoxPlotParams",
    "CalendarPlot",
    "ColumnChart",
    "ColumnContext",
    "ConfusionMatrix",
    "ConvertedGraph",
    "CornerPlot",
    "CorrelationPlot",
    "DataTable",
    "DataTableGraph",
    "Dendogram",
    "DendogramCluster",
    "Graph",
    "GraphContext",
    "GraphFields",
    "GraphT",
    "graph_to_class",
    "GraphType",
    "HeatMap",
    "HighchartsGraph",
    "Histogram",
    "HistogramData",
    "KDE",
    "LinearRegressionPlot",
    "LineGraph",
    "LineHistogram",
    "MarkerData",
    "Matrix",
    "GeoLocationPlot",
    "MultiClassPrecisionRecallCurve",
    "MultiClassROCCurve",
    "MultiColumn",
    "MultiColumn",
    "MultiWordCloud",
    "PieChart",
    "ParallelPlot",
    "ScatterPlot",
    "ScatterPlotData",
    "SingleColumn",
    "StockChart",
    "Surface3DPlot",
    "Table",
    "TimelineReport",
    "TimelineStep",
    "ViolinPlot",
    "BoxViolinPlot",
    "Waterfall",
    "WordCloud",
]
