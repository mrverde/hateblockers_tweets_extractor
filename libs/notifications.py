from datetime import datetime
from dotenv import dotenv_values


class Notifications():

    def notification(self, message: str):
        """
        Prints in console a message with the hour when a task was done
        :param message: Message to print
        """
        msg = f'{datetime.utcnow()} - {message}'

        print(msg)
        if dotenv_values()["LOG_FILE"]:
            self.add_to_a_log_file(msg)

    @staticmethod
    def add_to_a_log_file(message: str):
        """
        Exports to a log file. By default exports to a filename called sample.txt.
        Could be changed with a LOG_FILE property from .env if exists.
        :param message: Message to print
        :param filename: Name of the file where messages are going to be exported
        """
        file_object = open(dotenv_values()["LOG_FILE"], 'a')
        file_object.write(message + "\n")
        file_object.close()
