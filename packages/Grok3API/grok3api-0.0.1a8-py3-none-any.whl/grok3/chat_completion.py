import json
import os
import shutil
import warnings


import subprocess
import sys
import time
from typing import Any

import requests
import urllib3

from grok3.grok3api_logger import logger
from grok3.types.GrokResponse import GrokResponse

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.by import By
except ImportError:
    uc = None


TIMEOUT = 45

def _start_xvfb_if_needed():
    """Запускает Xvfb, если он ещё не запущен, для работы Chrome без GUI на Linux."""
    if sys.platform.startswith("linux"):
        if shutil.which("google-chrome") is None and shutil.which("chrome") is None:
            logger.error("В _fetch_cookies: Chrome не установлен, не удается обновить куки. Установите Chrome.")
            return
        if shutil.which("Xvfb") is None:
            logger.warning("⚠ Xvfb не установлен! Он нужен при отсутствии GUI на вашем линукс. Установите его командой: sudo apt install xvfb")
            return

        result = subprocess.run(["pgrep", "-f", f"Xvfb :99"], capture_output=True, text=True)

        if not result.stdout.strip():
            logger.debug("Запускаем Xvfb...")
            os.system("Xvfb :99 -screen 0 800x600x8 >/dev/null 2>&1 &")

            for _ in range(5):
                time.sleep(2)
                result = subprocess.run(["pgrep", "-f", f"Xvfb :99"], capture_output=True, text=True)
                if result.stdout.strip():
                    logger.debug("В _start_xvfb_if_needed: Xvfb успешно запущен.")
                    os.environ["DISPLAY"] = ":99"
                    return
            logger.error("В _start_xvfb_if_needed: Xvfb не запустился! Проверьте установку.")
            os.environ["DISPLAY"] = ":99"
        else:
            logger.debug("В _start_xvfb_if_needed: Xvfb уже запущен.")
            os.environ["DISPLAY"] = ":99"

def _fetch_cookies(use_xvfb: bool, auto_close_xvfb: bool) -> str:
    """Получение cookies через undetected_chromedriver с обходом Cloudflare."""
    try:
        logger.debug("Пробуем получить новые куки...")
        if use_xvfb:
            _start_xvfb_if_needed()
        if uc is None:
            logger.error("В _fetch_cookies: undetected_chromedriver не установлен, не удается обновить куки. Попробуйте: pip install undetected_chromedriver")
            return ""

        uc.Chrome.__del__ = lambda self_obj: None

        logger.debug("В _fetch_cookies: Запуск браузера...")
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options, headless=False, use_subprocess=False)

        try:
            driver.minimize_window()
        except Exception as e:
            logger.debug(f"В _fetch_cookies: Не удалось свернуть окно: {e}")

        try:
            logger.debug("В _fetch_cookies: Переход на https://grok.com/")
            driver.get("https://grok.com/")

            logger.debug("В _fetch_cookies: Ожидаем появления поля ввода...")
            WebDriverWait(driver, 30).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "div.relative.z-10 textarea"))
            )
            logger.debug("В _fetch_cookies: Поле ввода обнаружено, ждём ещё 2 секунды...")
            time.sleep(2)

            cookies = driver.get_cookies()
            if not cookies:
                logger.warning("В _fetch_cookies: Куки не найдены, пробуем ещё раз через 3 секунды...")
                time.sleep(1)
                cookies = driver.get_cookies()

            cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            logger.info(f"В _fetch_cookies: Полученные куки: {cookie_string}")
            return cookie_string

        except Exception as e:
            logger.error(f"В _fetch_cookies: {e}")
            return ""
        finally:

            try:
                if auto_close_xvfb and sys.platform.startswith("linux"):
                    subprocess.run(["pkill", "Xvfb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            finally:
                pass

            if driver:
                try:
                    logger.debug("В _fetch_cookies: Закрытие браузера")
                    driver.quit()
                except Exception as e:
                    logger.debug(f"В _fetch_cookies: Ошибка при закрытии браузера: {e}")
    except Exception as e:
        logger.error(f"В _fetch_cookies: {e}")
        return ""

def _save_cookies_to_env(cookie_string, env_file=".env"):
    """Сохраняет строку cookies в .env файл без использования dotenv, гарантируя запись с новой строки."""
    try:
        if not cookie_string or not env_file or cookie_string is None:
            logger.debug("В _save_cookies_to_env: Пустая строка cookie_string или некорректный env_file")
            return

        if " " in cookie_string or "=" in cookie_string or ";" in cookie_string:
            cookie_string = f'"{cookie_string}"'

        lines = []
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'

        with open(env_file, "w", encoding="utf-8") as file:
            found = False
            for line in lines:
                if line.startswith("INCOGNITO_COOKIES="):
                    file.write(f"INCOGNITO_COOKIES={cookie_string}\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(f"INCOGNITO_COOKIES={cookie_string}\n")

        logger.debug(f"В _save_cookies_to_env: INCOGNITO_COOKIES сохранены в {env_file}")
    except Exception as e:
        logger.error(f"В _save_cookies_to_env: Ошибка при сохранении cookies: {e}")

def _get_cookies_from_env(env_file=".env") -> str:
    """
    Извлекает значение переменной INCOGNITO_COOKIES из .env файла.

    Если переменная найдена, возвращает её значение без окружающих кавычек,
    иначе возвращает пустую строку.
    """
    try:
        if not os.path.exists(env_file):
            logger.debug(f"В _get_cookies_from_env: Файл {env_file} не найден.")
            return ""

        with open(env_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("INCOGNITO_COOKIES="):
                cookie_value = line[len("INCOGNITO_COOKIES="):].strip()
                if (cookie_value.startswith('"') and cookie_value.endswith('"')) or \
                   (cookie_value.startswith("'") and cookie_value.endswith("'")):
                    cookie_value = cookie_value[1:-1]
                logger.debug("В _get_cookies_from_env: INCOGNITO_COOKIES успешно извлечены из .env файла.")
                return cookie_value

        logger.debug("В _get_cookies_from_env: INCOGNITO_COOKIES не найдены в .env файле.")
        return ""
    except Exception as e:
        logger.error(f"В _get_cookies_from_env: {e}")
        return ""


class ChatCompletion:
    BASE_URL = "https://grok.com/rest/app-chat/conversations/new"

    def __init__(self, cookies: str = "", use_xvfb: bool = True, auto_close_xvfb: bool = False):
        self.cookies = cookies
        self.use_xvfb = use_xvfb
        self.auto_close_xvfb = auto_close_xvfb

    def _send_request(self, payload, headers, base_url, auto_update_cookies, timeout=TIMEOUT):
        """
        Синхронный HTTP-запрос через requests с отключением проверки SSL.

        Args:
            payload: Данные для отправки в формате JSON.
            headers: Заголовки запроса.
            base_url: URL для отправки запроса.
            auto_update_cookies: Флаг для автоматического обновления cookies при ошибках 429 или 401.
            timeout: Таймаут запроса (по умолчанию TIMEOUT).

        Returns:
            dict: Обработанный ответ или пустой словарь в случае ошибки.
        """
        try:
            warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
            logger.debug(f"Отправляем запрос:\nheaders: {headers}\npayload: {payload}")
            response = requests.post(
                base_url,
                json=payload,
                headers=headers,
                timeout=timeout,
                verify=False
            )
            response.raise_for_status()
            text = response.text

            final_dict = {}
            for line in text.splitlines():
                try:
                    parsed = json.loads(line)
                    if "modelResponse" in parsed["result"]["response"]:
                        final_dict = parsed
                        break
                except (json.JSONDecodeError, KeyError):
                    continue

            logger.debug(f"Обработанный ответ: {final_dict}")
            return final_dict

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in (429, 401):
                logger.info("Ошибка HTTP-запроса: Too Many Requests или Unauthorized.")
                if auto_update_cookies:
                    logger.info("Пробуем обновить Cookies...")
                    self.cookies = _fetch_cookies(self.use_xvfb, self.auto_close_xvfb)
                    if self.cookies and self.cookies != "" and self.cookies is not None:
                        logger.info("Успешно! Пробуем повторить запрос...")
                        headers["Cookie"] = self.cookies
                        return self._send_request(payload, headers, base_url, False, timeout)
                    else:
                        logger.error("Не удалось обновить Cookies.")
                        return {}
                else:
                    logger.error(f"Ошибка HTTP-запроса: {e.response.status_code}")
                    return {}
            else:
                logger.error(f"Ошибка HTTP-запроса: {e.response.status_code}")
                return {}

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP-запроса: {str(e)}")
            return {}

        except Exception as e:
            # Обрабатываем любые другие ошибки в функции
            logger.error(f"В _send_request: {e}")
            return {}

    def create(self, message: str, **kwargs: Any) -> GrokResponse:
        """
        Отправляет запрос к API Grok с одним сообщением и дополнительными параметрами.

        Args:
            message (str): Сообщение пользователя для отправки в API.
            **kwargs: Дополнительные параметры для настройки запроса.

        Keyword Args:
            auto_update_cookies (bool): Обновлять ли cookies автоматически при необходимости. По умолчанию True.
            env_file (str): Путь к файлу окружения для сохранения cookies. По умолчанию ".env".
            timeout (int): Таймаут одного ожидания получения ответа. По умолчанию: 45
            temporary (bool): Указывает, является ли сессия или запрос временным. По умолчанию False.
            modelName (str): Название модели AI для обработки запроса. По умолчанию "grok-3".
            fileAttachments (List[Dict[str, str]]): Список вложений файлов. Каждое вложение — словарь с ключами "name" и "content".
            imageAttachments (List[Dict[str, str]]): Список вложений изображений. Аналогично fileAttachments.
            customInstructions (str): Дополнительные инструкции или контекст для модели. По умолчанию пустая строка.
            deepsearch preset (str): Пред установка для глубокого поиска. По умолчанию пустая строка. Передаётся через словарь.
            disableSearch (bool): Отключить функцию поиска модели. По умолчанию False.
            enableImageGeneration (bool): Включить генерацию изображений в ответе. По умолчанию True.
            enableImageStreaming (bool): Включить потоковую передачу изображений. По умолчанию True.
            enableSideBySide (bool): Включить отображение информации бок о бок. По умолчанию True.
            imageGenerationCount (int): Количество генерируемых изображений. По умолчанию 2.
            isPreset (bool): Указывает, является ли сообщение предустановленным. По умолчанию False. Передаётся через словарь.
            isReasoning (bool): Включить режим рассуждений в ответе модели. По умолчанию False. Передаётся через словарь.
            returnImageBytes (bool): Возвращать данные изображений в виде байтов. По умолчанию False.
            returnRawGrokInXaiRequest (bool): Возвращать необработанный вывод модели. По умолчанию False.
            sendFinalMetadata (bool): Отправлять финальные метаданные с запросом. По умолчанию True.
            toolOverrides (Dict[str, Any]): Словарь для переопределения настроек инструментов. По умолчанию пустой словарь.

        Returns:
            GrokResponse: Объект ответа от API Grok.
        """
        try:
            base_headers = {
                "Content-Type": "application/json",
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"),
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Origin": "https://grok.com",
                "Referer": "https://grok.com/",
            }

            headers = base_headers.copy()

            auto_update_cookies = kwargs.get("auto_update_cookies", True)
            env_file = kwargs.get("env_file", ".env")
            timeout = kwargs.get("timeout", TIMEOUT)

            payload = {
                "temporary": False,
                "modelName": "grok-3",
                "message": message,
                "fileAttachments": [],
                "imageAttachments": [],
                "customInstructions": "",
                "deepsearch preset": "",
                "disableSearch": False,
                "enableImageGeneration": True,
                "enableImageStreaming": True,
                "enableSideBySide": True,
                "imageGenerationCount": 2,
                "isPreset": False,
                "isReasoning": False,
                "returnImageBytes": False,
                "returnRawGrokInXaiRequest": False,
                "sendFinalMetadata": True,
                "toolOverrides": {}
            }

            excluded_keys = {"auto_update_cookie", "env_file", "timeout", message}
            filtered_kwargs = {}
            for key, value in kwargs.items():
                if key not in excluded_keys:
                    filtered_kwargs[key] = value

            payload.update(filtered_kwargs)

            if not self.cookies or self.cookies is None:
                self.cookies = _get_cookies_from_env(env_file)
                if not self.cookies or self.cookies is None:
                    self.cookies = _fetch_cookies(self.use_xvfb,self.auto_close_xvfb)

            headers["Cookie"] = self.cookies

            logger.debug(f"Grok payload: {payload}")

            response_json = self._send_request(payload, headers, self.BASE_URL, auto_update_cookies, timeout)

            if isinstance(response_json, dict):
                _save_cookies_to_env(self.cookies, env_file)
                return GrokResponse(response_json, self.cookies)

            logger.error("Ошибка: неожиданный формат ответа от сервера")
            return GrokResponse(response_json, self.cookies)
        except Exception as e:
            logger.error(f"В create: {e}")
            return GrokResponse({}, self.cookies)
