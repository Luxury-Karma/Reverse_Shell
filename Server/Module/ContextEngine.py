from Server.Module import ConnectionHandler as CoHa

sock_handler: CoHa.SocketHandler


#                                              < ATTENTION WIP >
#                                   This is the pre development concept
#       _CONTEXT_
#           Keep reference to client connection, _CONTEXT REFERENCE_ or _REMOTE CONTEXT REFERENCE_
#       _REMOTE_CONTEXT_
#           _CONTEXT_ provided by a remote _CONTEXT ENGINE_
#       _ROOT_CONTEXT_
#           _CONTEXT_ containing every client in every client connected to connected sock_handler
#   _   _   _   _   _
#       SAVED_CONTEXT
#           _CONTEXT_ keep on permanent memory (Can be load as either a PERMANENT_CONTEXT or a TEMPORARY_CONTEXT)
#   _   _   _   _   _
#       PERMANENT_CONTEXT
#           _CONTEXT_ keep in memory even if exited need to be explicitly destroyed
#       TEMPORARY_CONTEXT
#           _CONTEXT_ keep in memory and automatically destroyed if exited
#   _   _   _   _   _
#       PARENT_CONTEXT
#           _CONTEXT_ keeping at least one _CHILD CONTEXT REFERENCE_
#       CHILD_CONTEXT
#           _CONTEXT_ having is reference referenced by a PARENT_CONTEXT
#   _   _   _   _   _
#       CURRENT DESIGN LOOK LIKE THIS
#       1 - Generate context
#       2 - Destroy context
#       3 - Query context
#       4 - Generate context reference (name i give to the context in reference to the user)
#       5 - Destroy context from reference (probably only a _d-=wa- for destroy context)
#       6 - Query context reference ( this will probably be is own query or maybe it is also onl-= for query context)
#       7 - Save context to disk
#       8 - Load context from disk
#       9 - Send Request to external context engine


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
