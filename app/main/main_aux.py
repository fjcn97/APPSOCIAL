#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SelectField
from app.main import bp

class CategoriaForm(FlaskForm):
    categoria = SelectField()
