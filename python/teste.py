# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# pip install get-chrome-driver
from get_chrome_driver import GetChromeDriver



print('Irá buscar dados de séries no Bacen...')

bacen_localiza_series = 'https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries'

chrome_options = webdriver.ChromeOptions()

## faz com que o browser não abra durante o processo
#chrome_options.add_argument("--headless") 

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Download do ChromeDriver para a versão do Chrome instalada na maquina
#get_driver = GetChromeDriver()
# Adiciona o ChromeDriver baixado para path
#get_driver.install()


## caminho para o seu webdriver
p = 'C:\\Users\\guilh\\OneDrive\\workspace-psi-sucri\\chromedriver\\101.0.4951.41\\bin'
#p = 'C:\\Users\\guilh\\OneDrive\\workspace-psi-sucri\\chromedriver'
driver = webdriver.Chrome(p +'\\chromedriver.exe', options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options)



# configuração do fluent wait do selenium para aguardar carregamento das telas
wait = WebDriverWait(driver, 30)

driver.get(bacen_localiza_series)

WebDriverWait(driver, 10).until(EC.alert_is_present())
driver.switch_to.alert.accept()


# Lista de xpaths usados para encontrar elementos na pagina
xpath_botao_pesquisa_avancada = '//span[contains(., "Pesquisa Avançada")]'
xpath_checkbox_pesquisar_todos = '//input[@name="chkClassificacao"]'
xpath_botao_pesquisar = '//input[@title="Pesquisar"]'
xpath_botao_visualizar_impressao = '//a/img[@alt="Visualizar Impressão"]'
xpath_botao_series_desativadas = '//td/span[contains(., "Séries desativadas")]'

wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_pesquisa_avancada))).click()

driver.switch_to.frame(driver.find_element_by_id('iCorpo'))

wait.until(EC.element_to_be_clickable((By.XPATH, xpath_checkbox_pesquisar_todos))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_pesquisar))).click()


wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_visualizar_impressao))).click()


janela_principal = driver.window_handles[0]
janela_impressao = driver.window_handles[1]



driver.switch_to.window(janela_impressao)


bs = BeautifulSoup(driver.page_source, 'html.parser')

titulos = bs.find('tr', {'class': 'fundoPadraoAEscuro3'})
descricoes = titulos.findChildren("th")
for titulo in descricoes:
    print(titulo['title'])


linhas = bs.find_all('tr', {'class':'fundoPadraoAClaro3'})
print(len(linhas))
colunas = linhas[0].findChildren("td")
for i in colunas:
    print(i.text)
    
    
todas_series = []
for l in linhas:
    linha = []
    colunas = l.findChildren("td")
    for i in colunas:
        linha.append(i.text)
    todas_series.append(linha)
    
    
    
driver.close()

driver.switch_to.window(janela_principal)


wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_series_desativadas))).click()

driver.switch_to.frame(driver.find_element_by_id('iCorpo'))

wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_visualizar_impressao))).click()


janela_impressao = driver.window_handles[1]
driver.switch_to.window(janela_impressao)


bs = BeautifulSoup(driver.page_source, 'html.parser')

titulos = bs.find('tr', {'class': 'fundoPadraoAEscuro3'})
descricoes = titulos.findChildren("th")
for titulo in descricoes:
    print(titulo['title'])


linhas = bs.find_all('tr', {'class':'fundoPadraoAClaro3'})
print(len(linhas))
colunas = linhas[0].findChildren("td")
for i in colunas:
    print(i.text)
    
    
    
series_desativadas = []
for l in linhas:
    linha = []
    colunas = l.findChildren("td")
    for i in colunas:
        linha.append(i.text)
    series_desativadas.append(linha)


for serie in todas_series:
    if serie in series_desativadas:
        serie.append('Desativada')
    else:
        serie.append('Ativa')

# check = True
# for des in series_desativadas:
#     tem = False
#     for serie in todas_series:
#         if des[0] == serie[0]:
#             tem = True
#     if not tem:
#         check = False
#         print(des)

# print(check)
# # True
    
