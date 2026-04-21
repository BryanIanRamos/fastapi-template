from datetime import date

from pydantic import BaseModel, ConfigDict


class BatchBase(BaseModel):
    date_started: date
    date_count: date
    male_count: int = 0
    female_count: int = 0
    total_population: int = 0
    status: str


class BatchCreate(BatchBase):
    model_config = ConfigDict(extra='forbid')


class BatchUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    date_started: date | None = None
    date_count: date | None = None
    male_count: int | None = None
    female_count: int | None = None
    total_population: int | None = None
    status: str | None = None


class BatchRead(BatchBase):
    batch_id: str

    class Config:
        from_attributes = True
