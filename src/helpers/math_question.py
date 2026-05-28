from src.helpers.enem_question_common import (
    build_enem_area_question_prompt,
    build_random_topic_context,
    get_catalog_topics,
)


MATH_TOPIC_CATALOG = {
    "Numeros e operacoes": {
        "subtopics": [
            {
                "name": "Significados e representacoes numericas",
                "description": (
                    "Reconhecimento de diferentes significados e representacoes de numeros "
                    "naturais, inteiros, racionais e reais em contextos sociais."
                ),
            },
            {
                "name": "Padroes numericos e contagem",
                "description": (
                    "Identificacao de padroes numericos, regularidades e principios de contagem "
                    "em situacoes-problema."
                ),
            },
            {
                "name": "Resolucao de problemas numericos",
                "description": (
                    "Resolucao e avaliacao de situacoes-problema envolvendo operacoes, "
                    "estimativas e analise da razoabilidade de resultados numericos."
                ),
            },
        ],
        "diversity_modes": [
            "contexto cotidiano",
            "estimativa e validacao de resultado",
            "planejamento financeiro",
            "comparacao de estrategias",
        ],
    },
    "Geometria": {
        "subtopics": [
            {
                "name": "Localizacao e movimentacao no espaco",
                "description": (
                    "Interpretacao da localizacao e da movimentacao de pessoas e objetos no "
                    "espaco tridimensional e sua representacao bidimensional."
                ),
            },
            {
                "name": "Figuras planas e espaciais",
                "description": (
                    "Identificacao de caracteristicas e propriedades de figuras planas e "
                    "espaciais em diferentes contextos."
                ),
            },
            {
                "name": "Espaco e forma em problemas do cotidiano",
                "description": (
                    "Resolucao de situacoes-problema que envolvem conhecimentos geometricos "
                    "de espaco e forma para interpretar e agir sobre a realidade."
                ),
            },
        ],
        "diversity_modes": [
            "leitura espacial",
            "aplicacao geometrica",
            "representacao visual",
            "contexto arquitetonico",
        ],
    },
    "Grandezas e medidas": {
        "subtopics": [
            {
                "name": "Relacoes entre grandezas e unidades",
                "description": (
                    "Identificacao de relacoes entre grandezas e unidades de medida em "
                    "contextos do cotidiano."
                ),
            },
            {
                "name": "Escalas e representacoes",
                "description": (
                    "Utilizacao da nocao de escala na leitura e interpretacao de "
                    "representacoes de situacoes reais."
                ),
            },
            {
                "name": "Medicao e avaliacao de resultados",
                "description": (
                    "Resolucao de problemas com medidas de grandezas e avaliacao critica de "
                    "resultados de medicoes."
                ),
            },
        ],
        "diversity_modes": [
            "contexto cotidiano",
            "leitura de escalas e medidas",
            "planejamento de recursos",
            "avaliacao de intervencao pratica",
        ],
    },
    "Variacao de grandezas": {
        "subtopics": [
            {
                "name": "Dependencia entre grandezas",
                "description": (
                    "Identificacao da relacao de dependencia entre grandezas em diferentes "
                    "fenomenos e contextos."
                ),
            },
            {
                "name": "Proporcionalidade direta e inversa",
                "description": (
                    "Resolucao de situacoes-problema envolvendo variacao de grandezas "
                    "diretamente ou inversamente proporcionais."
                ),
            },
            {
                "name": "Analise da variacao para argumentacao",
                "description": (
                    "Analise de informacoes envolvendo variacao de grandezas para construir "
                    "argumentacao e avaliar propostas de intervencao."
                ),
            },
        ],
        "diversity_modes": [
            "modelagem matematica",
            "planejamento e tomada de decisao",
            "comparacao de cenarios",
            "contexto socioeconomico",
        ],
    },
    "Algebra e modelagem": {
        "subtopics": [
            {
                "name": "Representacoes algebricas de grandezas",
                "description": (
                    "Identificacao de representacoes algebricas que expressem relacoes entre "
                    "grandezas."
                ),
            },
            {
                "name": "Interpretacao de grafico cartesiano",
                "description": (
                    "Interpretacao de graficos cartesianos que representam relacoes entre "
                    "grandezas."
                ),
            },
            {
                "name": "Modelagem algebrica de situacoes-problema",
                "description": (
                    "Resolucao de situacoes-problema cuja modelagem envolva conhecimentos "
                    "algebricos e geometrico-algebricos."
                ),
            },
        ],
        "diversity_modes": [
            "modelagem matematica",
            "interpretacao grafica",
            "contexto tecnico-cientifico",
            "argumentacao quantitativa",
        ],
    },
    "Graficos e tabelas": {
        "subtopics": [
            {
                "name": "Inferencias a partir de graficos e tabelas",
                "description": (
                    "Utilizacao de informacoes expressas em graficos ou tabelas para fazer "
                    "inferencias e previsoes."
                ),
            },
            {
                "name": "Resolucao de problemas com dados organizados",
                "description": (
                    "Resolucao de problemas com dados apresentados em tabelas, graficos, "
                    "interpolacoes, extrapolacoes e tendencias."
                ),
            },
            {
                "name": "Analise de dados para argumentacao",
                "description": (
                    "Analise de informacoes expressas em graficos e tabelas como recurso "
                    "para a construcao de argumentos."
                ),
            },
        ],
        "diversity_modes": [
            "interpretacao de tabela",
            "interpretacao grafica",
            "analise de tendencia",
            "contexto socioeconomico",
        ],
    },
    "Estatistica e probabilidade": {
        "subtopics": [
            {
                "name": "Medidas estatisticas",
                "description": (
                    "Calculo e interpretacao de medidas de tendencia central ou de dispersao "
                    "em conjuntos de dados."
                ),
            },
            {
                "name": "Probabilidade e amostragem",
                "description": (
                    "Resolucao de situacoes-problema que envolvam probabilidade, amostras "
                    "e fenomenos aleatorios."
                ),
            },
            {
                "name": "Argumentacao com dados estatisticos",
                "description": (
                    "Utilizacao de conhecimentos de estatistica e probabilidade para "
                    "interpretar informacoes, construir argumentacao e avaliar propostas "
                    "de intervencao."
                ),
            },
        ],
        "diversity_modes": [
            "analise quantitativa",
            "tomada de decisao",
            "contexto social",
            "leitura de dados",
        ],
    },
}

MATH_EVALUATION_POINTS = [
    "significados e representacoes de numeros naturais, inteiros, racionais e reais em contextos sociais",
    "padroes numericos, principios de contagem e avaliacao da razoabilidade de resultados",
    "leitura espacial e representacao bidimensional ou tridimensional",
    "identificacao de propriedades de figuras planas e espaciais em problemas aplicados",
    "grandezas, unidades de medida, escalas e avaliacao de medicoes",
    "relacoes de dependencia entre grandezas e proporcionalidade direta ou inversa",
    "representacoes algebricas entre grandezas e modelagem de situacoes-problema",
    "interpretacao de grafico cartesiano e articulacao entre algebra e geometria",
    "leitura, inferencia, interpolacao, extrapolacao e tendencia em tabelas e graficos",
    "medidas de tendencia central e dispersao",
    "probabilidade, amostragem e analise de fenomenos aleatorios",
    "uso da matematica para construir argumentacao, avaliar propostas e tomar decisoes em situacoes reais",
]

MATH_FREQUENT_CONTEXTS = [
    "consumo, planejamento financeiro, juros, descontos e economia domestica",
    "transporte, mobilidade urbana, trajetos, tempo e escalas",
    "saude publica, estatisticas, vacinacao, alimentacao e qualidade de vida",
    "meio ambiente, energia, agua, residuos e sustentabilidade",
    "dados de pesquisa, graficos, tabelas, probabilidades e comparacao de cenarios",
]

MATH_ADDITIONAL_GUIDELINES = [
    "Priorize porcentagem, razao e proporcao, regra de tres, interpretacao de graficos, estatistica, probabilidade, escalas e geometria aplicada.",
    "Evite algebra pesada, demonstracoes formais e calculos excessivamente longos sem ganho interpretativo.",
    "Nao gere questoes de troco direto, soma mecanica, multiplicacao trivial ou conta escolar sem interpretacao.",
    "Em matematica no estilo ENEM, privilegie suportes como grafico, tabela, esquema, planta, mapa simples, infografico ou imagem funcional, em vez de longos textos literarios.",
    "O desafio central deve estar na modelagem da situacao, na leitura dos dados e na tomada de decisao quantitativa.",
    "Quando usar diagrama, prefira dados estruturados com medidas, rotulos e escala, para que a figura seja renderizada de forma deterministica no front.",
    "Os distratores devem refletir erros comuns de unidade, escala, proporcionalidade, leitura de eixos, arredondamento ou interpretacao de percentuais.",
]

MATH_SUPPORT_MATERIAL_PRIORITIES = [
    "grafico cartesiano, de barras ou de linhas com tendencia ou comparacao de cenarios",
    "tabela de dados quantitativos, estatisticos, financeiros ou de medicao",
    "esquema, planta, figura geometrica ou diagrama estruturado com escalas e medidas",
    "infografico ou imagem funcional apenas quando a leitura espacial ou quantitativa for essencial",
]


def get_math_topics() -> list[str]:
    return get_catalog_topics(MATH_TOPIC_CATALOG)


def build_random_math_question_context(topic: str) -> dict[str, str]:
    return build_random_topic_context(MATH_TOPIC_CATALOG, topic)


def build_enem_math_question_prompt(
    topic: str,
    subtopic: str,
    subtopic_description: str,
    diversity_mode: str,
) -> str:
    return build_enem_area_question_prompt(
        area_name="Matematica e suas Tecnologias",
        topic=topic,
        subtopic=subtopic,
        subtopic_description=subtopic_description,
        diversity_mode=diversity_mode,
        evaluation_points=MATH_EVALUATION_POINTS,
        frequent_contexts=MATH_FREQUENT_CONTEXTS,
        additional_area_guidelines=MATH_ADDITIONAL_GUIDELINES,
        support_material_priorities=MATH_SUPPORT_MATERIAL_PRIORITIES,
    )
