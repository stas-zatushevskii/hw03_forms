# from django.shortcuts import render

# Create your views here.

# users/views.py
# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm

from .models import Contact

from .forms import ContactForm

from django.shortcuts import render

from django.shortcuts import redirect


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


# form_class — из какого класса взять форму
# success_url — куда перенаправить пользователя после успешной отправки формы
# template_name — имя шаблона, куда будет передана переменная form с объектом
    # HTML-формы. Всё это чем-то похоже
    # на вызов функции render() во view-функции.

def user_contact(request):
    # Проверяем, получен POST-запрос или какой-то другой:
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = ContactForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            # При необходимости обрабатываем данные
            contact = Contact.objects.get(pk=3)
            # Создаём объект формы и передаём в него объект модели с pk=3
            form = ContactForm(instance=contact)
            form.save()
            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect('/thank-you/')

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию,
        # чтобы не заставлять пользователя вносить их повторно
        return render(request, 'contact.html', {'form': form})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
