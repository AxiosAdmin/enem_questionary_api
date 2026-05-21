from src.helpers.enem_question_common import (
    build_enem_area_question_prompt,
    build_random_topic_context,
    get_catalog_topics,
)


NATURAL_SCIENCES_TOPIC_CATALOG = {
    "Fisica": {
        "subtopics": [
            {
                "name": "Movimento e leis fisicas",
                "description": (
                    "Interpretacao de movimento, forcas, equilibrio e conservacao em "
                    "situacoes-problema do cotidiano."
                ),
            },
            {
                "name": "Energia e termodinamica",
                "description": (
                    "Analise de transformacoes de energia, calor, temperatura, maquinas "
                    "termicas e fenomenos termicos usuais."
                ),
            },
            {
                "name": "Eletricidade e magnetismo",
                "description": (
                    "Compreensao de circuitos, consumo de energia, grandezas eletricas e "
                    "fenomenos magneticos em contextos praticos."
                ),
            },
            {
                "name": "Ondas e optica",
                "description": (
                    "Interpretacao de fenomenos ondulatorios, reflexao, refracao, lentes, "
                    "espelhos e propagacao de ondas."
                ),
            },
        ],
        "diversity_modes": [
            "experimento do cotidiano",
            "situacao tecnologica",
            "grafico ou tabela fisica",
            "problema energetico",
        ],
    },
    "Quimica": {
        "subtopics": [
            {
                "name": "Transformacoes quimicas e estequiometria",
                "description": (
                    "Interpretacao de reacoes quimicas, leis ponderais e relacoes "
                    "quantitativas em transformacoes da materia."
                ),
            },
            {
                "name": "Materiais, propriedades e solucoes",
                "description": (
                    "Analise de substancias, misturas, ligacoes, solucoes aquosas e "
                    "propriedades dos materiais."
                ),
            },
            {
                "name": "Energia e dinamica das reacoes",
                "description": (
                    "Compreensao de termoquimica, oxirreducoes, velocidade e equilibrio "
                    "quimico em contextos aplicados."
                ),
            },
            {
                "name": "Quimica organica e ambiente",
                "description": (
                    "Interpretacao de compostos de carbono, combustiveis, polimeros e "
                    "impactos ambientais associados."
                ),
            },
        ],
        "diversity_modes": [
            "problema ambiental",
            "situacao de laboratorio",
            "aplicacao industrial",
            "contexto de consumo e saude",
        ],
    },
    "Biologia": {
        "subtopics": [
            {
                "name": "Celulas, metabolismo e biotecnologia",
                "description": (
                    "Analise de processos celulares, metabolismo energetico e aplicacoes "
                    "biotecnologicas."
                ),
            },
            {
                "name": "Genetica e hereditariedade",
                "description": (
                    "Interpretacao de principios geneticos, diversidade biologica, mutacoes "
                    "e implicacoes para a vida humana."
                ),
            },
            {
                "name": "Ecologia e sustentabilidade",
                "description": (
                    "Compreensao de ecossistemas, ciclos, impactos ambientais, biomas e "
                    "conservacao da biodiversidade."
                ),
            },
            {
                "name": "Saude, evolucao e qualidade de vida",
                "description": (
                    "Analise de evolucao, fisiologia humana, doencas, saude publica e "
                    "qualidade de vida das populacoes."
                ),
            },
        ],
        "diversity_modes": [
            "saude publica",
            "pesquisa cientifica",
            "problema socioambiental",
            "interpretacao de experimento",
        ],
    },
}

NATURAL_SCIENCES_EVALUATION_POINTS = [
    "interpretacao de fenomenos cientificos com base em evidencias, modelos e experimentos",
    "relacao entre ciencia, tecnologia, sociedade e meio ambiente",
    "uso de linguagens cientificas, graficos, tabelas, grandezas, simbolos e representacoes",
    "fisica: movimento, energia, eletricidade, ondas, optica e fenomenos termicos",
    "quimica: transformacoes, materiais, solucoes, energia, equilibrio, compostos de carbono e ambiente",
    "biologia: celulas, genetica, ecologia, evolucao, saude, biotecnologia e qualidade de vida",
]

NATURAL_SCIENCES_FREQUENT_CONTEXTS = [
    "experimentos, divulgacao cientifica, saude publica e tecnologias do cotidiano",
    "problemas ambientais, energia, recursos naturais e sustentabilidade",
    "rotulos, medicamentos, processos industriais, consumo e seguranca",
    "graficos, tabelas, relatorios, infograficos e situacoes de investigacao cientifica",
]

NATURAL_SCIENCES_ADDITIONAL_GUIDELINES = [
    "A questao deve exigir interpretacao cientifica, e nao apenas lembranca isolada de definicoes.",
    "Quando apropriado, use experimentos, dados, fenomenos naturais, tecnologias e implicacoes sociais ou ambientais.",
    "Evite questoes puramente conteudistas, sem contexto, ou baseadas apenas em nomenclatura decorada.",
]


def get_natural_sciences_topics() -> list[str]:
    return get_catalog_topics(NATURAL_SCIENCES_TOPIC_CATALOG)


def build_random_natural_sciences_question_context(topic: str) -> dict[str, str]:
    return build_random_topic_context(NATURAL_SCIENCES_TOPIC_CATALOG, topic)


def build_enem_natural_sciences_question_prompt(
    topic: str,
    subtopic: str,
    subtopic_description: str,
    diversity_mode: str,
) -> str:
    return build_enem_area_question_prompt(
        area_name="Ciencias da Natureza e suas Tecnologias",
        topic=topic,
        subtopic=subtopic,
        subtopic_description=subtopic_description,
        diversity_mode=diversity_mode,
        evaluation_points=NATURAL_SCIENCES_EVALUATION_POINTS,
        frequent_contexts=NATURAL_SCIENCES_FREQUENT_CONTEXTS,
        additional_area_guidelines=NATURAL_SCIENCES_ADDITIONAL_GUIDELINES,
    )
