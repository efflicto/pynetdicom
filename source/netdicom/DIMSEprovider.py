#
# Copyright (c) 2012 Patrice Munger
# This file is part of pynetdicom, released under a modified MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pynetdicom.googlecode.com
#

import DIMSEmessages
import DIMSEparameters
from DIMSEmessages import DIMSEMessage


class DIMSEServiceProvider(object):
    def __init__(self, DUL):
        self.DUL = DUL
        self.message = None

    def Send(self,primitive,id, maxpdulength):
        # take a DIMSE primitive, convert it to one or more DUL primitive and send it
        if primitive.__class__ == DIMSEparameters.C_ECHO_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_ECHO_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_ECHO_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_STORE_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_STORE_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_STORE_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_FIND_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_FIND_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_FIND_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_GET_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_GET_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_GET_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_MOVE_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_MOVE_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_MOVE_RSP_Message()
        dimse_msg.FromParams(primitive)
        pdatas=dimse_msg.Encode(id,maxpdulength)
        for pp in pdatas:
            self.DUL.Send(pp)

    def Receive(self, Wait=False):
        if self.message == None:
            self.message = DIMSEMessage()
        if Wait:
            while not self.message.Decode(self.DUL.ReceiveDIMSE(Wait)):
                pass
            tmp = self.message
            self.message = None
            return tmp.ToParams(), tmp.ID
        else:
            if self.message.Decode(self.DUL.ReceiveDIMSE(Wait)):
                tmp = self.message
                self.message = None
                return tmp.ToParams(), tmp.ID
            else:
                return None, None