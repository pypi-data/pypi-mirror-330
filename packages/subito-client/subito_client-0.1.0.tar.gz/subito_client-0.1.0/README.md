# نحوه نصب

```bash
pip install subito-client
```
یا اگر دوست داشتید میتونید مستقیم از گیتهاب دانلود کنید:
```bash
git clone https://github.com/null3yte/subito-client.git
cd subito-client
pip install -e .
```

# نحوه استفاده
## 1. code
```python
from subito_client import translate
import asyncio

# در حال حاضر فقط ass و srt پشتیبانی میشه
# بجز فایل میتونید مسیر پوشه هم بدید
file_path = "path/to/your/file.ass"

# توصیه میشه بجای هاردکد کردن توکن، از environment variable استفاده کنید که     جلوتر توضیح میدیم نحوه ست کردنش رو
user_token = "your_user_token" 

# بصورت دیفالت None تعریف شده که یعنی بدون محدودیت هزینه هست و هر فایلی با هر   حجمی و قیمتی رو ترجمه میکنه.
max_price = 100_000 # optional

result_path = asyncio.run(translate(path=file_path, token=user_token, max_price=max_price))
```

## 2. cli
```bash
subito <file_path> [-t TOKEN] [-P MAX_PRICE] [-p PREFIX]

# Options:
#   -t, --token        Authentication token (default: $SUBITO_TOKEN)
#   -P, --max-price    Maximum acceptable price in toman
#   -p, --prefix       Filename prefix for translations (default: "_ fa - ")
```

# تنظیم توکن
برای اینکه لازم نباشه هر بار توکن رو وارد کنید، میتونید اون رو بصورت Environment Variable تنظیم کنید:

### Linux/macOS
برای bash:
```bash
echo 'export SUBITO_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

برای zsh:
```bash
echo 'export SUBITO_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

### Windows
از طریق Command Prompt با دسترسی Administrator بنویسید:
```cmd
setx SUBITO_TOKEN "your_token_here"
```

***بعد از تنظیم SUBITO_TOKEN، دیگه نیازی نیست موقع استفاده از CLI یا کد، توکن رو مستقیم وارد کنید.***

