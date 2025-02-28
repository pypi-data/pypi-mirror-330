# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger

# import logging ; logger = logging.getLogger(__name__)

# logger.info("20140227 dd.py a")

import time
# from asgiref.sync import sync_to_async

from django.conf import settings
from django.db.models import *
from django.utils import timezone

from lino.core.tables import VirtualTable

from lino.core.utils import resolve_model, UnresolvedModel

from lino.core.utils import resolve_app, require_app_models
from lino.core.utils import resolve_field, get_field
from lino.core.utils import obj2str
from lino.core.utils import obj2unicode
from lino.core.utils import range_filter
from lino.core.utils import inrange_filter
from lino.core.utils import overlap_range_filter
from lino.core.utils import full_model_name

from lino.core.model import Model

"Shortcut to :class:`lino.core.model.Model`."

from lino.core.merge import MergeAction

from lino.core.actors import Actor

from lino.core.dbtables import has_fk
from lino.core.dbtables import Table
from django.core.exceptions import FieldDoesNotExist
from django.db import models

from lino.core.frames import Frame
from lino.core.tables import VentilatingTable

from lino.core.actions import action
from lino.core.actions import Action
from lino.core.actions import WrappedAction
from lino.core.actions import MultipleRowAction
from lino.core.actions import ShowSlaveTable

from lino.core.actions import ShowTable, ShowDetail
from lino.core.actions import ShowInsert, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert

from lino.core.choicelists import ChoiceList, Choice
from lino.core.workflows import State, Workflow, ChangeStateAction

from lino.core.fields import fields_list, ImportedFields
from lino.core.fields import Dummy, DummyField
from lino.core.fields import TimeField
from lino.core.fields import TableRow

# 20140314 need a Dummy object to define a dummy module
# from lino.core.layouts import BaseLayout as Dummy  # 20140314
# from lino.core.actors import Actor as Dummy  # 20140314

from lino.core.fields import CustomField
from lino.core.fields import RecurrenceField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DatePickerField

# from lino.core.fields import NullCharField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import PercentageField

# ~ from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import DurationField
from lino.core.fields import HtmlBox, PriceField, RichTextField

from lino.core.fields import DisplayField, displayfield, htmlbox, delayedhtmlbox

# from lino.core.fields import DisplayField, displayfield, htmlbox
from lino.core.fields import VirtualField, virtualfield
from lino.core.fields import VirtualBooleanField
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant, constant
from lino.core.fields import ForeignKey, OneToOneField
from lino.core.fields import CharField

# from lino_xl.lib.appypod.mixins import PrintTableAction

from lino.core.utils import babelkw

# from lino.core.utils import babelattr
from lino.core.utils import babel_values  # alias for babelkw for backward compat

from lino.utils.choosers import chooser, action_chooser

# from lino.core.layouts import FormLayout
from lino.core.layouts import DetailLayout, InsertLayout, Panel
from lino.core.layouts import ParamsLayout, ActionParamsLayout
from lino.core.layouts import DummyPanel

from lino.core.signals import on_ui_created, pre_ui_delete, on_ui_updated

# from lino.core.signals import database_connected
from lino.core.signals import pre_startup, post_startup
from lino.core.signals import pre_analyze
from lino.core.signals import post_analyze
from lino.core.signals import auto_create
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child
from lino.core.signals import pre_remove_child
from lino.core.signals import pre_ui_save
from lino.core.signals import post_ui_save
from lino.core.signals import pre_ui_build
from lino.core.signals import post_ui_build
from lino.core.signals import post_delete, pre_delete

from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_init, post_init
from django.db.models.signals import class_prepared

from django.db.backends.signals import connection_created

from django.dispatch import receiver
# ~ from lino.core import signals

from django.db.models.fields import NOT_PROVIDED

from lino.core.inject import inject_action
from lino.core.inject import inject_field
from lino.core.inject import update_model
from lino.core.inject import update_field
from lino.core.inject import inject_quick_add_buttons
from lino.core.inject import do_when_prepared, when_prepared

from lino.core.utils import ParameterPanel, PseudoRequest

from lino.utils import IncompleteDate, read_exception

from lino.utils.format_date import fdm, fdl, fdf, fdmy
from lino.utils.format_date import fds as fds_
from lino.utils.format_date import ftl


def fds(d):
    if isinstance(d, IncompleteDate):
        return fds_(d.as_date())
    return fds_(d)


# backward compatibility
dtos = fds
from lino.utils.format_date import fdl as dtosl

babelitem = settings.SITE.babelitem
field2kw = settings.SITE.field2kw
# urlkwargs = settings.SITE.urlkwargs

from lino.utils.mldbc.fields import BabelTextField
from lino.utils.mldbc.fields import BabelCharField, LanguageField

from lino.modlib.system.choicelists import Genders, PeriodEvents, YesNo

from importlib import import_module

decfmt = settings.SITE.decfmt
str2kw = settings.SITE.str2kw
str2dict = settings.SITE.str2dict


def today(*args, **kwargs):
    # make it serializable for Django migrations
    return settings.SITE.today(*args, **kwargs)


# today = settings.SITE.today
strftime = settings.SITE.strftime
demo_date = settings.SITE.demo_date
is_abstract_model = settings.SITE.is_abstract_model
is_installed = settings.SITE.is_installed
is_hidden_plugin = settings.SITE.is_hidden_plugin
resolve_plugin = settings.SITE.resolve_plugin
get_plugin_setting = settings.SITE.get_plugin_setting
# get_db_overview_rst = settings.SITE.get_db_overview_rst
add_welcome_handler = settings.SITE.add_welcome_handler
build_media_url = settings.SITE.build_media_url
build_site_cache_url = settings.SITE.build_site_cache_url
build_static_url = settings.SITE.build_static_url
get_default_language = settings.SITE.get_default_language
get_language_info = settings.SITE.get_language_info
resolve_languages = settings.SITE.resolve_languages
babelattr = settings.SITE.babelattr
plugins = settings.SITE.plugins
format_currency = settings.SITE.format_currency

from django.utils import translation

get_language = translation.get_language

from lino.core.roles import SiteStaff, SiteUser, SiteAdmin, login_required

from lino.modlib.linod.choicelists import Procedures


def background_task(**kwargs):
    """
    Register the decorated function as a :term:`background task`.

    Keyword arguments are used as default values when checkdata creates a
    :class:`lino.modlib.linod.SystemTask` instance for this procedure.

    Except for the special keyword ``class_name``, which defaults to
    "linod.SystemTask". It is used by :mod:`lino_xl.lib.invoicing` to register a
    procedure that will create an :term:`invoicing task` instead of a normal
    :term:`background task`. :class:`lino_xl.lib.invoicing.InvoicingTask`
    instead of :class:`lino.modlib.linod.SystemTask`.

    """
    if "class_name" not in kwargs:
        kwargs["class_name"] = "linod.SystemTask"

    def decorator(func):
        Procedures.add_item(func, **kwargs)
        return func

    return decorator


def schedule_often(every=10, **kwargs):
    kwargs.update(every_unit="secondly", every=every)
    return background_task(**kwargs)


def schedule_daily(**kwargs):
    kwargs.update(every_unit="daily", every=1)
    return background_task(**kwargs)


def auto_height(n):
    """
    When specifying a `window_size`, the `height` should often be ``'auto'``,
    but extjs dopesn't support auto  height with text editor widget.
    """
    if settings.SITE.default_ui == "lino_react.react":
        return "auto"
    else:
        return n
