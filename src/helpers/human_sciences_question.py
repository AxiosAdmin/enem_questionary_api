from src.helpers.enem_question_common import (
    build_enem_area_question_prompt,
    build_random_topic_context,
    get_catalog_topics,
)


HUMAN_SCIENCES_TOPIC_CATALOG = {
    "Historia": {
        "subtopics": [
            {
                "name": "Memoria, cultura e identidades",
                "description": (
                    "Interpretacao historica de fontes, memoria social, patrimonio e "
                    "formacao de identidades em diferentes tempos."
                ),
            },
            {
                "name": "Poder, Estado e conflitos historicos",
                "description": (
                    "Analise de instituicoes, disputas de poder, conflitos sociais e "
                    "transformacoes politicas ao longo da historia."
                ),
            },
            {
                "name": "Brasil, colonizacao e formacao social",
                "description": (
                    "Compreensao de processos historicos ligados a colonizacao, escravidao, "
                    "resistencias e formacao da sociedade brasileira."
                ),
            },
        ],
        "diversity_modes": [
            "fonte historica",
            "texto interpretativo",
            "contexto politico-social",
            "comparacao entre epocas",
        ],
    },
    "Geografia": {
        "subtopics": [
            {
                "name": "Cartografia e representacoes do espaco",
                "description": (
                    "Interpretacao de mapas, representacoes graficas e leituras espaciais "
                    "em diferentes escalas."
                ),
            },
            {
                "name": "Territorio, poder e fluxos",
                "description": (
                    "Analise de relacoes de poder, organizacao territorial, populacao e "
                    "fluxos economicos e migratorios."
                ),
            },
            {
                "name": "Sociedade, natureza e questoes ambientais",
                "description": (
                    "Compreensao critica das interacoes entre sociedade e meio fisico, "
                    "recursos naturais e degradacao ambiental."
                ),
            },
        ],
        "diversity_modes": [
            "mapa ou cartografia",
            "contexto socioambiental",
            "dados geograficos",
            "analise territorial",
        ],
    },
    "Sociologia": {
        "subtopics": [
            {
                "name": "Movimentos sociais e participacao coletiva",
                "description": (
                    "Analise da dinamica dos movimentos sociais e da participacao social na "
                    "transformacao da realidade."
                ),
            },
            {
                "name": "Cidadania, democracia e inclusao social",
                "description": (
                    "Compreensao de cidadania, direitos, democracia e estrategias de "
                    "inclusao social."
                ),
            },
            {
                "name": "Trabalho, tecnologia e vida social",
                "description": (
                    "Analise de transformacoes tecnicas, organizacao do trabalho e impactos "
                    "sociais das novas tecnologias."
                ),
            },
        ],
        "diversity_modes": [
            "problema social contemporaneo",
            "dados de pesquisa social",
            "texto de ciencias sociais",
            "analise de politica publica",
        ],
    },
    "Filosofia": {
        "subtopics": [
            {
                "name": "Etica e vida em sociedade",
                "description": (
                    "Reflexao sobre valores eticos, convivio social, responsabilidade e "
                    "criterios para a vida coletiva."
                ),
            },
            {
                "name": "Poder, democracia e cidadania",
                "description": (
                    "Analise de conceitos filosoficos relacionados ao poder, ao Estado, "
                    "a democracia e a cidadania."
                ),
            },
            {
                "name": "Argumentacao e pensamento critico",
                "description": (
                    "Interpretacao de ideias, comparacao de pontos de vista e construcao "
                    "de argumentacao critica em temas sociais."
                ),
            },
        ],
        "diversity_modes": [
            "texto filosofico adaptado",
            "dilema etico",
            "problema politico-social",
            "comparacao de argumentos",
        ],
    },
}

HUMAN_SCIENCES_EVALUATION_POINTS = [
    "cultura, memoria, patrimonio, identidades e diversidade cultural",
    "representacoes graficas e cartograficas do espaco geografico",
    "relacoes de poder, territorio, fluxos populacionais e organizacao socioespacial",
    "instituicoes sociais, politicas e economicas, conflitos e movimentos sociais",
    "transformacoes tecnicas e tecnologicas e seus impactos no trabalho e na vida social",
    "cidadania, democracia, etica, inclusao social e legislacoes",
    "relacoes entre sociedade e natureza, recursos naturais, preservacao e degradacao ambiental",
]

HUMAN_SCIENCES_FREQUENT_CONTEXTS = [
    "fontes historicas, documentos, noticias, charges e textos interpretativos",
    "mapas, graficos demograficos, dados territoriais e problemas socioambientais",
    "debates sobre cidadania, direitos, tecnologia, trabalho e inclusao social",
    "situacoes politicas, culturais e economicas do Brasil e do mundo",
]

HUMAN_SCIENCES_ADDITIONAL_GUIDELINES = [
    "A questao deve privilegiar leitura critica de fontes, comparacao de perspectivas e interpretacao historico-geografica ou sociopolitica.",
    "Quando apropriado, use texto-base, mapa, dado social, documento, charge, noticia ou trecho analitico.",
    "Evite perguntas de pura memorizacao de datas, nomes ou definicoes descontextualizadas.",
    "Siga o padrao comum do ENEM em Humanas: documento, mapa, grafico, texto interpretativo ou imagem historica/social como base, seguido de um comando curto e analitico.",
    "O suporte deve funcionar como fonte historica, geografica, sociologica ou filosofica a ser interpretada criticamente, e nao apenas como ilustracao.",
    "As alternativas devem separar leituras superficiais de leituras contextualizadas, especialmente em temas de cidadania, poder, territorio, trabalho, memoria e conflito.",
    "Quando houver dados, mapas, diagramas ou imagens, explore relacoes entre escala, contexto, intencionalidade, processo historico e implicacoes sociopoliticas.",
]

HUMAN_SCIENCES_SUPPORT_MATERIAL_PRIORITIES = [
    "fonte historica, documento adaptado, noticia, manifesto ou texto analitico curto",
    "mapa, representacao cartografica, fluxograma territorial ou esquema socioespacial",
    "grafico ou tabela com dados demograficos, economicos, sociais ou ambientais",
    "charge, cartaz, fotografia historica ou imagem socialmente situada",
]


def get_human_sciences_topics() -> list[str]:
    return get_catalog_topics(HUMAN_SCIENCES_TOPIC_CATALOG)


def build_random_human_sciences_question_context(topic: str) -> dict[str, str]:
    return build_random_topic_context(HUMAN_SCIENCES_TOPIC_CATALOG, topic)


def build_enem_human_sciences_question_prompt(
    topic: str,
    subtopic: str,
    subtopic_description: str,
    diversity_mode: str,
) -> str:
    return build_enem_area_question_prompt(
        area_name="Ciencias Humanas e suas Tecnologias",
        topic=topic,
        subtopic=subtopic,
        subtopic_description=subtopic_description,
        diversity_mode=diversity_mode,
        evaluation_points=HUMAN_SCIENCES_EVALUATION_POINTS,
        frequent_contexts=HUMAN_SCIENCES_FREQUENT_CONTEXTS,
        additional_area_guidelines=HUMAN_SCIENCES_ADDITIONAL_GUIDELINES,
        support_material_priorities=HUMAN_SCIENCES_SUPPORT_MATERIAL_PRIORITIES,
    )
