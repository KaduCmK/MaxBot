from Scraper import Scraper

sc = Scraper()

sc.authenticateWithQRCode()

contatos = sc.coletarContatos(2)

sc.enviarMensagem(contatos, "abc")