# Импортируем необходимые модули Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Создаём форму регистрации, наследуясь от стандартной
class RegisterForm(UserCreationForm):
    # Добавляем поле email (обязательное)
    email = forms.EmailField(required=True)

    # Настройки формы
    class Meta:
        model = User  # Используем модель пользователя Django

        # Поля, которые будут отображаться в форме
        fields = ['username', 'email', 'password1', 'password2']

    # Переопределяем метод сохранения
    def save(self, commit=True):
        # Создаём объект пользователя, но не сохраняем его в БД
        user = super().save(commit=False)

        # Записываем email из формы в объект пользователя
        user.email = self.cleaned_data['email']

        # Если commit=True → сохраняем в базу данных
        if commit:
            user.save()

        # Возвращаем пользователя
        return user