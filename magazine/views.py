from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from .forms import RegistrationForm, AuthorizationForm, CartAddProductForm, CommentUserForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_POST
from .models import Product, Category, CommentUser
from django.core.paginator import Paginator
from .cart import Cart


# Create your views here.


dc_bar = [

    {'title': 'Главная', 'url_name': 'main-page'},
    {'title': 'Весь ассортимент', 'url_name': 'all_prod'},
    {'title': 'Гитары', 'url_name': 'guitars'},
    {'title': 'Ударные установки', 'url_name': 'drums'},
    {'title': 'Духовые инструменты', 'url_name': 'wind_instr'},
    {'title': 'Сопутствующий товар', 'url_name': 'related_prod'},

]


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'magazine/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['dc_bar'] = dc_bar
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main-page')


class AuthorizationView(LoginView):

    form_class = AuthorizationForm
    template_name = 'magazine/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['dc_bar'] = dc_bar
        return context

    def get_success_url(self):
        return reverse('all_prod')


def log_out_user(request):

    logout(request)
    return redirect('log_in')


def main_page(request):

    data = {
        'cat': Category.objects.all(),
        'dc_bar': dc_bar

    }
    return render(request, 'magazine/main_page.html', context=data)


# class DetailCategory(DetailView):
#
#     model = Category
#     template_name = 'magazine/category.html'
#     context_object_name = 'cat'
#     slug_url_kwarg = 'slug_cat'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'prod': Product.objects.all(),
#             'dc_bar': dc_bar,
#             'title': 'Категории'
#         })
#         return context


class ListProduct(ListView):

    model = Product
    template_name = 'magazine/index.html'
    context_object_name = 'prod'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Вся продукция',
            'dc_bar': dc_bar,

        })
        return context


class ListProductGuitars(ListView):

    model = Product
    template_name = 'magazine/guitars.html'
    context_object_name = 'guitars'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

            'prod': Product.objects.filter(Q(category_id=1), Q(availability=True)),
            'title': 'Гитары',
            'dc_bar': dc_bar

        })
        return context


class ListProductDrums(ListView):

    model = Product
    template_name = 'magazine/drums.html'
    context_object_name = 'drums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

            'prod': Product.objects.filter(Q(category_id=2), Q(availability=True)),
            'title': 'Ударные установки',
            'dc_bar': dc_bar

        })
        return context


class ListProductWind(ListView):

    model = Product
    template_name = 'magazine/wind.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

            'prod': Product.objects.filter(Q(category_id=3), Q(availability=True)),
            'title': 'Духовые инструменты',
            'dc_bar': dc_bar

        })
        return context


class ListProductRelated(ListView):

    model = Product
    template_name = 'magazine/related.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

            'prod': Product.objects.filter(Q(category_id=4), Q(availability=True)),
            'title': 'Сопутствующие товары',
            'dc_bar': dc_bar

        })
        return context


# class AddCommentUser(CreateView):
#
#     model = CommentUser
#     form_class = CommentUserForm
#     template_name = 'magazine/detail_product.html'
#     success_url = '/list'


class DetailProduct(FormMixin, DetailView):

    model = Product
    form_class = CommentUserForm
    template_name = 'magazine/detail_product.html'
    context_object_name = 'one_prod'
    slug_url_kwarg = 'slug_product'

    def get_success_url(self, **kwargs):
        return reverse_lazy('one_product', kwargs={'slug_product': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.name_product = self.get_object()
        self.object.name = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Об инструменте',
            'dc_bar': dc_bar,
            'cart_product_form': CartAddProductForm(),
        })
        return context


# def detail_product(request, slug_product):
#
#     prod = get_object_or_404(Product, slug=slug_product, available=True)
#     cart_product_form = CartAddProductForm()
#     data = {
#         'prod': prod,
#         'cart_product_form': cart_product_form
#     }
#     return render(request, 'magazine/detail_product.html', context=data)


@require_POST
def cart_add(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.product_add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def all_detail(request):

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                'update': True})
    return render(request, 'magazine/detail_cart.html', context={'cart': cart})





