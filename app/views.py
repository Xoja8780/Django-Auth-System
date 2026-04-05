# Импорт функций для рендеринга шаблонов и редиректов
from django.shortcuts import render, redirect

# Импорт функций для работы с аутентификацией в :contentReference[oaicite:0]{index=0}
from django.contrib.auth import login, logout, authenticate

# Декоратор, который пускает только авторизованных пользователей
from django.contrib.auth.decorators import login_required

# Твоя форма регистрации
from .forms import RegisterForm


# 🔹 РЕГИСТРАЦИЯ
def register_view(request):
    # Создаём пустую форму (для GET запроса)
    form = RegisterForm()

    # Если пользователь отправил форму
    if request.method == 'POST':

        # Заполняем форму данными из запроса
        form = RegisterForm(request.POST)

        # Проверяем валидность (логин, пароль и т.д.)
        if form.is_valid():
            # 🔥 СОЗДАЁМ И СОХРАНЯЕМ пользователя в БД
            user = form.save()

            # 🔐 Сразу логиним пользователя (создаётся сессия)
            login(request, user)

            # Перенаправляем на главную страницу
            return redirect('home')

    # Если GET или ошибка — показываем форму
    return render(request, 'register.html', {'form': form})


# 🔹 ЛОГИН
def login_view(request):
    # Если пользователь уже вошёл — отправляем на главную
    if request.user.is_authenticated:
        return redirect('home')

    # Переменная для ошибки
    error = None

    # Если отправили форму
    if request.method == 'POST':

        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 🔍 Проверяем: есть ли такой пользователь и правильный ли пароль
        user = authenticate(request, username=username, password=password)

        # Если пользователь найден
        if user is not None:

            # 🔐 Логиним (создаётся сессия)
            login(request, user)

            # Редирект
            return redirect('home')
        else:
            # Ошибка, если данные неверные
            error = 'Invalid username or password'

    # Показываем страницу логина
    return render(request, 'login.html', {'error': error})


# 🔹 ГЛАВНАЯ СТРАНИЦА (только для залогиненных)
@login_required
def home_view(request):
    # Если не залогинен → Django сам редиректит на login
    return render(request, 'home.html', {'user': request.user})


# 🔹 ВЫХОД
def logout_view(request):
    # 🚪 Удаляет сессию пользователя (разлогинивает)
    logout(request)

    # Перенаправляет на страницу логина
    return redirect('login')

@login_required
def profile_view(request):
    # request.user уже есть благодаря AuthenticationMiddleware
    return render(request, 'profile.html', {'user': request.user})