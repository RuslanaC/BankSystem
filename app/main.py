import tkinter as tk
from tkinter import messagebox


# ------------------------------
#     Простая "база данных"
# ------------------------------
# username: {"password": "...", "phone": "...", "balance": ..., "history": []}
users = {}


# Цвета интерфейса
BG_COLOR = "#001f3f"      # темно-синий
BUTTON_COLOR = "#00b3b3"  # бирюзовый
TEXT_COLOR = "white"
BALANCE_COLOR = "#c084fc"  # сиреневый


# Основной шрифт
FONT_MAIN = ("Century Gothic", 14)
FONT_TITLE = ("Century Gothic", 22)
FONT_BIG = ("Century Gothic", 20)


# ------------------------------
#        Главное приложение
# ------------------------------
class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛанаБанк")
        self.geometry("600x500")
        self.configure(bg=BG_COLOR)

        self.current_user = None
        self.frames = {}

        for F in (
            StartMenu, LoginPage, RegisterPage, MainMenu,
            TransferPage, PaymentPage, HistoryPage, BalancePage
        ):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(StartMenu)

    def show(self, frame_class):
        self.frames[frame_class].tkraise()

    def back(self):
        self.show(MainMenu)


# ------------------------------
#   Функция для красивых кнопок
# ------------------------------
def make_button(master, text, cmd):
    return tk.Button(
        master, text=text, width=25, command=cmd,
        bg=BUTTON_COLOR, fg="black",
        font=FONT_MAIN, relief="raised",
        activebackground="#00cccc"
    )


# ------------------------------
#        ЭКРАН: стартовое меню
# ------------------------------
class StartMenu(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)
        tk.Label(self, text="ЛанаБанк", font=("Century Gothic", 28),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=40)

        make_button(self, "Войти", lambda: app.show(LoginPage)).pack(pady=10)
        make_button(self, "Регистрация", lambda: app.show(RegisterPage)).pack(pady=10)
        make_button(self, "Выход", app.destroy).pack(pady=10)


# ------------------------------
#        ЭКРАН: вход
# ------------------------------
class LoginPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)
        tk.Label(self, text="Вход", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)

        tk.Label(self, text="Логин", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.username = tk.Entry(self, font=FONT_MAIN)
        self.username.pack()

        tk.Label(self, text="Пароль", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.password = tk.Entry(self, show="*", font=FONT_MAIN)
        self.password.pack()

        make_button(self, "Войти", self.login).pack(pady=15)
        make_button(self, "Назад", lambda: app.show(StartMenu)).pack()

        self.app = app

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in users and users[user]["password"] == pwd:
            self.app.current_user = user
            messagebox.showinfo("Добро пожаловать", f"Здравствуйте, {user}!")
            self.app.show(MainMenu)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")


# ------------------------------
#     ЭКРАН: регистрация
# ------------------------------
class RegisterPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="Регистрация", font=FONT_TITLE,
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)

        tk.Label(self, text="Логин", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.username = tk.Entry(self, font=FONT_MAIN)
        self.username.pack()

        tk.Label(self, text="Пароль", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.password = tk.Entry(self, show="*", font=FONT_MAIN)
        self.password.pack()

        tk.Label(self, text="Телефон (для переводов)", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.phone = tk.Entry(self, font=FONT_MAIN)
        self.phone.pack()

        make_button(self, "Создать аккаунт", self.register).pack(pady=20)
        make_button(self, "Назад", lambda: app.show(StartMenu)).pack()

    def register(self):
        user = self.username.get()
        pwd = self.password.get()
        phone = self.phone.get()

        if user in users:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
            return

        if not phone.isdigit() or len(phone) < 5:
            messagebox.showerror("Ошибка", "Телефон должен содержать только цифры")
            return

        users[user] = {
            "password": pwd,
            "phone": phone,
            "balance": 200_000,  # ⬅ новый дефолтный баланс
            "history": []
        }

        messagebox.showinfo("Успех", "Регистрация завершена!")
        self.master.show(StartMenu)


# ------------------------------
#       ЭКРАН: главное меню
# ------------------------------
class MainMenu(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="Главное меню", font=FONT_TITLE,
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)

        make_button(self, "Проверить баланс", lambda: app.show(BalancePage)).pack(pady=10)
        make_button(self, "Перевести средства", lambda: app.show(TransferPage)).pack(pady=10)
        make_button(self, "Оплата услуг", lambda: app.show(PaymentPage)).pack(pady=10)
        make_button(self, "История операций", lambda: app.show(HistoryPage)).pack(pady=10)
        make_button(self, "Выход в начало", lambda: app.show(StartMenu)).pack(pady=10)


# ------------------------------
#        ЭКРАН: баланс
# ------------------------------
class BalancePage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="Ваш баланс", font=FONT_TITLE,
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=40)

        self.label = tk.Label(self, text="", font=("Century Gothic", 28),
                              bg=BG_COLOR, fg=BALANCE_COLOR)
        self.label.pack(pady=20)

        make_button(self, "Назад", app.back).pack()

        self.app = app

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        user = self.app.current_user
        balance = users[user]["balance"]
        self.label.config(text=f"{balance:,.2f} ₽".replace(",", " "))


# ------------------------------
#    ЭКРАН: перевод средств
# ------------------------------
class TransferPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="Перевод по номеру телефона",
                 font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)

        tk.Label(self, text="Номер телефона:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.phone = tk.Entry(self, font=FONT_MAIN)
        self.phone.pack()

        tk.Label(self, text="Сумма:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.amount = tk.Entry(self, font=FONT_MAIN)
        self.amount.pack()

        make_button(self, "Перевести", self.transfer).pack(pady=20)
        make_button(self, "Назад", app.back).pack()

        self.app = app

    def transfer(self):
        user = self.app.current_user
        phone = self.phone.get()
        amount = float(self.amount.get())

        target = None
        for uname, data in users.items():
            if data["phone"] == phone:
                target = uname
                break

        if not target:
            messagebox.showerror("Ошибка", "Пользователь с таким телефоном не найден")
            return

        if users[user]["balance"] < amount:
            messagebox.showerror("Ошибка", "Недостаточно средств")
            return

        users[user]["balance"] -= amount
        users[target]["balance"] += amount

        users[user]["history"].append(f"Перевод {amount} ₽ пользователю {target}")
        users[target]["history"].append(f"Получено {amount} ₽ от {user}")

        messagebox.showinfo("Успех", "Перевод выполнен!")


# ------------------------------
#         ЭКРАН: Оплата
# ------------------------------
class PaymentPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="Оплата услуг", font=FONT_TITLE,
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)

        tk.Label(self, text="Тип услуги:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.service = tk.Entry(self, font=FONT_MAIN)
        self.service.pack()

        tk.Label(self, text="Сумма:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_MAIN).pack()
        self.amount = tk.Entry(self, font=FONT_MAIN)
        self.amount.pack()

        make_button(self, "Оплатить", self.pay).pack(pady=20)
        make_button(self, "Назад", app.back).pack()

        self.app = app

    def pay(self):
        user = self.app.current_user
        service = self.service.get()
        amount = float(self.amount.get())

        if users[user]["balance"] < amount:
            messagebox.showerror("Ошибка", "Недостаточно средств")
            return

        users[user]["balance"] -= amount
        users[user]["history"].append(f"Оплата услуги '{service}' на {amount} ₽")

        messagebox.showinfo("Успех", "Оплата успешно проведена!")


# ------------------------------
#       ЭКРАН: История
# ------------------------------
class HistoryPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)

        tk.Label(self, text="История операций", font=FONT_TITLE,
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)

        self.text = tk.Text(self, width=60, height=15, font=FONT_MAIN)
        self.text.pack()

        make_button(self, "Назад", app.back).pack(pady=10)

        self.app = app

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        user = self.app.current_user
        self.text.delete(1.0, tk.END)
        for record in users[user]["history"]:
            self.text.insert(tk.END, record + "\n")


# ------------------------------
#            RUN
# ------------------------------
if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
