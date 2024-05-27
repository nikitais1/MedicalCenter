import json
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse
from config import settings
from medical_center.forms import CategoryForm, ServicesForm
from medical_center.models import Category, Service, Cart

from django.urls import reverse_lazy


# Классы категории
class CategoryCreateView(CreateView, PermissionRequiredMixin):
    """Класс создания категорий медицинских услуг."""
    model = Category
    form_class = CategoryForm
    permission_required = 'medical_center.add_category'
    success_url = reverse_lazy("medical_center:category_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.add_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    """Класс отображения списка категорий медицинских услуг."""
    model = Category


class CategoryUpdateView(UpdateView, PermissionRequiredMixin):
    """Класс обновления категорий медицинских услуг."""
    model = Category
    form_class = CategoryForm
    permission_required = 'medical_center.change_category'
    success_url = reverse_lazy("medical_center:category_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.change_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView, PermissionRequiredMixin):
    """Класс удаления категорий медицинских услуг."""
    model = Category
    success_url = reverse_lazy("medical_center:category_list")
    permission_required = 'medical_center.delete_category'
    template_name = "medical_center/category_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_object().category_title
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.delete_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryServiceListView(ListView):
    """Класс отображения списка услуг по категориям медицинских услуг."""
    model = Service

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Service.objects.filter(category_id=category_pk)


# Классы услуг
class ServiceCreateView(CreateView, PermissionRequiredMixin):
    """Класс создания услуг."""
    model = Service
    form_class = ServicesForm
    permission_required = 'medical_center.add_service'
    success_url = reverse_lazy("medical_center:service_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.add_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ServiceListView(ListView):
    """Класс отображения списка услуг."""
    model = Service


class ServiceDetailView(DetailView):
    """Класс отображения детальной информации об услуге."""
    model = Service

    def get(self, request, pk):
        product = Service.objects.get(pk=pk)
        context = {
            'object_list': Service.objects.filter(id=pk),
        }
        return render(request, 'medical_center/service_detail.html', context)


class ServiceUpdateView(UpdateView, PermissionRequiredMixin):
    """Класс обновления услуг."""
    model = Service
    form_class = ServicesForm
    permission_required = 'medical_center.change_service'
    success_url = reverse_lazy("medical_center:service_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.change_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ServiceDeleteView(DeleteView, PermissionRequiredMixin):
    """Класс удаления услуг."""
    model = Service
    success_url = reverse_lazy("medical_center:service_list")
    permission_required = 'medical_center.delete_service'
    template_name = "medical_center/service_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_object().services_title
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_center.delete_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ContactView(View):
    """Класс обработки формы обратной связи."""

    def get(self, request):
        return render(request, 'medical_center/contacts.html')

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            # Логика для отправки письма администратору
            subject = 'Обращение от посетителя сайта'
            admin_message = f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}'
            send_mail(
                subject=subject,
                message=admin_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Замените на реальный адрес администратора
            )

            success_message = 'Ваше сообщение успешно отправлено. Мы свяжемся с вами в ближайшее время.'
            context = {'success_message': success_message}
            return render(request, 'medical_center/contacts_success.html', context)


class ServiceCartView(View):
    """Класс отображения корзины услуг."""
    model = Cart

    def get(self, request):
        # Получаем объект корзины для текущего пользователя
        cart = Cart.objects.filter(client=request.user).first()

        # Получаем количество услуг в корзине
        services_count = cart.services.count() if cart else 0

        # Получаем список услуг в корзине
        services = cart.services.all() if cart else []

        # Получаем данные о клиенте
        client = cart.client if cart else None

        # Получаем сумму покупок услуг в корзине
        total_price = sum(service.price for service in services)

        # Обновляем контекст
        context = {
            'services_count': services_count,
            'services': services,
            'total_price': total_price,
            'client': client
        }
        return render(request, 'medical_center/shopping_cart.html', context)

    def post(self, request):
        cart = Cart.objects.filter(client=request.user).first()
        if cart:
            services = cart.services.all()
            total_price = sum(service.price for service in services)

            # Логика для отправки письма администратору
            context = {'services': services, 'total_price': total_price, 'user': request.user}
            admin_message = render_to_string('medical_center/admin_cart_email.html', context)
            send_mail(
                subject='Новый заказ в медицинской клинике',
                message='Новый заказ в медицинской клинике',
                html_message=admin_message,  # Отправка HTML-сообщения
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Замените на реальный адрес администратора
            )

            # Логика для отправки письма пользователю
            user_message = render_to_string('medical_center/cart_email.html', context)
            send_mail(
                subject='Оформление заказа в медицинской клинике',
                message='Оформление заказа в медицинской клинике',
                html_message=user_message,  # Отправка HTML-сообщения
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
            )

            cart.services.clear()  # Очистка корзины

            success_message = 'Ваше сообщение успешно отправлено. Мы свяжемся с вами в ближайшее время.'
            context = {'success_message': success_message}
            return render(request, 'medical_center/contacts_success.html', context)
        else:
            return HttpResponse('Ошибка отправки письма о заказе на вашу почту')


class AddToCartView(View):
    """Класс добавления услуги в корзину."""
    def post(self, request, pk):
        json_data = json.loads(request.body)
        service_id = json_data.get('service_id')
        service = Service.objects.get(pk=service_id)

        # Получите объект корзины текущего пользователя или создайте новый
        cart, created = Cart.objects.get_or_create(client=request.user)

        # Добавление услуги в корзину
        cart.services.add(service)

        return JsonResponse({'message': 'Услуга успешно добавлена в корзину.'})


def home(request):
    """Функция отображения главной страницы."""
    return render(request, 'medical_center/home.html')


def remove_service(request, service_id):
    """Функция удаления услуги из корзины."""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        cart = Cart.objects.get(client=request.user)
        cart.services.remove(service)
        return redirect(reverse('medical_center:service_cart'))
    else:
        return redirect(reverse('medical_center:service_cart'))


def clear_service(request):
    """Функция очистки корзины."""
    if request.method == 'POST':
        cart = Cart.objects.get(client=request.user)
        cart.services.clear()
        return redirect(reverse('medical_center:service_cart'))
    else:
        return redirect(reverse('medical_center:service_cart'))