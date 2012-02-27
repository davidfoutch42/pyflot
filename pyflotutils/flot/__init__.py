import time
try:
    import json
except ImportError:
    import simplejson as json

import exception


class Variable(object):
    "Genric Variable Object"

    def contribute_to_class(self, obj, attr_name, data=None):
        if getattr(obj, self._var_name, False):
            raise exception.MultipleAxisException
        setattr(obj, self._var_name, self)
        if data:
            self._set_points(attr_name, data)


class Axis(object):
    ""
    def __repr__(self):
        return self._var_name

    def __str__(self):
        return self._var_name


class XAxis(Axis):
    "X Axis Object"
    _var_name = '_x'


class YAxis(Axis):
    "Y Axis Object"
    _var_name = '_y'


class LinearVariable(Variable):
    "Linear Variable Object. No adjustment its done to the points"
    def __init__(self, points=None, **kwargs):
        if points is not None:
            self.points = points

    def _set_points(self, attr_name, data):
        self.points = [getattr(sample, attr_name) for sample in data]


class TimeVariable(Variable):
    "Time Variable Object. Points content its adjusted"
    def __init__(self, points=None, *kwargs):
        if points is not None:
            self.points = [int(time.mktime(point.timetuple()) * 1000)\
                                                    for point in points]

    def _set_points(self, attr_name, data):
        an = attr_name
        self.points = [int(time.mktime(getattr(s, an).timetuple()) * 1000)\
                                                    for s in data]


class XVariable(XAxis, LinearVariable):
    "Linear Variable on X Axis"


class YVariable(YAxis, LinearVariable):
    "Linear Variable on Y Axis"


class TimeXVariable(XAxis, TimeVariable):
    "Time Variable on X Axis"


class TimeYVariable(YAxis, TimeVariable):
    "Time Variable on Y Axis"


class Series(dict):
    "This class represents the actual flot series"

    _options = ('label',    # meta
                'color',    # meta
                'xaxis',    # 0/1 meta
                'yaxis',    # 0/1 meta
                'clickable',    # 0/1 meta
                'hoverable',    # 0/1 meta
                'shadowSize')   # 0/1 meta

    def __init__(self, data=None, *args, **kwargs):
        """
        """
        if 'data' not in dir(self) and data is not None:
            # if not data is defined in Class def try to get is by args
            self.data = data
        # through class definition
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, attr_name, self.data)
        # through kwargs
        for name, attr in kwargs.iteritems():
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, name)
        self['data'] = zip(self._x.points, self._y.points)
        # set series options
        for option in dir(self.Meta):
            if option in self._options:
                self[option] = getattr(self.Meta, option)
        super(Series, self).__init__()

    @property
    def json_series(self):
        "serializes a Series object"
        return json.dumps(self)

    class Meta:
        pass


class Graph(object):
    "Contains the data object and also the plot options"

    _series = []
    _options = {
        'xaxis' : {},
        'yaxis' : {},
    }

    def __init__(self, **kwargs):
        ""
        self._series = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Series):
                self._series.append(attr)
        for arg in kwargs.values():
            if isinstance(arg, Series):
                self._series.append(arg)

        self._set_options()


    def _get_axis_mode(self, axis):
        "will get the axis mode for the current series"
        if all([isinstance(getattr(s, axis), TimeVariable) for s in self._series]):
            return 'time'
        return 'null'

    def _set_options(self):
        "sets the graph ploting options"
        self._options = {
            'xaxis' : {'mode' : self._get_axis_mode(XAxis._var_name)},
            'yaxis' : {'mode' : self._get_axis_mode(YAxis._var_name)},
        }

    @property
    def json_data(self):
        "returns its json data serialized"
        return json.dumps(self._series)

    @property
    def options(self):
        ""
        return json.dumps(self._options)

    class Meta:
        pass
