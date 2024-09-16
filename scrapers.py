import requests
import re
import time
import pandas as pd


class SpodeliScraper:

    def get_story_paragraphs(self, url):
        req = requests.get(url)
        stories = re.findall(
            r'<p style="line-height.*?</p>', req.text, re.DOTALL)
        story = re.findall(r'<span style="line-height.*?</span>',
                           stories[0], re.DOTALL)
        paragraphs = re.findall(
            r'<span style="line-height:150%;">.*?<br />', story[0])
        paragraphs += re.findall(r'\n.*?<br />', story[0])
        paragraphs += re.findall(r'\n.*?</span>', story[0])
        paragraphs += re.findall(
            r'<span style="line-height:150%;">.*</span>', story[0])
        title = re.findall(r'<span class="t16b".*</span>', stories[0])[0].replace(
            '<span class="t16b" style="font-family: Georgia">', '').replace('</span>', '')
        return (title, [paragarph.replace('<span style="line-height:150%;">', "")
                        .replace('<br />', "")
                        .replace('\n', "")
                        .replace('</span>', "") for paragarph in paragraphs])

    def get_urls_at(self, url):
        req = requests.get(url)
        page = req.text
        page_list = re.findall(r'<ol.*?</ol>', page, re.DOTALL)[0]
        elements_with_urls = re.findall(r'<a href=".*?</a>', page_list)
        return [re.findall('http://.*html', element)[0] for element in elements_with_urls]

    def extract_post_info(self, list_urls, output_file='urls.csv'):

        urls = []
        for url in list_urls:
            post_urls = self.get_urls_at(url)
            for post_url in post_urls:
                time.sleep(20)
                title, paragraphs = self.get_story_paragraphs(post_url)
                urls.append([title, post_url, len('\n'.join(paragraphs)), len(
                    paragraphs)]+[len(paragraph) for paragraph in paragraphs])
        df = pd.DataFrame(urls)
        df.columns = ['tile', 'URL',
                      'length', 'paragraphs']+[f'paragraph{i}Length' for i in range(len(df.columns)-4)]
        df.to_csv(output_file)
        return df
