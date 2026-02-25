from fastapi import APIRouter,Body, HTTPException,UploadFile,File,Form,Response,Request

from src.route.dependency import AdminDep,DbDep
from src.schemas.masters import MasterSpecializationCreateSchema
from src.schemas.service import ServiceCreateSchemas
from src.schemas.admin import AdminLoginSchema
from src.service.masters import MastersService
from src.service.salon import SalonService
from src.service.masters_specializations import MasterSpecializationService
from src.service.service import ServService
from src.service.users import UsersService
from src.service.admin import AdminService
from src.utils.exceptions import ApplicationApproved,ApplicationNoFound,AdminNoFound,IncorectNowPassword, IncorectSecretWord, IncorectToken ,RequestCooldownError,ImageInDbNoFound, ImageInDirNoFound, IncorectTypeFile, IncorectTypeImage, SalonNoFound, SessionExpired, UserNoFound,IdSpecializationNoFound,ServiceNoFound
from src.models.enum import CityEnum

router = APIRouter(prefix="/admin",tags=["Админ ручки"])


@router.post("/service-add/{specialization_id}", summary="Добавление услуг")
async def add_service(specialization_id : int ,db : DbDep,admin : AdminDep, data : ServiceCreateSchemas = Body(openapi_examples= {"1" : {
    "summary" : "Наращивание ресниц",
    "value" : {
        "name": "Наращивание ресниц",
        "category": "lash"
    }
 }})):
    try:
        result = await ServService(db).create(specialization_id,data)
        await db.commit()
        return {"data" : result}
    except IdSpecializationNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.post(
    path="/master/confirm/{id}", summary="Одобрение заявки на добавления мастера админом"
)
async def confirm_application(id: int,admin : AdminDep, db: DbDep):
    try:
        result = await MastersService(db).confirm(id)
        await db.commit()
        return {"data": result}
    except ApplicationNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except ApplicationApproved as exc:
        raise HTTPException(status_code=409, detail=exc.detail)


@router.post(path='/specialization/add', summary="Добавление специализации")
async def add_specialization(db : DbDep,admin : AdminDep, data : MasterSpecializationCreateSchema = Body(openapi_examples={"1" : {
    "summary" : "Лашмейкер",
    "value" : {
        "name" : "Лашмейкер"
    }
}
})):
    result = await MasterSpecializationService(db).create(data)
    await db.commit()
    return {"data" : result}

@router.delete("/user/delete/{id}", summary="Удалить пользователя")
async def user_delete(db: DbDep, id: int, admin : AdminDep):
    try:
        result = await UsersService(db).delete_user(id)
        await db.commit()
        return {"data": result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    
@router.delete("/service/delete/{id}",summary="Удалить услугу")
async def service_delete(db : DbDep, id : int, admin : AdminDep):
    try:
        result = await ServService(db).delete_service(id)
        await db.commit()
        return {"data" : result}
    except ServiceNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)

@router.patch("/user/create-administrator/{id_user}", summary="Сделать пользователя администратором")
async def create_administrator(db : DbDep, id_user : int, admin : AdminDep):
    try: 
        result = await UsersService(db).replace_role_the_administrator(id_user)
        await db.commit()
        return {"data" : result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404,detail=exc.detail)
    
@router.post("/salon/create", summary='Добавить салон')
async def salon_create(db : DbDep, 
                       admin : AdminDep, 
                       name : str = Form(),
                       address : str = Form(),
                       city : CityEnum = Form(),
                       image : UploadFile = File()
):
    try:
        result = await SalonService(db).salon_create(
            name=name,
            city=city.value,
            image=image,
            address=address
            )
        await db.commit()
        return {"message" : result}
    except IncorectTypeImage as exc:
        raise HTTPException(status_code=415, detail=exc.detail)

@router.patch(path='/update', summary='Обновление данных о салоне')
async def update_salons(db : DbDep,
                        admin : AdminDep,
                        id_salon : int,
                        name : str | None = Form(None),
                        address : str | None = Form(None),
                        city : CityEnum | None = Form(None),
                        delete_portfolio_images : list[str] | None = Form(None),  
                        image : UploadFile | None = File(None),
                        portfolio_image : list[UploadFile] | None = File(None)            
):
    try:
        result = await SalonService(db).salon_update(
            id_salon=id_salon,
            name=name,
            address=address,
            city=city,
            image=image,
            portfolio_image=portfolio_image,
            delete_portfolio_images=delete_portfolio_images     
        )
        await db.commit()
        return {'message' : result}
    except SalonNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except IncorectTypeFile as exc:
        raise HTTPException(status_code=400, detail=exc.detail)
    except ImageInDbNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except ImageInDirNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.post(path='/login', summary='Логирование для админов')
async def login_admin(db : DbDep,response : Response,data_login : AdminLoginSchema):
    try:
        result = await AdminService(db).login_admins(data_login)
        await db.commit()
        response.set_cookie('verify_token', result)
        return {'message' : 'OK'}
    except AdminNoFound:
        raise HTTPException(status_code=400, detail='Что то пошло не так')
    except IncorectNowPassword:
        await db.commit()
        raise HTTPException(status_code=400, detail='Что совершилось не так')
    except RequestCooldownError:
        raise HTTPException(status_code=400, detail='Повторите позже')
    
@router.post(path='/login/verify', summary='Проверка секретного слова')
async def verify_secret_word(db : DbDep,request : Request,secret_word : str = Body()):
    token = request.cookies.get('verify_token')
    if not token:
        raise HTTPException(status_code=400, detail='Что то пошло не так...')
    try: 
        await AdminService(db).verify_secret_word(token, secret_word)
    except AdminNoFound:
        raise HTTPException(status_code=400,detail='Путь не найден')
    except SessionExpired:
        raise HTTPException(status_code=400,detail='Путь истёк')
    except IncorectToken:
        raise HTTPException(status_code=400,detail='Неверный путь')
    except IncorectSecretWord:
        raise HTTPException(status_code=400,detail='Неверный путеводитель')

    await db.commit()
    return {'message' : 'OK'}