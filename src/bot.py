import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = "8543437954:AAFXlKNJxOrK36WAgVd8uoXOJu2x4sBPba0"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🧮 Привет! Я бот-калькулятор!

Я могу вычислять математические выражения.

Примеры:
• 2 + 2
• 10 * (5 - 3)
• 15 / 3
• 2 ** 8

Просто напиши математическое выражение!
    """
    await update.message.reply_text(welcome_text)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 Доступные операции:
+ сложение
- вычитание
* умножение
/ деление
** возведение в степень
() скобки

Пример: (10 + 5) * 2 / 3
    """
    await update.message.reply_text(help_text)

# Обработка математических выражений
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    try:
        # Безопасное вычисление выражения
        result = eval(user_message, {"__builtins__": {}}, {})

        # Форматируем результат
        if isinstance(result, (int, float)):
            if result == int(result):
                result = int(result)

            await update.message.reply_text(
                f"✅ Результат: {result}\n"
                f"Выражение: {user_message} = {result}"
            )
        else:
            await update.message.reply_text("❌ Я могу вычислять только числа!")

    except ZeroDivisionError:
        await update.message.reply_text("❌ Ошибка: Деление на ноль!")
    except SyntaxError:
        await update.message.reply_text("❌ Ошибка: Неправильный синтаксис!")
    except NameError:
        await update.message.reply_text("❌ Ошибка: Используй только числа и математические операторы!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

# Обработка неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Я понимаю только математические выражения! Используй /help для справки.")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик математических выражений (только текст с числами и операторами)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        calculate
    ))

    # Обработчик неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Запуск бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()