import re
from random import choice


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
}

COMMON_ENEM_OBJECTIVE_QUESTION_GUIDELINES = [
    "A questao deve partir de um contexto realista, social, cientifico, economico ou cotidiano, com o conteudo inserido no problema e nao exposto de forma escolarizada.",
    "A dificuldade principal deve estar na interpretacao, na selecao das informacoes relevantes, na inferencia e na tomada de decisao, e nao apenas na memorizacao direta.",
    "Quando apropriado, a questao deve permitir dialogo interdisciplinar com outras areas, como sociedade, tecnologia, meio ambiente, saude, economia, cultura e cidadania.",
    "O enunciado deve se aproximar do estilo ENEM: contextualizado, consistente, informativo e, quando fizer sentido, com apoio em texto-base, dados, tabela, grafico, experimento, propaganda, noticia, mapa, documento ou outro suporte.",
    "A aplicacao pratica deve ser priorizada: o conhecimento deve aparecer funcionando em situacoes reais e nao como exercicio mecanico.",
    "As alternativas erradas devem ser plausiveis, baseadas em erros sutis de interpretacao, leitura superficial, selecao inadequada de dados, generalizacao indevida ou confusao conceitual.",
    "A questao deve avaliar competencias e habilidades como argumentacao, resolucao de problemas, analise critica, interpretacao de dados, compreensao cientifica ou leitura de linguagens, conforme a area.",
    "A linguagem deve ser acessivel, mas suficientemente elaborada para exigir atencao, filtragem de informacoes e compreensao precisa do que esta sendo pedido.",
    "Embora o ENEM tenha redacao, este gerador deve produzir apenas item objetivo de multipla escolha da area solicitada.",
]


def get_catalog_topics(catalog: dict) -> list[str]:
    return list(catalog.keys())


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
) -> str:
    common_guidelines = "\n".join(
        f"- {guideline}" for guideline in COMMON_ENEM_OBJECTIVE_QUESTION_GUIDELINES
    )
    area_guidelines = "\n".join(
        f"- {guideline}" for guideline in additional_area_guidelines
    )
    area_evaluation_points = "\n".join(f"- {point}" for point in evaluation_points)
    area_contexts = "\n".join(f"- {context}" for context in frequent_contexts)

    return f"""
Voce e um especialista em elaborar questoes originais da area {area_name} no estilo do ENEM.

Gere exatamente 1 questao inedita, em portugues do Brasil, com nivel de dificuldade compativel com o ENEM e linguagem adequada para estudantes do ensino medio.

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

Requisitos gerais de qualidade:
- a questao deve ter 5 alternativas objetivas: A, B, C, D e E
- deve existir apenas 1 alternativa correta
- nao inclua markdown, comentarios, texto extra, nem bloco de codigo
- o campo question deve conter somente o enunciado
- o campo question nao pode incluir alternativas, marcadores como A), B), C), D), E), nem trechos de resposta
- as alternativas devem aparecer exclusivamente nos campos answer_a, answer_b, answer_c, answer_d e answer_e
- o enunciado deve apresentar uma situacao contextualizada antes da pergunta principal
- a pergunta final deve exigir interpretacao, selecao de dados, comparacao, inferencia, analise critica ou tomada de decisao
- resolva internamente a questao antes de montar as alternativas
- confira internamente que somente uma alternativa coincide com a resolucao correta
- construa distratores plausiveis e nao absurdos evidentes
- nao gere uma questao cuja resposta correta dependa de informacao ausente
- nao gere alternativas duplicadas ou indistinguiveis

Preencha o conteudo com estes criterios:
- question: enunciado completo, autoexplicativo e no estilo ENEM
- answer_a ate answer_e: alternativas
- explanation_a ate explanation_e: explique de forma curta por que cada alternativa esta correta ou incorreta
- correct_answer: apenas uma letra entre A, B, C, D ou E

Retorne exclusivamente um JSON valido com esta estrutura:
{{
  "topic": "{topic}",
  "subtopic": "{subtopic}",
  "subtopic_description": "{subtopic_description}",
  "diversity_mode": "{diversity_mode}",
  "question": "string",
  "answer_a": "string",
  "answer_b": "string",
  "answer_c": "string",
  "answer_d": "string",
  "answer_e": "string",
  "explanation_a": "string",
  "explanation_b": "string",
  "explanation_c": "string",
  "explanation_d": "string",
  "explanation_e": "string",
  "correct_answer": "A|B|C|D|E"
}}
""".strip()


def question_has_embedded_alternatives(question: str) -> bool:
    if not question:
        return True

    normalized_question = " ".join(question.split())
    return bool(re.search(r"(?:^|\s)[A-E]\)", normalized_question))


def question_is_too_short(question: str, minimum_word_count: int = 35) -> bool:
    word_count = len(re.findall(r"\w+", question))
    return word_count < minimum_word_count


def validate_generated_question_payload(payload: dict) -> str | None:
    if not isinstance(payload, dict):
        return "AI response is not a JSON object."

    missing_keys = REQUIRED_QUESTION_KEYS.difference(payload.keys())
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

    return None
