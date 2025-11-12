from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from app.api.v1.dtos.healthcheck_dto import HealthcheckDTO
from app.core.container.container import Container
from app.services.healthcheck_service import HealthCheckService

api_router = APIRouter()


@api_router.get(
    "/healthcheck",
    response_model=HealthcheckDTO,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_healthcheck(
    response: Response,
    healthcheck_service: HealthCheckService = Depends(
        Provide[Container.healthcheck_service]
    ),
) -> HealthcheckDTO:
    await healthcheck_service.check_health()
    healthcheck_dto = HealthcheckDTO.model_validate(obj={"message": "Healthy"})
    response.status_code = status.HTTP_200_OK
    return healthcheck_dto
