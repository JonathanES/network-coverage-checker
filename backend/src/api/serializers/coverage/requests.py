from typing import Annotated, Dict
from pydantic import Field


CoverageRequestBody = Annotated[
    Dict[str, str],
    Field(
        description="Dictionary mapping location IDs to addresses",
        examples=[
            {
                "id1": "157 boulevard Mac Donald 75019 Paris",
                "id4": "5 avenue Anatole France 75007 Paris",
                "id5": "1 Bd de Parc, 77700 Coupvray",
                "id6": "Place d'Armes, 78000 Versailles",
                "id7": "17 Rue René Cassin, 51430 Bezannes",
                "id8": "78 Le Poujol, 30125 L'Estréchure",
            }
        ],
    ),
]
