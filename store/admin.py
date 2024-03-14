from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("name", "price")
    list_display = ("name", "category")



# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile



# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Profile)


# Unregister the old way
admin.site.unregister(User)

# Re-register new
admin.site.register(User, UserAdmin)

