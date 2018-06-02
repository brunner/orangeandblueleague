#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def anchor(url, content):
    return '<a href="{}">{}</a>'.format(url, content)


def card(href='',
         title='',
         info='',
         code='',
         table=None,
         ts='',
         success='',
         danger=''):
    return {
        'href': href,
        'title': title,
        'info': info,
        'code': code,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }


def span(classes, text):
    return '<span class="{}">{}</span>'.format(' '.join(classes), text)


def table(clazz='border mt-3',
          id_='',
          hcols=None,
          bcols=None,
          head=None,
          body=None):
    return {
        'clazz': clazz,
        'id': id_,
        'hcols': hcols,
        'bcols': bcols,
        'head': head,
        'body': body
    }
