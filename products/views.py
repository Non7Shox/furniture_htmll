from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from products.models import ProductsModel, ProductsCategoryModel, ProductTagModel


class ProductsListView(ListView):
    template_name = 'products/products_list.html'
    model = ProductsModel
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductsCategoryModel.objects.all()
        context["tags"] = ProductTagModel.objects.all()
        context["products"] = ProductsModel.objects.all()
        context["famous_products"] = ProductsModel.objects.all().order_by('created_at')[:2]
        return context


class ProductsDetailView(DetailView):
    template_name = 'products/products-detail.html'
    context_object_name = 'product'
    model = ProductsModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = ProductsCategoryModel.objects.all()
        context["tags"] = ProductTagModel.objects.all()
        context["famous_blogs"] = ProductsModel.objects.all().order_by('created_at')[:2]
        context["related_blogs"] = ProductsModel.objects.filter(categories__in=self.object.categories.all())[:3]
        return context


def add_or_remove(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
    else:
        cart.append(pk)

    request.session['cart'] = cart
    print(request.session.get('cart', []))
    return redirect('products:list')
