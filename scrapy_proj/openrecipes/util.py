import isodate
import datetime

zeroInterval = datetime.timedelta(0)


def parse_iso_date(scope):
    try:
        return sum(
            (isodate.parse_duration(time) for time in scope.select('@content | @datetime').extract()),
            zeroInterval
        )
    except:
        return scope.select('text()').extract()
