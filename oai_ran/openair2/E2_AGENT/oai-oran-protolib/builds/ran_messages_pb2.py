# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ran_messages.proto
# Protobuf Python Version: 5.29.4
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    4,
    '',
    'ran_messages.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ran_messages.proto\"\xf2\x01\n\x13RAN_param_map_entry\x12\x1b\n\x03key\x18\x01 \x02(\x0e\x32\x0e.RAN_parameter\x12\x15\n\x0bint64_value\x18\x02 \x01(\x03H\x00\x12\x16\n\x0cstring_value\x18\x03 \x01(\tH\x00\x12\x14\n\nbool_value\x18\x04 \x01(\x08H\x00\x12\x1d\n\x07ue_list\x18\x05 \x01(\x0b\x32\n.ue_list_mH\x00\x12%\n\tsche_ctrl\x18\x06 \x01(\x0b\x32\x10.sched_control_mH\x00\x12*\n\x0cslicing_ctrl\x18\x07 \x01(\x0b\x32\x12.slicing_control_mH\x00\x42\x07\n\x05value\"?\n\x16RAN_indication_request\x12%\n\rtarget_params\x18\x01 \x03(\x0e\x32\x0e.RAN_parameter\"B\n\x17RAN_indication_response\x12\'\n\tparam_map\x18\x01 \x03(\x0b\x32\x14.RAN_param_map_entry\"E\n\x13RAN_control_request\x12.\n\x10target_param_map\x18\x01 \x03(\x0b\x32\x14.RAN_param_map_entry\"\xea\x01\n\x0bRAN_message\x12#\n\x08msg_type\x18\x01 \x02(\x0e\x32\x11.RAN_message_type\x12\x39\n\x16ran_indication_request\x18\x02 \x01(\x0b\x32\x17.RAN_indication_requestH\x00\x12;\n\x17ran_indication_response\x18\x03 \x01(\x0b\x32\x18.RAN_indication_responseH\x00\x12\x33\n\x13ran_control_request\x18\x04 \x01(\x0b\x32\x14.RAN_control_requestH\x00\x42\t\n\x07payload\"\xfc\x03\n\tue_info_m\x12\x0c\n\x04rnti\x18\x01 \x02(\x05\x12\x12\n\ntbs_avg_dl\x18\x02 \x01(\x02\x12\x12\n\ntbs_avg_ul\x18\x03 \x01(\x02\x12\x16\n\x0etbs_dl_toapply\x18\x04 \x01(\x02\x12\x16\n\x0etbs_ul_toapply\x18\x05 \x01(\x02\x12\x0e\n\x06is_GBR\x18\x06 \x01(\x08\x12 \n\x18\x64l_mac_buffer_occupation\x18\x07 \x01(\x02\x12\x13\n\x0b\x61vg_prbs_dl\x18\x08 \x01(\x02\x12\x13\n\x0b\x61vg_prbs_ul\x18\t \x01(\x02\x12\x0b\n\x03mcs\x18\n \x01(\x05\x12\x1a\n\x12\x61vg_tbs_per_prb_dl\x18\x0b \x01(\x02\x12\x1a\n\x12\x61vg_tbs_per_prb_ul\x18\x0c \x01(\x02\x12\x10\n\x08\x61vg_rsrp\x18\r \x01(\x02\x12\n\n\x02ph\x18\x0e \x01(\x02\x12\r\n\x05pcmax\x18\x0f \x01(\x02\x12\x16\n\x0e\x64l_total_bytes\x18\x10 \x01(\x02\x12\x11\n\tdl_errors\x18\x11 \x01(\x02\x12\x0f\n\x07\x64l_bler\x18\x12 \x01(\x02\x12\x0e\n\x06\x64l_mcs\x18\x13 \x01(\x02\x12\x16\n\x0eul_total_bytes\x18\x14 \x01(\x02\x12\x11\n\tul_errors\x18\x15 \x01(\x02\x12\x0f\n\x07ul_bler\x18\x16 \x01(\x02\x12\x0e\n\x06ul_mcs\x18\x17 \x01(\x02\x12\x11\n\tnssai_sST\x18\x18 \x01(\x05\x12\x10\n\x08nssai_sD\x18\x19 \x01(\x05\"?\n\tue_list_m\x12\x15\n\rconnected_ues\x18\x01 \x02(\x05\x12\x1b\n\x07ue_info\x18\x02 \x03(\x0b\x32\n.ue_info_m\"2\n\x0fsched_control_m\x12\x1f\n\x17max_cell_allocable_prbs\x18\x01 \x01(\x05\"R\n\x11slicing_control_m\x12\x0b\n\x03sst\x18\x01 \x02(\x05\x12\n\n\x02sd\x18\x02 \x01(\x05\x12\x11\n\tmin_ratio\x18\x03 \x02(\x05\x12\x11\n\tmax_ratio\x18\x04 \x02(\x05*v\n\x10RAN_message_type\x12\x10\n\x0cSUBSCRIPTION\x10\x01\x12\x16\n\x12INDICATION_REQUEST\x10\x02\x12\x17\n\x13INDICATION_RESPONSE\x10\x03\x12\x0b\n\x07\x43ONTROL\x10\x04\x12\x12\n\x0eSOMETHING_ELSE\x10\x05*\x8f\x01\n\rRAN_parameter\x12\n\n\x06GNB_ID\x10\x01\x12\r\n\tSOMETHING\x10\x02\x12\x0b\n\x07UE_LIST\x10\x03\x12\x0f\n\x0bSCHED_INFO_\x10\x04\x12\x11\n\rSCHED_CONTROL\x10\x05\x12\x0b\n\x07MAX_PRB\x10\x06\x12\x10\n\x0cUSE_TRUE_GBR\x10\x07\x12\x13\n\x0fSLICING_CONTROL\x10\x08')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ran_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RAN_MESSAGE_TYPE']._serialized_start=1420
  _globals['_RAN_MESSAGE_TYPE']._serialized_end=1538
  _globals['_RAN_PARAMETER']._serialized_start=1541
  _globals['_RAN_PARAMETER']._serialized_end=1684
  _globals['_RAN_PARAM_MAP_ENTRY']._serialized_start=23
  _globals['_RAN_PARAM_MAP_ENTRY']._serialized_end=265
  _globals['_RAN_INDICATION_REQUEST']._serialized_start=267
  _globals['_RAN_INDICATION_REQUEST']._serialized_end=330
  _globals['_RAN_INDICATION_RESPONSE']._serialized_start=332
  _globals['_RAN_INDICATION_RESPONSE']._serialized_end=398
  _globals['_RAN_CONTROL_REQUEST']._serialized_start=400
  _globals['_RAN_CONTROL_REQUEST']._serialized_end=469
  _globals['_RAN_MESSAGE']._serialized_start=472
  _globals['_RAN_MESSAGE']._serialized_end=706
  _globals['_UE_INFO_M']._serialized_start=709
  _globals['_UE_INFO_M']._serialized_end=1217
  _globals['_UE_LIST_M']._serialized_start=1219
  _globals['_UE_LIST_M']._serialized_end=1282
  _globals['_SCHED_CONTROL_M']._serialized_start=1284
  _globals['_SCHED_CONTROL_M']._serialized_end=1334
  _globals['_SLICING_CONTROL_M']._serialized_start=1336
  _globals['_SLICING_CONTROL_M']._serialized_end=1418
# @@protoc_insertion_point(module_scope)
