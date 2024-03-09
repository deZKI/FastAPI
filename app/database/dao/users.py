import qrcode
import aiofiles
from io import BytesIO

from sqlalchemy import update

from app.database.dao.base import BaseDAO
from app.database.models.users import Users
from app.database.connection import async_session_maker
from app.config import settings


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_with_qr_code(cls, **data):
        # Сначала добавляем пользователя в базу данных
        user = await cls.add(**data)

        if user:
            user_id = user.id
            # Генерация данных QR-кода
            qr_data = f"{settings.SITE_URL}/users/{user_id}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Сохраняем QR-код в файл
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            qr_code_path = f"app/media/qr_code/user_{user_id}_qr.png"

            async with aiofiles.open(qr_code_path, 'wb') as f:
                await f.write(img_bytes)

            # Обновляем путь к QR-коду для пользователя в базе данных
            async with async_session_maker() as session:
                async with session.begin():
                    await session.execute(
                        update(cls.model).
                        where(cls.model.id == user_id).
                        values(qr_code_path=qr_code_path)
                    )
                await session.commit()

            return user
