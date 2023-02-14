from datetime import datetime
import pytz

class Message:
    def __init__(self):
        self.success_title='<div class="toast-header bg-success"><h4 style="color:#fff;"><strong class="me-auto">Success!</strong></h4><button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>'
        self.error_title='<div class="toast-header bg-danger"><h4 style="color:#fff;"><strong class="me-auto">Error!</strong></h4><button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>'
        self.info_title='<div class="toast-header bg-info"><h4 style="color:#fff;"><strong class="me-auto">Info!</strong></h4><button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>'

    def error(self, text):
        return f'{self.error_title}<div class="toast-body">{text}</div>'

    def success(self, text):
        return f'{self.success_title}<div class="toast-body">{text}</div>'

    def info(self, text):
        return f'{self.info_title}<div class="toast-body">{text}</div>'


def datify(d, style="basic", tzaware=False, timezone='US/Central'):
    d = int(d)
    tz = pytz.timezone(timezone)
    if style == 'basic':
        if tzaware:
            dob = datetime.utcfromtimestamp(d).replace(tzinfo=tz)
        else:
            dob = datetime.fromtimestamp(d)
        return dob.strftime('%m/%d/%Y')
    elif style == 'datetime':
        if tzaware:
            dob = datetime.utcfromtimestamp(d).replace(tzinfo=tz)
        else:
            dob = datetime.fromtimestamp(d)
        return dob.strftime('%m/%d/%Y %H:%M:%S')
    elif style == 'human':
        if tzaware:
            now = datetime.now(tz=tz)
            then = datetime.fromtimestamp(d, tz=pytz.UTC)
        else:
            now = datetime.now()
            then = datetime.fromtimestamp(d)
        diff = now-then
        days, seconds = diff.days, diff.seconds
        if days == 0:
            hours = days * 24 + seconds //3600
            minutes = (seconds % 3600) //60
            if minutes == 1:
                min = 'minute'
            else:
                min = 'minutes'
            if hours == 0:
                out = f'{minutes} {min} ago'
            elif hours == 1:
                out = f'{hours} hour and {minutes} {min} ago'
            else:
                out = f'{hours} hours and {minutes} {min} ago'
        elif days == 1:
            out = 'Yesterday'
        elif days > 1 and days < 7:
            out = f'{days} days ago'
        elif days >= 7 and days <= 112:
            weeks = days//7
            if weeks == 1:
                out = f'{weeks} week ago'
            else:
                out = f'{weeks} weeks ago'
        elif days >112 and days <=365:
            months = days//30
            out = f'{months} months ago'
        elif days > 365:
            years = days//365
            months = days%365//30
            if years == 1:
                y = f'{years} year'
            else:
                y = f'{years} years'
            if months > 0 and months == 1:
                m = f' and {months} month ago'
            elif months > 1:
                m = f' and {months} months ago'
            else:
                m = ''
            out = f'{y}{m}'
        else:
            out = then.strftime('%m/%d/%Y')
        return out
    else:
        return datetime.fromtimestamp(d).strftime('%m/%d/%Y')