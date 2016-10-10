#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Poem


def more_poems(request):
    if request.is_ajax():
        Poems = Poem.objects.all()
        #[{author:'allen',title:'1'},{}]
        data = get_json_objects(Poems, Poem)
        print(data)
        print(type(data))
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def json_filed(field_data):
    if isinstance(field_data, str):
        return "\"" + field_data + "\""
    if isinstance(field_data, bool):
        if field_data == 'False':
            return 'false'
        else:
            return 'true'
    return str(field_data)

def json_encode_dict(dict_data):
    json_data = "{"
    for (k,v) in dict_data.items():
        json_data = json_data +json_filed(k) + ": " + json_filed(v) + ","
    print(type(json_data))
    print "json_data:",json_data
    print "json_data[:-2]:",json_data[:-1]
    json_data = json_data[:-1] + "}"
    return json_data

def json_encode_list(list_data):
    json_res = "["
    for item in list_data:
        json_res = json_res + json_encode_dict(item) + ","

    return json_res[:-1] + "]"

#model_meta为原型,objects为对象
def get_json_objects(objects, model_meta):
    concrete_model = Poem._meta.concrete_model
    print "concrete_model:",type(concrete_model)
    list_data = []
    for obj in objects:
        dict_data = {}
        for field in Poem._meta.local_fields:#把所有的字段拿出来，但不需要id
            if field.name == 'id':
                continue
            value = field.value_from_object(obj)#拿出字段的值
            dict_data[field.name] = value

        list_data.append(dict_data)
    print "list_data:",list_data
    #data=list_data
    data = json_encode_list(list_data)
    return data

import ast

#ast.literal_eval()
#则会判断需要计算的内容计算后是不是合法的python类型，如果是则进行运算，否则就不进行运算。


def add(request):
    if request.is_ajax() and request.POST:
        json_str = request.POST.get('poems')
        data = "post success 学习Python"
        json_list = ast.literal_eval(json_str)
        #print "json_list:",json_list

        for item in json_list:
            print "item:",item
            new_obj = Poem()
            for filed in item:
                setattr(new_obj, filed, item[filed])
            print(new_obj.author, new_obj.title, new_obj.poem_id)
            new_obj.save()
        return HttpResponse(data, content_type='application/text')
    else:
        return Http404

def index(request):
    return render(request,'index.html',locals())
    