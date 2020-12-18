import os
import sys
import math

import asyncio
import aiofiles
import tqdm.asyncio
from aiohttp import ClientSession


class Scraper:
    def __init__(self, query):
        self.query = query
        self.url = f'https://unsplash.com/napi/search/photos?query={query}'
        self.images_count = None
        self.create_folder()

    def create_folder(self):
        """ Create a folder called images and a sub folder named like the query """
        path = os.path.join(os.getcwd(), 'images', self.query)
        if not os.path.isdir(path):
            os.makedirs(path)

    async def get_images_count(self, url):
        """ Return the amount of images found for a query """
        print(f"Searching for '{self.query}'...", end='\r')

        content = await self.fetch_page(url)
        images_count = content['total']

        print(f"The query '{self.query}' returned {images_count} images")
        return images_count

    async def fetch_page(self, page_num=1):
        """ Asynchronously fetch a single page, which contain the images info. Returns a JSON response."""
        async with asyncio.Semaphore(10):
            async with ClientSession() as session:
                params = {'per_page': '20', 'page': page_num}
                async with session.get(self.url, params=params) as response:
                    return await response.json()

    async def download_images(self, page, pbar, sem):
        """ Download every image contained by a page. """
        images = page['results']
        tasks = []

        for image in images:
            # The download takes a looooong time, the 'raw' images are really heavy.
            # Change it to 'regular' for faster download times.
            url = image['urls']['raw']

            if image['description']:
                name = image['description']
            elif image['alt_description']:
                name = image['alt_description']
            else:
                name = image['id']

            # Remove any illegal filename characters.
            name = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
            # Limit name length.
            name = name[:100]

            tasks.append(asyncio.create_task(self.fetch_image(url, name, pbar, sem)))

        await asyncio.gather(*tasks)

    async def fetch_image(self, url, name, pbar, sem):
        """ Asynchronously fetch a single image and write it to a file."""
        async with sem, ClientSession() as session:
            async with session.get(url) as response:
                img_data = await response.read()
                await self.write_to_disk(name, img_data)
                pbar.update(1)

    async def write_to_disk(self, name, image):
        """ Write the downloaded image into the corresponding folder """
        path = os.path.join('images', self.query, name + '.jpeg')
        f = await aiofiles.open(path, mode='wb')
        await f.write(image)
        await f.close()


async def main():
    query = sys.argv[1]
    scraper = Scraper(query)
    scraper.images_count = await scraper.get_images_count(scraper.url)

    if scraper.images_count < 1:
        print("\nSorry, that query did not returned any result. Exiting...")
        exit()

    # I divide and round up the total amount of images per the amount of imager per page,
    # getting the total amount of pages.
    pages = math.ceil(scraper.images_count / 20)

    # I get every page which contains the JSON with the image's links.
    print("Getting images links...")
    tasks = [asyncio.create_task(scraper.fetch_page(page)) for page in range(pages)]
    content_pages = []
    for task in tqdm.asyncio.tqdm.as_completed(tasks, file=sys.stdout, colour='green'):
        content_pages.append(await task)

    # I start downloading the images.
    print("\nDownloading images. Feel free to grab a cup of coffee, this will take a while...")
    # The server greatly limits the amount of simultaneous requests I can make, it also really slows down the downloads
    # when I open too many connections. So I create a semaphore and pass it to each download_images method, which will
    # pass it to the fetch_image method, preventing the creation of thousands of connections.
    sem = asyncio.Semaphore(15)

    with tqdm.tqdm(total=scraper.images_count, file=sys.stdout, colour='green') as progressbar:
        async with sem:
            tasks = [asyncio.create_task(scraper.download_images(page, progressbar, sem)) for page in content_pages]
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
