# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from imio.fpaudit import _
from imio.fpaudit.storage import store_config
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import widget
from plone.registry.interfaces import IRecordModifiedEvent
from plone.z3cform import layout
from z3c.form.validator import NoInputData
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant


class ILogInfoSchema(Interface):
    log_id = schema.TextLine(
        title=_("Log id"),
        required=True,
    )

    audit_log = schema.TextLine(
        title=_("Audit file name"),
        description=_("Will be located in var/log"),
        required=True,
    )

    log_format = schema.TextLine(
        title=_("Log format"),
        default=u"%(asctime)s - %(message)s",
        required=True,
    )


class IFPAuditSettings(Interface):

    log_entries = schema.List(
        title=_(""),
        required=False,
        value_type=DictRow(title=_(u"Field"), schema=ILogInfoSchema, required=False),
    )
    widget(
        "log_entries",
        DataGridFieldFactory,
        display_table_css_class="listing",
        allow_reorder=False,
        auto_append=False,
    )

    @invariant
    def validate_settings(data):  # noqa
        # check ITableListSchema id uniqueness
        ids = []
        try:
            values = getattr(data, "log_entries") or []
        except NoInputData:
            return
        for entry in values:
            if entry["log_id"] in ids:
                raise Invalid(
                    _(
                        u"You cannot use same id multiple times '${id}'",
                        mapping={"id": entry["log_id"]},
                    )
                )
            ids.append(entry["log_id"])


class FPAuditSettings(RegistryEditForm):

    schema = IFPAuditSettings
    schema_prefix = "imio.fpaudit.settings"
    label = _("FP Audit Settings")


FPAuditSettingsView = layout.wrap_form(FPAuditSettings, ControlPanelFormWrapper)


def settings_changed(event):
    """Manage a record change"""
    if (
        IRecordModifiedEvent.providedBy(event)
        and event.record.interfaceName
        and event.record.interface != IFPAuditSettings
    ):
        return
    if event.record.fieldName == "log_entries":
        store_config(event.record.value)
