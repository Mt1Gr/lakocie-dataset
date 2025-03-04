from lakocie_dataset.scrap.stores import store_definitions


def test_store_choice():
    assert len(store_definitions.StoreChoice) == 1

    assert store_definitions.StoreChoice.KF.value.name == "Kocie Figle"
    assert store_definitions.StoreChoice.KF.value.base_url == "https://kociefigle.pl/"
    assert (
        store_definitions.StoreChoice.KF.value.scrap_start_url
        == "https://kociefigle.pl/Karmy-Mokre"
    )


def test_base_store():
    test_store = store_definitions.BaseStore(
        name="Test Store",
        base_url="https://teststore.com/",
        scrap_start_url="https://teststore.com/products",
    )

    assert test_store.name == "Test Store"
    assert test_store.base_url == "https://teststore.com/"
    assert test_store.scrap_start_url == "https://teststore.com/products"
