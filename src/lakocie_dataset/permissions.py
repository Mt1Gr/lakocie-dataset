from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


def webscrapping_allowed(url: str) -> bool:
    """function checks robots.txt file for webscrapping permissions"""
    # get the base url and the robots.txt file url
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"

    # initialize and run the RobotFileParser object
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch("*", url)
