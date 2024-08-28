from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products' , views.ProductsViewSet)
router.register('categories' , views.CategoryViewSet)



# urlpatterns = router.urls

urlpatterns = [
    path("" , include(router.urls))
    # path("products", views.api_products),
    # path("products/<str:pk>", views.api_product),
    # path("categories", views.api_categories),
    # path("categories/<str:pk>", views.api_category)
    # path("products" , views.ProductsViewSet.as_view() , name="products"),
    # path("products/<str:pk>" , views.ProsuctDetailsApi.as_view() , name="product-details"),
    # path("categories/" , views.CategoriesListApi.as_view() , name="categories"),
    # path("categories/<str:pk>" , views.CategoriesDetailsApi.as_view() , name="category-details"),
]