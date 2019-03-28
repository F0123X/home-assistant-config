VERSION = '0.1.0'

DOMAIN = 'say'

ATTR_MASTER = 'master'
ATTR_ENTITY_ID  = 'entity_id'
ATTR_VOLUME_LEVEL = 'volume_level'
ATTR_MESSAGE = 'message'

# { "master": "media_player.living_room_sonos", "entity_id": "media_player.living_room_sonos, media_player.family_room_sonos", "volume_level": 0.30, "message": "This is a test", "output_type": "sonos"}

ATTR_OPERATION = 'operation'

ATTR_OP_SONOS_SNAPSHOT = 'sonos_snapshot'
ATTR_OP_SONOS_UNJOIN = 'sonos_unjoin'
ATTR_OP_SONOS_JOIN = 'sonos_join'


ATTR_OP_SONOS_RESTORE = 'sonos_restore'



ATTR_OP_VOLUME_SET = 'volume_set'


TTS_DOMAIN = 'tts'
MEDIA_PLAYER_DOMAIN = 'media_player'


ATTR_TTS_SERVICE = 'google_say'


ATTR_OUTPUT_TYPE = 'output_type'
""" Not programmed yet - holding for future release """
ATTR_OT_ALEXA = 'alexa'
ATTR_OT_GOOGLE_HOME = 'google_home'
ATTR_OT_SONOS = 'sonos'

ATTR_VOLUME = 0.30

# def get_devices(master, entity_id, output_type):
#     entity_id = get_entity_ids(entity_id)
#     # if output_type == ATTR_OT_SONOS:
#     #     logger.debug('Selected Sonos as output type.')
#     if entity_id:
#         entity_id = get_entity_ids(entity_id)
#         if not master and entity_id:
#             master = entity_id[0]
#     else:
#         entity_id = get_all_devices(output_type)
#         if not master and entity_id:
#             master = entity_id[0]
#     return master, entity_id, output_type
#     # elif output_type == ATTR_OT_ALEXA:
#     #     logger.warn('This output type has not yet been programmed. Expected sonos.')
#     # elif output_type == ATTR_OT_GOOGLE_HOME:
#     #     logger.warn('This output type has not yet been programmed. Expected sonos.')
#     # else:
#     #     logger.error('Invalid output type.')

# def get_entity_ids(entity_id):
#     """ Expands entity_id (accepts group and media_player elements) """
#     if isinstance(entity_id, str):
#         entity_id = [e.strip() for e in entity_id.split(',')]
#     expanded_a_group = True
#     while entity_id and expanded_a_group:
#         expanded_a_group = False
#         for e in entity_id:
#             if e.startswith('group.'):
#                 entity_id.remove(e)
#                 g = hass.states.get(e)
#                 if g and 'entity_id' in g.attributes:
#                     entity_id.extend(g.attributes['entity_id'])
#                     expanded_a_group = True
#     return entity_id
    
# def get_all_devices(output_type):
#     """ Gets all possible media_players by type (sonos, alexa, or google_home) """
#     entity_ids = hass.states.entity_ids('media_player')
#     media_players = []
#     for e in entity_ids:
#         if output_type == ATTR_OT_SONOS and ATTR_OT_SONOS in e:
#             media_players.append(e)
#         elif output_type == ATTR_OT_ALEXA and ATTR_OT_ALEXA in e:
#             media_players.append(e)
#         elif output_type == ATTR_OT_GOOGLE_HOME and ATTR_OT_GOOGLE_HOME in e:
#             media_players.append(e)
#     return media_players

            
    
# def store_entity_id(store_name, entity_id):
#     return '{}.{}'.format(store_name, entity_id.replace('.', '_'))

entity_id = data.get(ATTR_ENTITY_ID)
master = data.get(ATTR_MASTER)
output_type = data.get(ATTR_OUTPUT_TYPE, ATTR_OT_SONOS)
volume_level = data.get(ATTR_VOLUME_LEVEL, ATTR_VOLUME)
message = data.get(ATTR_MESSAGE)


if isinstance(entity_id, str):
    entity_id = [e.strip() for e in entity_id.split(',')]
expanded_a_group = True
while entity_id and expanded_a_group:
    expanded_a_group = False
    for e in entity_id:
        if e.startswith('group.'):
            entity_id.remove(e)
            g = hass.states.get(e)
            if g and 'entity_id' in g.attributes:
                entity_id.extend(g.attributes['entity_id'])
                expanded_a_group = True

if entity_id and not master:
    master = entity_id[0]
elif not entity_id:
    entity_ids = hass.states.entity_ids('media_player')
    entity_id = [e for e in entity_ids if e.contains(output_type)]
    master = entity_id[0]
    # for e in entity_ids:
    #     if output_type in e:
    #         entity_id.append(e)
    #     if output_type == ATTR_OT_SONOS and ATTR_OT_SONOS in e:
    #         media_players.append(e)
    #     elif output_type == ATTR_OT_ALEXA and ATTR_OT_ALEXA in e:
    #         media_players.append(e)
    #     elif output_type == ATTR_OT_GOOGLE_HOME and ATTR_OT_GOOGLE_HOME in e:
    #         media_players.append(e)
    # return media_players

    # entity_id = get_all_devices(output_type)
    # if not master and entity_id:
    #     master = entity_id[0]






# master, entity_id, output_type = get_devices(master, entity_id, output_type)


if master and entity_id and message:
    entity_id = ', '.join(entity_id)
    logger.debug('Sonos entity_id is/(are) {}'.format(entity_id))

    service_data = {
        'with_group': True
    }
    hass.services.call(MEDIA_PLAYER_DOMAIN, ATTR_OP_SONOS_SNAPSHOT, service_data, True)
    logger.debug('Sonos snapshot taken.')

    service_data = {
        ATTR_ENTITY_ID: entity_id
    }
    hass.services.call(MEDIA_PLAYER_DOMAIN, ATTR_OP_SONOS_UNJOIN, service_data, True)
    logger.debug('Sonos entities are unjoined.')

    service_data = {
        ATTR_MASTER: master,
        ATTR_ENTITY_ID: entity_id
    }
    hass.services.call(MEDIA_PLAYER_DOMAIN, ATTR_OP_SONOS_JOIN, service_data, True)
    logger.debug('Sonos entities are joined.')
    
    service_data = {
        ATTR_ENTITY_ID: entity_id,
        ATTR_VOLUME_LEVEL: volume_level
    }
    hass.services.call(MEDIA_PLAYER_DOMAIN, ATTR_OP_VOLUME_SET, service_data, True)
    logger.debug('Entity volume level is set.')


    service_data = {
        "data": 
            {
                ATTR_ENTITY_ID: master,
                ATTR_MESSAGE: message
            }
    }
    
    hass.services.call(TTS_DOMAIN, ATTR_TTS_SERVICE, service_data, True)
    logger.debug('TTS process has commenced - the message is {}.'.format(message))
    logger.debug('Current status of sonos media_player is {}'.format(hass.states.get(master)))
    
    
    

    service_data = {
        'with_group': True
    }
    hass.services.call(MEDIA_PLAYER_DOMAIN, ATTR_OP_SONOS_RESTORE, service_data, True)



# # Get operation (default to save.)
# operation = data.get(ATTR_OPERATION, ATTR_OP_SAVE)
# if operation not in [ATTR_OP_SAVE, ATTR_OP_RESTORE]:
#     logger.error('Invalid operation. Expected {} or {}, got: {}'.format(
#         ATTR_OP_SAVE, ATTR_OP_RESTORE, operation))
# else:
#     # Get optional store name (default to DOMAIN.)
#     store_name = data.get(ATTR_STORE_NAME, DOMAIN)
    
#     # Get optional overwrite parameter (only applies to saving.)
#     overwrite = data.get(ATTR_OVERWRITE, True)

#     # Get optional list (or comma separated string) of switches & lights to
#     # save/restore.
#     entity_id = data.get(ATTR_ENTITY_ID)
#     if isinstance(entity_id, str):
#         entity_id = [e.strip() for e in entity_id.split(',')]

#     # Replace any group entities with their contents.
#     # Repeat until no groups left in list.
#     expanded_a_group = True
#     while entity_id and expanded_a_group:
#         expanded_a_group = False
#         for e in entity_id:
#             if e.startswith('group.'):
#                 entity_id.remove(e)
#                 g = hass.states.get(e)
#                 if g and 'entity_id' in g.attributes:
#                     entity_id.extend(g.attributes['entity_id'])
#                     expanded_a_group = True

#     # Get lists of switches and lights that actually exist,
#     # and list of entities that were previously saved.
#     entity_ids = (hass.states.entity_ids('switch') +
#                   hass.states.entity_ids('light'))
#     saved      = hass.states.entity_ids(store_name)
#     # When restoring, limit to existing entities that were saved.
#     if operation == ATTR_OP_RESTORE:
#         saved_entity_ids = []
#         for e in entity_ids:
#             if store_entity_id(store_name, e) in saved:
#                 saved_entity_ids.append(e)
#         entity_ids = saved_entity_ids

#     # If a list of entities was specified, further limit to just those.
#     # Otherwise, save all existing switches and lights, or restore
#     # all existing switches and lights that were previously saved.
#     if entity_id:
#         entity_ids = tuple(set(entity_ids).intersection(set(entity_id)))

#     if operation == ATTR_OP_SAVE:
#         # Only save if not already saved, or if overwite is True.
#         if not saved or overwrite:
#             # Clear out any previously saved states.
#             for entity_id in saved:
#                 hass.states.remove(entity_id)

#             # Save selected switches and lights to store.
#             for entity_id in entity_ids:
#                 cur_state = hass.states.get(entity_id)
#                 if cur_state is None:
#                     logger.error('Could not get state of {}.'.format(entity_id))
#                 else:
#                     attributes = {}
#                     if entity_id.startswith('light.') and cur_state.state == 'on':
#                         for attr in GEN_ATTRS:
#                             if attr in cur_state.attributes:
#                                 attributes[attr] = cur_state.attributes[attr]
#                         for attr in COLOR_ATTRS:
#                             if attr in cur_state.attributes:
#                                 attributes[attr] = cur_state.attributes[attr]
#                                 break
#                     hass.states.set(store_entity_id(store_name, entity_id),
#                                     cur_state.state, attributes)
#     else:
#         # Restore selected switches and lights from store.
#         for entity_id in entity_ids:
#             old_state = hass.states.get(store_entity_id(store_name, entity_id))
#             if old_state is None:
#                 logger.error('No saved state for {}.'.format(entity_id))
#             else:
#                 turn_on = old_state.state == 'on'
#                 service_data = {'entity_id': entity_id}
#                 component = entity_id.split('.')[0]
#                 if component == 'light' and turn_on and old_state.attributes:
#                     service_data.update(old_state.attributes)
#                 hass.services.call(component,
#                                   'turn_on' if turn_on else 'turn_off',
#                                   service_data)

#         # Remove saved states now that we're done with them.
#         for entity_id in saved:
#             hass.states.remove(entity_id)