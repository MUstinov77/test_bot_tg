from schema.question import QuestionSchema
from docx import Document
from service.question import get_question_service


async def make_test():
    file = "test.docx"
    test_id = 1
    doc = Document(file)
    number_of_variants = 2
    for i, paragraph in enumerate(doc.paragraphs):
        right_answer = "1" if i % 2 == 0 else "2"
        question_service = await get_question_service()
        question_data = QuestionSchema(
            text=paragraph.text,
            right_answer=right_answer,
            number_of_variants=number_of_variants,
            test_id=test_id
        )
        await question_service.create_instance(question_data.model_dump())