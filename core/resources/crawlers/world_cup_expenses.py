import xml.etree.ElementTree as ET
from collections import OrderedDict,defaultdict
from os import path , getcwd
import requests
from utils import save_csv
from bs4 import BeautifulSoup

URL = "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"

file_path = path.join(path.dirname(getcwd()),"data","world_cup_expense.xml")

completed_spent_data = []
ufs = {}

def calculate_executed_value(negotiated_value,percentual):
    return negotiated_value * percentual / 100
    
def is_valid_file():
    if path.exists(file_path):
        if path.getsize(file_path) > 0:
            return True
        return False
    return False

if not is_valid_file():
    with open(file_path,"w") as xml:
        content = requests.get(URL).text
        xml.write(content)

with open(file_path) as xml:
    root = ET.fromstring(xml.read())

for children in root:
    uf = children.find("uf")

    if uf:
        _id = uf.find("id").text
        ufs[_id] = uf.find("nome").text
    
for index,spent in enumerate(root):
    '''
     Fields to collect

        - Uf ok
        - Tema( descrição ) ok
            - Aeroportos
            - Esportes
            - Turismos
        - Valor Total Previsto ok
        - Valor Total Executado ok
        - Tipo Instituição ok
        - Instituição ok
        - Quantidade de obras no estado ( In memory process)
    '''

    negotiated = spent.find("valorTotalPrevisto")

    # Removing all "empreendimentos" that haven't negotiated value defined
    if negotiated is not None:

        theme = spent.find("tema").find("descricao").text       
        
        institution = spent.find("instituicao")
        name_institution = institution.find("nome").text.capitalize()
        part_institution = institution.find("tipoInstituicao").find('descricao').text

        city = spent.find("cidadeSede")

        uf_xml = city.find("uf")

        status = spent.find("andamento").find("descricao").text

        if uf_xml:
            uf_name = uf_xml.find("nome").text
        else:
            id_uf = city.find("id").text
            uf_name = ufs.get(id_uf)

        negotiated = float(negotiated.text)

        executed = spent.find("valorPercentualExecucaoFisica")

        if executed is None:
            executed = 100
        else:
            executed = float(executed.text)

        spent_data = OrderedDict()
        spent_data["uf"] = uf_name
        spent_data["tema"] = theme
        spent_data["tipo_instituicao"] = part_institution
        spent_data["instituicao"] = name_institution
        spent_data["status"] = status
        spent_data["negociado"] = negotiated
        spent_data["executado"] = calculate_executed_value(negotiated,executed)

        completed_spent_data.append(spent_data)     

print([item for item in completed_spent_data if item["status"] != "Concluído"][0])

save_csv("spent_world_cup.csv",data=completed_spent_data)