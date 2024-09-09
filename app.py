"""

Sistema utilizando PYTHON para automatizar a geração de certificados através dos dados
de uma planilha em Excel

No arquivo tem o nom do curso, nome do participante, tipo de participação, data do inicio,
data do final, carga horária do curso, data de emissão do certificado

"""

# Pegar os dados da planilha importando a biblioteca OpenPyXL
import openpyxl
# importar a biblioteca Pillow para manipular a imagem. 
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode
# Abrindo a planilha que será utilizada
planilha_alunos = openpyxl.load_workbook('./assets/data/planilha_alunos.xlsx')

# Página da planilha que será utilizada
pagina_alunos = planilha_alunos['Sheet1']

# Extraindo as informações por linha a partir de uma linha especifica (Para assim, poder pular o cabeçalho, caso tenha)
for indice, linha in enumerate(pagina_alunos.iter_rows(min_row=2,max_row=10)):
  # Agora busca pelas células a informação necessária
  nome_do_curso = linha[0].value
  nome_do_participante = linha[1].value
  tipo_de_participacao = linha[2].value
  data_inicio = linha[3].value
  data_final = linha[4].value
  carga_horaria = linha[5].value 
  data_emissao = linha[6].value

  ## Transferindo para a imagem do certificado os dados do aluno
  # Configurações e importação das fontes para sobreposição na imagem do certificado padrão
  fonte_negrito = ImageFont.truetype('./assets/fonts/tahomabd.ttf', 90) # Fonte em Negrito, tamanho
  fonte_geral = ImageFont.truetype('./assets/fonts/tahoma.ttf', 80) # Fonte Normal para os outros textos, tamanho
  fonte_data = ImageFont.truetype('./tahoma.ttf',55)
  fonte_cor = 'black'
  fonte_cor_destaque = 'blue'

  # Buscando o caminho da imagem (Certificado)
  certificados = Image.open('./assets/images/certificado_padrao.jpg')

  # Setar a variável para gerar a imagem do certificado
  gerar = ImageDraw.Draw(certificados)

  ##  Inserindo o texto de acordo com a variável da localização dos campos no certificado
  # Nome do Participante
  gerar.text((1020, 827), nome_do_participante, fill=fonte_cor, font=fonte_negrito)
  # Nome do Curso
  gerar.text((1060,950),nome_do_curso, fill=fonte_cor,font=fonte_geral)
  #Tipo de Participação
  gerar.text((1435,1065),tipo_de_participacao, fill=fonte_cor,font=fonte_geral)
  # Carga Horária do curso
  gerar.text((1485, 1182),f'{str(carga_horaria)} horas',fill=fonte_cor,font=fonte_geral)
  
  # Data de Início
  gerar.text((750, 1770),data_inicio,fill=fonte_cor_destaque,font=fonte_data)
  # Data Final
  gerar.text((750, 1930),data_final,fill=fonte_cor_destaque,font=fonte_data)

  # Data de Emissão do certificado
  gerar.text((2220, 1930),data_emissao,fill=fonte_cor_destaque,font=fonte_data)

  # Formato do arquivo (jpg, png, pdf)
  formato_do_arquivo = 'pdf'
  # Transforma o nome do arquivo em minúsculas
  nome_em_minusculo = f'{str.lower(nome_do_participante)}-{str.lower(nome_do_curso)}-certificado.{formato_do_arquivo}'
  # Retira as acentuações e espaços
  nome_do_arquivo = unidecode(nome_em_minusculo).replace(' ', '_')

  # Salvar o certificado gerado na pasta especificada
  certificados.save(f'./assets/certificados_gerados/{indice}-{nome_do_arquivo}')
