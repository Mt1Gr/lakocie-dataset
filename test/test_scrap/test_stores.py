from lakocie_dataset.scrap import stores


def test_store_choice():
    assert len(stores.StoreChoice) == 1

    assert stores.StoreChoice.KF.value.name == "Kocie Figle"
    assert stores.StoreChoice.KF.value.base_url == "https://kociefigle.pl/"
    assert (
        stores.StoreChoice.KF.value.scrap_start_url
        == "https://kociefigle.pl/Karmy-Mokre"
    )


def test_base_store():
    test_store = stores.BaseStore(
        name="Test Store",
        base_url="https://teststore.com/",
        scrap_start_url="https://teststore.com/products",
    )

    assert test_store.name == "Test Store"
    assert test_store.base_url == "https://teststore.com/"
    assert test_store.scrap_start_url == "https://teststore.com/products"
