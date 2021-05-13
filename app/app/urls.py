from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/',include('accounts.urls',namespace='accounts')),
    path('api/recipe/',include('recipe.urls',namespace='recipe'))
]
