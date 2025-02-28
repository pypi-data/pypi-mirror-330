# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/2/19 18:50
from collections import namedtuple

MessageMemoryTypeParameter = namedtuple('MessageMemoryType', ['other', 'permanent', 'changeable',
                                                              'volatile', 'currentBuffer', 'schedule', 'blank'])

MessageMemoryType = MessageMemoryTypeParameter(1, 2, 3, 4, 5, 6, 7)

MessageStatusParameter = namedtuple('MessageStatus', ['notUsed', 'modifying', 'validating',
                                                      'valid', 'error', 'modifyReq', 'validateReq', 'notUsedReq'])
MessageStatus = MessageStatusParameter(1, 2, 3, 4, 5, 6, 7, 8)

ShortErrorStatusParameter = namedtuple('ShortErrorStatus', ['reserved', 'communications_error',
                                                            'power_error', 'attached_device_error', 'lamp_error',
                                                            'pixel_error', 'photocell_error',
                                                            'message_error', 'controller_error', 'temperature_warning',
                                                            'climate_control_system_error',
                                                            'critical_temperature_error', 'drum_sign_rotor_error',
                                                            'door_open_error', 'humidity_warning'
                                                            ])
