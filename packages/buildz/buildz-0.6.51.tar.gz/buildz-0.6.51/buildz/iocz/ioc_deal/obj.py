
from .base import *
from ... import dz,pyz
from ..ioc.single import Single
class ObjectEncape(BaseEncape):
    '''
        id=?
        
    '''
    def init(self, single, src, args, maps, sets, before_set=None, after_set=None):
        super().init()
        self.single = Single(single)
        self.src, self.args, self.maps, self.sets = src, args, maps, sets
        self.before_set = before_set
        self.after_set = after_set
        self.objs = {}
    def call(self, params=None, **maps):
        obj, find = self.single.get(params)
        if find:
            return obj
        src = self.src
        if params is None:
            obj_conf = Params(obj = self)
        else:
            obj_conf = params.clone(obj=self)
        if isinstance(src, Encape):
            src = src(obj_conf)
        args = [self.obj(k,obj_conf) for k in self.args]
        _maps = {self.obj(k,obj_conf):self.obj(v,obj_conf) for k,v in self.maps}
        obj = src(*args, **_maps)
        self.obj(self.before_set, obj_conf)
        for k,v in self.sets:
            setattr(obj, self.obj(k,obj_conf), self.obj(v,obj_conf))
        self.obj(self.after_set, obj_conf)
        self.single.set(params, obj)
        return obj
class ObjectDeal(BaseDeal):
    def init(self):
        super().init()
        self.load_srcs = {}
    def build(self, conf, unit):
        id,id_find = unit.conf_key(conf)
        single = dz.g(conf, single=None)
        if single is None and not id_find:
            single = Single.Key.multi
        src, args, maps, sets = dz.g(conf, source=None, args=[], maps={},sets=[])
        before_set, after_set = dz.g(conf, before_set=None, after_set=None)
        before_set = self.get_encape(before_set, unit)
        after_set = self.get_encape(after_set, unit)
        if Confs.is_conf(src):
            src = unit.get_encape(src, unit)
        elif type(src)==str:
            if src not in self.load_srcs:
                self.load_srcs[src] = pyz.load(src)
            src = self.load_srcs[src]
        args = [self.get_encape(k, unit) for k in args]
        lmaps = []
        for k,v in dz.dict2iter(maps):
            lmaps.append((self.get_encape(k, unit),self.get_encape(v, unit)))
        lsets = []
        for k,v in dz.dict2iter(sets):
            lsets.append((self.get_encape(k, unit),self.get_encape(v, unit)))
        encape = ObjectEncape(single, src, args, lmaps, lsets,before_set,after_set)
        return encape

pass