import re
from datetime import datetime
from typing import Union

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils import formats
from django.utils.html import escape, format_html
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from .models import FormatterChoices

TRAILING_ZERO = re.compile(r"[,\.]0+$")


def render_value(column, value):
    return format_html(
        "{prefix}{value}{postfix}",
        prefix=column.prefix,
        value=value,
        postfix=column.postfix,
    )


def try_format(args, key, row_data, default=""):
    try:
        value = args[key]
        return value.format(**row_data)
    except (KeyError, ValueError):
        return default


def generate_formatted_attrs(args, row_data):
    return mark_safe(
        " ".join(
            '{}="{}"'.format(escape(k), escape(try_format(args, k, row_data)))
            for k in args
        )
    )


ALIGN_RIGHT = "text-end"
ALIGN_CENTER = "text-center"
NUMBER = "tabular-numbers text-end"


def format_column(column):
    css = ""
    formatter = column.formatter
    if formatter == FormatterChoices.FLOAT:
        css = ALIGN_RIGHT
    elif formatter == FormatterChoices.INTEGER:
        css = ALIGN_RIGHT
    elif formatter == FormatterChoices.DATE:
        css = ALIGN_RIGHT
    elif formatter == FormatterChoices.DATETIME:
        css = ALIGN_RIGHT
    elif formatter == FormatterChoices.BOOLEAN:
        css = ALIGN_CENTER
    return css


FormattedValue = tuple[str, Union[str, SafeString]]


def format_link(value, args, row_data):
    attrs = generate_formatted_attrs(args, row_data)
    return format_html(
        "<a {attrs}>{link}</a>",
        attrs=attrs,
        link=value,
    )


def format_value(column, value, row_data, detail=False) -> FormattedValue:
    css = ""
    formatter = column.formatter
    args = column.formatter_arguments
    if value is None:
        value = mark_safe('<span class="text-secondary">–</span>')
        if formatter == FormatterChoices.BOOLEAN:
            css = ALIGN_CENTER
        if formatter in (
            FormatterChoices.FLOAT,
            FormatterChoices.INTEGER,
            FormatterChoices.DATE,
            FormatterChoices.DATETIME,
        ):
            css = ALIGN_RIGHT
        if formatter == FormatterChoices.LINK:
            return css, render_value(column, format_link(value, args, row_data))
        return css, value

    if formatter == FormatterChoices.FLOAT:
        value = intcomma(value)
        css = NUMBER
    elif formatter == FormatterChoices.INTEGER:
        value = TRAILING_ZERO.sub("", intcomma(value))
        css = NUMBER
    elif formatter == FormatterChoices.DATE:
        value = formats.date_format(datetime.fromisoformat(value), "SHORT_DATE_FORMAT")
        css = NUMBER
    elif formatter == FormatterChoices.DATETIME:
        value = formats.date_format(
            datetime.fromisoformat(value), "SHORT_DATETIME_FORMAT"
        )
        css = NUMBER
    elif formatter == FormatterChoices.BOOLEAN:
        if value:
            value = format_html(
                '<span class="text-success">✅ {}</span>',
                _("Yes"),
            )
        else:
            value = format_html(
                '<span class="text-danger">❌ {}</span>',
                _("No"),
            )
        css = ALIGN_CENTER
    elif formatter == FormatterChoices.LINK:
        value = format_link(value, args, row_data)
    elif formatter == FormatterChoices.SUMMARY:
        if not detail:
            summary = try_format(args, "summary", row_data, _("Details"))
            value = format_html(
                '<details class="datashow-summary"><summary><span>{summary}</span></summary>{details}</details>',
                summary=summary,
                details=value,
            )
    elif formatter == FormatterChoices.ABBREVIATION:
        title = try_format(args, "title", row_data, None)
        if title is None:
            value = format_html("<abbr>{value}</abbr>", value=value)
        else:
            value = format_html(
                '<abbr title="{title}">{value}</abbr>',
                title=title,
                value=value,
            )
    elif formatter == FormatterChoices.IFRAME:
        attrs = generate_formatted_attrs(args, row_data)
        value = format_html(
            '<iframe src="{url}" {attrs}></iframe>', url=value, attrs=attrs
        )

    return css, render_value(column, value)
