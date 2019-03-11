class Log:
    @staticmethod
    def log_error(error_code, error_txt, app_id):
        try: 
            with open('log/app{}.log'.format(app_id), mode='a+') as f:
                # f.write(json.dumps(blockchain))
                f.write('{} - {} \n'.format(error_code, error_txt))
        except (IOError, IndexError):
            print('Saving failed!')
    
    @staticmethod
    def log_status(status_code, status_txt, app_id):
        try: 
            with open('log/app{}.log'.format(app_id), mode='a+') as f:
                # f.write(json.dumps(blockchain))
                f.write('{} - {} \n'.format(status_code, status_txt))
        except (IOError, IndexError):
            print('Saving failed!')

    @staticmethod        
    def log_message(message_txt, app_id):
        try: 
            with open('log/app{}.log'.format(app_id), mode='a+') as f:
                # f.write(json.dumps(blockchain))
                f.write('MSG - {}\n'.format(message_txt))
        except (IOError, IndexError):
            print('Saving failed!')
