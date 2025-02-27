import logging
from typing import Literal
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from agentiacap.agents.agentCleaner import cleaner
from agentiacap.agents.agentClassifier import classifier
from agentiacap.agents.agentExtractor import extractor
from agentiacap.utils.globals import InputSchema, OutputSchema, MailSchema, relevant_categories, lista_sociedades
from agentiacap.llms.llms import llm4o_mini, llm4o

# Configuración del logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def call_cleaner(state: InputSchema) -> MailSchema:
    try:
        cleaned_result = await cleaner.ainvoke(state)
        return {"asunto":cleaned_result["asunto"], "cuerpo":cleaned_result["cuerpo"], "adjuntos":cleaned_result["adjuntos"]}
    except Exception as e:
        logger.error(f"Error en 'call_cleaner': {str(e)}")
        raise

async def call_classifier(state: MailSchema) -> Command[Literal["Extractor", "Output"]]:
    try:
        input_schema = InputSchema(asunto=state["asunto"], cuerpo=state["cuerpo"], adjuntos=state["adjuntos"])
        classified_result = await classifier.ainvoke(input_schema)
        if classified_result["category"] in relevant_categories:
            goto = "Extractor"
        else:
            goto = "Output"
        return Command(
            update={"categoria": classified_result["category"]},
            goto=goto
        )
    except Exception as e:
        logger.error(f"Error en 'call_classifier': {str(e)}")
        raise

async def call_extractor(state: MailSchema) -> MailSchema:
    try:
        input_schema = InputSchema(asunto=state["asunto"], cuerpo=state["cuerpo"], adjuntos=state["adjuntos"])
        extracted_result = await extractor.ainvoke(input_schema)
        return {"extracciones": extracted_result["extractions"], "tokens": extracted_result["tokens"]}
    except Exception as e:
        logger.error(f"Error en 'call_extractor': {str(e)}")
        print(f"Error en 'call_extractor': {str(e)}")
        raise

def output_node(state: MailSchema) -> OutputSchema:
    import json

    def obtener_valor_por_prioridad(extractions, campo, fuentes_prioritarias):
        for fuente in fuentes_prioritarias:
            for extraccion in extractions:
                if extraccion["source"] == fuente and campo in extraccion["fields"]:
                    valor = extraccion["fields"].get(campo, "").strip()
                    if valor:
                        return valor
        return ""

    def obtener_facturas(extractions):
        facturas = []
        ids_vistos = set()
        fuentes_facturas = ["Document Intelligence", "Vision"]
        
        for fuente in fuentes_facturas:
            for extraccion in extractions:
                if extraccion["source"] == fuente:
                    invoice_id = extraccion["fields"].get("InvoiceId", "").strip()
                    invoice_date = extraccion["fields"].get("InvoiceDate", "").strip()
                    if invoice_id and invoice_id not in ids_vistos:
                        facturas.append({"ID": invoice_id, "Fecha": invoice_date})
                        ids_vistos.add(invoice_id)
        
        if not facturas:
            for extraccion in extractions:
                if extraccion["source"] == "Mail":
                    invoice_ids = extraccion["fields"].get("InvoiceId", [])
                    if isinstance(invoice_ids, list):
                        for invoice_id in invoice_ids:
                            if invoice_id not in ids_vistos:
                                facturas.append({"ID": invoice_id, "Fecha": ""})
                                ids_vistos.add(invoice_id)
        
        return facturas

    def get_codSap(customer):
        for soc in lista_sociedades:
            if soc.get("Nombre Soc SAP") == customer:
                return soc.get("Código SAP")
        return customer

    def generar_json(datos):
        extractions = datos.get("extracciones", [])
        fuentes_prioritarias = ["Mail", "Document Intelligence", "Vision"]
        
        json_generado = {
            "CUIT": obtener_valor_por_prioridad(extractions, "VendorTaxId", fuentes_prioritarias),
            "Sociedad": get_codSap(obtener_valor_por_prioridad(extractions, "CustomerName", fuentes_prioritarias)),
            "Factura": obtener_facturas(extractions)
        }
        
        return json_generado

    def faltan_datos(categoria, resume):
        required_fields = ["CUIT", "Sociedad"]
        
        if not all(field in resume and resume[field] for field in required_fields):
            return True
        
        if categoria == "Impresión de OP y/o Retenciones":
            if "Factura" not in resume or not resume["Factura"]:
                return True
        
        if categoria == "Pedido devolución retenciones":
            if "Factura" not in resume or not any("Fecha" in factura and factura["Fecha"] for factura in resume["Factura"]):
                return True
        
        return False

    def generate_message(cuerpo, category, resume):
        response = llm4o_mini.invoke(f"""En base a este mail de entrada: {cuerpo}. 
                                 Redactá un mail con la siguiente estructura y alguna leve variación para que parezca redactado por un ser humano y que la respuesta no sea siempre la misma:
 
                                Estimado, 
                                
                                Su caso ha sido catalogado como {category}. Para poder darte una respuesta necesitamos que nos brindes los siguientes datos:
                                CUIT
                                Sociedad de YPF a la que se facturó
                                Facturas (recordá mencionarlas con su numero completo 9999A99999999)
                                Fecha de las facturas
                                Montos
                                De tu consulta pudimos obtener la siguiente información:
                                <formatear el input para que sea legible y mantenga la manera de escribir que se viene usando en el mail>
                                {resume}
                                
                                En caso que haya algún dato incorrecto, por favor aclaralo en tu respuesta.
                                El mail lo va a leer una persona que no tiene conocimientos de sistemas y datos. Solo necesito el cuerpo del mail en html (ya que es el contenido de un mail) y no incluyas asunto en la respuesta.
                                Firma siempre el mail con 'CAP - Centro de Atención a Proveedores YPF'.
                                 """)
        return response.content

    try:
        resume = generar_json(state) 
        category = state.get("categoria", "Desconocida")
        is_missing_data = faltan_datos(category, resume)
        message = ""
        if is_missing_data:
            message = generate_message(state.get("cuerpo"), category, resume)

        result = {
            "category": category,
            "extractions": state.get("extracciones", []),  # Valor por defecto: diccionario vacío
            "tokens": state.get("tokens", 0),  # Valor por defecto: 0
            "resume": resume,
            "is_missing_data": is_missing_data,
            "message": message
        }
        return {"result": result}
    except Exception as e:
        logger.error(f"Error en 'output_node': {str(e)}")
        raise


# Workflow principal
builder = StateGraph(MailSchema, input=InputSchema, output=OutputSchema)

builder.add_node("Cleaner", call_cleaner)
builder.add_node("Classifier", call_classifier)
builder.add_node("Extractor", call_extractor)
builder.add_node("Output", output_node)

builder.add_edge(START, "Cleaner")
builder.add_edge("Cleaner", "Classifier")
builder.add_edge("Extractor", "Output")
builder.add_edge("Output", END)

graph = builder.compile()
