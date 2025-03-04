from lakocie_dataset.scrap import fetch, permissions
from enum import Enum
from lakocie_dataset.scrap import kf
from lakocie_dataset.scrap.kf import BASE_URL, ProductParameterChoice
from bs4 import BeautifulSoup


class KFPages(Enum):
    PAGINATION_PAGE = "https://kociefigle.pl/Karmy-Mokre/pa/4"
    PRODUCT_PAGE = (
        "https://kociefigle.pl/Almo-Nature-HFC-Complete-Kurczak-i-Marchew-70g-p815"
    )


class CorrectTestData(Enum):
    PROD_NAME = "Almo Nature - HFC Complete - Kurczak i Marchew - 70g"
    PORD_INFO_FROM_NAME = [
        "Almo Nature",
        "HFC Complete",
        "Kurczak i Marchew",
        "70g",
    ]
    PROD_PRICE = 5.85
    PROD_PARAMETERS = {
        "rozmiar opakowania": "70g",
        "smak": "Kurczak, Marchew",
        "typ karmy": "Pełnoporcjowa",
        "wiek kota": "Dorosłe koty",
    }
    PROD_WEIGHT = PROD_PARAMETERS["rozmiar opakowania"]
    PROD_FLAVOUR = PROD_PARAMETERS["smak"]
    PROD_TYPE = PROD_PARAMETERS["typ karmy"]
    PROD_CAT_AGE = PROD_PARAMETERS["wiek kota"]
    PROD_EAN_CODE = "8001154127294"
    PROD_FIRST_DESC_PAR = "Kompletna karma pełnoporcjowa."
    PROD_SOME_COMP_TEXT = "skrobia z tapioki"
    PROD_SOME_ANALYTIC_TEXT = "włókno surowe 0,5%"
    PROD_SOME_DIET_SUPP_TEXT = "wit.E 48IU/kg"
    COLL_NEXT_PAGE_LINK = "https://kociefigle.pl/Karmy-Mokre/pa/5"
    COLL_LEN_PRODUCT_LINKS = 18


product_page_soup = None
pagination_page_soup = None


def setup_module(module):
    """
    Set up module-level test fixtures for product and pagination page parsing.

    This function initializes global BeautifulSoup objects for product and pagination pages
    by fetching content from test URLs and parsing the HTML. It checks if web scraping is
    allowed before making any requests.

    Globals:
        product_page_soup (BeautifulSoup): Parsed HTML content of the product page
        pagination_page_soup (BeautifulSoup): Parsed HTML content of the pagination page

    Raises:
        Exception: If web scraping is not allowed for the base URL
    """
    global product_page_soup, pagination_page_soup
    try:
        if not permissions.webscrapping_allowed(BASE_URL):
            raise Exception("Web scrapping is not allowed")
        product_page_soup = BeautifulSoup(
            fetch.get_content(KFPages.PRODUCT_PAGE.value), "html.parser"
        )
        pagination_page_soup = BeautifulSoup(
            fetch.get_content(KFPages.PAGINATION_PAGE.value), "html.parser"
        )
    except Exception as e:
        print(e)


def test_get_product_name():
    assert (
        kf.get_product_name(product_page_soup) == CorrectTestData.PROD_NAME.value
        if product_page_soup
        else None
    )


def test_extract_info_from_name():
    name_info_str = "Almo Nature - HFC Complete - Kurczak i Marchew - 70g"
    assert (
        kf.extract_info_from_name(name_info_str)
        == CorrectTestData.PORD_INFO_FROM_NAME.value
    )


def test_get_product_manufacturer():
    assert (
        kf.get_product_manufacturer(product_page_soup)
        == CorrectTestData.PORD_INFO_FROM_NAME.value[0]
        if product_page_soup
        else None
    )


def test_get_product_price():
    assert (
        kf.get_product_price(product_page_soup) == CorrectTestData.PROD_PRICE.value
        if product_page_soup
        else None
    )


def test_get_product_parameters():
    assert (
        kf.get_product_parameters(product_page_soup)
        == CorrectTestData.PROD_PARAMETERS.value
        if product_page_soup
        else None
    )


def test_get_product_weight():
    assert (
        kf.get_product_parameters(
            product_page_soup, ProductParameterChoice.PACKAGING_SIZE
        )
        == CorrectTestData.PROD_PARAMETERS.value["rozmiar opakowania"]
        if product_page_soup
        else None
    )


def test_get_product_flavor():
    assert (
        kf.get_product_parameters(product_page_soup, ProductParameterChoice.FLAVOR)
        == CorrectTestData.PROD_PARAMETERS.value["smak"]
        if product_page_soup
        else None
    )


def test_get_product_type():
    assert (
        kf.get_product_parameters(product_page_soup, ProductParameterChoice.FOOD_TYPE)
        == CorrectTestData.PROD_PARAMETERS.value["typ karmy"]
        if product_page_soup
        else None
    )


def test_get_product_target_age():
    assert (
        kf.get_product_parameters(product_page_soup, ProductParameterChoice.CAT_AGE)
        == CorrectTestData.PROD_PARAMETERS.value["wiek kota"]
        if product_page_soup
        else None
    )


def test_get_product_ean_code():
    assert (
        kf.get_product_ean_code(product_page_soup)
        == CorrectTestData.PROD_EAN_CODE.value
        if product_page_soup
        else None
    )


def test_get_product_description():
    soup = product_page_soup if product_page_soup else BeautifulSoup("", "html.parser")
    description = soup.find("div", class_="tab", attrs={"data-tab": "description"})
    assert description is not None


def test_get_product_description_paragraphs():
    soup = product_page_soup if product_page_soup else BeautifulSoup("", "html.parser")
    pars = kf.get_product_description_paragraphs(soup)
    pars = [par.text for par in pars]
    assert CorrectTestData.PROD_FIRST_DESC_PAR.value in pars[0]


def test_get_product_composition():
    soup = product_page_soup if product_page_soup else BeautifulSoup("", "html.parser")
    assert (
        CorrectTestData.PROD_SOME_COMP_TEXT.value in kf.get_product_composition(soup)  # type: ignore
    )


def test_get_product_analytical_composition():
    soup = product_page_soup if product_page_soup else BeautifulSoup("", "html.parser")
    comp = kf.get_product_analytical_composition(soup)
    assert CorrectTestData.PROD_SOME_ANALYTIC_TEXT.value in comp  # type: ignore


def test_get_product_dietary_supplements():
    soup = product_page_soup if product_page_soup else BeautifulSoup("", "html.parser")
    diet_supp = kf.get_product_dietary_supplements(soup)
    assert CorrectTestData.PROD_SOME_DIET_SUPP_TEXT.value in diet_supp  # type: ignore


def test_get_pagnation_div():
    pagination_div = (
        kf.get_pagination_div(pagination_page_soup) if pagination_page_soup else None
    )
    assert pagination_div is not None


def test_get_next_page_link():
    assert (
        kf.get_next_page_link(pagination_page_soup)
        == CorrectTestData.COLL_NEXT_PAGE_LINK.value
        if pagination_page_soup
        else False
    )


def test_get_product_tiles():
    tiles = kf.get_product_tiles(pagination_page_soup) if pagination_page_soup else None
    assert (
        len(tiles) == CorrectTestData.COLL_LEN_PRODUCT_LINKS.value if tiles else False
    )


def test_get_product_links():
    links = kf.get_product_links(pagination_page_soup) if pagination_page_soup else None
    assert (
        len(links) == CorrectTestData.COLL_LEN_PRODUCT_LINKS.value if links else False
    )
