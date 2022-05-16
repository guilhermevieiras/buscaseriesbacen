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



def executaBuscaSeries():
    print('Irá buscar dados de séries no Bacen...')
    
    URL_BACEN_SERIES = 'https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries'

    chrome_options = Options()

    ## faz com que o browser não abra durante o processo
    chrome_options.add_argument("--headless") 
    
    # Download do ChromeDriver para a versão do Chrome instalada na maquina
    get_driver = GetChromeDriver()
    # Adiciona o ChromeDriver baixado para path
    get_driver.install()


    ## caminho para o um ChromeDriver baixado manualmente - caso o ambiente não permita baixar automaticamente
    # p = 'C:\\Users\\guilh\\OneDrive\\workspace-psi-sucri\\chromedriver\\chromedriver.exe'
    # driver = webdriver.Chrome(p, options=chrome_options)
    
    ## Instalação de ChromeDriver baixado automaticamente pelo get_driver
    driver = webdriver.Chrome(options=chrome_options)
    
    

    # configuração do fluent wait do selenium para aguardar carregamento das telas
    wait = WebDriverWait(driver, 30)
    
    driver.get(URL_BACEN_SERIES)

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()


    # Lista de xpaths usados para encontrar elementos na pagina
    XPATH_BOTAO_PESQUISA_AVANCADA = '//span[contains(., "Pesquisa Avançada")]'
    XPATH_CHECKBOX_PESQUISAR_TODOS = '//input[@name="chkClassificacao"]'
    XPATH_BOTAO_PESQUISAR = '//input[@title="Pesquisar"]'
    XPATH_BOTAO_VISUALIZAR_IMPRESSAO = '//a/img[@alt="Visualizar Impressão"]'
    XPATH_BOTAO_SERIES_DESATIVADAS = '//td/span[contains(., "Séries desativadas")]'

    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_PESQUISA_AVANCADA))).click()

    driver.switch_to.frame(driver.find_element_by_id('iCorpo'))

    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CHECKBOX_PESQUISAR_TODOS))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_PESQUISAR))).click()


    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_VISUALIZAR_IMPRESSAO))).click()


    janela_principal = driver.window_handles[0]
    janela_impressao = driver.window_handles[1]



    driver.switch_to.window(janela_impressao)


    bs = BeautifulSoup(driver.page_source, 'html.parser')

    # titulos = bs.find('tr', {'class': 'fundoPadraoAEscuro3'})
    # descricoes = titulos.findChildren("th")
    # for titulo in descricoes:
    #     print(titulo['title'])


    linhas = bs.find_all('tr', {'class':'fundoPadraoAClaro3'})
    # print(len(linhas))
    # colunas = linhas[0].findChildren("td")
    # for i in colunas:
    #     print(i.text)
        
        
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
        
        
        
    driver.close()

    driver.switch_to.window(janela_principal)


    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_SERIES_DESATIVADAS))).click()

    driver.switch_to.frame(driver.find_element_by_id('iCorpo'))

    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_VISUALIZAR_IMPRESSAO))).click()


    janela_impressao = driver.window_handles[1]
    driver.switch_to.window(janela_impressao)


    bs = BeautifulSoup(driver.page_source, 'html.parser')

    # titulos = bs.find('tr', {'class': 'fundoPadraoAEscuro3'})
    # descricoes = titulos.findChildren("th")
    # for titulo in descricoes:
    #     print(titulo['title'])


    linhas = bs.find_all('tr', {'class':'fundoPadraoAClaro3'})
    # print(len(linhas))
    # colunas = linhas[0].findChildren("td")
    # for i in colunas:
    #     print(i.text)
        
        
        
    #series_desativadas = []
    for l in linhas:
        #linha = []
        colunas = l.findChildren("td")
        # linha = SeriesModel(
        #     int(colunas[0].text), 
        #     colunas[1].text, 
        #     colunas[2].text, 
        #     colunas[3].text, 
        #     datetime.strptime(colunas[4].text, "%d/%m/%Y"), 
        #     colunas[5].text, 
        #     colunas[6].text, 
        #     colunas[7].text, 
        #     ''
        # )
        #series_desativadas.append(linha)
        if int(colunas[0].text) in mapa_series:
            mapa_series[int(colunas[0].text)].status = 'Desativada'
        else:
            print('Serie Não Encontrada', colunas)


    # for serie in todas_series:
    #     if serie in series_desativadas:
    #         serie.status = 'Desativada'
    #     else:
    #         serie.status = 'Ativa'

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
    
    print('Terminou de Carregar dados do Bacen, encontrou', len(todas_series), 'séries...')
    
    return todas_series


if __name__ == '__main__':
    executaBuscaSeries()