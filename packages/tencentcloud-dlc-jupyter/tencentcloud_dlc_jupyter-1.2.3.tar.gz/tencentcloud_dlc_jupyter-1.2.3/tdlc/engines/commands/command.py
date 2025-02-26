import re
from IPython.display import Image
from tdlc.utils import render, constants, log
from tdlc import exceptions
from ipywidgets.widgets import FloatProgress, Layout

import base64
import textwrap


LOG = log.getLogger('Command')
class Command:

    def __init__(self, code) -> None:

        self.code = code
    

    def execute(self, session, kind=None):
        # TODO events
        LOG.info(f"Executing command using {session}")
        LOG.debug(f"Executing command with code:\n{self.code}")

        statement_id = -1
        try:
            session.wait_for_idle()

            r = session.submit_statement(self.code, kind)
            statement_id = r["statementId"]
            output = self._get_statement_output(session, statement_id)

        except KeyboardInterrupt as e:
            # TODO events
            try:
                if statement_id > 0:
                    r = session.cancel_statement(statement_id)
                    session.wait_for_idle()
            except Exception as e:
                LOG.error(e)
                raise exceptions.StatementCancelFailedException(pre='Interrup by user.')
            else:
                raise exceptions.StatementCancelledException(pre="Interrupt by user.")
        except Exception as e:
            # TODO events
            raise
        else:
            # TODO events
            return output
    
    def _get_statement_output(self, session, statement_id):

        progress = FloatProgress(
            value=0.0,
            min=0.0,
            max=1.0,
            step=0.01,
            description='progress:',
            bar_style='info',
            orientation='horizontal',
            layout=Layout(width="50%", height="25px"),
        )
        render.render(progress)

        retries = 1

        while True:
            statement = session.get_statement(statement_id)
            LOG.debug("The statement is :", statement)
            status = statement['status'].lower()

            if status not in constants.STATEMENT_FINAL_STATUS:
                progress.value = statement.get("progress", 0.0)
                session.sleep(1)
                retries += 1
            else:
                output = statement["output"]
                progress.close()

                if output is None:
                    return (True, "",  constants.MIMETYPE_TEXT_PLAIN)
                
                if output['status'] == constants.OUTPUT_STATUS_OK:
                    data = output['data']

                    if constants.MIMETYPE_IMAGE_PNG in data:
                        image = Image(base64.b64decode(data[constants.MIMETYPE_IMAGE_PNG]))
                        return (True, image, constants.MIMETYPE_IMAGE_PNG)
                    
                    elif constants.MIMETYPE_TEXT_HTML in data:
                        return (True, data[constants.MIMETYPE_TEXT_HTML], constants.MIMETYPE_TEXT_HTML)
                    
                    # elif constants.MIMETYPE_TEXT_PLAIN in data:
                    #     return (True, data[constants.MIMETYPE_TEXT_PLAIN], constants.MIMETYPE_TEXT_PLAIN)
                    else:
                        return (True, data[constants.MIMETYPE_TEXT_PLAIN], constants.MIMETYPE_TEXT_PLAIN)
                        # return (True, "", constants.MIMETYPE_TEXT_PLAIN)

                elif output['status'] == constants.OUTPUT_STATUS_ERROR:
                    error = output['error']
                    error_message =f'{error.get("name", "")}: {error.get("value", "")}\n {error.get("message", "")}'
                    return (False, f'{error_message}', constants.MIMETYPE_TEXT_PLAIN)
                
                else:
                    raise exceptions.UnknownStatusException(f"Unknown status 'f{output['status']}' from server.")
    