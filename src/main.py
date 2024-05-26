from Scraper import Scraper

sc = Scraper()

sc.authenticateWithQRCode()

# sc.coletarEtiquetas()

contatos = sc.coletarContatos(5)

print(f'erros: {sc.enviarMensagem(contatos, "abc")}')
