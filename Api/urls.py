from django.urls import path
from . import views



urlpatterns = [
    # path("products", views.api_products),
    # path("products/<str:pk>", views.api_product),
    # path("categories", views.api_categories),
    # path("categories/<str:pk>", views.api_category)
    path("products" , views.ProductListApi.as_view() , name="products"),
    path("products/<str:pk>" , views.ProsuctDetailsApi.as_view() , name="product-details"),
    path("categories/" , views.CategoriesListApi.as_view() , name="categories"),
    path("categories/<str:pk>" , views.CategoriesDetailsApi.as_view() , name="category-details"),
]