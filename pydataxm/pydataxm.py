import requests
import json
import pandas as pd
import datetime as dt
# noinspection SpellCheckingInspection


class ReadDB(object):
    
    def __new__(cls):
        return super(ReadDB, cls).__new__(cls)
    
    def __init__(self):
        """This object was created to extract data from API XM"""
        
        self.url = "http://servapibi.xm.com.co/{period_base}"
        self.connection = None
        self.request = ''
        self.lectura = requests.get(r'https://raw.githubusercontent.com/EquipoAnaliticaXM/API_XM/master/pydataxm/metricasAPI.json').json()
        self.inventario_metricas = json.loads(self.lectura)
    
    def get_collections(self, coleccion):

        return self.inventario_metricas[coleccion]

    def request_data(self, coleccion, metrica, start_date, end_date, filtros=None):
        """ request public server data from XM by the API
        Args:
            coleccion: one of the set of variables availables at self.get_collections()
            metrica:one of this variables available in "ListadoMetricas", you have to enter MetricID
            start_date: start date consult data using YYYY-MM-DD format
            end_date: end date consult data using YYYY-MM-DD format
            filter: optional parameter, list of values to filter data
        Returns: DataFrame with the raw Data
        """
        if type(filtros)==list:
            self.filtros = filtros
        elif filtros ==None:
            self.filtros=[]
        else:
            print('Los filtros deben ingresarse como una lista de valores')
            self.filtros = list
        if coleccion not in self.inventario_metricas.keys():
            print('No existe la colección {}'.format(coleccion))
            return pd.DataFrame()
        if metrica > len(self.inventario_metricas[coleccion]):
            print('No existe la metrica')
            return pd.DataFrame()

        if self.inventario_metricas[coleccion][metrica][3] == 'Horaria':
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'hourly'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2],
                                "Filter": self.filtros}

                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria':
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'daily'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2],
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Mensual':
            
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'monthly'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 732:
                    end = start_date + dt.timedelta(731)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2],
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'MonthlyEntities','Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(732)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 731 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Anual':
            
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'annual'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2],
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux


        elif self.inventario_metricas[coleccion][metrica][3] == 'Lista':
            period_base = 'lists'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            self.request = {'MetricId': coleccion,
                            'Entity': self.inventario_metricas[coleccion][metrica][2]}
  
            self.connection = requests.post(self.url, json=self.request)
            data_json = json.loads(self.connection.content)
            data = pd.json_normalize(data_json['Items'], 'ListEntities','Date', sep='_')
    
        
        cols = data.columns
        for col in cols:
            data[col] = pd.to_numeric(data[col],errors='ignore')
        if ('Date' or 'date') in cols:
            data['Date'] = pd.to_datetime(data['Date'],errors='ignore', format= '%Y-%m-%d')
        return data


if __name__ == "__main__":
    consult = ReadDB()
    df1 = consult.request_data("Gene", 0, dt.date(2021, 1, 1), dt.date(2021, 1, 5))


    
    
    
    
    