from django.contrib import admin

from medical_center.models import Category, Service, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'category_description', 'category_image')
    search_fields = ('category_title', 'category_description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('services_title', 'services_description', 'price', 'category', 'deadline')
    search_fields = ('services_title', 'services_description')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('get_client_username', 'get_services', 'date')
    search_fields = ('client__last_name', 'services__services_title', 'date')

    def get_client_username(self, obj):
        return f'{obj.client.first_name} {obj.client.last_name}'

    get_client_username.short_description = 'client'

    def get_services(self, obj):
        return ', '.join([service.services_title for service in obj.services.all()])

    get_services.short_description = 'services'