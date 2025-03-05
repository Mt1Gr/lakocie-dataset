from abc import ABC, abstractmethod
from typing import Any

from bs4 import BeautifulSoup
from .stores import kf, store_definitions


class Scrapper(ABC):
    def __init__(self, soup: BeautifulSoup) -> None:
        """Initialize Scrapper object."""
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("soup must be a BeautifulSoup object")
        elif not soup or not soup.find():
            raise ValueError("BeautifulSoup object cannot be empty")

        self.soup = soup

    def change_soup(self, soup: BeautifulSoup) -> None:
        """Change soup attribute."""
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("soup must be a BeautifulSoup object")
        elif not soup or not soup.find():
            raise ValueError("BeautifulSoup object cannot be empty")
        self.soup = soup

    @abstractmethod
    def get_product_name(self) -> str:
        """Extract product name from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_manufacturer(self) -> str:
        """Extract manufacturer name from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_price(self) -> float:
        """Extract product price from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_size(self) -> str | int:
        """Extract product size from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_flavour(self) -> str:
        """Extract product flavour from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_type(self) -> str:
        """Extract product type from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_age_group(self) -> str:
        """Extract product age group from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_ean_code(self) -> str | int:
        """Extract product EAN code from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_composition(self) -> str:
        """Extract product composition as list of ingredients. Extract from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_analytical_composition(self) -> str:
        """Extract analytical composition as dictionary of values. Extract from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_dietary_supplements(self) -> str:
        """Extract dietary supplements as dictionary of values. Extract from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_next_page_link(self) -> str | None:
        """Extract next page URL, return None if no next page. Extract from self.soup: BeautifulSoup object."""
        raise NotImplementedError

    @abstractmethod
    def get_product_links(self) -> list[str]:
        """Extract list of product URLs from page. Extract from self.soup: BeautifulSoup object."""
        raise NotImplementedError


class KFScrapper(Scrapper):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__(soup)

    def change_soup(self, soup: BeautifulSoup) -> None:
        super().change_soup(soup)

    def get_product_name(self) -> str:
        name = kf.get_product_name(self.soup)
        return name if name else "not found"

    def get_product_manufacturer(self) -> str:
        manufacturer = kf.get_product_manufacturer(self.soup)
        return manufacturer if manufacturer else "not found"

    def get_product_price(self) -> float:
        price = kf.get_product_price(self.soup)
        return price if price else float("nan")

    def get_product_size(self) -> str | int:
        size = kf.get_product_parameters(
            self.soup, kf.ProductParameterChoice.PACKAGING_SIZE
        )
        if size and isinstance(size, str):
            size = int(size) if size.isdigit() else size
        return size if size else "not found"  # type: ignore

    def get_product_flavour(self) -> str:
        flavour = kf.get_product_parameters(
            self.soup, kf.ProductParameterChoice.FLAVOUR
        )
        return flavour if flavour else "not found"  # type: ignore

    def get_product_age_group(self) -> str:
        age_group = kf.get_product_parameters(
            self.soup, kf.ProductParameterChoice.CAT_AGE
        )
        return age_group if age_group else "not found"  # type: ignore

    def get_product_type(self) -> str:
        product_type = kf.get_product_parameters(
            self.soup, kf.ProductParameterChoice.FOOD_TYPE
        )
        return product_type if product_type else "not found"  # type: ignore

    def get_product_ean_code(self) -> str | int:
        ean_code = kf.get_product_ean_code(self.soup)
        if isinstance(ean_code, str):
            ean_code = int(ean_code) if ean_code.isdigit() else ean_code
        return ean_code if ean_code else "not found"

    def get_product_composition(self) -> str:
        composition = kf.get_product_composition(self.soup)
        return composition if composition else "not found"

    def get_product_analytical_composition(self) -> str:
        analytical_composition = kf.get_product_analytical_composition(self.soup)
        return analytical_composition if analytical_composition else "not found"

    def get_product_dietary_supplements(self) -> str:
        dietary_supplements = kf.get_product_dietary_supplements(self.soup)
        return dietary_supplements if dietary_supplements else "not found"

    def get_next_page_link(self) -> str | None:
        next_page_link = kf.get_next_page_link(self.soup)
        return next_page_link if next_page_link else None

    def get_product_links(self) -> list[str]:
        product_links = kf.get_product_links(self.soup)
        return product_links if product_links else []


def get_scrapper(
    store_choice: store_definitions.StoreChoice, soup: BeautifulSoup
) -> KFScrapper:
    match store_choice:
        case store_definitions.StoreChoice.KF:
            return KFScrapper(soup)
        case _:
            raise ValueError("Store not supported")
