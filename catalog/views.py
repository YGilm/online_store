from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, BlogPost, Version
from .forms import ProductForm, VersionForm
from .services import get_cached_categories


class HomeListView(ListView):
    """
    Отображение главной страницы с тремя топовыми продуктами по категориям.
    """
    template_name = 'catalog/home.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        categories = get_cached_categories()
        top_products = []

        for category in categories:
            top_product = Product.objects.filter(category=category).order_by('-creation_date').first()
            if top_product:
                top_products.append(top_product)

        return top_products[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'home page'
        return context


class ProductListView(LoginRequiredMixin, ListView):
    """
    Отображение списка всех продуктов.
    """
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'catalog'
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Отображение детальной информации о продукте.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product_name
        context['active_versions'] = self.object.version_set.filter(is_current=True)
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление продукта.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_superuser


@login_required
def contacts(request):
    """
    Страница контактов с возможностью отправки запроса на обратную связь.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'У вас новый запрос на обратную связь: {name} {phone}: {message}')

    context = {
        'title': 'contacts'
    }
    return render(request, 'catalog/contacts.html', context)


class BlogPostListView(ListView):
    """
    Отображение списка опубликованных блогов, отсортированных по дате создания.
    """
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogs'

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_published=True).order_by('-created_at')

        return query


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    """
    Отображение детальной информации о блоге и учет количества просмотров.
    """
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        self.object.views_count += 1
        self.object.save()

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Создание нового блога с указанием основных полей.
    """
    model = BlogPost
    permission_required = 'catalog.add_blog'
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('catalog:blogs')

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.object.image:
            self.object.image = 'media/note_image.jpg'
            self.object.save()
        return response


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Обновление существующего блога.
    """
    model = BlogPost
    permission_required = 'catalog.change_blog'
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('catalog:blogs')

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление блога.
    """
    model = BlogPost
    success_url = reverse_lazy('catalog:blogs')

    def test_func(self):
        return self.request.user.is_superuser
