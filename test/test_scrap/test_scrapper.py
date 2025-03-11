from bs4 import BeautifulSoup
import pytest
from lakocie_dataset.scrap import scrapper


def test_KFScrapper_params():
    # check if all abstract methods are implemented
    empty_soup = BeautifulSoup()
    with pytest.raises(ValueError):
        kfscrapper = scrapper.KFScrapper(empty_soup)

    # fill soup with some data for testing
    html = """
    <html>
        <body>
            <div class="product">
                <h1>Test Product</h1>
                <p class="price">10.99</p>
                <span class="size">1kg</span>
                <div class="flavour">Chicken</div>
                <div class="type">Dry Food</div>
                <div class="age">Adult</div>
                <div class="ean">1234567890</div>
                <div class="composition">Chicken, Rice</div>
                <div class="analytical">Protein: 20%</div>
                <div class="supplements">Vitamins A, D</div>
                <a href="/next-page">Next</a>
                <div class="products">
                    <a href="/product1">Product 1</a>
                    <a href="/product2">Product 2</a>
                </div>
            </div>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    kfscrapper = scrapper.KFScrapper(soup)

    with pytest.raises(ValueError):
        kfscrapper.change_soup(empty_soup)

    with pytest.raises(TypeError):
        fail_scrape = scrapper.KFScrapper(1)  # type: ignore
        fail_scrape.change_soup(2)  # type: ignore

    # check if params are correct
    with pytest.raises(TypeError):
        kfscrapper.get_product_name(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_price(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_weight(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_flavour(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_type(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_age_group(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_ean_code(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_composition(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_analytical_composition(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_dietary_supplements(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_next_page_link(1)  # type: ignore
    with pytest.raises(TypeError):
        kfscrapper.get_product_links(1)  # type: ignore

    with pytest.raises(TypeError):
        kfscrapper.get_product_name(1)  # type: ignore
