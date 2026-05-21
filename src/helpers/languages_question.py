from src.helpers.enem_question_common import (
    build_enem_area_question_prompt,
    build_random_topic_context,
    get_catalog_topics,
)


LANGUAGES_TOPIC_CATALOG = {
    "Lingua Portuguesa": {
        "subtopics": [
            {
                "name": "Leitura e interpretacao de generos textuais",
                "description": (
                    "Analise de generos textuais, sequencias discursivas, efeitos de sentido "
                    "e organizacao do texto em contextos sociais."
                ),
            },
            {
                "name": "Coesao, coerencia e progressao textual",
                "description": (
                    "Identificacao de elementos de articulacao de ideias, progressao tematica "
                    "e organizacao semantica em diferentes textos."
                ),
            },
            {
                "name": "Norma padrao e variacao linguistica",
                "description": (
                    "Reconhecimento de usos da lingua, marcas de variedade linguistica e "
                    "adequacao ao contexto comunicativo."
                ),
            },
        ],
        "diversity_modes": [
            "noticia e interpretacao",
            "campanha publicitaria",
            "artigo de opiniao",
            "tirinha ou charge",
        ],
    },
    "Literatura": {
        "subtopics": [
            {
                "name": "Texto literario e contexto historico-social",
                "description": (
                    "Relacao entre texto literario, momento de producao, contexto historico, "
                    "social e politico."
                ),
            },
            {
                "name": "Procedimentos de construcao literaria",
                "description": (
                    "Analise de recursos expressivos, organizacao textual e concepcoes "
                    "artisticas em diferentes generos literarios."
                ),
            },
            {
                "name": "Patrimonio literario e valores humanos",
                "description": (
                    "Reconhecimento da permanencia e atualizacao de valores sociais e "
                    "humanos no patrimonio literario."
                ),
            },
        ],
        "diversity_modes": [
            "fragmento literario",
            "comparacao de estilos",
            "contexto historico-cultural",
            "analise de linguagem poetica",
        ],
    },
    "Artes": {
        "subtopics": [
            {
                "name": "Funcoes sociais da arte",
                "description": (
                    "Reconhecimento das funcoes da arte e das producoes artisticas em seus "
                    "meios culturais."
                ),
            },
            {
                "name": "Diversidade artistica e cultural",
                "description": (
                    "Analise da diversidade de producoes artisticas e de suas relacoes com "
                    "cultura, identidade e preconceitos."
                ),
            },
            {
                "name": "Leitura de linguagens artisticas",
                "description": (
                    "Interpretacao de elementos de artes visuais, musica, teatro ou danca "
                    "em situacoes de fruicao e cidadania."
                ),
            },
        ],
        "diversity_modes": [
            "obra artistica comentada",
            "critica cultural",
            "cartaz de exposicao",
            "leitura de imagem",
        ],
    },
    "Educacao Fisica": {
        "subtopics": [
            {
                "name": "Linguagem corporal e identidade",
                "description": (
                    "Compreensao da linguagem corporal como meio de interacao social e "
                    "formacao de identidade."
                ),
            },
            {
                "name": "Praticas corporais e cultura",
                "description": (
                    "Reconhecimento das praticas corporais como manifestacoes culturais, "
                    "sociais e historicas."
                ),
            },
            {
                "name": "Corpo, saude e sociedade",
                "description": (
                    "Analise de exercicio fisico, saude, lazer e transformacao de habitos "
                    "corporais em diferentes contextos."
                ),
            },
        ],
        "diversity_modes": [
            "situacao cotidiana de saude",
            "campanha de qualidade de vida",
            "pratica corporal e cultura",
            "analise critica de comportamento",
        ],
    },
    "Lingua Estrangeira": {
        "subtopics": [
            {
                "name": "Compreensao de tema em lingua estrangeira",
                "description": (
                    "Associacao de vocabulos e expressoes em lingua estrangeira moderna "
                    "ao tema e ao contexto do texto."
                ),
            },
            {
                "name": "Estruturas linguisticas e uso social",
                "description": (
                    "Relacao entre estruturas linguisticas, funcao do texto e seu uso social "
                    "em lingua estrangeira moderna."
                ),
            },
            {
                "name": "Diversidade cultural e linguistica",
                "description": (
                    "Reconhecimento da importancia da producao cultural em lingua estrangeira "
                    "como representacao de diversidade cultural."
                ),
            },
        ],
        "diversity_modes": [
            "texto em lingua estrangeira",
            "campanha internacional",
            "postagem digital",
            "producao cultural estrangeira",
        ],
    },
    "Tecnologias da Comunicacao": {
        "subtopics": [
            {
                "name": "Sistemas de comunicacao e informacao",
                "description": (
                    "Identificacao das linguagens e dos recursos expressivos dos sistemas "
                    "de comunicacao e informacao."
                ),
            },
            {
                "name": "Funcao social das tecnologias da comunicacao",
                "description": (
                    "Analise do impacto social das tecnologias de comunicacao e informacao "
                    "no cotidiano e no desenvolvimento do conhecimento."
                ),
            },
            {
                "name": "Generos digitais e interacao",
                "description": (
                    "Interpretacao de generos digitais, interlocutores, recursos linguisticos "
                    "e funcao social das novas tecnologias."
                ),
            },
        ],
        "diversity_modes": [
            "genero digital",
            "analise de rede social",
            "texto multimodal",
            "campanha de comunicacao",
        ],
    },
}

LANGUAGES_EVALUATION_POINTS = [
    "generos textuais e sequencias discursivas em diferentes esferas sociais",
    "coerencia, coesao, progressao tematica e organizacao semantica do texto",
    "recursos expressivos, funcoes da linguagem e estrategias argumentativas",
    "norma padrao, variacao linguistica e adequacao ao contexto de uso",
    "relacoes entre texto literario, contexto historico e procedimentos de construcao",
    "producao artistica, diversidade cultural e leitura de linguagens esteticas",
    "linguagem corporal, praticas corporais, identidade e saude",
    "compreensao de textos em lingua estrangeira moderna e suas funcoes sociais",
    "tecnologias da comunicacao, generos digitais e impacto social das linguagens",
]

LANGUAGES_FREQUENT_CONTEXTS = [
    "noticias, reportagens, textos de divulgacao e artigos de opiniao",
    "propagandas, campanhas publicas, posts digitais, memes, tirinhas e charges",
    "poemas, contos, cronicas, letras de musica e outros fragmentos literarios",
    "cartazes, obras de arte, criticas culturais e situacoes de linguagem corporal",
]

LANGUAGES_ADDITIONAL_GUIDELINES = [
    "Priorize leitura atenta, inferencia, analise de efeito de sentido e interpretacao de linguagem verbal e nao verbal.",
    "Quando apropriado, use texto-base, fragmento literario, propaganda, charge, campanha, postagem digital ou outro genero frequente no ENEM.",
    "Evite questoes de pura classificacao gramatical sem contexto e sem efeito interpretativo.",
]


def get_languages_topics() -> list[str]:
    return get_catalog_topics(LANGUAGES_TOPIC_CATALOG)


def build_random_languages_question_context(topic: str) -> dict[str, str]:
    return build_random_topic_context(LANGUAGES_TOPIC_CATALOG, topic)


def build_enem_languages_question_prompt(
    topic: str,
    subtopic: str,
    subtopic_description: str,
    diversity_mode: str,
) -> str:
    return build_enem_area_question_prompt(
        area_name="Linguagens, Codigos e suas Tecnologias",
        topic=topic,
        subtopic=subtopic,
        subtopic_description=subtopic_description,
        diversity_mode=diversity_mode,
        evaluation_points=LANGUAGES_EVALUATION_POINTS,
        frequent_contexts=LANGUAGES_FREQUENT_CONTEXTS,
        additional_area_guidelines=LANGUAGES_ADDITIONAL_GUIDELINES,
    )
