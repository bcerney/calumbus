from contextlib import closing
from datetime import datetime

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape
from requests import get
from requests.exceptions import RequestException

JINJA_ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
CAT_INFO_LIST = [
    ("Live Music", "tribe-events-category-live-music-events"),
    ("Film", "tribe-events-category-film-events"),
    ("Art", "tribe-events-category-art-events")
]

# Code sampled from this tutorial: https://realpython.com/python-web-scraping-practical-introduction/
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def main():

    for cat_info in CAT_INFO_LIST:
        events_list = get_html(cat_info)
        x = 1

    

        with open('divs.html', mode="a", encoding="utf8") as file:
            for div in divs:
                file.write(div.prettify())    


def get_html(cat_info):
    events_list = []
    for x in range(5):
        raw_html = simple_get(build_events_url(x))
        html = BeautifulSoup(raw_html, 'html.parser')
        events_list.append(html.find_all(name="div", attrs={"class": "type-tribe_events", "class": cat_info[1]}))

    return events_list


def build_events_url(page_number):
    return f"https://www.columbusunderground.com/events?action=tribe_photo&tribe_paged={page_number}&tribe_event_display=photo&tribe-bar-date=2020-02-16"


def render_calumbus_template(category_info, events):
    template = JINJA_ENV.get_template("calumbus.j2")
    render = template.render(category_info=category_info, events=events)
    return render


class Event:

    def __init__(self, event_data):
        self.data = []


if __name__ == "__main__":
    main()
