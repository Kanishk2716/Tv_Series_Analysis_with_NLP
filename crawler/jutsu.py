import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'narutospider'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        # Loop through the Jutsu links
        for href in response.css('.smw-columnlist-container')[0].css("a::attr(href)").extract():
            extracted_data = scrapy.Request("https://naruto.fandom.com" + href,
                                            callback=self.parse_jutsu)    
            yield extracted_data

        # Follow next page link if present
        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)
    
    def parse_jutsu(self, response):
        jutsu_name = response.css("span.mw-page-title-main::text").get().strip()

        div_selector = response.css("div.mw-parser-output")
        if not div_selector:
            return  # Skip if the expected structure isn't present
        
        div_html = div_selector.extract_first()
        soup = BeautifulSoup(div_html, 'html.parser')

        # Extract classification/type if available
        jutsu_type = ""
        aside = soup.find('aside')
        if aside:
            for cell in aside.find_all('div', {'class': 'pi-data'}):
                if cell.find('h3') and cell.find('h3').text.strip() == "Classification":
                    jutsu_type = cell.find('div').text.strip()

            # Remove the 'aside' section from soup to avoid including it in description
            aside.decompose()

        # Extract the Jutsu description, removing unwanted text like 'Trivia'
        jutsu_description = soup.get_text().split('Trivia')[0].strip()

        # Return the extracted data as a dictionary
        return {
            'jutsu_name': jutsu_name,
            'jutsu_type': jutsu_type,
            'jutsu_description': jutsu_description
        }
