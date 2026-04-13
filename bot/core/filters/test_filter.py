from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.models.test import Test
from bot.service.test import get_test_service


class TestFilter(Filter):


    async def __call__(
            self,
            message: Message,
            state: FSMContext,
            *args,
            **kwargs
    ):
        if message.text:
            test_service = await get_test_service()
            tests = await test_service.get_all()
            tests_names = [test.name for test in tests]
            plain_test_name = message.text.lower()
            if plain_test_name in tests_names:
                test_service = await get_test_service()
                test = await test_service.get_scalar_by_field(
                    Test.name,
                    plain_test_name
                )
                await state.update_data(test_id=test.id)
                return True
        return False