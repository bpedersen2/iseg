#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2020 by Andreas Langhoff *
#* <andreas.langhoff@frm2.tum.de> *
#* This program is free software; you can redistribute it and/or modify *
#* it under the terms of the GNU General Public License v3 as published *
#* by the Free Software Foundation; *
# **************************************************************************

import json
from entangle import base
from entangle.core import states , Prop, Attr
from  entangle.device.iseg import CC2xlib
import entangle.device.iseg.CC2xlib.globals

class PowerSupply(base.PowerSupply):
    properties = {
        'address': Prop(str, 'ip address of device.'),
        'user': Prop(str, 'user.'),
        'password': Prop(str, 'pw.'),
        'channel': Prop(str, 'channel.'),
        'operatingstyle': Prop(str, 'operatingstyle.',default=''),
    }

    attributes = {
         'jsonstatus':   Attr(str,'',writable = False,memorized = False),
    }

    def init(self):
        self._state = (states.INIT,self.address)
        self.channels_handled = [self.channel]
        self.waitstring =''
        self.waitstringmintime = ''
        CC2xlib.globals.CRATE.lock.acquire()
        CC2xlib.globals.CRATE.instances.append(self)
        CC2xlib.globals.CRATE.lock.release()
        CC2xlib.globals.add_monitor(self.address,self.user,self.password)

    def rolisAlive(self):
        # this function is called once the crate is alive (= can accept parameters)
        rol = []
        print("rolisAlive")
        jos = json.loads(self.operatingstyle)
        for item in jos:
            v = jos[item]
            rol.append(CC2xlib.json_data.make_requestobject("setItem",self.channel,item,v))
        return rol

    def delete(self):
        print("isegCC2xChannel.delete")
        n_instances = 0
        CC2xlib.globals.CRATE.lock.acquire()
        for i in CC2xlib.globals.CRATE.instances:
            if i == self :
                CC2xlib.globals.CRATE.instances.remove(i)
                n_instances = len(CC2xlib.globals.CRATE.instances)
        CC2xlib.globals.CRATE.lock.release()
        if not n_instances:
            CC2xlib.globals.reset()

    def On(self):
        rol = []
        rol.append(CC2xlib.json_data.make_requestobject("setItem",self.channel,"Control.On",1))
        CC2xlib.globals.queue_request(rol)

    def Off(self):
        rol = []
        rol.append(CC2xlib.json_data.make_requestobject("setItem",self.channel,"Control.On",0))
        CC2xlib.globals.queue_request(rol)


    def getItemValue(self, cmd:str)->float:
        rv = 0
        CC2xlib.globals.CRATE.lock.acquire()

        if self.channel in CC2xlib.globals.CRATE.itemUpdated:
            ours = CC2xlib.globals.CRATE.itemUpdated[self.channel]
            if cmd in ours:
                vu = ours[cmd]
                rv = float(vu['v'])
        CC2xlib.globals.CRATE.lock.release()
        return rv


    def read_voltage(self):
        return self.getItemValue("Status.voltageMeasure")


    def write_voltage(self, value):
        rol = []
        rol.append(CC2xlib.json_data.make_requestobject("setItem",self.channel,"Control.voltageSet",str(value)))
        CC2xlib.globals.queue_request(rol)


    def read_current(self):
        return self.getItemValue("Status.currentMeasure")

    def write_current(self, value):
        rol = []
        rol.append(CC2xlib.json_data.make_requestobject("setItem",self.channel,"Control.currentSet",str(value)))
        CC2xlib.globals.queue_request(rol)


    def read_jsonstatus(self):
        ours = CC2xlib.globals.StatusJson(self.channels_handled)
        return ours

    def get_jsonstatus_unit(self):
        return ''
    def state(self):
        currstate = (states.UNKNOWN,'unknown')
        CC2xlib.globals.CRATE.lock.acquire()
        currstate =  self._state  # copy.deepcopy(self._state)
        #ouritems = CC2xlib.globals.itemUpdated[self.channel] #  all messages for channel
        CC2xlib.globals.CRATE.lock.release()
        return currstate
      #  return self._state # not good as global listen function can change this value (running in another thread)
