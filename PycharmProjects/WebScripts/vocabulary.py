import urllib.parse
import urllib.request


if __name__=='__main__':
    # wordeeee = "eeeeeeeeeeee"
    # word = "safe"
    # link = "https://s3.amazonaws.com/audio.oxforddictionaries.com/en/mp3/{}_gb_1.mp3".format(word)
    # token = urllib.parse.urlparse(link)
    #
    #
    # invalid_url = "https://s3.amazonaws.com/audio.oxforddictionaries.com/en/mp3/{}_gb_1.mp3".format(wordeeee)
    # valid_url = "https://s3.amazonaws.com/audio.oxforddictionaries.com/en/mp3/{}_gb_1.mp3".format(word)
    # tokens = [urllib.parse.urlparse(url) for url in (invalid_url, valid_url)]
    #
    # for token in tokens:
    #     print(token)
    #
    # min_attributes = ('scheme', 'netloc')  # add attrs to your liking
    # for token in tokens:
    #     if not all([getattr(token, attr) for attr in min_attributes]):
    #         error = "'{url}' string has no scheme or netloc.".format(url=token.geturl())
    #         print(error)
    #     else:
    #         print("'{url}' is probably a valid url.".format(url=token.geturl()))
    link = "https://tproger.ru/articles/regexp-for-beginners/?" \
           "utm_source=grf-eng&utm_medium=partner&utm_campaign=giraff.io"
    req = urllib.request.Request(link)
    webpage = urllib.request.urlopen(req).read()
    print(webpage)



