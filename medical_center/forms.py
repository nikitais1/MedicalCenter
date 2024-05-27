from django import forms
from medical_center.models import Service, Category, Cart


class CategoryForm(forms.ModelForm):
    """Форма создания категорий медицинских услуг."""
    class Meta:
        model = Category
        fields = ("category_title", "category_description", "category_image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ServicesForm(forms.ModelForm):
    """Форма создания услуги."""
    class Meta:
        model = Service
        fields = ("services_title", "services_description", "category", "price", "deadline",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CartForm(forms.ModelForm):
    """Форма создания корзины."""
    class Meta:
        model = Cart
        fields = ("services", "date", "client",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'