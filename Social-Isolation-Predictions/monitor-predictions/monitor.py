import time
import os
import subprocess
from minio import Minio
import pandas as pd
import pickle
from elasticsearch import Elasticsearch
from sklearn.preprocessing import StandardScaler
import re
import io
  
def group_sleep(row): 
  """
    Hours sleep was further categorized into three groups: 
        -3: hours<6
        -2: 6<=hours<=8
        -1: hours>8
  """    
  if row['hsleep'] < 6:
    return 3
  elif row['hsleep'] > 8:
    return 1
  else:
    return 2

def group_pa(row): 
  """
    Physical activity was further categorized into three groups: 
        -3: None (no moderate or vigorous activity on a weekly basis)
        -2: Moderate activity at least once a week
        -1: Vigorous activity at least once a week
    Raises:
        ValueError: If none of the specified columns exist in the file.
  """    
  if row['heacta'] <= 2:
    return 1
  elif row['heactb'] <= 2:
    return 2
  else:
    return 3
  
def group_he(row): 
  """
    Self-reported health was further categorized into 2 groups: 
        -1: good health, comprising those who reported their health as excellent, very good or good
        -2: poor health, comprising fair and poor responses
  """    
  if row['hehelf'] <= 3:
    return 1
  else:
    return 2
  
def group_eye(row): 
  """
    Eyesight was further categorized into three groups: 
        -1: Optimal(Excellent and Very good)
        -2: Good
        -3: Poor(Fair or Poor)
  """    
  if row['heeye'] <= 2:
    return 1
  elif row['heeye'] == 3:
    return 2
  else:
    return 3
  
def group_hear(row): 
  """
    Hearing was further categorized into three groups: 
        -1: Optimal(Excellent and Very good)
        -2: Good
        -3: Poor(Fair or Poor)
  """    
  if row['hehear'] <= 2:
    return 1
  elif row['hehear'] == 3:
    return 2
  else:
    return 3

def obtain_data_minio(bucket_path):
    try:
        result = subprocess.run(['mc', 'ls', '--recursive', bucket_path], capture_output=True, text=True, check=True)
        output = result.stdout
        archivos = []
        for line in output.strip().split('\n'):
            match = re.search(r'\s+([^\s]+)$', line)
            if match:
                archivos.append(match.group(1))
        return archivos
    except subprocess.CalledProcessError as e:
        print(f"Error executing mc ls: {e}")
        return []

def procesar_archivo(minio_client, minio_bucket, archivo, es, model, scaler):
    try:
        data = minio_client.get_object(minio_bucket, archivo)
        df = pd.read_csv(io.BytesIO(data.data), encoding='utf-8')
        of = ['scfam','scfamg','scfamh','scfamj','scfamk']
        ch=['scchd','scchdg','scchdh','scchdj','scchdk']
        spart=['spcar','spcara','sptraa']
        fr = ['scfrd','scfrdg','scfrdh','scfrdj','scfrdk']
        
        #Sleep
        df['gsleep'] = df.apply(group_sleep, axis=1).copy()
        #Physical Activity
        df['gpa'] = df.apply(group_pa, axis=1).copy()
        #Self report Health
        df['ghealt1'] = df.apply(group_he, axis=1).copy()
        df['ghealt2'] = df['heill'].replace({1: 2, 2: 1}).copy()
        #Eye
        df['heeye'] = df['heeye'].replace(6, 5).copy()
        df['geye'] = df.apply(group_eye, axis=1).copy()
        #Hear
        df['hehear'] = df['hehear'].replace(6, 5).copy()
        df['ghear'] = df.apply(group_hear, axis=1).copy()
        #Dif walking
        df['hefunc'] = df['hefunc'].replace(4, 3).copy()
        df['gwdif'] = df['hefunc'].copy()
        #Weight
        df['gwg'] = df['heswgh'].replace({1: 2, 2: 3, 3: 1}).copy()
        #Children
        df[ch] = df[ch].replace(-1, 6).copy()
        #Other Family
        df[of] = df[of].replace(-1, 6).copy()
        #Friend
        df[fr] = df[fr].replace(-1, 6).copy()

        features_isolation = spart+ch+of+fr+['scprt','scorg96','gsleep','gpa','ghealt1','ghealt2','geye','ghear','gwdif','gwg']

        X = df[features_isolation]

        #Escalar datos
        X_scaled = scaler.transform(X)

        predictions = model.predict(X_scaled)
        df['prediction'] = predictions

        for index, row in df.iterrows():
            doc = row.to_dict()
            doc['archivo'] = archivo
            es.index(index="predicciones", document=doc)

        print(f"Archivo {archivo} procesado y enviado a Elasticsearch.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")

#Alias, bucket and key: Storage in local machine secrets.yaml
#First Elasticsearch configure
if __name__ == "__main__":
    minio_alias = os.environ.get("MINIO_ALIAS", "myminio")
    minio_bucket = os.environ.get("MINIO_BUCKET", "radar-intermediate-storage")
    bucket_path = f"{minio_alias}/{minio_bucket}"
    minio_endpoint = os.environ.get("MINIO_ENDPOINT", "minio-service:9000")
    minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
    minio_secret_key = os.environ.get("MINIO_SECRET_KEY")
    elasticsearch_host = os.environ.get("ELASTICSEARCH_HOST", "elasticsearch-service")
    elasticsearch_port = int(os.environ.get("ELASTICSEARCH_PORT", 9200))

    try:
      minio_client = Minio(minio_endpoint,
                        access_key=minio_access_key,
                        secret_key=minio_secret_key,
                        secure=False)
    except Exception as e:
      print(f"Error connecting with minio: {e}")
      exit()

    try:
      es = Elasticsearch([{'host': elasticsearch_host, 'port': elasticsearch_port}])
    except Exception as e:
      print(f"Error connecting with elasticsearch: {e}")
      exit()

#Use mlpclassifier or other model and scaler
    try:
      with open('/app/mlp_cl.pkl', 'rb') as f:
          model = pickle.load(f)
    except Exception as e:
      print(f"Error loading model: {e}")
      exit()

    try:
      with open('/app/scalermlp_cl.pkl', 'rb') as f:
          scaler = pickle.load(f)
    except Exception as e:
      print(f"Error loading scaler: {e}")
      exit()

    archivos_procesados = set()

    print("Starting monitoring...")

    while True:
        try:
            archivos = obtain_data_minio(bucket_path)

            if archivos:
                print(f"File find en MinIO: {archivos}")
                for archivo in archivos:
                    if archivo not in archivos_procesados and archivo.endswith('.csv'):
                        print(f"Processing File: {archivo}")
                        procesar_archivo(minio_client, minio_bucket, archivo, es, model, scaler)
                        archivos_procesados.add(archivo)

            time.sleep(60)

        except Exception as e:
            print(f"Error general: {e}")
            time.sleep(60)