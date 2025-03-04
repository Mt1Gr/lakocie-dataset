from lakocie_dataset.scrap.stores import string_utils


def test_add_base_url_in_return():
    @string_utils.add_base_url_in_return("https://www.shop.com/")
    def ret_url(prod_name: str | None) -> str | None:
        if prod_name is None:
            return None
        return f"/{prod_name}"

    assert ret_url("product") == "https://www.shop.com/product"
    assert ret_url("/product2") == "https://www.shop.com/product2"
    assert ret_url("product3/") == "https://www.shop.com/product3/"
    assert ret_url("/product4/") == "https://www.shop.com/product4/"
    assert ret_url("") == "https://www.shop.com/"
    assert ret_url(None) is None
