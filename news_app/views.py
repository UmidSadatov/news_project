from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, \
    UpdateView, DeleteView
from .models import News, Category
from .forms import ContactForm


def get_news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


def get_news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }
    return render(request, "news/news_detail.html", context)

# class NewsList(ListView):
#     model = News
#     template_name = "news/news_list.html"
#     context_object_name = "news_list"
#
#     # Переопределяем метод get_queryset, чтобы использовать менеджер published
#     def get_queryset(self):
#         return News.published.all()
#
#
# class NewsDetail(DetailView):
#     model = News
#     template_name = "news/news_detail.html"
#     context_object_name = "news"
#
#     # Получаем объект по id и фильтруем по статусу Published
#     def get_object(self, queryset=None):
#         return get_object_or_404(
#             News, id=self.kwargs['id'], status=News.Status.Published
#         )


# def home_page_view(request):
#
#     news_list = (News.published
#                  .all()
#                  .order_by("-publish_time")[:10])
#
#     local_one = (News.published
#                 .filter(category__name="Mahalliy")
#                 .order_by("-publish_time")[0])
#
#     local_news = (News.published
#                   .all().filter(category__name="Mahalliy")
#                   .order_by("-publish_time")[1:6])
#
#     categories = Category.objects.all()
#
#     context = {
#         'news_list': news_list,
#         'local_one': local_one,
#         'local_news': local_news,
#         'categories': categories
#     }
#
#     return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news_list'] = (self.model.published
                                .all()
                                .order_by("-publish_time")[:5])

        context['local_news'] = (self.model.published
                                 .all().filter(category__name="Mahalliy")
                                 .order_by("-publish_time")[:5])

        context['foreign_news'] = (self.model.published
                                 .all().filter(category__name="Xorij")
                                 .order_by("-publish_time")[:5])

        context['sport_news'] = (self.model.published
                                 .all().filter(category__name="Sport")
                                 .order_by("-publish_time")[:5])

        context['tech_news'] = (self.model.published
                                 .all().filter(category__name="Texnologiyalar")
                                 .order_by("-publish_time")[:5])

        context['categories'] = Category.objects.all()

        return context


# def contact_page_view(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog‘langaningiz uchun tashakkur! "
#                             "</h2>")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(
                "<h2>Biz bilan bog'langaniz uchun rahmat!</h2>"
            )


class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign_news.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news


class TechNewsView(ListView):
    model = News
    template_name = 'news/tech_news.html'
    context_object_name = 'tech_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiyalar")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
