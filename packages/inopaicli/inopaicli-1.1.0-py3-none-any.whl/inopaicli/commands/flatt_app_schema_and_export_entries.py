import json
from argparse import ArgumentParser
from inopaicli.concepts.io_search.functions import io_search
from inopaicli.core.export import get_export_filename
from inopaicli.core.file import write_json
from inopaicli.concepts.app.api import get_apps, get_time_entries

DESCRIPTION = "Export group ios entries in json format"
EXAMPLES = [
    "inopaicli flatt_app_schema_and_export_entries -a 3580 -g 6264 --buildappschema=true --column properties.status,properties.product.properties.brand  -f ./a.json --force --transitionlogstats=true --timeentriesstats=true",
    "inopaicli flatt_app_schema_and_export_entries -a 3580  -g 6264 --buildappschema=true --column properties.estimatedworkvalueforrepairprice,properties.orderNumber,properties.status,properties.errorDescriptionCustomer,properties.imagesForErrorDescription,properties.desiredDateCompletion,properties.storageLocation,properties.createdAt,properties.failures,properties.repairUpTo,properties.notesForDelivery,properties.wunschterminzurabholung,properties.priority,properties.deliveryOrPickUpAtStore,properties.contactviaemail,properties.contactviatelephone,properties.contactviawhatsapp,properties.costEstimation,properties.visualCheckAdditionalInformation,properties.visualCheck,properties.contactviaemailtext,properties.contactviatelephonetext,properties.contactviawhatsapptext,properties.accessories,properties.pickUpFromCustomer,properties.pickUpFromCustomerDesiredDate,properties.contactviaemailabholung,properties.contactviaemailtextabholung,properties.contactviatelephoneabholung,properties.contactviatelephonetextabholung,properties.contactviawhatsappabholung,properties.contactviawhatsapptextabholung,properties.pickUpFromCustomerNote,properties.servicePackageAdditionalInformation,properties.customerDoesNotWantRepair,properties.privacyPolicyAccepted,properties.termsAccepted,properties.contact_salutation,properties.contact_title,properties.contact_firstName,properties.contact_lastName,properties.contact_email,properties.contact_mobile,properties.contact_phone,properties.billingAddress_recipient,properties.billingAddress_streetName,properties.billingAddress_streetNumber,properties.billingAddress_postalCode,properties.billingAddress_city,properties.billingAddress_country,properties.deliveryAddress_recipient,properties.deliveryAddress_streetName,properties.deliveryAddress_streetNumber,properties.deliveryAddress_postalCode,properties.deliveryAddress_city,properties.deliveryAddress_country,properties.checklistitems,properties.estimatedworkvalueforrepair,properties.workvaluefordiagnosis,properties.workvaluefordiagnosisprice,properties.totalworkvalue,properties.totalworkvalueprice,properties.totalloss,properties.workvalueforrepair,properties.notesforrepair,properties.notestotalloss,properties.errordescriptionmechanic,properties.notesfinalcheck,properties.costestimationcleared,properties.notescostestimation,properties.billavailable,properties.notesworkshopmanager,properties.errordescriptionmechanicna,properties.devicepickedupordisposed,properties.estimatedtotalworkvalueprice,properties.failurecodes,properties.checklistitemsna,properties.errordescriptionmechanicna2,properties.estimatedworkvalueforrepairna,properties.workvaluefordiagnosisna,properties.totallossna,properties.notestotallossna,properties.workvaluefordiagnosisna2,properties.mechanic,properties.notesdisposedevice,properties.servicepackages,properties.diagnosefinisheddatetime,properties.erpid,properties.imported,properties.contactviasms,properties.contactviasmstext,properties.contactviasmsabholung,properties.contactviasmstextabholung,properties.diagnosefinisheddatetimena,properties.devicepickedup,properties.deposit,properties.pickUpAddress_recipient,properties.pickUpAddress_streetName,properties.pickUpAddress_streetNumber,properties.pickUpAddress_postalCode,properties.pickUpAddress_city,properties.pickUpAddress_country,properties.totalprice,properties.customerserviceprice,properties.estimatedtotalprice,properties.sparepartsready,properties.imagesfordiagnosis,properties.imagesforrepair,properties.imagesforfinalinspection,properties.temperature,properties.altitude,properties.weather,properties.fueltype,properties.customerwishesrepair,properties.notesforspareparts,properties.diagnosisreport2,properties.reportdiagnosis,properties.productdisposed,properties.totalpricewithtax,properties.norepairrequired,properties.expecteddelivery,properties.repairuntil,properties.repairimmediately,properties.repaironsite,properties.customerbuysnewdevice,properties.notesforbill,properties.notesnorepairrequired,properties.notescustomerbuysnewdevice,properties.productwasdisposed,properties.storeproduct,properties.anyusedsparepartswarrantytrue,properties.devicenolongerstored,properties.productproductgroup,properties.kostenstelle,properties.billingaddress_name2,properties.billingaddress_name3,properties.billingAddress_name2,properties.billingAddress_name3,properties.customer_customertype,properties.customer_memo,properties.customer_notes,properties.customer_searchname,properties.customer_vat,properties.warrantyorderexists,properties.checkwarranty,properties.totalpricewithtaxsaas,properties.hasotheropenservices,properties.customerreferencenumber,properties.commissionnumber,properties.archived,properties.statuslastmodified,properties.product_operatinghours,properties.warrantycompleted,properties.notesforwarranty,properties.warrantystatus,properties.warrantycreatedate,properties.warrantytotalprice,properties.warrantytotalpricewithtax,properties.warrantytotalpricewithtaxtest,properties.status,properties.product.properties.brand,properties.product.properties.productGroup  -f ./basefile --timeentriesstats=true"
]


def get_relation_columns(*, columns):
    result = []
    for c in columns:
        # properties.customer.properties.brand
        path_depth = len(c.split("."))
        if path_depth == 1:
            raise Exception(f"{c} not possible ")
        if path_depth == 3:
            raise Exception("properties.relation.properties not possible ")
        if path_depth > 4:
            raise Exception("unkown case")
        if path_depth == 4:
            result.append(c)
    return result


def get_flatted_property_name(*, c_name):
    return "__".join([e for e in c_name.split(".") if e != "properties"])


from datetime import datetime


def get_status_switch_time(hit, status):
    if status == "created":
        return hit["created"]
    transitionstats = hit["transitionstats"]
    for t in transitionstats:
        if t.get("state_next") == status:
            return t.get("created")
    return None


def diff_status_time(*, hit, status1, status2):
    t1 = get_status_switch_time(hit=hit, status=status1)
    t2 = get_status_switch_time(hit=hit, status=status2)
    if (t1 is None) or (t2 is None):
        return None
    return (time_format(time=format_z(time=t2)) -
            time_format(time=format_z(time=t1))).total_seconds()


def format_z(*, time):
    if '+' in time:
        time = f"{time.split('+')[0]}Z"
    FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(time, FORMAT).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def time_format(*, time):
    FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(time, FORMAT)


def add_status_stats(hit, properties, handled_status):
    created = hit["created"]
    i = 0
    transitionstats = hit["transitionstats"]

    while (i < len(transitionstats)):
        status_name = transitionstats[i].get("state_next")
        if status_name not in handled_status:
            handled_status.append(status_name)
        properties[f"status__{status_name}_start"] = format_z(
            time=transitionstats[i - 1].get("created") if i != 0 else created
        )
        properties[f"status__{status_name}_end"] = format_z(
            time=transitionstats[i].get("created")
        )
        properties[f"status__{status_name}_diff"] = (
            time_format(time=properties[f"status__{status_name}_end"]) -
            time_format(time=properties[f"status__{status_name}_start"])
        ).total_seconds()
        i = i + 1


transitionlog_stats_metrics = {
    "tranisitionlog__count":
    lambda hit: len(hit.get("tranisitionlog", {}).get("statusanalytics", [])),
    "tranisitionlog__time_until_repairstart":
    lambda hit:
    diff_status_time(hit=hit, status1="created", status2="JA_Reparatur_durchführen"),
    "tranisitionlog__time_until_abgeschlossen":
    lambda hit:
    diff_status_time(hit=hit, status1="created", status2="PA_Auftrag_abgeschlossen"),
    "tranisitionlog__time_diagnose_until_repairstart":
    lambda hit: diff_status_time(
        hit=hit, status1="BA_Diagnose_durchführen", status2="JA_Reparatur_durchführen"
    ),
}


def add_transitionlogstats(*, properties, hit, handled_status):
    add_status_stats(properties=properties, hit=hit, handled_status=handled_status)
    for metric, cal_method in transitionlog_stats_metrics.items():
        properties[metric] = cal_method(hit)


def extend_with_time_entries_stats(
    *, time_entries_for_io, properties, transition_status
):
    know_users = []
    properties["timetracking__count"] = len(time_entries_for_io)
    for time_entry in time_entries_for_io:
        if time_entry is None:
            continue
        data_snapshot = time_entry.get("data_snapshot", {})

        status = None

        if data_snapshot:
            status = data_snapshot.get("status", {})
        if status not in transition_status:
            transition_status.append(status)
        if status:
            properties[f"timetracking__{status}__time_in_seconds"] = time_entry.get(
                "time_in_seconds"
            )
            properties[f"timetracking__{status}__time_in_seconds_corrected"
                       ] = time_entry.get("time_in_seconds_corrected")
        if time_entry.get("user") not in know_users:
            know_users.append(time_entry.get("user"))
    properties["timetracking__usercount"] = len(know_users)


def get_ios_to_sync(*, hits, columns, transitionlogstats, time_entries):
    properties_to_sync = []
    handled_status = []
    transition_status = []

    relation_columns = get_relation_columns(columns=columns)
    for hit in hits:
        properties = {}
        if time_entries:
            #  print(str(hit.get("id")), time_entries.keys())
            extend_with_time_entries_stats(
                time_entries_for_io=time_entries.get(str(hit.get("id")), []),
                properties=properties,
                transition_status=transition_status
            )

        if transitionlogstats:

            add_transitionlogstats(
                properties=properties, hit=hit, handled_status=handled_status
            )
        for c in columns:
            if c in relation_columns:
                f_name = get_flatted_property_name(c_name=c)
                properties[f_name] = find(c, hit)
            else:
                p_name = c.split(".")[1]
                properties[p_name] = hit.get("properties").get(p_name)
        properties_to_sync.append(properties)
    return properties_to_sync, handled_status, transition_status


def get_related_required_apps(*, url, app, columns, session_id):
    relation_columns = get_relation_columns(columns=columns)
    app_ids = []
    for c in relation_columns:
        relation_name = c.split(".")[1]
        property_schema = app["schema"]["properties"][relation_name]
        app_ids.append(property_schema["ranges"][0])
    apps = get_apps(baseurl=url, app_ids=app_ids, session_id=session_id)
    result = {}
    for app in apps["rows"]:
        result[str(app["id"])] = app
    return result


def get_unique_key(*, dict, property_name):
    i = 0
    while property_name in dict:
        property_name = f'{property_name}_{i}'
        i = i + 1
    return property_name


def handle_choice_properties(*, p_schema, root_app, new_schema):
    #    if p_schema.get("format", None) in ["choices", "multichoices"] and p_schema.get("choices", {}).get("$ref", None) :

    if p_schema.get("format", None) not in [
        "choice", "multichoices"
    ] or not p_schema.get("choices", {}).get("$ref", None):
        return
    ref = p_schema.get("choices", {}).get("$ref", None)
    if ref is None:
        return
    definition_ref = ref.replace("#/schema/definitions/", "")
    definition_ref = definition_ref.replace("#/definitions/", "")
    definition = root_app["schema"]["definitions"][definition_ref]
    new_definition_name = get_unique_key(
        dict=new_schema["definitions"], property_name=definition_ref
    )
    new_schema["definitions"][new_definition_name] = definition
    p_schema["choices"]["$ref"] = f"#/definitions/{new_definition_name}"


#  new_schema["properties"][p_name] = p_schema


def get_initial_properties_schema(
    *, status_time, transitionlogstats, transition_status
):
    properties_schema = {}
    if transitionlogstats:
        properties_schema = {
            "tranisitionlog__time_until_repairstart": {
                "type": "number",
                "verbose_name": "tranisitionlog__time_until_repairstart"
            },
            "tranisitionlog__time_until_abgeschlossen": {
                "type": "number",
                "verbose_name": "tranisitionlog__time_until_abgeschlossen"
            },
            "tranisitionlog__time_diagnose_until_repairstart": {
                "type": "number",
                "verbose_name": "tranisitionlog__time_diagnose_until_repairstart"
            },
            "tranisitionlog__count": {
                "type": "integer", "verbose_name": "tranisitionlog__count"
            },
        }
    for s in status_time:
        properties_schema[f"status__{s}_start"] = {
            "format": "date-time",
            "type": "string",
            "verbose_name": f"status__{s}_start"
        }
        properties_schema[f"status__{s}_end"] = {
            "format": "date-time", "type": "string", "verbose_name": f"status__{s}_end"
        }
        properties_schema[f"status__{s}_diff"] = {
            "type": "number", "verbose_name": f"status__{s}_diff"
        }
    print(
        transition_status,
        "transition_statustransition_statustransition_statustransition_statustransition_status"
    )
    for s in transition_status:
        properties_schema[f"timetracking__{s}__time_in_seconds_corrected"] = {
            "type": "number",
            "verbose_name": f"timetracking__{s}__time_in_seconds_corrected"
        }
        properties_schema[f"timetracking__{s}__time_in_seconds"] = {
            "type": "number", "verbose_name": f"timetracking__{s}__time_in_seconds"
        }
    return properties_schema


def get_build_app_schema(
    *,
    related_apps,
    root_app,
    columns,
    transition_status,
    status_time,
    transitionlogstats
):
    print(status_time, transition_status)
    relation_columns = get_relation_columns(columns=columns)
    schema = {
        "properties":
        get_initial_properties_schema(
            status_time=status_time,
            transition_status=transition_status,
            transitionlogstats=transitionlogstats
        ),
        "definitions": {}
    }
    for c in columns:
        p_name = c.split(".")[1]
        p_schema = root_app.get("schema").get("properties").get(p_name, None)
        if p_schema is None:
            continue
        if p_schema.get("format") in ['relation', 'multirelation'
                                      ] and len(c.split(".")) == 2:

            print(
                f"warning!, you are trying to add a relation {c} to schema, this is not possible please make sure to export subproperty of the relation like this: properties.{c}.properties.thePropertyYouNeedToExport"
            )
            continue
        if c in relation_columns:
            related_app_id = p_schema["ranges"][0]
            related_app = related_apps[str(related_app_id)]
            related_property_name = c.split(".")[3]
            relation_p_schema = related_app.get("schema").get("properties").get(
                related_property_name, None
            )
            relation_p_schema.pop('formula', None)
            handle_choice_properties(
                p_schema=relation_p_schema, root_app=related_app, new_schema=schema
            )
            schema["properties"][get_flatted_property_name(c_name=c)
                                 ] = relation_p_schema
        else:
            p_schema.pop('formula', None)
            handle_choice_properties(
                p_schema=p_schema, root_app=root_app, new_schema=schema
            )
            schema["properties"][p_name] = p_schema
    return schema


def find(element, json):
    keys = element.split('.')
    rv = json
    for key in keys:
        rv = rv.get(key, None)
        if not rv:
            return None
    return rv


def init(parser: ArgumentParser):
    parser.add_argument('-a', '--app', type=int, help='Application ID')
    parser.add_argument('-g', '--group', type=int, help='Group ID')
    parser.add_argument('--columns')
    parser.add_argument(
        '-f',
        '--filename',
        help='Filename for destination json file (print if no filename given)'
    )
    parser.add_argument('--force', action='store_true', default=False)
    parser.add_argument('-q', '--query', default="")
    parser.add_argument('--buildappschema', default=False)
    parser.add_argument('--timeentriesstats', default=False)
    parser.add_argument('--transitionlogstats', default=False)

    parser.add_argument('--sourceoverride', default=False)
    parser.add_argument(
        '--limitresults', type=int, help='Total Results Limit', default=0
    )


def get_properties(*, columns):
    return [c for c in columns.split(",") if len(c.split(".")) > 0]


def main(
    url: str,
    session_id: str,
    group: int,
    app: int,
    filename: str,
    limitresults: int,
    query=None,
    force=False,
    sourceoverride=None,
    columns=None,
    buildappschema=False,
    timeentriesstats=False,
    transitionlogstats=False,
    **kwargs,
):
    filename = get_export_filename(group, app, 'json', filename, force)
    source_override = json.loads(sourceoverride) if sourceoverride else None
    if columns:
        source_override = columns.split(',')

    embedded = ['io_type', 'related_ios', 'related_ios__io_type'
                ] if buildappschema else []

    if source_override is None:
        source_override = []
    if len(source_override) != 0:
        source_override.append("group")
        source_override.append("id")
        source_override.append("io_type")
        source_override.append("created")
        if transitionlogstats:
            source_override.append("transitionlogstats")
            source_override.append("transitionstats")

    search_response = io_search(
        url=url,
        session_id=session_id,
        group=group,
        app=app,
        query=query,
        modified=False,
        field_query_extra={},
        source_override=source_override,
        total_limit=limitresults,
        embedded=embedded,
        search_once=False
    )

    time_entries = None
    if timeentriesstats:
        time_entries = get_time_entries(
            baseurl=url, app_id=app, session_id=session_id, debug=True
        )
    write_json(data=time_entries, filename=f"{filename}_time_entries")
    the_root_app = search_response["apps"][0]

    hits = search_response["hits"]
    ios = [hit.get("_source") for hit in hits]

    write_json(data=ios, filename=f"{filename}_ios1234.json")



    properties_to_upload, status_time, transition_status = get_ios_to_sync(hits=ios, columns=get_properties(columns=columns), transitionlogstats=transitionlogstats, time_entries=time_entries)
    write_json(data=properties_to_upload, filename=f"{filename}_ios.json")

    related_apps = get_related_required_apps(
        url=url, session_id=session_id, app=the_root_app, columns=columns.split(",")
    )

    print(status_time, transition_status)
    new_schema = get_build_app_schema(
        related_apps=related_apps,
        root_app=the_root_app,
        columns=columns.split(","),
        transition_status=transition_status,
        status_time=status_time,
        transitionlogstats=transitionlogstats,
    )

    #  print(new_schema)

    write_json(data={"schema": new_schema}, filename=f"{filename}_schema.json")
