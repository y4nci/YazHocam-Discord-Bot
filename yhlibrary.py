import requests
from bs4 import BeautifulSoup

# erase() is a function whose job is to clear the file "author".
#
# ascii() is a function which helps us to get rid of Turkish characters, it is crucial for getting the links.
#
# getauthor(author) is the main function that returns the top 10 most used words of the given author.
#
# whichtext(author) finds the article which the bot has generated a quote from.


def erase():
    with open("author", "w", encoding="utf-8") as file:
        file.write("")


def ascii(txt):
    _dict_ = {"ö": "o", "ü": "u", "ğ": "g", "ç": "c", "ş": "s", "ı": "i"}

    for char in _dict_:
        if char in txt:
            txt = txt.replace(char, _dict_[char])

    return txt


def getauthor(author):
    output = f"{author}\n\n************************************************"
    author = author.lower()
    author = ascii(author)
    author = author.replace(" ", "")

    error_message = "\nAradığın içeriğe ulaşamadım. Bunun nedeni şunlar olabilir:\n\n" \
                    "Adını girdiğin yazarın sitede hiç yazısı bulunmuyor olabilir.\n" \
                    "Yazısı bulunmasına rağmen adı farklı kaydedilmiş olabilir, bu durumda şunları deneyebilirsin:\n" \
                    "\tYazarın adını soyisim isim şeklinde girmek\n" \
                    "\tYazarın birden çok adı varsa sadece birini kullanmak\n" \
                    "\tYazarın adını Türkçe karakter kullanmadan girmek\n" \
                    "YazHocam yanıt vermiyor olabilir, halbuki hiç böyle yapmazdı..\n" \
                    "Bot düzgün çalışmıyor olabilir. Bu durumda üstün kabiliyetlere sahip ekibimiz sorunu çözecektir."

    soup = requests.get(f"https://yazhocam.com/author/{author}/")

    if soup.status_code == 404:
        return error_message  # The site isn't quite helping sometimes, but we should be.

    r = BeautifulSoup(soup.content, "lxml")
    links = r.find_all("div", attrs={"class": "td_module_1 td_module_wrap td-animation-stack"})  # To get the links of the articles written by given author.
    sources = []

    for link in links:

        reqs = link.find_all("h3", attrs={"class": "entry-title td-module-title"})

        for req in reqs:

            req = str(req)
            source = req[49:req.find("\" rel")]
            sources.append(source)
            output = output + "\n" + source + "\n\n************************************************"

    erase()

    def getarticles(args):
        for arg in args:
            data = requests.get(arg)
            content = BeautifulSoup(data.content, "lxml").find_all("div", attrs={"class": "td-post-content"})
            text = ""

            for t in content:

                text += t.text

            with open("author", "a", encoding="utf-8") as file:
                file.write(text)

    # To make things easier, this functions stores the article in a file named "author" and works on it.

    getarticles(sources)

    with open("author", "r", encoding="utf-8") as file:
        article = file.read()

    _database_ = ""
    nogo = ["\n", "-", "%", ",", ".", "/", "!", "?", ":", ";", "\t", "<", ">", "=", "^", "+", "&", "*", "(", ")", "[",
            "]", "{", "}", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "\"", "”", "–", "’"]  # To eliminate unwanted characters

    words = [word.lower() for word in article.split(" ") if word not in nogo]
    _w_, _wc_, _wb_ = [], [], []  # These are some valuables that will help us sorting the most used words.

    for i in words:
        if i != "" and _w_.count(i) != 1:
            _w_.append(i)
            _wc_.append(words.count(i))
            _wb_.append(words.count(i))

    _wc_.sort(reverse=True)
    index = 1

    output = output + "\n\n" + "Yazarın bağlaç edat vs. DAHİL en çok kullandığı 10 kelime:\n\n"

    # Here we are including conjunctions, prepositions etc.

    for i in _wc_[:10]:
        output = output + f"#{index} - {_w_[_wb_.index(i)]}: {i}\n"
        _w_.pop(_wb_.index(i))
        _wb_.pop(_wb_.index(i))
        index += 1

    _w_, _wc_, _wb_ = [], [], []

    garbage = ["", "ve", "veya", "ile", "ama", "de", "da", "ancak", "çünkü", "eğer", "hâlbuki", "hem", "hiç değilse",
               "ise", "ki", "lâkin", "meğer", "nasıl ki", "ne", "nasıl", "kim", "neden", "hiç", "hep", "öyle", "öyle ki",
               "sanki", "şu var ki", "üstelik", "yahut", "yalnız", "yani", "yoksa", "zira", "çünkü", "ile", "gibi", "için",
               "diye", "üzere", "kadar", "yalnız", "ancak", "karşın", "başka", "fakat", "dolayı", "ötürü", "beri", "göre",
               "bu", "şu", "o", "en"]

    # Now we will do another top 10 without conjunctions, prepositions etc.

    for word in words:
        if word not in garbage and _w_.count(word) != 1:
            _w_.append(word)
            _wc_.append(words.count(word))
            _wb_.append(words.count(word))

    _wc_.sort(reverse=True)
    index = 1

    output = output + "\nYazarın bağlaç edat vs. HARİÇ en çok kullandığı 10 kelime:\n\n"

    for i in _wc_[:10]:
        output = output + "#{} - {}: {}\n".format(index, _w_[_wb_.index(i)], i)
        _w_.pop(_wb_.index(i))
        _wb_.pop(_wb_.index(i))
        index += 1

    erase()

    return output


def whichtext(txt):

    # This function works like this: firstly it finds the index of the last message the bot sent -which is the part from
    # a randomly chosen article- and then finds the first link after that index and that link is the very link of the
    # article. See the file named yazhocam to understand it better.

    file = open("archive", "r", encoding="utf-8")
    texts = file.read()
    file.close()

    txtindex = texts.find(txt)

    if txtindex == -1:  # Error message
        return "Bulamadım :(. Unutma, bir kesit paylaştıktan sonra bu komut yazılmadan araya başka bir mesaj girerse" \
               " o yazıyı bulamam."

    linkindex = texts[txtindex:].find("https://yazhocam.com/")
    newlineindex = texts[txtindex + linkindex:].find("\n")

    return f"Aradığın yazı bu:\n{texts[txtindex + linkindex:txtindex + linkindex + newlineindex]}"
