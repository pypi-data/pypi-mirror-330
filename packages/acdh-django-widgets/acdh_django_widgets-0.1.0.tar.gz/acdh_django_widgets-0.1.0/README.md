# acdh-django-widgets
acdh-django-widgets is a [Django](https://www.djangoproject.com/) app providing a collection of custom widgets for Django-Forms/Filter

## Installation/Usage

Install the package e.g. 
```bash
pip install acdh-django-widgets
```

add `acdh-django-widgets` to your
[INSTALLED_APPS](https://docs.djangoproject.com/en/stable/ref/settings/#std-setting-INSTALLED_APPS)

```python
INSTALLED_APPS = [
    ...
    "acdh-django-widgets",
    ...
]
```

## Widgets

### MartinAntonMuellerWidget

This widget extends `django_filters.widgets.RangeWidget` to provide a one-line
range input interface, separated with a 'Halbgeviertstrich' ('–'). It's designed for numeric range filtering where two input fields (min and max) are displayed in a single line.
It is named after @martinantonmueller because he likes the 'Halbgeviertstrich' ('–').
```python

from acdh_django_widgets.widgets import MartinAntonMuellerWidget

class MyCustomFilter(FilterSet):
    
    start_date__year = RangeFilter(
        label=" Zeitraum: Anfang – Ende (z. B. 1862–1931)",
        widget=MartinAntonMuellerWidget
    )
    
```
### DateRangePickerWidget

A custom DateRangeWidget that renders a date range picker using a template.
This widget extends `django_filters.widgets.DateRangeWidget` to provide a date range
picker interface. It uses a custom template for rendering the widget and allows
setting minimum and maximum date values.

```python
from acdh_django_widgets.widgets import DateRangePickerWidget

class MyCustomFilter(FilterSet):
    decission_date = django_filters.DateFromToRangeFilter(
        help_text=CourtDecission._meta.get_field("decission_date").help_text,
        label=CourtDecission._meta.get_field("decission_date").verbose_name,
        widget=DateRangePickerWidget
    )
```

### RangeSliderWidget
A Django widget that renders a range slider using [noUiSlider](https://refreshless.com/nouislider/).
This widget extends django_filters.widgets.RangeWidget to create an interactive
range slider for selecting numeric ranges. It uses the [noUiSlider](https://refreshless.com/nouislider/) JavaScript library for the slider functionality and [wNumb](https://refreshless.com/wnumb/) for number formatting.

```python
from acdh_django_widgets.widgets import RangeSliderWidget

class MyCustomFilter(FilterSet):
    year = django_filters.RangeFilter(
        help_text=YearBook._meta.get_field("year").help_text,
        label=YearBook._meta.get_field("year").verbose_name,
        widget=RangeSliderWidget(
            attrs={"min": "1900", "max": "2030", "hide_input_fileds": False}
        ),
    )
```


> [!IMPORTANT]  
> The templates used in those widgets are using bootstrap5 classes so ideally those widgets are used with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) and [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)