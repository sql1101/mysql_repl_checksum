#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：xushaohui time:2022/5/23

def html_data(data):
    html_body = """
        <html><head>
    <meta charset="UTF-8">
    <style>
    .mytable table {
        width:100%%;
        margin:15px 0;
        border:0;
    }
    .mytable,.mytable th,.mytable td {
        font-size:0.9em;
        text-align:left;
        padding:4px;
        border-collapse:collapse;
    }
    .mytable th,.mytable td {
        border: 1px solid #ffffff;
        border-width:1px
    }
    .mytable th {
        border: 1px solid #cde6fe;
        border-width:1px 0 1px 0
    }
    .mytable td {
        border: 1px solid #eeeeee;
        border-width:1px 0 1px 0
    }
    .mytable tr {
        border: 1px solid #ffffff;
    }
    .mytable tr:nth-child(odd){
        background-color:#f7f7f7;
    }
    .mytable tr:nth-child(even){
        background-color:#ffffff;
    }
    .mytable2 th, .mytable2 td {
        border-width:1px 1 1px 1
    }
    </style>
        </head><body>
        <div>
        %s
     </div><br/>
    </body></html>
    """ % ("".join(map(str, data)))
    return html_body
