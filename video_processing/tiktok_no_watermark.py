from aiogram import Bot
from bs4 import BeautifulSoup
import aiohttp

async def DownloadVideoTikTok(bot: Bot, link):
    # Нужные параметры
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'HX-Request': 'true',
        'HX-Trigger': '_gcaptcha_pt',
        'HX-Target': 'target',
        'HX-Current-URL': 'https://ssstik.io/ru',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ssstik.io',
        'Alt-Used': 'ssstik.io',
        'Connection': 'keep-alive',
        'Referer': 'https://ssstik.io/ru',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'ru',
        'tt': 'WmFOMWhh',
    }

    print("Getting the download link")

    # отправляем POST запрос сайту sstik.io для получение ссылки видео без водяных знаков
    async with aiohttp.ClientSession() as session:
        async with session.post('https://ssstik.io/abc', params=params, headers=headers, data=data) as response:
            response_text = await response.text()
            downloadSoup = BeautifulSoup(response_text, "html.parser")
            downloadLink = downloadSoup.a['href']

    return downloadLink
