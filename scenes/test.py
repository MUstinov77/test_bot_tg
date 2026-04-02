from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message

from keyboards.dynamic import get_enumerated_keyboard, get_dynamic_keyboard
from service.question import get_question_service
from service.test import get_test_service


class TestScene(Scene, state="test"):

    @on.message.enter()
    async def on_enter(
            self,
            message: Message,
            state: FSMContext
    ):
        await message.answer(
            "Чтобы завершить тест, нажмите /stop"
        )
        data = await state.get_data()
        test_id = data.get("test_id")
        question_service = await get_question_service()
        question = await question_service.get_random_question(test_id)
        await state.update_data(
            questions_count=0,
            right_answers_count=0,
            question=question,
        )
        await message.answer(
            question.text,
            reply_markup=get_enumerated_keyboard(question.number_of_variants).as_markup(resize_keyboard=True)
        )

    @on.message(F.text.isdigit())
    async def answer(
            self,
            message: Message,
            state: FSMContext
    ):
        data = await state.get_data()
        question = data.get("question")
        questions_count = data.get("questions_count")
        right_answers_count = data.get("right_answers_count")
        if message.text == question.right_answer:
            right_answers_count += 1
            await state.update_data(
                right_answers_count=right_answers_count,
            )
            await message.answer("Правильно!")
        else:
            await message.answer(f"Неправильно :( Правильным ответом было {question.right_answer}")
        test_id = data.get("test_id")
        question_service = await get_question_service()
        next_question = await question_service.get_random_question(test_id)
        while question.id == next_question.id:
            question_service = await get_question_service()
            next_question = await question_service.get_random_question(test_id)
        await state.update_data(
            questions_count=questions_count+1,
            question=next_question
        )
        await message.answer(
            next_question.text,
            reply_markup=get_enumerated_keyboard(question.number_of_variants).as_markup(resize_keyboard=True)
        )


    @on.message(Command("stop"))
    async def stop_test(self, message: Message):
        await self.wizard.exit()


    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext):
        data = await state.get_data()
        questions_count = data.get("questions_count")
        right_answers_count = data.get("right_answers_count")
        answer = f"Тест окончен\n Всего вопросов: {questions_count}\n Правильных ответов: {right_answers_count}\n"
        await message.answer(answer)
        test_service = await get_test_service()
        test_names = [test.name for test in await test_service.get_all()]
        await message.answer(
            "Возвращаюсь к выбору теста",
            reply_markup=get_dynamic_keyboard(test_names).as_markup(resize_keyboard=True)
        )