# shim module so tests importing pages.products_page still work
from .product_page import ProductPage
__all__ = ["ProductPage"]
