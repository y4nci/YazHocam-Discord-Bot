import requests
from bs4 import BeautifulSoup


def getlinks():
    link_template = "https://yazhocam.com/category/one-cikanlar/"
    source = requests.get(link_template)
    content = BeautifulSoup(source.content, "lxml")
    pages_info = content.find("span", attrs={"class": "pages"})
    num = pages_info.text
    total_pages = int(num.split(" ")[0])

    print(f"{total_pages} pages were found.")

    file = open("links.txt", "w", encoding="utf-8")

    for page in range(1, total_pages + 1):
        page_link = link_template + "page/" + str(page)
        page_source = requests.get(page_link)
        page_content = BeautifulSoup(page_source.content, "lxml")
        link_blocks = page_content.find_all("div", attrs={"class": "td-module-meta-holder"})

        for link_block in link_blocks:
            link = link_block.find("a")

            if "coz-hocam" not in link.get("href"):  # Those are quizzes and doesn't include any important quotes.
                file.write(link.get("href") + "\n")

        print(f"{page}/{total_pages}")

    file.close()

    print("done\n")


def getarchive():
    links_txt = open("links.txt", "r", encoding="utf-8")
    rawlinks = links_txt.readlines()
    links_txt.close()
    links = [rawlink[:-1] for rawlink in rawlinks]
    length = len(links)

    yazhocam = open("archive", "w", encoding="utf-8")
    index = 0
    line_number = 0

    print(f"{length} links were found.")

    for link in links:
        comments = []
        data = requests.get(link)

        if data.status_code == 200:
            index += 1

        elif data.status_code == 404:
            print(f"an error occurred while getting the data. link number = {index}")
            index += 1

        texts = BeautifulSoup(data.content, "lxml").find_all("p")
        comment_blocks = BeautifulSoup(data.content, "lxml").find_all("div", attrs={"class": "comment-content"})

        for comment_block in comment_blocks:
            comment = comment_block.find("p").text
            comments.append(comment)

        for text in texts:
            if text.text in ["Kaynakça", "KAYNAKÇA", "Kaynakça:", "KAYNAKÇA:",
                             " Bir dahaki sefere yorum yaptığımda kullanılmak üzere adımı, e-posta adresimi ve web site adresimi bu tarayıcıya kaydet."] \
                    or text.text in comments:
                break

            elif text.text in ["", " ", " ", "\n"]:
                pass

            elif text.text.count("\n") != 0:
                line_number += 1
                yazhocam.write(text.text.replace("\n", " ") + "\n")

            elif text.text[-1] == "." or text.text[-1] == "?" or text.text[-1] == "!":
                line_number += 1
                yazhocam.write(text.text + "\n")

        yazhocam.write(link + "\n")
        line_number += 1
        print(f"{index}/{length}")

    yazhocam.close()

    print("done")


getlinks()
getarchive()
