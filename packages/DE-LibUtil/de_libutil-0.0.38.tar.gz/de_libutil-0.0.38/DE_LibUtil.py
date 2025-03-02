import hashlib
import datetime as dt
import rsa
from cryptography.fernet import Fernet
#import pandas as pd
import string
from random import choice
import random as rd
import base64 as b64
import re
import os
import signal
import requests
import json

KEYS_RSA = rsa.newkeys(512)

class LIB:
    def __init__(self):
        #print('teste')
        pass

    @staticmethod
    def ping(hostname):
        # hostname = "google.com"  # example
        response = os.system("ping -n 1 " + hostname + " >> trash_ping.log")
        # and then check the response...
        if response == 0:
            result = f"""{hostname} Sucesso!"""
        else:
            result = f"""{hostname} Não encontrado!"""
        return result

    @staticmethod
    def post_message_to_slack(token, channel, text, icon_emoji, username, blocks=None, url="https://slack.com/api/chat.postMessage" ):
        return requests.post(url,
                             {'token': token,
                              'channel': channel,
                              'text': text,
                              'icon_emoji': icon_emoji,
                              'username': username,
                              'blocks': json.dumps(blocks) if blocks else None
                              }
                             ).json()

    @staticmethod
    def getPID():
        return os.getpid()

    @staticmethod
    def killPID(pid):
        result = True
        try:
            os.kill(pid, signal.SIGKILL)
        except Exception as error:
            result = False
        finally:
            return result

    @staticmethod
    def colunas_cursor(cursor) -> list:
        header = [head[0] for head in cursor.description]
        return header

    @staticmethod
    def base64_encrypt(word: str, encode_pattern: str = "utf-8"):
        encoded = (b64.b64encode(word.encode(encode_pattern)))
        encoded_ascii = encoded.decode(encode_pattern)
        return encoded_ascii

    @staticmethod
    def base64_decrypt(word: str, encode_pattern: str = "utf-8"):
        try:
            word = word.encode(encode_pattern)
            decoded = b64.b64decode(word).decode(encode_pattern)
            #decoded_ascii = decoded.decode()
        except Exception as error:
            decoded = error
        finally:
            return decodede

    @staticmethod
    def findchar(string: str, pattern: str, ocorrencia: int = None, inicio: int = 0, fim: int = 0, trim: bool = True):
        try:
            if trim:
                string = string.strip()
            if fim == 0:
                fim = len(string)
            if fim > inicio and (fim-inicio) > len(pattern):
                string = string[inicio:fim]
            if ocorrencia is not None:
                locate = re.findall(pattern, string)
                if ocorrencia is not None:
                    if ocorrencia > len(locate):
                        locate = locate[len(locate)-1]


        except Exception as error:
            locate = error
        finally:
            return locate


        # ocorrencia_localizada = []
        # while (True):
        #     str = string[string.find(substring):string.find(substring) + len(substring)]
        #     ocorrencia_localizada.append(str)
        #     if str == '':
        #         break
        # print(ocorrencia_localizada)

    @staticmethod
    def build_key(size: int = 24,
                  sep: str = "-",
                  word_length: int = 4,
                  lower_case: bool = True,
                  upper_case: bool = True,
                  digits: bool = True,
                  hex_digits: bool = False,
                  oct_digits: bool = False,
                  special_chars: bool = False,
                  printable_chars: bool = False,
                  control_chars: bool = False
                  ) -> str:
        index = 1
        key = ""
        literal = ""
        if lower_case:
            literal = literal + string.ascii_lowercase
        if upper_case:
            literal = literal + string.ascii_uppercase
        if digits:
            literal = literal + string.digits
        if hex_digits:
            literal = literal + string.hexdigits
        if oct_digits:
            literal = literal + string.octdigits
        if special_chars:
            literal = literal + string.punctuation
        if printable_chars:
            literal = literal + string.printable
        if control_chars:
            literal = literal + string.whitespace
        try:
            for i in range(size):
                letra = choice(literal)
                if index == word_length and i < size - 1:
                    key += letra + sep
                    index = 1
                else:
                    key += letra
                    index += 1
        except Exception as error:
            key = f"Impossivel gerar uma chave. Erro: {error}"
        return key

    @staticmethod
    def build_keys(qtd: int = 1,
                   size: int = 24,
                   sep: str = "-",
                   word_length: int = 4,
                   lower_case: bool = True,
                   upper_case: bool = True,
                   digits: bool = True,
                   hex_digits: bool = False,
                   oct_digits: bool = False,
                   special_chars: bool = False,
                   printable_chars: bool = False,
                   control_chars: bool = False) -> list:
        keys = []
        for index in range(qtd):
            k = LIB.build_key(size=size,
                              sep=sep,
                              word_length=word_length,
                              lower_case=lower_case,
                              upper_case=upper_case,
                              digits=digits,
                              hex_digits=hex_digits,
                              oct_digits=oct_digits,
                              special_chars=special_chars,
                              printable_chars=printable_chars,
                              control_chars=control_chars
                              )
            keys.append(k)
        return keys

    @staticmethod
    def hash(word: str, pattern: str = "md5"):
        pattern_list = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
        h, msg, error = None, None, None
        try:
            #value /= b'{word}'/
            if pattern == pattern_list[0]:
                h = hashlib.md5()
            elif pattern == pattern_list[1]:
                h = hashlib.sha1()
            elif pattern == pattern_list[2]:
                h = hashlib.sha224()
            elif pattern == pattern_list[3]:
                h = hashlib.sha256()
            elif pattern == pattern_list[4]:
                h = hashlib.sha384()
            elif pattern == pattern_list[5]:
                h = hashlib.sha512()
            h.update({word.encode()})
            msg = h.hexdigest()
        except Exception as error:
            msg = f"""Erro ao tentar montar o HASH. Erro: {error}"""
        finally:
            return msg

    @staticmethod
    def rsa_encrypt(word: str):
        msg = None
        try:
            PUBLIC_KEY = KEYS_RSA[0]
            msg = rsa.encrypt(word.encode(), PUBLIC_KEY)
            print(type(msg))
        except Exception as error:
            msg = f"""Falha ao tentar encriptografar a palavra {word}. Erro: {error}"""
        finally:
            return msg

    @staticmethod
    def rsa_decrypt(word: str):
        msg = None
        try:
            PRIVATE_KEY = KEYS_RSA[1]
            msg = rsa.decrypt(word.encode(), PRIVATE_KEY).decode()
        except Exception as error:
            msg = f"""Falha ao tentar Descriptografar a palavra {word}. Erro: {error}"""
        finally:
            return msg

    @staticmethod
    def Date_to_DateAsLong(value):
        try:
            dataaslong = int(dt.datetime.timestamp(value) * 1e3)
            return dataaslong
        except Exception as error:
            msgerro = f"""Falha ao tentar transformar um DATA em um LONG: "{value}". {error}"""
            raise Exception(msgerro)

    @staticmethod
    def DateAsLong_to_Date(value):
        try:
            date = dt.datetime.fromtimestamp(value / 1e3)
            return date
        except Exception as error:
            msgerro = f"""Falha ao tentar transformar um LONG em uma data: "{value}". {error}"""
            raise Exception(msgerro)

    @staticmethod
    def TimeAsLong_to_Time(value: dt.timedelta):
        try:
            horas_total = round((value.days * 24) + int(value.seconds / 60 / 60), 2)
            minutos = round(((value.seconds / 60 / 60) - int((value.seconds / 60) / 60)) * 60, 2)
            seg = round(((minutos - int(minutos)) * 60), 2)
            hora = f"""{horas_total}:{int(minutos):02}:{int(round(seg)):02}"""
            return hora
        except Exception as error:
            msgerro = f"""Falha ao tentar converter um timedelta para um tempo (HH:mm:ss) "{value}". {error}"""
            raise Exception(msgerro)

    @staticmethod
    def Time_to_TimeAsLong(value):
        try:
            td = value.split(":")
            h = round(int(td[0]) * 60 * 60 * 1000)
            m = round(int(td[1]) * 60 * 1000)
            s = round(int(td[2]) * 1000)
            tempo = h + m + s
            return tempo
        except Exception as error:
            msgerro = f"""Falha ao tentar converter um horario em LONG "{value}". {error}"""
            raise Exception(msgerro)

    @staticmethod
    def ifnull(var, val):
        if (var is None or var == 'None'):
            value = val
        else:
            value = var
        return value

    @staticmethod
    def iif(condicao: bool, value_true, value_false):
        if condicao:
            value = value_true
        else:
            value = value_false
        return value

    @staticmethod
    def Crud(sql: str = None, values: dict = None, conexao = None, commit: bool = True):
        msg, result, linhas_afetadas = None, [], 0
        try:
            if not isinstance(sql, str) or sql is None:
                raise Exception(f"""Comando sql não foi definido {sql}""")
            if conexao is None:
                raise Exception(f"""Conexão não foi informada {conexao}""")
            if not isinstance(values, dict):
                raise Exception(f"""Lista de valores não foi informada {values}""")
            cursor = conexao.cursor()
            cursor.execute(sql, values)
            linhas_afetadas = cursor.rowcount
            cursor.close()
            if commit:
                conexao.commit()
            msg = f"""Comando SQL executado com sucesso!"""
        except Exception as error:
            msg = f"""Falha ao tentar executar o comando SQL! Erro: {error}"""
            result = msg
        finally:
            result = {"linhas_afetadas": linhas_afetadas, "mensagem": msg, "sql": sql}
            return result

    @staticmethod
    def token_get() -> str:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        # return key.decode("ascii")
        return cipher_suite

    @staticmethod
    def CRYPTOGRAPHY(word: str, token: str = None, action: str = "E"):
        msg, result = None, None
        try:
            if action == "E":
                if isinstance(word, str):
                    word = word.encode()
                result = token.encrypt(word).decode()
            else:
                if isinstance(word, str):
                    word = word.encode()
                result = token.decrypt(word).decode()
        except Exception as error:
            msg = error.args[0]
            result = msg
        finally:
            return result

    @staticmethod
    def cores_ansi() -> dict:
        cores = {"Preto": ["\033[1;30m", "\033[1;40m"],
                 "Vermelho": ["\033[1;31m", "\033[1;41m"],
                 "Verde": ["\033[1;32m", "\033[1;42m"],
                 "Amarelo": ["\033[1;33m", "\033[1;43m"],
                 "Azul": ["\033[1;34m", "\033[1;44m"],
                 "Magenta": ["\033[1;35m", "\033[1;45m"],
                 "Cyan": ["\033[1;36m", "\033[1;46m"],
                 "Cinza Claro": ["\033[1;37m", "\033[1;47m"],
                 "Cinza Escuro": ["\033[1;90m", "\033[1;100m"],
                 "Vermelho Claro": ["\033[1;91m", "\033[1;101m"],
                 "Verde Claro": ["\033[1;92m", "\033[1;102m"],
                 "Amarelo Claro": ["\033[1;93m", "\033[1;103m"],
                 "Azul Claro": ["\033[1;94m", "\033[1;104m"],
                 "Magenta Claro": ["\033[1;95m", "\033[1;105m"],
                 "Cyan Claro": ["\033[1;96m", "\033[1;106m"],
                 "Branco": ["\033[1;97m", "\033[1;107m"],
                 "Negrito": ["\033[;1m", None],
                 "Inverte": ["\033[;7m", None],
                 "Reset (remove formatação)": ["\033[0;0m", None]}
        return cores

    @staticmethod
    def random_generator(size: int = 6, chars: str = string.ascii_uppercase + string.digits):
        value = ''.join(rd.choice(chars) for _ in range(size))
        return value

if __name__ == "__main__":
    x = LIB()
    t = x.base64_encrypt("PagSeguro-Akron")
    print(t)

