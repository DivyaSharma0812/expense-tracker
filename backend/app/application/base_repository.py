from typing import Generic, List, Optional, Type, TypeVar
from ..extensions import database

T = TypeVar("T", bound=database.Model)


class BaseRepository(Generic[T]):
    model_class: Type[T]

    def find_by_id(self, id: int) -> Optional[T]:
        return database.session.get(self.model_class, id)

    def find_all(self) -> List[T]:
        return database.session.execute(
            database.select(self.model_class)
        ).scalars().all()

    def save(self, instance: T) -> T:
        database.session.add(instance)
        database.session.commit()
        return instance

    def delete(self, instance: T) -> None:
        database.session.delete(instance)
        database.session.commit()
