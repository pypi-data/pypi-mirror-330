import django_filters
import django_filters.widgets

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class RangeSliderWidget(django_filters.widgets.RangeWidget):
    """A Django widget that renders a range slider using noUiSlider.
    This widget extends django_filters.widgets.RangeWidget to create an interactive
    range slider for selecting numeric ranges. It uses the noUiSlider JavaScript library
    for the slider functionality and wNumb for number formatting.
    Attributes:
        template_name (str): Path to the template used to render the slider
        Media (class): Inner class defining required CSS and JavaScript files from CDN
    Example:
        ```python
        class MyFilterSet(django_filters.FilterSet):
            price = django_filters.RangeFilter(widget=RangeSliderWidget(attrs={
                'min': 0,
                'max': 1000,
                'step': 10
            }))
        ```
    The widget supports the following attrs:
        - min: Minimum value for the range (default: 0)
        - max: Maximum value for the range (default: 100)
        - step: Step size for the slider
        - connect: Boolean to connect/disconnect handles
        - tooltips: Enable/disable tooltips
    """

    template_name = "acdh_django_widgets/range_slider_widget.html"

    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.1/nouislider.css",
            )
        }
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.1/nouislider.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/wnumb/1.2.0/wNumb.min.js",
        )

    def render(self, name, value, attrs=None, renderer=None):
        if value[0] is None:
            value = [self.attrs.get("min", 0), self.attrs.get("max", 100)]
        context = {"name": name, "value": value, "attrs": self.attrs}
        rendered = render_to_string(self.template_name, context)
        return mark_safe(rendered)


class DateRangePickerWidget(django_filters.widgets.DateRangeWidget):
    """A custom DateRangeWidget that renders a date range picker using a template.
    This widget extends django_filters.widgets.DateRangeWidget to provide a date range
    picker interface. It uses a custom template for rendering the widget and allows
    setting minimum and maximum date values.
    Attributes:
        template_name (str): Path to the template used for rendering the widget.
    Args:
        name (str): The name of the form field
        value (list): Two-element list containing the start and end dates
        attrs (dict, optional): HTML attributes for the widget
        renderer (object, optional): The template renderer to be used
    Returns:
        str: The rendered HTML for the date range picker widget
    Example:
        >>> widget = DateRangePickerWidget()
        >>> widget.render('daterange', [date(2020,1,1), date(2020,12,31)])
    """

    template_name = "acdh_django_widgets/range_datepicker_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        if value[0] is None:
            value = [self.attrs.get("min", 0), self.attrs.get("max", 100)]
        context = {"name": name, "value": value, "attrs": self.attrs}
        rendered = render_to_string(self.template_name, context)
        return mark_safe(rendered)


class MartinAntonMuellerWidget(django_filters.widgets.RangeWidget):
    """A custom RangeWidget for filtering numeric values.
    This widget extends django_filters.widgets.RangeWidget to provide a one-line
    range input interface, separated with a 'Halbgeviertstrich' ('–') by using a custom template.
    It's designed for numeric range filtering where two input fields (min and max) are displayed in a single line.
    Attributes:
        template_name (str): Path to the custom template used for rendering the widget.
                            Default is "acdh_django_widgets/range_one_line.html"
    Methods:
        render(name, value, attrs=None, renderer=None): Renders the widget using the
            specified template and returns safe HTML markup.
            Args:
                name (str): The name of the form field
                value (Any): The value to be rendered
                attrs (dict, optional): HTML attributes for the widget. Defaults to None.
                renderer (object, optional): Template renderer. Defaults to None.
            Returns:
                SafeString: The rendered HTML markup for the widget
    """

    template_name = "acdh_django_widgets/range_one_line.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = {"name": name, "value": value, "attrs": self.attrs}
        rendered = render_to_string(self.template_name, context)
        return mark_safe(rendered)
