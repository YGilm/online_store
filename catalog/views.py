from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Product, BlogPost


class HomeListView(ListView):
    template_name = 'catalog/home.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        categories = Category.objects.all()
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


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'catalog'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product_name
        return context


def contacts(request):
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
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogs'

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_published=True).order_by('-created_at')

        return query


class BlogPostDetailView(DetailView):
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


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('catalog:blogs')

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.object.image:
            self.object.image = 'media/note_image.jpg'
            self.object.save()
        return response


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('catalog:blogs')

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:blogs')
