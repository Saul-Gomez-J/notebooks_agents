from typing import Type, Optional
from crewai_tools import BaseTool
from pydantic import BaseModel, Field, field_validator, ValidationError
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import logging

class CryptoToolInput(BaseModel):
    """Esquema de entrada para la herramienta CryptoDataTool."""
    coin_id: str = Field(..., description="ID de la criptomoneda en CoinGecko (e.g., 'bitcoin').")
    vs_currency: str = Field('usd', description="Moneda de referencia para los precios (e.g., 'usd', 'eur').")
    interval: str = Field('daily', description="Intervalo de los datos. Opciones: 'daily', 'hourly'.")
    end_date: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime('%Y-%m-%d'),
        description="Fecha de fin en formato 'YYYY-MM-DD'. Si se omite, se usará la fecha actual."
    )
    
    @field_validator('end_date')
    def validate_end_date_format(cls, v):
        """Valida que end_date esté en el formato correcto."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("`end_date` debe estar en formato 'YYYY-MM-DD'.")

class CryptoDataTool(BaseTool):
    name: str = "CryptoDataTool"
    description: str = (
        "Obtiene datos de precios y otros datos relevantes de un activo criptográfico "
        "utilizando la API de CoinGecko. Devuelve los últimos 30 días de datos."
    )
    args_schema: Type[BaseModel] = CryptoToolInput

    def _run(
        self, 
        coin_id: str, 
        vs_currency: str = 'usd', 
        interval: str = 'daily', 
        end_date: Optional[str] = None
    ) -> dict:
        """
        Recupera los datos de velas de una criptomoneda específica desde CoinGecko para los últimos 30 días.

        Args:
            coin_id (str): ID de la criptomoneda en CoinGecko.
            vs_currency (str): Moneda de referencia.
            interval (str): Intervalo de los datos ('daily' o 'hourly').
            end_date (Optional[str]): Fecha de fin en formato 'YYYY-MM-DD'. Si se omite, se usará la fecha actual.

        Returns:
            dict: Diccionario con los datos de velas y el precio actual.
        """
        try:
            logger = logging.getLogger(self.name)

            # Determinar end_date
            if end_date is None:
                end_datetime = datetime.now()
                end_date = end_datetime.strftime('%Y-%m-%d')
            else:
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

            # Calcular start_date (30 días antes de end_date)
            start_datetime = end_datetime - timedelta(days=30)
            start_date = start_datetime.strftime('%Y-%m-%d')
            
            logger.info(f"Solicitando datos para {coin_id} desde {start_date} hasta {end_date}.")
            
            # Convertir fechas a timestamp
            start_timestamp = int(time.mktime(start_datetime.timetuple()))
            end_timestamp = int(time.mktime(end_datetime.timetuple()))

            # Validar intervalo
            if interval not in ['daily', 'hourly']:
                raise ValueError("El intervalo debe ser 'daily' o 'hourly'.")

            # URL del endpoint
            url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range'

            # Parámetros de la solicitud
            params = {
                'vs_currency': vs_currency,
                'from': start_timestamp,
                'to': end_timestamp
            }

            # Realizar la solicitud
            response = requests.get(url, params=params)

            # Verificar el estado de la respuesta
            if response.status_code != 200:
                raise Exception(f"Error {response.status_code}: {response.text}")

            data = response.json()

            # Verificar si los datos están presentes
            if 'prices' not in data:
                raise ValueError("No se encontraron datos de precios en la respuesta de CoinGecko.")

            # Procesar los datos de precios
            prices = data['prices']
            df_prices = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
            df_prices['Date'] = pd.to_datetime(df_prices['Timestamp'], unit='ms')
            df_prices.set_index('Date', inplace=True)
            
            # Simplificar los datos de precios para el LLM
            df_prices = df_prices.resample('D').mean()  # Resamplear a datos diarios
            df_prices = df_prices.round(2)  # Redondear a 2 decimales
            
            # Procesar los datos de volúmenes de manera similar
            volumes = data.get('total_volumes', [])
            df_volumes = pd.DataFrame(volumes, columns=['Timestamp', 'Volume'])
            df_volumes['Date'] = pd.to_datetime(df_volumes['Timestamp'], unit='ms')
            df_volumes.set_index('Date', inplace=True)
            df_volumes = df_volumes.resample('D').mean()
            df_volumes = df_volumes.round(2)

            # Obtener el precio actual
            price_url = f'https://api.coingecko.com/api/v3/simple/price'
            price_params = {
                'ids': coin_id,
                'vs_currencies': vs_currency
            }
            price_response = requests.get(price_url, params=price_params)
            
            if price_response.status_code == 200:
                price_data = price_response.json()
                current_price = price_data.get(coin_id, {}).get(vs_currency, None)
                if current_price is None:
                    raise ValueError("No se pudo obtener el precio actual.")
            else:
                raise Exception(f"Error {price_response.status_code}: {price_response.text}")

            # Preparar la salida en un formato más simple
            prices_list = [
                {
                    "date": date.strftime('%Y-%m-%d'),
                    "price": float(price)
                }
                for date, price in df_prices['Price'].items()
            ]

            volumes_list = [
                {
                    "date": date.strftime('%Y-%m-%d'),
                    "volume": float(volume)
                }
                for date, volume in df_volumes['Volume'].items()
            ]

            # Preparar la salida
            output = {
                "prices": prices_list,
                "volumes": volumes_list,
                "current_price": round(current_price, 2)
            }

            logger.info(f"Datos recuperados exitosamente para {coin_id}.")
            return output

        except Exception as e:
            logging.error(f"Ocurrió un error al procesar la solicitud: {e}")
            raise RuntimeError(f"Ocurrió un error al procesar la solicitud: {e}")

if __name__ == "__main__":
    # Ejemplo de uso
    tool_instance = CryptoDataTool()
    input_params = {
        'coin_id': 'bitcoin',
        'vs_currency': 'usd',
        'interval': 'daily',
    }
    
    try:
        output = tool_instance.run(**input_params)
        print("\nEjemplo de datos de precios:")
        print(output['prices'][:5])  # Mostrar los primeros 5 registros
        print("\nPrecio actual:", output['current_price'])
    except Exception as e:
        print(e)