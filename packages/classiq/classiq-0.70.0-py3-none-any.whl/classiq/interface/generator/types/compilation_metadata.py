from pydantic import BaseModel, Field, NonNegativeInt


class CompilationMetadata(BaseModel):
    should_synthesize_separately: bool = Field(default=False)
    occurrences_number: NonNegativeInt = Field(default=1)
