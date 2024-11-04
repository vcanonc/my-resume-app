from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from .forms import ContactForm
from . import models


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        testimonials = models.Testimonial.objects.filter(is_active=True)
        certificates = models.Certificate.objects.filter(is_active=True)
        blogs = models.Blog.objects.filter(is_active=True).order_by("-timestamp")[:4]
        portfolio = models.Portfolio.objects.filter(is_active=True)
        experiences = models.Experience.objects.filter(is_active=True)

        context["testimonials"] = testimonials
        context["certificates"] = certificates
        context["blogs"] = blogs
        context["portfolio"] = portfolio
        context["experiences"] = experiences

        return context


class ContactView(generic.FormView):
    template_name = "main/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. We will be in touch soon.")
        return super().form_valid(form)


class PortfolioView(generic.ListView):
    model = models.Portfolio
    template_name = "main/portfolio.html"
    paginate_by = 10
    context_object_name = "projects"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
    model = models.Portfolio
    template_name = "main/portfolio-detail.html"
    context_object_name = "portfolio"


class BlogView(generic.ListView):
    model = models.Blog
    template_name = "main/blog.html"
    paginate_by = 10
    context_object_name = "blogs"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by("-timestamp")


class BlogDetailView(generic.DetailView):
    model = models.Blog
    template_name = "main/blog-detail.html"
    context_object_name = "blog"

    def get_queryset(self):
        return models.Blog.objects.filter(is_active=True)


class ExperienceView(generic.ListView):
    model = models.Experience
    template_name = "main/experience.html"
    paginate_by = 10
    context_object_name = "experiences"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ExperienceDetailView(generic.DetailView):
    model = models.Experience
    template_name = "main/experience-detail.html"
    context_object_name = "experience"
