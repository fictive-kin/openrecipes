import isodate
from dateutil.parser import parse
from scrapy import log
import bleach


def parse_iso_date(scope):
    try:
        return scope.select('@content | @datetime').extract()[0]
    except:
        return ''


def flatten(list_or_string):
    if not list_or_string:
        return ''
    if isinstance(list_or_string, list):
        return list_or_string[0]
    else:
        return list_or_string


def strip_html(html_str):
    """removes all HTML markup using the Bleach lib"""
    return bleach.clean(html_str, tags=[], attributes={},
                                   styles=[], strip=True)


def trim_whitespace(str):
    """calls .strip() on passed str"""
    return str.strip()


def get_isodate(date_str):
    """convert the given date_str string into an iso 8601 date"""
    iso_date = None

    if not date_str:
        return None

    #first, is it already a valid isodate?
    try:
        isodate.parse_date(date_str)
        return date_str
    except isodate.ISO8601Error, e:
        # if not, try to parse it
        try:
            iso_date = isodate.date_isoformat(parse(date_str))
        except Exception, e:
            log.msg(e.message, level=log.WARNING)
            return None

        return iso_date


def get_isoduration(date_str):
    """convert the given date_str string into an iso 8601 duration"""
    iso_duration = None

    if not date_str:
        return None

    #first, is it already a valid isoduration?
    try:
        isodate.parse_duration(date_str)
        return date_str
    except isodate.ISO8601Error, e:
        # if not, try to parse it
        try:
            delta = (parse(date_str) - parse(''))
            iso_duration = isodate.duration_isoformat(delta)
        except Exception, e:
            log.msg(e.message, level=log.WARNING)
            return None

        return iso_duration


def parse_isodate(iso_date):
    """parse the given iso8601 date string into a python date object"""
    date = None

    try:
        date = isodate.parse_date(iso_date)
    except Exception, e:
        log.msg(e.message, level=log.WARNING)

    return date


def parse_isoduration(iso_duration):
    """parse the given iso8601 duration string into a python timedelta object"""
    delta = None

    try:
        delta = isodate.parse_duration(iso_duration)
    except Exception, e:
        log.msg(e.message, level=log.WARNING)

    return delta
