import pandas as pd
from .base import MagmaBaseModel
from .station import Station
from pandas.errors import EmptyDataError
from playhouse.migrate import *
from typing import Any, Dict, List


class Sds(MagmaBaseModel):
    nslc = ForeignKeyField(Station, field='nslc', backref='sds')
    date = DateField(index=True)
    start_time = DateTimeField(index=True, null=True)
    end_time = DateTimeField(index=True, null=True)
    completeness = DecimalField(max_digits=10, decimal_places=6)
    sampling_rate = DecimalField(max_digits=10, decimal_places=2)
    file_location = CharField()
    relative_path = CharField()
    file_size = BigIntegerField()

    class Meta:
        table_name = 'sds'
        indexes = (
            (('nslc', 'date'), True),
        )

    @staticmethod
    def to_list(page_number: int = 1, item_per_page: int = 100, nslc: str = None, ) -> List[Dict[str, Any]]:
        """Get list of SDS from database

        Returns:
            List[Dict[str, Any]]
        """
        sds_list = []

        query = Sds.select().order_by(Sds.nslc, Sds.date)
        sds_dicts = query.where(Sds.nslc == nslc.upper()) if nslc is not None else query

        _sds_list = [dict(sds_dict) for sds_dict in sds_dicts.paginate(page_number, item_per_page).dicts()]

        if len(_sds_list) == 0:
            raise EmptyDataError(f"⛔ No data for {nslc}. Check your station parameters.")

        for sds in _sds_list:
            _sds = {
                'id': sds['id'],
                'nslc': sds['nslc'],
                'date': str(sds['date']),
                'start_time': str(sds['start_time']),
                'end_time': str(sds['end_time']),
                'completeness': float(sds['completeness']),
                'sampling_rate': float(sds['sampling_rate']),
                'file_location': sds['file_location'],
                'relative_path': sds['relative_path'],
                'file_size': sds['file_size'],
                'created_at': str(sds['created_at']),
                'updated_at': str(sds['updated_at']),
            }
            sds_list.append(_sds)

        return sds_list

    @staticmethod
    def to_df(nslc: str) -> pd.DataFrame:
        df = pd.DataFrame(Sds.to_list(nslc))
        df.set_index('id', inplace=True)
        return df
