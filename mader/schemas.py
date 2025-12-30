from pydantic import BaseModel, ConfigDict, EmailStr, Field


class _SerializationConfig(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str = Field(min_length=3)


class PublicUser(BaseModel):
    email: EmailStr
    username: str


class Message(BaseModel):
    message: str


class TokenSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class _BookOptionalBase(_SerializationConfig):
    ano: int | None
    titulo: str | None


class BookSchema(_SerializationConfig):
    ano: int
    titulo: str
    romancista_id: int


class BookUpdate(_BookOptionalBase):
    romancista_id: int | None


class PublicBook(BookSchema):
    id: int


class FilterBook(_BookOptionalBase):
    pass


class Books(BaseModel):
    livro: list[PublicBook | None]


class _AuthorOptionalBase(_SerializationConfig):
    nome: str | None = None


class AuthorSchema(_SerializationConfig):
    nome: str


class AuthorUpdate(_AuthorOptionalBase):
    pass


class PublicAuthor(BaseModel):
    id: int
    name: str


class FilterAuthor(_AuthorOptionalBase):
    page: int = Field(ge=1, default=1)


class Authors(BaseModel):
    romancistas: list[PublicAuthor]
