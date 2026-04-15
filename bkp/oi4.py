import re

def extract_images(xml_text):
    matches = re.findall(r'\[\[(?:Arquivo|File):(.*?)\]\]', xml_text)

    clean_names = set()

    for m in matches:
        {'GERANDO BPA 4.png', 'MENU SOLICITANTE 1.png', 'MENU EXECUTANTE.png', 'MENU VIDEOFONISTA.png', 'Task.png|40px', 'Gear-icon.png|30px', 'MENU COORDENADOR.png', 'MENU REGULADOR.png', 'Psr-1.jpg', 'Captche SISREG.gif', 'Psr console.png', 'WIN+R.jpg', 'AUD MENU.png', 'ADM MENU.png', 'PRINT - TECLADO.jpg', 'Logo Ministerio Saude.png|left|100px', 'Task.png|30px', 'Logo-crga.png|frame|FONTE: http://www.saude.gov.br/cgra', 'Question-mark.png|30px', 'Library.png|30px', 'Task2.png|50px', 'Voltar.png|30px', 'Gear-icon.png|40px', 'Voltar.png|50px', 'COLAR NO WORD.png'}
        name = m.split("|")[0].strip()
        clean_names.add(name)

    return clean_names