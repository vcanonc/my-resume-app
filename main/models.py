from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


# Create your models here.
class Skill(models.Model):
    
    class Meta:
        verbose_name_plural = 'Skills'
        verbose_name = 'Skill'
    
    name = models.CharField(max_length=20, blank=True, null=True)
    score = models.IntegerField(default=80, blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='skills')
    is_key_skill = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    
    class Meta:
        verbose_name_plural = 'User profiles'
        verbose_name = 'User profile'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatar/')
    title = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    cv = models.FileField(blank=True, null=True, upload_to='cv/')
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ContactProfile(models.Model):
    
    class Meta:
        verbose_name_plural = 'Contact profiles'
        verbose_name = 'Contact profile'
        ordering = ['timestamp']

    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(verbose_name='Name', max_length=100)
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')


class Testimonial(models.Model):
    
    class Meta:
        verbose_name_plural = 'Testimonials'
        verbose_name = 'Testimonial'
        ordering = ['name']
    
    thumbnail = models.ImageField(blank=True, null=True, upload_to='testimonials/')
    name = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    quote = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Media(models.Model):
    
    class Meta:
        verbose_name_plural = 'Media Files'
        verbose_name = 'Media'
        ordering = ['name']
    
    image = models.ImageField(blank=True, null=True, upload_to='media/')
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_image = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.url:
            self.is_image = False
        super(Media, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Portfolio(models.Model):
    
    class Meta:
        verbose_name_plural = 'Portfolio Profiles'
        verbose_name = 'Porfolio'
        ordering = ['name']
    
    date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='portfolio/')
    repository_url = models.URLField(max_length=200, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Portfolio, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'portfolio/{self.slug}'


class Blog(models.Model):
    
    class Meta:
        verbose_name_plural = 'Blog Profiles'
        verbose_name = 'Blog'
        ordering = ['timestamp']
    
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='blog/')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Blog, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'blog/{self.slug}'


class Certificate(models.Model):
    
    class Meta:
        verbose_name_plural = 'Certificates'
        verbose_name = 'Certificate'
    
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Experience(models.Model):
    
    EMPLOYMENT_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CT', 'Contract'),
        ('IN', 'Intership'),
        ('FR', 'Freelance'),
    ]
    
    class Meta:
        verbose_name_plural = 'Experiences'
        verbose_name = 'Experience'
        ordering = ['-start_date']
    
    title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.title} at {self.company}'
    
    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        
        if not self.id:
            self.slug = slugify(f'{self.title} {self.company} {self.start_date}')
        
        super(Experience, self).save(*args, **kwargs)
    
    def duration(self):
        if self.is_current:
            return 'Current'
        
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days // 30
        
        return 'N/A'
