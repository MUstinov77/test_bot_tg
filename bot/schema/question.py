from pydantic import BaseModel


class QuestionSchema(BaseModel):
    text: str
    right_answer: str
    number_of_variants: int
    test_id: int