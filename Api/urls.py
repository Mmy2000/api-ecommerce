from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products' , views.ProductsViewSet)
router.register('categories' , views.CategoryViewSet)
router.register("carts", views.CartViewSet)

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")

# urlpatterns = router.urls

urlpatterns = [
    path("" , include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    # path("products", views.api_products),
    # path("products/<str:pk>", views.api_product),
    # path("categories", views.api_categories),
    # path("categories/<str:pk>", views.api_category)
    # path("products" , views.ProductsViewSet.as_view() , name="products"),
    # path("products/<str:pk>" , views.ProsuctDetailsApi.as_view() , name="product-details"),
    # path("categories/" , views.CategoriesListApi.as_view() , name="categories"),
    # path("categories/<str:pk>" , views.CategoriesDetailsApi.as_view() , name="category-details"),
]