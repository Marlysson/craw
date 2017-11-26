from collections import OrderedDict,defaultdict
from utils import save_csv, load_xml_resource

completed_spent_data = []
ufs = {}

def calculate_executed_value(negotiated_value,percentual):
    return negotiated_value * percentual / 100
    
def capitalize_text(text):
    words = []

    if len(text) > 1:
        for part in text.split():
            if len(part) > 3:
                words.append(part.capitalize())
            else:
                words.append(part)

        return " ".join(words)
    return text

root = load_xml_resource("world_cup_expenses.xml")

for children in root:
    uf = children.find("uf")

    if uf:
        _id = uf.find("id").text
        ufs[_id] = uf.find("nome").text
    
for spent in root:
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
        spent_data["tema"] = capitalize_text(theme)
        spent_data["tipo_instituicao"] = capitalize_text(part_institution)
        spent_data["instituicao"] = capitalize_text(name_institution)
        spent_data["status"] = capitalize_text(status)
        spent_data["negociado"] = negotiated
        spent_data["executado"] = calculate_executed_value(negotiated,executed)

        completed_spent_data.append(spent_data)     

save_csv(__file__, completed_spent_data)