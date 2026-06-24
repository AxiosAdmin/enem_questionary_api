import json
import re
from random import choice

from src.services.question_asset_service import (
    serialize_question_asset_for_prompt,
    validate_question_assets,
)

REQUIRED_QUESTION_KEYS = {
    "topic",
    "subtopic",
    "subtopic_description",
    "diversity_mode",
    "question",
    "answer_a",
    "answer_b",
    "answer_c",
    "answer_d",
    "answer_e",
    "explanation_a",
    "explanation_b",
    "explanation_c",
    "explanation_d",
    "explanation_e",
    "correct_answer",
    "question_assets",
}

COMMON_ENEM_OBJECTIVE_QUESTION_GUIDELINES = [
    "A questao deve partir de um contexto realista, social, cientifico, economico ou cotidiano, com o conteudo inserido no problema e nao exposto de forma escolarizada.",
    "A dificuldade principal deve estar na interpretacao, na selecao das informacoes relevantes, na inferencia e na tomada de decisao, e nao apenas na memorizacao direta.",
    "Quando apropriado, a questao deve permitir dialogo interdisciplinar com outras areas, como sociedade, tecnologia, meio ambiente, saude, economia, cultura e cidadania.",
    "O enunciado deve se aproximar do estilo ENEM observado nos cadernos recentes: contextualizado, consistente, informativo, com comando final objetivo e frequentemente apoiado em texto-base, imagem, grafico, tabela, mapa, documento, experimento, cartaz, propaganda, noticia ou outro suporte multimodal.",
    "A aplicacao pratica deve ser priorizada: o conhecimento deve aparecer funcionando em situacoes reais e nao como exercicio mecanico.",
    "As alternativas erradas devem ser plausiveis, baseadas em erros sutis de interpretacao, leitura superficial, selecao inadequada de dados, generalizacao indevida ou confusao conceitual.",
    "A questao deve avaliar competencias e habilidades como argumentacao, resolucao de problemas, analise critica, interpretacao de dados, compreensao cientifica ou leitura de linguagens, conforme a area.",
    "A linguagem deve ser acessivel, mas suficientemente elaborada para exigir atencao, filtragem de informacoes e compreensao precisa do que esta sendo pedido.",
    "Quando houver suporte complementar, ele deve ser essencial para resolver a questao e nao apenas decorativo.",
    "Quando fizer sentido, use rotulos em estilo ENEM, como Texto I, Texto II, legenda, fonte, adaptado de, dados de pesquisa ou descricao de imagem.",
    "As alternativas devem ser paralelas entre si, relativamente equilibradas em extensao e sem pistas formais da resposta correta.",
    "Embora o ENEM tenha redacao, este gerador deve produzir apenas item objetivo de multipla escolha da area solicitada.",
]


def get_catalog_topics(catalog: dict) -> list[str]:
    return list(catalog.keys())


def get_catalog_topics_with_subtopics(catalog: dict) -> list[dict[str, object]]:
    return [
        {
            "topic": topic,
            "subtopics": [
                {
                    "name": subtopic["name"],
                    "description": subtopic["description"],
                }
                for subtopic in configuration["subtopics"]
            ],
        }
        for topic, configuration in catalog.items()
    ]


def get_topic_configuration(catalog: dict, topic: str) -> dict:
    if topic not in catalog:
        raise ValueError(f"Unsupported topic: {topic}")
    return catalog[topic]


def build_random_topic_context(catalog: dict, topic: str) -> dict[str, str]:
    topic_configuration = get_topic_configuration(catalog, topic)
    selected_subtopic = choice(topic_configuration["subtopics"])
    selected_diversity_mode = choice(topic_configuration["diversity_modes"])

    return {
        "topic": topic,
        "subtopic": selected_subtopic["name"],
        "subtopic_description": selected_subtopic["description"],
        "diversity_mode": selected_diversity_mode,
    }


def build_enem_area_question_prompt(
    area_name: str,
    topic: str,
    subtopic: str,
    subtopic_description: str,
    diversity_mode: str,
    evaluation_points: list[str],
    frequent_contexts: list[str],
    additional_area_guidelines: list[str],
    question_asset_priorities: list[str],
    forced_question_assets: list | None = None,
) -> str:
    common_guidelines = "\n".join(
        f"- {guideline}" for guideline in COMMON_ENEM_OBJECTIVE_QUESTION_GUIDELINES
    )
    area_guidelines = "\n".join(
        f"- {guideline}" for guideline in additional_area_guidelines
    )
    area_evaluation_points = "\n".join(f"- {point}" for point in evaluation_points)
    area_contexts = "\n".join(f"- {context}" for context in frequent_contexts)
    area_question_assets = "\n".join(
        f"- {question_asset}" for question_asset in question_asset_priorities
    )
    forced_assets_instruction = ""
    required_question_keys = sorted(REQUIRED_QUESTION_KEYS)
    response_structure_lines = [
        f'  "{key}": "string",' for key in required_question_keys if key != "question_assets"
    ]

    if forced_question_assets:
        serialized_forced_assets = json.dumps(
            [
                serialize_question_asset_for_prompt(asset)
                for asset in forced_question_assets
            ],
            ensure_ascii=True,
            indent=2,
        )
        forced_assets_instruction = f"""

Materiais de suporte ja fornecidos pela aplicacao e que devem ser usados obrigatoriamente:
{serialized_forced_assets}

Regras obrigatorias para estes materiais fornecidos:
- use esses materiais de suporte como base da resolucao da questao
- faca referencia explicita aos materiais no enunciado
- nao invente novos question_assets
- nao altere, nao resuma e nao substitua os materiais fornecidos
- como os materiais ja serao vinculados pela aplicacao, nao retorne o campo question_assets no JSON final
""".rstrip()
        required_question_keys = sorted(REQUIRED_QUESTION_KEYS.difference({"question_assets"}))
        response_structure_lines = [
            f'  "{key}": "A|B|C|D|E",' if key == "correct_answer" else f'  "{key}": "string",'
            for key in required_question_keys
        ]
    else:
        response_structure_lines = [
            f'  "{key}": "A|B|C|D|E",' if key == "correct_answer" else f'  "{key}": "string",'
            for key in sorted(REQUIRED_QUESTION_KEYS.difference({"question_assets"}))
        ]
        response_structure_lines.append('  "question_assets": [')
        response_structure_lines.append("    {")
        response_structure_lines.append(
            '      "asset_type": "text|table|chart|diagram|image|map|infographic",'
        )
        response_structure_lines.append(
            '      "rendering_mode": "inline_text|structured_data|generated_image",'
        )
        response_structure_lines.append(
            '      "position": "before_statement|after_statement"'
        )
        response_structure_lines.append("    }")
        response_structure_lines.append("  ]")

    return f"""
Voce e um especialista em elaborar questoes originais da area {area_name} no estilo do ENEM.

Gere exatamente 1 questao inedita, em portugues do Brasil, com nivel de dificuldade compativel com o ENEM, linguagem adequada para estudantes do ensino medio e estrutura compativel com os cadernos recentes do exame.

Use obrigatoriamente estes parametros definidos pela aplicacao:
- topic: {topic}
- subtopic: {subtopic}
- subtopic_description: {subtopic_description}
- diversity_mode: {diversity_mode}

Esses quatro campos sao obrigatorios e devem ser retornados exatamente com esses valores, sem criar variacoes.

Formato obrigatorio da questao no estilo ENEM:
{common_guidelines}

Orientacoes adicionais especificas desta area:
{area_guidelines}

Pontos de avaliacao da area que devem orientar a elaboracao:
{area_evaluation_points}

Contextos frequentes e adequados para inspirar a questao:
{area_contexts}

Suportes multimodais mais adequados para esta area:
{area_question_assets}
{forced_assets_instruction}

Requisitos gerais de qualidade:
- a questao deve ter 5 alternativas objetivas: A, B, C, D e E
- deve existir apenas 1 alternativa correta
- nao inclua markdown, comentarios, texto extra, nem bloco de codigo
- o campo question deve conter somente o enunciado
- o campo question nao pode incluir alternativas, marcadores como A), B), C), D), E), nem trechos de resposta
- as alternativas devem aparecer exclusivamente nos campos answer_a, answer_b, answer_c, answer_d e answer_e
- o campo question deve apresentar uma situacao contextualizada e uma pergunta final objetiva, sem reproduzir integralmente os materiais de apoio
- a pergunta final deve exigir interpretacao, selecao de dados, comparacao, inferencia, analise critica ou tomada de decisao
- resolva internamente a questao antes de montar as alternativas
- confira internamente que somente uma alternativa coincide com a resolucao correta
- construa distratores plausiveis e nao absurdos evidentes
- nao gere uma questao cuja resposta correta dependa de informacao ausente
- nao gere alternativas duplicadas ou indistinguiveis
- retorne obrigatoriamente de 1 a 2 itens em question_assets quando a aplicacao nao tiver fornecido materiais prontos
- cada item de question_assets deve ser indispensavel para resolver a questao quando esse campo for solicitado
- o enunciado deve fazer referencia explicita ao suporte complementar quando ele existir
- se usar texto-base, prefira trechos curtos ou medios e, quando pertinente, use rotulos como Texto I e Texto II
- se usar material visual, descreva-o com clareza por meio de alt_text e legenda coerente
- imagem gerada e opcional, nunca obrigatoria
- so use rendering_mode "generated_image" quando a resolucao realmente depender de um apoio visual que nao possa ser representado com a mesma fidelidade por texto, tabela, grafico ou diagrama estruturado
- quando texto, tabela, grafico ou diagrama forem suficientes, prefira essas formas e nao gere imagem
- como esta aplicacao nao fornece fonte externa real, nunca invente referencias, autores, orgaos, links ou creditos
- quando houver campo source_label em material sintetico, use exatamente: "Texto elaborado para fins educacionais."

Preencha o conteudo com estes criterios:
- question: enunciado completo, autoexplicativo e no estilo ENEM
- answer_a ate answer_e: alternativas
- explanation_a ate explanation_e: explique de forma curta por que cada alternativa esta correta ou incorreta
- correct_answer: apenas uma letra entre A, B, C, D ou E
- question_assets: lista com 1 ou 2 materiais de apoio essenciais, usando exclusivamente um dos formatos abaixo:
  1. texto de apoio:
     {{
       "asset_type": "text",
       "rendering_mode": "inline_text",
       "position": "before_statement",
       "title": "Texto I",
       "caption": "opcional",
       "source_label": "Texto elaborado para fins educacionais.",
       "content": "texto do material"
     }}
  2. tabela, grafico ou diagrama estruturado:
     {{
       "asset_type": "table", "chart" ou "diagram",
       "rendering_mode": "structured_data",
       "position": "before_statement",
       "title": "Tabela 1", "Grafico 1" ou "Figura 1",
       "caption": "opcional",
       "source_label": "Texto elaborado para fins educacionais.",
       "data": {{
         "chart_type": "bar|line|pie" apenas para chart,
         "columns": ["coluna 1", "coluna 2"] apenas para table,
         "rows": [["valor 1", "valor 2"]] apenas para table,
         "labels": ["rotulo 1", "rotulo 2"] apenas para chart,
         "series": [{{"name": "serie", "values": [1, 2]}}] apenas para chart,
         "diagram_type": "rectangle_dimensions" apenas para diagram,
         "width_label": "24 m" apenas para diagram,
         "height_label": "18 m" apenas para diagram,
         "scale_label": "1:300" apenas para diagram
       }}
     }}
  3. material visual gerado:
     {{
       "asset_type": "image", "map" ou "infographic",
       "rendering_mode": "generated_image",
       "position": "before_statement",
       "title": "opcional",
       "caption": "legenda curta",
       "alt_text": "descricao objetiva e acessivel do visual",
       "source_label": "Texto elaborado para fins educacionais.",
       "image_generation_prompt": "instrucao detalhada, realista e segura para gerar a imagem"
     }}

Regras adicionais para diagram:
- quando a questao exigir representacao geometrica, esquema simples, planta basica, circuito muito simples ou figura funcional, prefira asset_type "diagram" com rendering_mode "structured_data"
- use diagramas estruturados em vez de imagem gerada sempre que a interpretacao depender de medidas, rotulos, lados, escalas ou posicoes
- nao use generated_image para diagram

Retorne exclusivamente um JSON valido com esta estrutura:
{{
{chr(10).join(response_structure_lines)}
}}
""".strip()


def question_has_embedded_alternatives(question: str) -> bool:
    if not question:
        return True

    normalized_question = " ".join(question.split())
    return bool(re.search(r"(?:^|\s)[A-E]\)", normalized_question))


def question_is_too_short(question: str, minimum_word_count: int = 18) -> bool:
    word_count = len(re.findall(r"\w+", question))
    return word_count < minimum_word_count


def validate_generated_question_payload(
    payload: dict,
    *,
    require_question_assets: bool = True,
) -> str | None:
    if not isinstance(payload, dict):
        return "AI response is not a JSON object."

    required_keys = (
        REQUIRED_QUESTION_KEYS
        if require_question_assets
        else REQUIRED_QUESTION_KEYS.difference({"question_assets"})
    )
    missing_keys = required_keys.difference(payload.keys())
    if missing_keys:
        return f"AI response is missing required keys: {sorted(missing_keys)}"

    question = payload.get("question", "")
    if question_has_embedded_alternatives(question):
        return "AI response returned alternatives inside the question statement."

    if question_is_too_short(question):
        return "AI response returned a question statement that is too short for ENEM style."

    correct_answer = payload.get("correct_answer", "")
    if correct_answer not in {"A", "B", "C", "D", "E"}:
        return "AI response returned an invalid correct_answer."

    answer_fields = {
        "A": payload.get("answer_a", "").strip(),
        "B": payload.get("answer_b", "").strip(),
        "C": payload.get("answer_c", "").strip(),
        "D": payload.get("answer_d", "").strip(),
        "E": payload.get("answer_e", "").strip(),
    }
    if any(not value for value in answer_fields.values()):
        return "AI response returned empty answer alternatives."

    if len(set(answer_fields.values())) != len(answer_fields):
        return "AI response returned duplicated answer alternatives."

    if require_question_assets:
        question_assets_error = validate_question_assets(
            payload.get("question_assets")
        )
        if question_assets_error is not None:
            return question_assets_error

    return None
