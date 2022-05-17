from datetime import datetime

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

from models import SeriesModel


URL_BACEN_SERIES = 'https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries'

# Lista de xpaths usados para encontrar elementos na pagina
XPATH_BOTAO_PESQUISA_AVANCADA = '//span[contains(., "Pesquisa Avançada")]'
XPATH_CHECKBOX_PESQUISAR_TODOS = '//input[@name="chkClassificacao"]'
XPATH_BOTAO_PESQUISAR = '//input[@title="Pesquisar"]'
XPATH_BOTAO_VISUALIZAR_IMPRESSAO = '//a/img[@alt="Visualizar Impressão"]'
XPATH_BOTAO_SERIES_DESATIVADAS = '//td/span[contains(., "Séries desativadas")]'


def inicializaDriverChrome():
    chrome_options = Options()

    ## faz com que o browser não abra durante o processo
    chrome_options.add_argument("--headless") 
    
    # Download do ChromeDriver para a versão do Chrome instalada na maquina
    get_driver = GetChromeDriver()
    # Adiciona o ChromeDriver baixado para path
    try:
        get_driver.install()
    except:
        print('webdriver já está instalado')
    


    ## caminho para o um ChromeDriver baixado manualmente - caso o ambiente não permita baixar automaticamente
    # p = 'C:\\Users\\guilh\\OneDrive\\workspace-psi-sucri\\chromedriver\\chromedriver.exe'
    # driver = webdriver.Chrome(p, options=chrome_options)
    
    ## Instalação de ChromeDriver baixado automaticamente pelo get_driver
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def clicaAlertComecoTela(driver):
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    
    

def buscaTodasSeriesNaPaginaBuscaAvancada(driver, wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_PESQUISA_AVANCADA))).click()
    driver.switch_to.frame(driver.find_element_by_id('iCorpo'))
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CHECKBOX_PESQUISAR_TODOS))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_PESQUISAR))).click()
    
    
def buscaTodasSeriesDesativadas(driver, wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_SERIES_DESATIVADAS))).click()
    driver.switch_to.frame(driver.find_element_by_id('iCorpo'))


def recuperaDadosJanelaImpressao(driver, wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_VISUALIZAR_IMPRESSAO))).click()
    janela_principal = driver.window_handles[0]
    janela_impressao = driver.window_handles[1]
    driver.switch_to.window(janela_impressao)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    linhas = bs.find_all('tr', {'class':'fundoPadraoAClaro3'})
    driver.close()
    driver.switch_to.window(janela_principal)
    return linhas


def executaBuscaSeries():
    print('Irá buscar dados de séries no Bacen...')

    driver = inicializaDriverChrome()

    # configuração do fluent wait do selenium para aguardar carregamento das telas
    wait = WebDriverWait(driver, 50)
    
    # Inicializa Pagina
    driver.get(URL_BACEN_SERIES)
    
    clicaAlertComecoTela(driver)

    buscaTodasSeriesNaPaginaBuscaAvancada(driver, wait)
    
    linhas = recuperaDadosJanelaImpressao(driver, wait)

    # Salva todas series num array
    todas_series = []
    mapa_series = {}
    for l in linhas:
        colunas = l.findChildren("td")
        linha = SeriesModel(
            int(colunas[0].text), 
            colunas[1].text, 
            colunas[2].text, 
            colunas[3].text, 
            datetime.strptime(colunas[4].text, "%d/%m/%Y"), 
            colunas[5].text, 
            colunas[6].text, 
            colunas[7].text, 
            'Ativa'
        )
        todas_series.append(linha)
        mapa_series[linha.codigo] = linha
        
    buscaTodasSeriesDesativadas(driver, wait)
               
    linhas = recuperaDadosJanelaImpressao(driver, wait)
  
    # Salva todas series desativadas com o status de 'Desativada'    
    for l in linhas:
        colunas = l.findChildren("td")
        if int(colunas[0].text) in mapa_series:
            mapa_series[int(colunas[0].text)].status = 'Desativada'
        else:
            print('Serie Não Encontrada', colunas)
    
    print('Terminou de Carregar dados do Bacen, encontrou', len(todas_series), 'séries...')
    
    return todas_series


if __name__ == '__main__':
    executaBuscaSeries()