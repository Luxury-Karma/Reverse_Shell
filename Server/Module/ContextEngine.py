from Server.Module import ConnectionHandler as CoHa

sock_handler: CoHa.SocketHandler


# wip>                                                  ATTENTION
# wip>                           THIS IS A list PRE-DEVELOPMENT CONCEPT AS CURRENTLY DEFINED

# wip>   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___

# wip>     <CONTEXT>
# wip>         Keep reference to client connection, _CONTEXT_REFERENCE_ or _REMOTE_CONTEXT_REFERENCE_

# wip>     <REMOTE CONTEXT>
# wip>         _CONTEXT_ provided by a remote _CONTEXT_ENGINE_

# wip>     <ROOT CONTEXT>
# wip>         _CONTEXT_ containing every client in every client connected to connected sock_handler

# wip>     <SAVED CONTEXT>
# wip>         _CONTEXT_ keep on permanent memory (Can be load as either a _PERMANENT_CONTEXT_ or a _TEMPORARY_CONTEXT_)

# wip>     <PERMANENT CONTEXT>
# wip>         _CONTEXT_ keep in memory even if exited need to be explicitly destroyed

# wip>     <TEMPORARY CONTEXT>
# wip>         _CONTEXT_ keep in memory and automatically destroyed if exited

# wip>     <PARENT CONTEXT>
# wip>         _CONTEXT_ keeping at least one _CHILD_CONTEXT_REFERENCE_

# wip>     <CHILD CONTEXT>
# wip>         _CONTEXT_ having is reference referenced by a _PARENT_CONTEXT_

# wip>   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___   ___

# wip>                                                  ATTENTION
# wip>                           THIS IS A list OF MY CURRENT OVERVIEW OF CONTEXT ENGINE

# wip>                          <BASE COMPONENT>
# wip>
# wip>                      1 - Generate context
# wip>                      2 - Destroy context
# wip>                      3 - Query context

# wip>                          <REFERENCE COMPONENT>
# wip>
# wip>                      1 - Generate context reference (name i give to the context in reference to the user)
# wip>                      2 - Destroy context from reference (probably using destroy context)
# wip>                      3 - Query context from reference ( probably using query context )

# wip>                          <PERMANENCE COMPONENT>
# wip>
# wip>                      1 - Save context to disk
# wip>                      2 - Load context from disk


# wip>                          <REMOTE CONTEXT COMPONENT>
# wip>
# wip>                                  ATTENTION
# wip>                      Remote context component is a module
# wip>
# wip>                      -OUTGOING
# wip>                          1 - Connect to external engine
# wip>                          2 - Disconnect from outgoing external engine connection
# wip>                          4 - List outgoing connection
# wip>                          5 - Request for remote context information
# wip>
# wip>                      -INGOING
# wip>                          3 - List ingoing connection
# wip>                          3 - Disconnect incoming external engine connection
# wip>                          5 - Send context

class ContextEngine:
    def get_root_context(self):
        return -1

    def new_context(self):
        return -1

    def del_context(self):
        return -1

    def get_context(self):
        return -1

    def new_reference(self):
        return -1

    def del_reference(self):
        return -1

    def del_from_reference(self):
        return -1

    def query_reference(self):
        return -1

    def query_from_reference(self):
        return -1

    def save_reference(self):
        return -1

    def load_reference(selfs):
        return -1

class Context:
    def __init__(self):
        pass
    def __del__(self):
        return -1



def get_connection(_id=None, single=False):
    """
    TRASH CODE TO BE REWORKED THIS IS ONLY A TEMPORARY BUFFER TO KEEP EVERYTHING WORKING WILL I WORK ON ALL THE FEATURE

    :param _id: if specified filter on id
    :return: filtered list
    :param single: bool changing type of output
    :return: single connection default to last connected if multiple in query list

    """
    global sock_handler

    # Get every connection
    connection_list = [connection[0] for connection in sock_handler.connection_list]
    # If no connection return empty
    if len(connection_list) < 1:
        return []

    # Get every connection with id
    if _id and _id != 'root':
        connection_list = [connection for connection in connection_list if _id == connection.get_id()]

    # region TODO move that part to a lib for context,context should always be list
    # Return only one item
    if single and _id:  #
        # If multiple return last connected
        if len(connection_list) > 1:
            print(f' --> [ ERROR ] MULTIPLE CONNECTION WITH SAME ID : {_id}'
                  f'\n --> Returning Last Connected {len(connection_list) - 1} excluded')
        connection_list = connection_list[-1] if connection_list else []
    elif single:
        print(' --> [ ERROR ] Single need a ID specified')
    # endregion
    return connection_list if connection_list else []
