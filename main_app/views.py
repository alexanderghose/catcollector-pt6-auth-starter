from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView # add these 

from .models import Cat, Toy
from .forms import FeedingForm # import the custom form we just made

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello World! /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
  return render(request, 'about.html')

def cat_index(request):
  cats = Cat.objects.all()
  # [{"name": "c1", "breed":"breed1"}, {"name":"c2", "breed":"breed2"}, {}]
  return render(request, 'cats/index.html', {'cats': cats})

def cat_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  #toys = Toy.objects.all() # grab all toys
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))

  feeding_form = FeedingForm()
  # feedings = cat.feeding_set.all()
  print(cat)
  return render(request, 'cats/detail.html', { 'toys':toys_cat_doesnt_have, 'cat': cat, 'feeding_form': feeding_form })

class CatCreate(CreateView):
  model = Cat
  #fields = '__all__'
  fields = ['name', 'breed', 'description', 'age']
  # success_url = '/cats/'

class CatUpdate(UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

def add_feeding(request, cat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('cat-detail', cat_id = cat_id)

def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    c = Cat.objects.get(id=cat_id)
    c.toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)