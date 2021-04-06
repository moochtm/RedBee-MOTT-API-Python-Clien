
import json
import subprocess
import os
import logging

supported_file_extensions = ['.jpg', '.mp4']


class Upload:
    def __init__(self, path, request_maker):
        self.__path = path
        self.__request_maker = request_maker
        return self.__upload(path)

    def __upload(self, path):
        """
        Uploads a file, returns a url
        :param path: path to file
        :return: url to file
        """
        if not os.path.exists(path):  # check file exists
            raise FileExistsError('File does not exist: {0}'.format(path))
        _, ext = os.path.splitext(path)  # get file extension
        if ext.lower() not in supported_file_extensions:
            raise Exception('File extension not supported: {0} ({1})'.format(path, supported_file_extensions))

        logging.debug(path)
        logging.debug(ext)

        url = self.__get_sas_uri(ext)
        _azcopy(path, url)
        return url

    def __get_sas_uri(self, extension):
        url = 'api/v1/sas/write'

        response = self.__request_maker.get(url=url)
        logging.debug(response.text.encode('utf8'))

        response = json.loads(response.text.encode('utf8'))
        uuid = response['uuid']
        sas_uri = response['sasUri']
        full_sas_uri = sas_uri.replace('customerportal', 'customerportal/' + uuid + extension)

        logging.debug('returning: %s' % full_sas_uri)
        return full_sas_uri


def _azcopy(path, url):
    cmd = r' '.join(('azcopy', 'cp', '"' + path + '"', '"' + url + '"'))
    logging.debug(cmd)
    subprocess.call(cmd)