from typing import Any, List, Dict, Literal
from pydantic import BaseModel, EmailStr, Field, HttpUrl, PrivateAttr
from enum import Enum
from datetime import date, datetime


class ISoggetto(BaseModel):
    tipo: Literal["F", "G"]
    codice: str
    nome: str | None
    cognome: str | None
    denominazione: str | None = None
    indirizzo: str | None = None
    civico: str | None = None
    cap: str | None = None
    loc: str | None = None
    prov: str | None = None
    nazione: str | None = None
    email: str | None
    
class IImporto(BaseModel):
    tipo_id: str
    prog: int | None = None
    causale: str | None = None
    importo: float
    capitolo: str | None = None
    

class IChiaveDebito(BaseModel):
    idpos: str #max 256
    iddeb: str | None = None
    codice: str | None = None
    
class IDebito(IChiaveDebito):
    
    iuv: str | None = None
    dettaglio: str | None = Field(None, max_length=1000) #descrizione del pagamento(causale lunga)
    gruppo: str | None = None
    ordinamento: int | None = None
    data_inizio: date
    data_scadenza: date | None = None
    data_scadenza_avviso: date | None = None
    importo: float
    causale: str | None = Field(None, max_length=140) #causale passata a pagopa
    importi: list[IImporto]

    
class IDebitoxxx(BaseModel):
    idpos: str #max 256
    codice: str | None = None
    dettaglio: str #max 1000
    iddeb: str #univoco max 256
    iuv: str | None = None
    gruppo: str | None = None
    ordinamento: int | None = None
    data_inizio: str
    data_fine: str | None = None
    data_limite: str | None = None
    importo: float
    causale: str # max 140 
    importi: list[IImporto]
    
class IDataPagoPa(BaseModel):
    soggetto: ISoggetto
    debito: IDebito

class IEsito(BaseModel):
    esito: Literal["OK", "ERROR"]
    messaggio: str | None = None

class IConfigPagoPa(BaseModel):
    wsUrl: str
    wsUser: str
    wsPassword: str
    wsPrintUrl: str
    logoUrl: str
    codiceIpa: str
    codiceServizio: str
    notificaOK: str | None = None
    notificaKO: str | None = None
    notificaPagamento: str



