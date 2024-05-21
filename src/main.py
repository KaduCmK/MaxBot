from Scraper import Scraper

sc = Scraper()

sc.authenticateWithQRCode()

print(sc.coletarContatos(20))