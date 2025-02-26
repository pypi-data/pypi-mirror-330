from typing import Annotated
from fastapi import Depends
from magma_database import Sds
from magma_indonesia.dependencies import pagination as pagination_dependency
from magma_indonesia.routers.router import ApiV1Router

SeismicRouter = ApiV1Router


@SeismicRouter.get("/seismic", tags=["Seismic Index List"], name="seismic-index")
async def index(pagination: Annotated[dict, Depends(pagination_dependency)]):
    seismic_indexes = Sds.to_list(
        page_number=pagination["page"],
        item_per_page=pagination["limit"]
    )

    return {
        "total": 10,
        "pagination": pagination,
        "data": seismic_indexes,
    }
