"""
Scrapping functions for Kocie Figle web shop
"""

from enum import Enum
from typing import Any
from bs4 import BeautifulSoup, ResultSet

from . import store_definitions
from . import string_utils

BASE_URL = store_definitions.StoreChoice.KF.value.base_url


class HtmlElement(Enum):
    """HTML element selectors for web scraping.

    This enum class defines the HTML element selectors used for scraping product information
    from a website. Each constant represents a specific HTML element with its corresponding
    tag, class, and optional attributes.

    Attributes:
        INFORMATION_SECTION: Section element containing product information
        PRODUCT_PARAMETER_ROWS: Div elements containing product parameter rows
        HIDDEN_TR: Hidden table rows
        PRODUCT_DESCRIPTION: Div element containing product description tab
        PRODUCT_DESCRIPTION_PARAGRAPHS: Paragraph elements within product description
        PAGINATION_DIV: Div element containing pagination
        PRODUCT_TILES: Figure elements representing product tiles
    """

    INFORMATION_SECTION = {"tag": "section", "class": "product-informations"}
    PRODUCT_PARAMETER_ROWS = {"tag": "div", "class": "product-parameter-row"}
    HIDDEN_TR = {"tag": "tr", "class": "hidden"}
    PRODUCT_DESCRIPTION = {
        "tag": "div",
        "class": "tab",
        "attrs": {"data-tab": "description"},
    }
    PRODUCT_DESCRIPTION_PARAGRAPHS = {"tag": "p"}
    PAGINATION_DIV = {"tag": "div", "class": "pagination"}
    PRODUCT_TILES = {"tag": "figure", "class": "product-tile"}


class ProductParameterChoice(Enum):
    """Enum class representing various product parameter choices for cat food.

    This enum defines different parameters that can be used to categorize and filter cat food products.

    Attributes:
        PACKAGING_SIZE (str): Parameter for package size selection
        FLAVOR (str): Parameter for flavor/taste selection
        FOOD_TYPE (str): Parameter for type of cat food selection
        CAT_AGE (str): Parameter for cat age group selection
        ALL (list): List containing all parameter choices
    """

    PACKAGING_SIZE = "rozmiar opakowania"
    FLAVOUR = "smak"
    FOOD_TYPE = "typ karmy"
    CAT_AGE = "wiek kota"
    ALL = [PACKAGING_SIZE, FLAVOUR, FOOD_TYPE, CAT_AGE]


def select(choice: HtmlElement):
    """Decorator that filters BeautifulSoup object based on HTML element choice.

    This decorator wraps functions that process BeautifulSoup objects, filtering the HTML
    content based on the specified HtmlElement enum choice before passing it to the
    wrapped function.

    Args:
        choice (HtmlElement): Enum specifying which HTML element to select/filter.

    Returns:
        callable: Decorated function that receives the filtered BeautifulSoup object.

    Example:
    ```
        @select(HtmlElement.PRODUCT_DESCRIPTION)
        def process_description(filtered_soup):
            # Process only product description HTML
            pass
    ```
    """

    def decorator(func):
        def wrapper(soup: BeautifulSoup, *args, **kwargs):
            match choice:
                case HtmlElement.INFORMATION_SECTION:
                    filtered_soup = soup.find(
                        choice.value["tag"], class_=choice.value["class"]
                    )
                case HtmlElement.PRODUCT_PARAMETER_ROWS:
                    filtered_soup = soup.find_all(
                        choice.value["tag"], class_=choice.value["class"]
                    )
                case HtmlElement.HIDDEN_TR:
                    filtered_soup = soup.find_all(
                        choice.value["tag"], class_=choice.value["class"]
                    )
                case HtmlElement.PRODUCT_DESCRIPTION:
                    filtered_soup = soup.find(
                        choice.value["tag"],
                        class_=choice.value["class"],
                        attrs=choice.value["attrs"],
                    )
                case HtmlElement.PRODUCT_DESCRIPTION_PARAGRAPHS:

                    @select(HtmlElement.PRODUCT_DESCRIPTION)
                    def get_desc_soup(soup: BeautifulSoup):
                        return soup

                    desc = get_desc_soup(soup)
                    filtered_soup = desc.find_all(
                        choice.value["tag"],
                    )  # type: ignore
                case HtmlElement.PAGINATION_DIV:
                    filtered_soup = soup.find(
                        choice.value["tag"], class_=choice.value["class"]
                    )
                case HtmlElement.PRODUCT_TILES:
                    main_products_div = soup.find("div", class_="col-sm-9")
                    filtered_soup = (
                        main_products_div.find_all("figure", class_="product-tile")  # type: ignore
                        if main_products_div
                        else None
                    )

            return func(filtered_soup, *args, **kwargs)

        return wrapper

    return decorator


"""Product related functions"""


def extract_info_from_name(name: str) -> list:
    return name.split(" - ")


def get_product_name(soup: BeautifulSoup) -> str | None:
    prod_name = soup.find("h1", class_="title")
    return prod_name.text if prod_name else None


def get_product_manufacturer(soup: BeautifulSoup) -> str | None:
    prod_name = get_product_name(soup)
    return extract_info_from_name(prod_name)[0] if prod_name else None


@select(HtmlElement.INFORMATION_SECTION)
def get_product_price(soup: BeautifulSoup) -> float | None:
    product_price_divs = soup.find_all("div", class_="product-price")
    try:
        prices = (
            list(map(lambda x: x.text.strip().lower(), product_price_divs))
            if product_price_divs
            else None
        )
        prices = list(filter(lambda x: x != "brak towaru", prices)) if prices else None
        if prices is not None and len(prices) == 1:
            return float(prices[0].replace("zł", ""))
        else:
            print(f"Many prices in {soup}")
    except Exception as e:
        print(f"Error: {e}")


@select(HtmlElement.PRODUCT_PARAMETER_ROWS)
def get_product_parameters(
    soup: BeautifulSoup | ResultSet[Any],
    par_choice: ProductParameterChoice = ProductParameterChoice.ALL,
) -> dict[str, str | int]:
    if type(soup) is BeautifulSoup:
        raise Exception("Expected ResultSet, got BeautifulSoup")

    parameters = {}
    for row in soup:
        # Extract parameter name
        name = row.find("span", class_="parameter-name").text.strip().rstrip(":")  # type: ignore
        # Extract parameter value
        value = row.find("span", class_="text-field").text.strip()  # type: ignore
        parameters[name.lower()] = value
    return parameters


def get_product_size(soup: BeautifulSoup) -> str | None:
    parameters = get_product_parameters(soup)
    size = parameters.get(ProductParameterChoice.PACKAGING_SIZE.value, None)
    if size is None:
        return None
    return str(size)


def get_product_flavour(soup: BeautifulSoup) -> str:
    parameters = get_product_parameters(soup)
    flavour = parameters.get(ProductParameterChoice.FLAVOUR.value, None)
    if flavour is None:
        return "not found"
    return str(flavour)


def get_product_age_group(soup: BeautifulSoup) -> str:
    parameters = get_product_parameters(soup)
    age_group = parameters.get(ProductParameterChoice.CAT_AGE.value, None)
    if age_group is None:
        return "not found"
    return str(age_group)


def get_product_type(soup: BeautifulSoup) -> str:
    parameters = get_product_parameters(soup)
    product_type = parameters.get(ProductParameterChoice.FOOD_TYPE.value, None)
    if product_type is None:
        return "not found"
    return str(product_type)


@select(HtmlElement.HIDDEN_TR)
def get_product_ean_code(soup: BeautifulSoup | ResultSet[Any]) -> int | None:
    if type(soup) is BeautifulSoup:
        raise Exception("Expected ResultSet, got BeautifulSoup")

    for row in soup:
        params = row.attrs  # type: ignore
        if (
            "data-parameter-value" in params
            and params.get("data-parameter-value") == "ean"
        ):
            return (
                params.get("data-parameter-default-value")
                if "data-parameter-default-value" in params
                else None
            )
    return None


@select(HtmlElement.PRODUCT_DESCRIPTION)
def get_product_description(soup: BeautifulSoup) -> BeautifulSoup | ResultSet[Any]:
    return soup


@select(HtmlElement.PRODUCT_DESCRIPTION_PARAGRAPHS)
def get_product_description_paragraphs(
    soup: BeautifulSoup,
) -> BeautifulSoup | ResultSet[Any]:
    return soup


@select(HtmlElement.PRODUCT_DESCRIPTION_PARAGRAPHS)
def get_product_composition(soup: BeautifulSoup | ResultSet[Any]) -> str | None:
    if type(soup) is BeautifulSoup:
        raise Exception("Expected ResultSet, got BeautifulSoup")

    composition = next((p.text.strip() for p in soup if "Skład:" in p.text), None)
    if composition is None:
        composition = next((p.text.strip() for p in soup if "Skład" in p.text), None)
    return composition


@select(HtmlElement.PRODUCT_DESCRIPTION_PARAGRAPHS)
def get_product_analytical_composition(
    soup: BeautifulSoup | ResultSet[Any],
) -> str | None:
    if type(soup) is BeautifulSoup:
        raise Exception("Expected ResultSet, got BeautifulSoup")

    analytical_composition = next(
        (p.text.strip() for p in soup if "Składniki analityczne" in p.text),  # type: ignore
        None,
    )
    return analytical_composition


@select(HtmlElement.PRODUCT_DESCRIPTION_PARAGRAPHS)
def get_product_dietary_supplements(soup: BeautifulSoup | ResultSet[Any]) -> str | None:
    if type(soup) is BeautifulSoup:
        raise Exception("Expected ResultSet, got BeautifulSoup")
    diatairy_supplements = next(
        (p.text.strip() for p in soup if "Dodatki dietetyczne na kg" in p.text),  # type: ignore
        None,
    )
    return diatairy_supplements


"""collection product pages functions"""


@select(HtmlElement.PAGINATION_DIV)
def get_pagination_div(soup: BeautifulSoup) -> BeautifulSoup:
    return soup


@string_utils.add_base_url_in_return(BASE_URL)
@select(HtmlElement.PAGINATION_DIV)
def get_next_page_link(soup: BeautifulSoup) -> str | None:
    try:
        next_page_icon = soup.find("i", class_="fa fa-chevron-right")  # type: ignore
        next_page_link = (
            next_page_icon.find_parent("a")["href"] if next_page_icon else None  # type: ignore
        )
        return str(next_page_link) if next_page_link else None
    except TypeError:
        return None


@select(HtmlElement.PRODUCT_TILES)
def get_product_tiles(soup: BeautifulSoup) -> list[BeautifulSoup] | None:
    if type(soup) is None:
        raise Exception("Expected BeautifulSoup got None")
    return soup  # type: ignore


@string_utils.add_base_url_in_return(BASE_URL)
def get_product_link(soup: BeautifulSoup) -> str | None:
    product_link = soup.find("a")["href"]  # type: ignore
    return str(product_link) if product_link else None


@select(HtmlElement.PRODUCT_TILES)
def get_product_links(soup: list[BeautifulSoup] | BeautifulSoup) -> list[str]:
    return list(map(get_product_link, soup))  # type: ignore
