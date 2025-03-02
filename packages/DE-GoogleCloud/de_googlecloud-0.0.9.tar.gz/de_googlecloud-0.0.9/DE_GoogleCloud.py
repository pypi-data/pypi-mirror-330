# -*- coding: utf-8 -*-
import os
import datetime as dt
import hashlib
import base64
from google.cloud import storage
from google.cloud import bigquery
import google.auth



class GCP:
    def __init__(self, **kwargs):
        self._avalia_parametros_recebidos(**kwargs)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self._BUCKET_KEY

    def Upload_Bucket_Single_File(self, filename_read: str, bucket_name: str = None, bucket_path: str = None):
        tx_inicio, tx_termino, tx_tempo, msg, tx_filesize, hash_file_bucket, hash_file_local = None, None, None, None, None, None, None
        try:
            tx_inicio = dt.datetime.now()
            # Avaliando se foi informado um nome de bucket (obrigatorio ser um bucket valido)
            if bucket_name is None:
                if self._BUCKET_NAME is None:
                    raise Exception("É necessário informar um nome de bucket válido!")
                else:
                    bucket_name = self._BUCKET_NAME
            # Avaliando se foi informado um path dentro do bucket
            if bucket_path is None:
                if self._BUCKET_PATH is None:
                    bucket_path = ""
                else:
                    bucket_path = self._BUCKET_PATH
            # Obtendo o arquivo e preparando para a escrita no bucket
            basefilename = os.path.basename(filename_read)
            if bucket_path is not None:
                filename_write = os.path.join(bucket_path, basefilename).replace("\\", "/")
            else:
                filename_write = basefilename
            # Verificando se arquivo existe na origem para começar o Upload
            if os.path.isfile(filename_read):
                tx_filesize = os.path.getsize(filename_read)
                client = storage.Client()
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(filename_write)
                blob.upload_from_filename(filename_read, timeout=60)
                hash_file_bucket = self._hash_file_bucket(bucket_filename=filename_write, bucket_name=bucket_name)
                hash_file_local = self._hash_file_local(filename_read)
                if hash_file_local != hash_file_bucket:
                    msg = "Upload do arquivo foi efetuado, porém os HASH´s estão diferentes, cabe verificacao!"
                else:
                    msg = "Upload do arquivo efetuado com sucesso!"
            else:
                msg = """Arquivo não existe na origem (LOCAL). Upload não efetuado!"""
        except Exception as error:
            msg = error
        finally:
            tx_termino = dt.datetime.now()
            tx_tempo = tx_termino - tx_inicio
            file_tx_status = {"bucket": bucket_name, "buckt_path": bucket_path, "file": filename_read, "size": tx_filesize, "hash_file_bucket": str(hash_file_bucket), "hash_file_local": str(hash_file_local),  "tx_inicio": str(tx_inicio), "tx_termino": str(tx_termino), "tx_tempo": str(tx_tempo), "msg": msg}
            return file_tx_status

    def Download_Bucket_Single_File(self, bucket_filename: str, nome_bucket: str = None, path_bucket: str = None, path_local: str = None, local_filename: str = None):
        result, rx_inicio, rx_termino, rx_tempo, tx_filesize, msg, hash_file_bucket, hash_file_local = None, None, None, None, None, None, None, None
        try:
            rx_inicio = dt.datetime.now()

            # Avaliando se foi informado um nome de bucket (obrigatorio ser um bucket valido)
            if nome_bucket is None:
                if self._BUCKET_NAME is None:
                    raise Exception("É necessário informar um nome de bucket válido!")
                else:
                    nome_bucket = self._BUCKET_NAME

            # Avaliando se foi informado um path dentro do bucket
            if path_bucket is None:
                if self._BUCKET_PATH is None:
                    path_bucket = ""
                else:
                    path_bucket = self._BUCKET_PATH
            file_read = os.path.join(path_bucket, bucket_filename).replace("\\", "/")

            # Avaliando se foi informado o local e nome do arquivo
            if path_local is None:
                path_local = os.getcwd()
            if local_filename is None:
                local_filename = bucket_filename
            filename_write = os.path.join(path_local, local_filename)

            # Verificando se arquivo existe na origem
            if self._hash_file_bucket(bucket_filename=file_read, bucket_name=nome_bucket) is not None:
                if os.path.exists(path_local):
                    # Inicio do Download
                    client = storage.Client()
                    bucket = client.get_bucket(nome_bucket)
                    blob = bucket.blob(file_read)
                    blob.download_to_filename(filename_write, timeout=60)
                    hash_file_bucket = self._hash_file_bucket(bucket_filename=file_read, bucket_name=nome_bucket)
                    tx_filesize = os.path.getsize(filename_write)
                    hash_file_local = self._hash_file_local(filename_write)
                    if hash_file_local != hash_file_bucket:
                        msg = "Download do arquivo foi efetuado, porém os HASH´s estao diferentes, cabe verificacao!"
                    else:
                        msg = "Download do arquivo efetuado com sucesso!"
                else:
                    msg = "Pasta local para download não existe. Download nao efetuado!"
            else:
                msg = "Arquivo nao existe na origem (GCP). Download nao efetuado!"
        except Exception as error:
            msg = error
        finally:
            rx_termino = dt.datetime.now()
            rx_tempo = rx_termino - rx_inicio
            status = {"file": bucket_filename, "size": tx_filesize, "hash_file_bucket": str(hash_file_bucket), "hash_file_local": str(hash_file_local), "rx_inicio": str(rx_inicio), "rx_termino": str(rx_termino), "rx_tempo": str(rx_tempo), "msg": msg}
            return status

    def Upload_Bucket_Multiple_Files(self, file_list: list, nome_bucket: str = None, path_bucket: str = None):
        status_list = []
        try:
            # Avaliando se foi informado um nome de bucket (obrigatorio ser um bucket valido)
            if nome_bucket is None:
                if self._BUCKET_NAME is None:
                    raise Exception("É necessário informar um nome de bucket válido!")
                else:
                    nome_bucket = self._BUCKET_NAME
            # Avaliando se foi informado um path dentro do bucket
            if path_bucket is None:
                if self._BUCKET_PATH is None:
                    path_bucket = ""
                else:
                    path_bucket = self._BUCKET_PATH

            if file_list is None or not isinstance(file_list, list):
                raise Exception("Não existe uma lista de arquivos a ser transferida para o bucket")
            else:
                for file in file_list:
                    status = self.Upload_Bucket_Single_File(filename_read=file, bucket_name=nome_bucket, bucket_path=path_bucket)
                    status_list.append(status)

        except Exception as error:
            msg = error
        finally:
            return status_list

    def Download_Bucket_Multiple_file(self, file_list: list, bucket_name: str = None, bucket_path: str = None, local_path: str = None):
        status_list = []
        try:
            if file_list is None or not isinstance(file_list, list):
                raise Exception("Não existe uma lista de arquivos a ser transferida para o bucket")
            else:
                if file_list is None or not isinstance(file_list, list):
                    raise Exception("Não existe uma lista de arquivos a ser transferida para o bucket")
                else:
                    for file in file_list:
                        status = self.Download_Bucket_Single_File(bucket_filename=file, nome_bucket=bucket_name, path_bucket=bucket_path, path_local=local_path)
                        status_list.append(status)
        except Exception as error:
            msg = error
        finally:
            return status_list

    def _hash_file_local(self, filename: str):
        result, hash = None, None
        try:
            binary_hash = hashlib.md5(open(filename, "rb").read()).digest()
            hash = base64.b64encode(binary_hash)
        except Exception as error:
            hash = error
        finally:
            return hash.decode()

    def _hash_file_bucket(self, bucket_filename: str, bucket_name: str = None):
        result = None
        try:
            #file = os.path.join(bucket_path, bucket_filename).replace("\\", "/")
            client = storage.Client()
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(bucket_filename)
            blob.reload()
            result = blob.md5_hash
        except Exception as error:
            result = error
        finally:
            #print(result)
            return result

    def _get_crc32(self, file: str, bucket: str = None):
        # Nao Utilizada
        client = storage.Client()
        bucket = client.get_bucket(self._BUCKET_NAME)
        blob = bucket.blob(file)
        crc32 = blob.crc32c
        print(crc32)
        blob.reload()
        crc32 = blob.crc32c
        print(crc32)
        md5 = blob.md5_hash
        print(md5)
        blob = bucket.get_blob(file)
        crc32 = blob.crc32c
        print(crc32)

    def _avalia_parametros_recebidos(self, **kwargs):
        try:
            if "bucket_key" in kwargs.keys():
                self._BUCKET_KEY = kwargs.get("bucket_key")
            if "bucket_name" in kwargs.keys():
                self._BUCKET_NAME = kwargs.get("bucket_name")
            if "bucket_path" in kwargs.keys():
                self._BUCKET_PATH = kwargs.get("bucket_path")
            pass
        except Exception as error:
            raise Exception(error)
        finally:
            pass

    def bigquery_select(self):
        try:
            #credentials, project = google.auth.default()
            #credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
            #credentials, project = google.auth.default(scopes=["https://www.google.apois.com/auth/bigquery"])
            #projeto = "interoper-dataplatform-prd"
            query = "SELECT * FROM `interoper-dataplatform-prd.work_dasabi.FT_PEER_LEARNING` LIMIT 1000"
            client = bigquery.Client()
            query_job = client.query(query)
            rows = query_job.result()
            for row in rows:
                print(row.descritivo)
        except Exception as error:
            print(error)
        finally:
            pass

    def bigquery_createtable(self):
        try:
            bigquery_client = bigquery.Client()
            bigquery_dataset = bigquery_client.dataset("work_dasabi")
            client = bigquery.Client()
            table_id = bigquery_dataset.table("prmt_extracao")
            schema = [bigquery.SchemaField(name="id_sistema", field_type="STRING", mode="REQUIRED", description="ID do sistema de origem da informação"),
                      bigquery.SchemaField(name="nom_tabela", field_type="STRING", mode="REQUIRED", description="Nome da tabela no sistema de origem"),
                      bigquery.SchemaField(name="chave_tabela_values", field_type="STRING", mode="REQUIRED", description="Chave de acesso a tabela (valores)"),
                      bigquery.SchemaField(name="chave_tabela_columns", field_type="STRING", mode="REQUIRED", description="Descrição da chave da tabela (nome das colunas)"),
                      bigquery.SchemaField(name="dth_modificacao", field_type="DATETIME", mode="NULLABLE", description="Data/Hora em que houve uma modificação na tabela no sistema de origem"),
                      bigquery.SchemaField(name="dth_extracao", field_type="DATETIME", mode="REQUIRED", description="Data/Hora em que este registro foi extraido no sistema de origem"),
                      bigquery.SchemaField(name="dth_ingestao", field_type="DATETIME", mode="REQUIRED", description="Data/Hora da ingestão deste registro nesta tabela"),
                      bigquery.SchemaField(name="flg_tipo_modificacao", field_type="STRING", mode="NULLABLE", description="Tipo de modificacao que gerou este registro (I=Inclusao, U=Update, D=Delete)	"),
                      bigquery.SchemaField(name="rowid_tabela", field_type="STRING", mode="NULLABLE", description="Identificador unico do registro da tabela no sistema de origem"),
                      bigquery.SchemaField(name="referencia_extracao", field_type="STRING", mode="REQUIRED", description="Numero de lote ou qualquer informação de agrupamento para a extração"),
                      bigquery.SchemaField(name="payload", field_type="STRING", mode="REQUIRED", description="Payload do registro original no momento da extração (dh_extracao)"),
                      bigquery.SchemaField(name="hash", field_type="INTEGER", mode="REQUIRED", description="HASH-endereço logico do registro nesta tabela (primary key)"),
                      ]
            table = bigquery.Table(table_ref=table_id, schema=schema)
            table = client.create_table(table)
            print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
        except Exception as error:
            print(error)
        finally:
            pass

    def bigquery_Insert_PRMT(self):
        try:
            pass
        except Exception as error:
            print(error)
        finally:
            pass

    def bigquery_INSERT_teste(self, query_insert: str):
        try:
            # Esta aç]ão parte do principio de que o acesso ao GCP ja esta garantido no instanciamento da classe
            # bigquery_client = bigquery.Client()
            # bigquery_dataset = bigquery_client.dataset("work_dasabi")
            # client = bigquery.Client()
            # table_id = bigquery_dataset.table("TESTE_REFERENCIA_TABELA")
            query = "INSERT INTO interoper-dataplatform-prd.work_dasabi.FT_PEER_LEARNING (ID, DESCRITIVO, FLG_STATUS) VALUES(33, 'teste via python 33', 'x')"
            client = bigquery.Client()

            query_job = client.query(query)

        except Exception as error:
            print(error)
        finally:
            pass

    def bigquery_INSERT_json(self, tableID: str, rows: list, projectID: str = None, datasetID: str = None):
        try:
            client = bigquery.Client()
            if projectID is None:
                projectID = client.project
            if datasetID is None:
                datasetID = client.dataset()
            if tableID is not None:
                table_name = f"""{projectID}.{datasetID}.{tableID}"""

            errors = client.insert_rows_json(table_name, rows)

            if errors == []:
                msg = "Linhas adicionadas sem erros!"
            else:
                msg = f"""Foram encontrados erros durante a inserção das linhas. Erro: {errors}"""
        except Exception as error:
            msg = error
        finally:
            print(msg)
            return msg


if __name__ == "__main__":
    parametros = {"bucket_key": "C:\Projetos\DASABI\LibDASA\Template\interoper-dataplatform-prd-bd35fd0be08e.json",
                  "bucket_name": "interoper-dataplatform-prd-landing-dasabi",
                  "bucket_path": "Testes_almir"
                  }
    g = GCP(**parametros)
    # file_read = os.path.join("CALL_PWD_L000001_CHAMADA_SENHAS_00008.csv").replace("\\", "/")
    # g._hash_file_bucket(file_read)
    #g.bigquery_select()
    #g.bigquery_createtable()
    rows = [{"id_sistema": "gliese",
             "nom_tabela": "MPac",
             "chave_tabela_columns": "MPac_cip||MPac_visita||MPac_afinidade",
             "chave_tabela_values": "7666300895||13||1",
             "dth_modificacao": str(dt.datetime.strptime("18/02/2022", "%d/%m/%Y")),
             "dth_extracao": str(dt.datetime.now()),
             "dth_ingestao": str(dt.datetime.now()),
             "flg_tipo_modificacao": "I",
             "rowid_tabela": "AAC4pFACdAAALa3AAa",
             "referencia_extracao": "Lote 001",
             "hash": 1,
             "payload": r"""{"MPac_afinidade": 1,
                              "MPac_assinatura": None,
                              "MPac_cip": 7666300895,
                              "MPac_codigoAgenda": None,
                              "MPac_codigoInternoLaboratorio": None,
                              "MPac_data": "28022022",
                              "MPac_dataHora": "20220228 000052",
                              "MPac_dataHoraAltAdm": None,
                              "MPac_dataPreAdm": None,
                              "MPac_empresa": "31",
                              "MPac_flagPreAdm": "1",
                              "MPac_idMultimed": None,
                              "MPac_laboratorio": "null",
                              "MPac_refHistorica": None,
                              "MPac_regHospital": None,
                              "MPac_status": None,
                              "MPac_tipoPacHospital": None,
                              "MPac_unidadeAtendimento": "DPI",
                              "MPac_unidadeAtendimentoAdm": "DPI",
                              "MPac_visita": 13,
                              "id": "7666300895||13||1",
                              "MPac_dataAlteracaoConvenio": None,
                              "MPac_isK2": None,
                              "MPac_dataHoraTermino": None,
                              "MPac_dataHoraInicio": None,
                              "MPac_ColConsultorio": "null",
                              "MPac_admOrigem": "AGD",
                              "MPac_checkin": "Sim",
                              "ROWID_TABELA": "AAC4pFACdAAALa3AAa",
                              "CHAVE_TABELA": "7666300895||13||1",
                              "NOME_TABELA": "MPac"}""".strip("\t")
             },
            {"id_sistema": "gliese",
             "nom_tabela": "MPac",
             "chave_tabela_columns": "MPac_cip||MPac_visita||MPac_afinidade",
             "chave_tabela_values": "7666300895||13||1",
             "dth_modificacao": str(dt.datetime.strptime("18/02/2022", "%d/%m/%Y")),
             "dth_extracao": str(dt.datetime.now()),
             "dth_ingestao": str(dt.datetime.now()),
             "flg_tipo_modificacao": "I",
             "rowid_tabela": "AAC4pFACdAAALa3AAa",
             "referencia_extracao": "Lote 001",
             "hash": 1,
             "payload": r"""{"MPac_afinidade": 1,
                                  "MPac_assinatura": None,
                                  "MPac_cip": 7666300895,
                                  "MPac_codigoAgenda": None,
                                  "MPac_codigoInternoLaboratorio": None,
                                  "MPac_data": "28022022",
                                  "MPac_dataHora": "20220228 000052",
                                  "MPac_dataHoraAltAdm": None,
                                  "MPac_dataPreAdm": None,
                                  "MPac_empresa": "31",
                                  "MPac_flagPreAdm": "1",
                                  "MPac_idMultimed": None,
                                  "MPac_laboratorio": "null",
                                  "MPac_refHistorica": None,
                                  "MPac_regHospital": None,
                                  "MPac_status": None,
                                  "MPac_tipoPacHospital": None,
                                  "MPac_unidadeAtendimento": "DPI",
                                  "MPac_unidadeAtendimentoAdm": "DPI",
                                  "MPac_visita": 13,
                                  "id": "7666300895||13||1",
                                  "MPac_dataAlteracaoConvenio": None,
                                  "MPac_isK2": None,
                                  "MPac_dataHoraTermino": None,
                                  "MPac_dataHoraInicio": None,
                                  "MPac_ColConsultorio": "null",
                                  "MPac_admOrigem": "AGD",
                                  "MPac_checkin": "Sim",
                                  "ROWID_TABELA": "AAC4pFACdAAALa3AAa",
                                  "CHAVE_TABELA": "7666300895||13||1",
                                  "NOME_TABELA": "MPac"}""".strip("\t")
             },
            {"id_sistema": "gliese",
             "nom_tabela": "MPac",
             "chave_tabela_columns": "MPac_cip||MPac_visita||MPac_afinidade",
             "chave_tabela_values": "7666300895||13||1",
             "dth_modificacao": str(dt.datetime.strptime("18/02/2022", "%d/%m/%Y")),
             "dth_extracao": str(dt.datetime.now()),
             "dth_ingestao": str(dt.datetime.now()),
             "flg_tipo_modificacao": "I",
             "rowid_tabela": "AAC4pFACdAAALa3AAa",
             "referencia_extracao": "Lote 001",
             "hash": 1,
             "payload": r"""{"MPac_afinidade": 1,
                                  "MPac_assinatura": None,
                                  "MPac_cip": 7666300895,
                                  "MPac_codigoAgenda": None,
                                  "MPac_codigoInternoLaboratorio": None,
                                  "MPac_data": "28022022",
                                  "MPac_dataHora": "20220228 000052",
                                  "MPac_dataHoraAltAdm": None,
                                  "MPac_dataPreAdm": None,
                                  "MPac_empresa": "31",
                                  "MPac_flagPreAdm": "1",
                                  "MPac_idMultimed": None,
                                  "MPac_laboratorio": "null",
                                  "MPac_refHistorica": None,
                                  "MPac_regHospital": None,
                                  "MPac_status": None,
                                  "MPac_tipoPacHospital": None,
                                  "MPac_unidadeAtendimento": "DPI",
                                  "MPac_unidadeAtendimentoAdm": "DPI",
                                  "MPac_visita": 13,
                                  "id": "7666300895||13||1",
                                  "MPac_dataAlteracaoConvenio": None,
                                  "MPac_isK2": None,
                                  "MPac_dataHoraTermino": None,
                                  "MPac_dataHoraInicio": None,
                                  "MPac_ColConsultorio": "null",
                                  "MPac_admOrigem": "AGD",
                                  "MPac_checkin": "Sim",
                                  "ROWID_TABELA": "AAC4pFACdAAALa3AAa",
                                  "CHAVE_TABELA": "7666300895||13||1",
                                  "NOME_TABELA": "MPac"}""".strip("\t")
             }
            ]
    g.bigquery_INSERT_json(projectID="interoper-dataplatform-prd", datasetID="work_dasabi", tableID="prmt_extracao", rows=rows)