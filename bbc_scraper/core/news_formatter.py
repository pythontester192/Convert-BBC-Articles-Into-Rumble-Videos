import json
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag as Element


class NewsFormatter:

    def format_articles(self, pages_html: List[str]):
        return [x for x in self._format_articles(pages_html)]

    def _format_articles(self, pages_html: List[str]) -> List[dict]:
        for html in pages_html:
            soup = BeautifulSoup(html, "html.parser")
            head = soup.find("head")
            if not head:
                continue
            is_article = head.find("meta", {"property": "og:type"}).get("content")
            if is_article != "article":
                continue
            try:
                info_element = head.find("script", {"type": "application/ld+json", "data-rh": "true"})
                info = json.loads(info_element.text)
                # General Info
                title = self.html_to_string(info["headline"])
                link = info["mainEntityOfPage"]
                thumbnail = info["thumbnailUrl"]
                desc = self.html_to_string(info["description"])
                source = {"name": "BBC News", "short": "BBC"}
                temp_time = info["datePublished"]
                published = temp_time[:10] + " " + temp_time[11:19]
                # Article
                articleElement = soup.find("article")
                storyElements = articleElement.find_all("div", {"data-component": "text-block"})
                article = "\n".join([self.html_to_string(x.text) for x in storyElements])
                # Author
                author = info["author"]["name"].replace("By ", "")
                # Tags
                temp_tags_list = soup.find("section", {"data-component": "tag-list"})
                if temp_tags_list:
                    tags = list()
                    for ele in temp_tags_list.find_all("li"):
                        if "," in ele.text:
                            second_temp_tag = [x.replace(" ", "-").lower() for x in ele.text.split(",")]
                            second_temp_tag = [x[1:] if x[0] == "-" else x for x in second_temp_tag]
                            tags += second_temp_tag
                        else:
                            tags.append(ele.text.replace(" ", "-").lower())
                else:
                    tags = link.split("/")[-1].split("-")[:-1]
                # Photos
                photo_elements = articleElement.find_all("div", {"data-component": "image-block"})
                photos = self._get_photos(photo_elements)
            except Exception as e:
                print(f"BBC formatter exception, {e}")
                continue

            article = {
                "title": title,
                "link": link,
                "desc": desc,
                "thumbnail": thumbnail,
                "source": source,
                "published": published,
                "article": article,
                "author": author,
                "tags": tags,
                "photos": photos}

            yield article

    @staticmethod
    def _get_photos(photo_elements: List[Element]) -> List[str]:
        photos = list()
        for element in photo_elements:
            try:
                img_url = element.find("img").get("src")
                photos.append(img_url)
            except:
                continue
        return photos

    @staticmethod
    def html_to_string(html: str) -> str:
        html_obj = BeautifulSoup(html, 'html.parser')
        text = html_obj.text.encode("ascii", "ignore").decode()
        return text
