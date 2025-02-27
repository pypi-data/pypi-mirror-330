# Copyright (c) 2019-2025 Watsen Networks. All Rights Reserved.

from __future__ import annotations
_k=' found): '
_j='module'
_i='.plugins.'
_h='operation-failed'
_g='data-exists'
_f='missing-attribute'
_e='Unable to parse "input" JSON document: '
_d='malformed-message'
_c='text/plain'
_b='yangcore:'
_a='reference-statistics'
_Z='": '
_Y='cert-data'
_X='\\g<1>'
_W='.*plugins/plugin=([^/]*).*'
_V='pytest missing?'
_U='cleartext-private-key'
_T='function'
_S='application/yang-data+json'
_R='certificates'
_Q='YANGCORE_TEST_FIFO'
_P='public-key'
_O='name'
_N='plugin'
_M='certificate'
_L='operation-not-supported'
_K=False
_J=True
_I='functions'
_H='unknown-element'
_G='sleep'
_F='asymmetric-key'
_E='invalid-value'
_D='application'
_C='protocol'
_B='/'
_A=None
from enum import IntFlag
from enum import Enum
import contextlib,importlib,datetime,asyncio,signal,base64,json,sys,os,re,yangson,basicauth
from aiohttp import web
from fifolock import FifoLock
from passlib.hash import sha256_crypt
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5915
from pyasn1_modules import rfc5652
from pyasn1.error import PyAsn1Error
from pyasn1.codec.der.decoder import decode as decode_der
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import ExtensionOID
from cryptography import x509
from.val import ValidationLayer
from.rcsvr import RestconfServer
from.handler import RouteHandler
from.import dal
from.import val
from.import utils
from yangcore.yl import yl_8525_to_7895
class RefAction(IntFlag):ADDED=1;REMOVED=2
class TimeUnit(Enum):DAYS=2;HOURS=1;MINUTES=0
class Period:
	def __init__(A,amount,units):A.amount=amount;A.units=units
class PluginNotFound(Exception):0
class PluginSyntaxError(Exception):0
class FunctionNotFound(Exception):0
class FunctionNotCallable(Exception):0
class Read(asyncio.Future):
	@staticmethod
	def is_compatible(holds):return not holds[Write]
class Write(asyncio.Future):
	@staticmethod
	def is_compatible(holds):A=holds;return not A[Read]and not A[Write]
class BinaryTypePatcher:
	def __init__(A):A.save=yangson.datatype.BinaryType.from_raw
	async def __aenter__(B):
		def A(self,raw):assert self is not _A;assert raw is not _A;return bytes(0)
		yangson.datatype.BinaryType.from_raw=A
	async def __aexit__(A,exc_type,exc,tb):yangson.datatype.BinaryType.from_raw=A.save
class NativeViewHandler(RouteHandler):
	len_prefix_running=RestconfServer.len_prefix_running;len_prefix_operational=RestconfServer.len_prefix_operational;len_prefix_operations=RestconfServer.len_prefix_operations;supported_media_types=_S,
	def __init__(A,_dal,_loop):
		N='certificates/certificate/cert-data';M='yangcore:plugins';A.dal=_dal;A.loop=_loop;A.fifolock=FifoLock();A.create_callbacks={};A.change_callbacks={};A.delete_callbacks={};A.subtree_change_callbacks={};A.somehow_change_callbacks={};A.leafref_callbacks={};A.periodic_callbacks={};A.onetime_callbacks={};A.plugins={};B=A.dal.handle_get_opstate_request('/ietf-yang-library:yang-library',{});O=A.loop.run_until_complete(B);P=yl_8525_to_7895(O);A.dm=yangson.DataModel(json.dumps(P),A.dal.module_paths);A.val=ValidationLayer(A.dm,A.dal);B=A.dal.handle_get_opstate_request('/yangcore:plugins',{})
		try:G=A.loop.run_until_complete(B)
		except dal.NodeNotFound:pass
		else:
			if _N in G[M]:
				for D in G[M][_N]:
					Q=D[_O];B=_handle_plugin_created('',{_N:D},'',A);A.loop.run_until_complete(B)
					if _I in D:
						for R in D[_I][_T]:S='FOO/plugins/plugin='+Q+'/BAR';B=_handle_function_created('',{_T:R},S,A);A.loop.run_until_complete(B)
		H='/yangcore:users/user/authentication/password-based/password';A.register_create_callback(H,_handle_user_passwd_created);A.register_change_callback(H,_handle_user_passwd_changed);F='/yangcore:plugins/plugin';A.register_create_callback(F,_handle_plugin_created);A.register_delete_callback(F,_handle_plugin_deleted);I=F+'/functions/function';A.register_create_callback(I,_handle_function_created);A.register_delete_callback(I,_handle_function_deleted);C='/ietf-keystore:keystore/asymmetric-keys/asymmetric-key/';A.register_create_callback(C+_P,_handle_asymmetric_public_key_created_or_changed);A.register_change_callback(C+_P,_handle_asymmetric_public_key_created_or_changed);A.register_create_callback(C+_U,_handle_asymmetric_private_key_created_or_changed);A.register_change_callback(C+_U,_handle_asymmetric_private_key_created_or_changed);A.register_create_callback(C+N,_handle_asymmetric_key_cert_created_or_changed);A.register_change_callback(C+N,_handle_asymmetric_key_cert_created_or_changed);J='/ietf-truststore:truststore/certificate-bags/'+'certificate-bag/certificate/cert-data';A.register_create_callback(J,_handle_trust_anchor_cert_created_or_changed);A.register_change_callback(J,_handle_trust_anchor_cert_created_or_changed);E='/ietf-restconf-server:restconf-server';A.register_change_callback(E+'/listen',_handle_transport_changed);A.register_change_callback(E+'/listen/endpoints',_handle_transport_changed);A.register_change_callback(E+'/listen/endpoints/endpoint',_handle_transport_changed);A.register_delete_callback(E+'',_handle_transport_delete)
		for K in A.dal.ref_stat_collectors:
			assert K.endswith(_a);L,T=K.rsplit(_B,1)
			if T.startswith(_b):A.register_create_callback(L,_handle_ref_stat_parent_created_yc)
			else:A.register_create_callback(L,_handle_ref_stat_parent_created)
	def register_create_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.create_callbacks:A.create_callbacks[B]=[C]
		else:A.create_callbacks[B].append(C)
	def register_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.change_callbacks:A.change_callbacks[B]=[C]
		else:A.change_callbacks[B].append(C)
	def register_delete_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.delete_callbacks:A.delete_callbacks[B]=[C]
		else:A.delete_callbacks[B].append(C)
	def register_subtree_change_callback(A,schema_path,callback):raise NotImplementedError
	def register_somehow_change_callback(A,schema_path,callback):raise NotImplementedError
	def register_onetime_callback(A,timestamp,callback,opaque):raise NotImplementedError
	def register_periodic_callback(A,period,anchor,callback):raise NotImplementedError('periodic callbacks not implemented yet')
	def register_leafref_callback(A,schema_path,callback):raise NotImplementedError
	async def _check_auth(B,request,data_path):
		P='No authorization required for fresh installs.';O='/yangcore:users/user';L='access-denied';K='failure';J='success';G='comment';E='outcome';D=request;assert data_path is not _A;A={};A['timestamp']=datetime.datetime.now(datetime.UTC).replace(microsecond=0);A['source-ip']=D.remote
		if len(D.forwarded):A['source-proxies']=list(D.forwarded)
		A['host']=D.host;A['method']=D.method;A['path']=D.path;M=D.headers.get('AUTHORIZATION')
		if M is _A:
			H=await B.dal.num_elements_in_list(O)
			if H==0:A[E]=J;A[G]=P;await utils.insert_audit_log_record(B.dal,B.plugins,A);return web.Response(status=200)
			A[E]=K;A[G]='No authorization specified in the HTTP header.';await utils.insert_audit_log_record(B.dal,B.plugins,A);C=web.Response(status=401);F=utils.gen_rc_errors(_C,L);C.text=json.dumps(F,indent=2);return C
		I,Q=basicauth.decode(M);R='/yangcore:users/user='+I+'/authentication/password-based/password'
		try:S=await B.dal.handle_get_config_request(R,{})
		except dal.NodeNotFound:
			H=await B.dal.num_elements_in_list(O)
			if H==0:A[E]=J;A[G]=P;await utils.insert_audit_log_record(B.dal,B.plugins,A);return web.Response(status=200)
			A[E]=K;A[G]='Unknown user: '+I;await utils.insert_audit_log_record(B.dal,B.plugins,A);C=web.Response(status=401);F=utils.gen_rc_errors(_C,L);C.text=json.dumps(F,indent=2);return C
		N=S['yangcore:password'];assert N.startswith('$5$')
		if not sha256_crypt.verify(Q,N):A[E]=K;A[G]='Password mismatch for user '+I;await utils.insert_audit_log_record(B.dal,B.plugins,A);C=web.Response(status=401);F=utils.gen_rc_errors(_C,L);C.text=json.dumps(F,indent=2);return C
		A[E]=J;await utils.insert_audit_log_record(B.dal,B.plugins,A);return web.Response(status=200)
	async def handle_get_restconf_root(D,request):
		E=request;G=_B;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_J)
		if isinstance(B,web.Response):A=B;return A
		assert isinstance(B,str);C=B;assert C!=_c;F=utils.Encoding[C.rsplit('+',1)[1].upper()];A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.JSON:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert F==utils.Encoding.XML;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2019-01-04</yang-library-version>\n</restconf>\n'
		return A
	async def handle_get_yang_library_version(D,request):
		E=request;G=_B;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_J)
		if isinstance(B,web.Response):A=B;return A
		assert isinstance(B,str);C=B;assert C!=_c;F=utils.Encoding[C.rsplit('+',1)[1].upper()];A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.JSON:A.text='{ "ietf-restconf:yang-library-version" : "2019-01-04" }'
		else:assert F==utils.Encoding.XML;A.text='<yang-library-version xmlns="urn:ietf:params:xml:'+'ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		return A
	async def handle_get_opstate_request(B,request):
		C=request;D,G=utils.parse_raw_path(C._message.path[RestconfServer.len_prefix_operational:]);A=await B._check_auth(C,D)
		if A.status==401:return A
		E,I=utils.check_http_headers(C,B.supported_media_types,accept_required=_J)
		if isinstance(E,web.Response):H=E;return H
		A,F=await B.handle_get_opstate_request_lower_half(D,G)
		if F is not _A:A.text=json.dumps(F,indent=2)
		return A
	async def handle_get_opstate_request_lower_half(E,data_path,query_dict):
		B=query_dict
		async with E.fifolock(Read),contextlib.nullcontext():
			if os.environ.get(_Q)and _G in B:await asyncio.sleep(int(B[_G]))
			try:F=await E.dal.handle_get_opstate_request(data_path,B)
			except dal.NodeNotFound as C:A=web.Response(status=404);D=utils.gen_rc_errors(_C,_H,error_message=str(C));A.text=json.dumps(D,indent=2);return A,_A
			except NotImplementedError as C:assert _K;A=web.Response(status=501);D=utils.gen_rc_errors(_D,_L,error_message=str(C));A.text=json.dumps(D,indent=2j);return A,_A
			A=web.Response(status=200);A.content_type=_S;return A,F
	async def handle_get_config_request(B,request):
		C=request;D,G=utils.parse_raw_path(C._message.path[RestconfServer.len_prefix_running:]);A=await B._check_auth(C,D)
		if A.status==401:return A
		E,I=utils.check_http_headers(C,B.supported_media_types,accept_required=_J)
		if isinstance(E,web.Response):H=E;return H
		A,F=await B.handle_get_config_request_lower_half(D,G)
		if F is not _A:A.text=json.dumps(F,indent=2)
		return A
	async def handle_get_config_request_lower_half(E,data_path,query_dict):
		F=data_path;D=query_dict
		async with E.fifolock(Read),contextlib.nullcontext():
			try:await E.val.handle_get_config_request(F,D)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_A
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_A
			except val.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_A
			if os.environ.get(_Q)and _G in D:await asyncio.sleep(int(D[_G]))
			try:G=await E.dal.handle_get_config_request(F,D)
			except dal.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_A
			A=web.Response(status=200);A.content_type=_S;return A,G
	async def handle_post_config_request(A,request):
		B=request;D,G=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);E=await A._check_auth(B,D)
		if E.status==401:return E
		F,K=utils.check_http_headers(B,A.supported_media_types,accept_required=_K)
		if isinstance(F,web.Response):C=F;return C
		try:H=await B.json()
		except json.decoder.JSONDecodeError as I:C=web.Response(status=400);J=utils.gen_rc_errors(_C,_d,error_message=_e+str(I));C.text=json.dumps(J,indent=2);return C
		return await A.handle_post_config_request_lower_half(D,G,H)
	async def handle_post_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write),BinaryTypePatcher():
			try:await D.val.handle_post_config_request(F,E,G)
			except(val.InvalidInputDocument,val.UnrecognizedQueryParameter,val.InvalidQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_f,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ValidationFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_L,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_D,_g,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_Q)and _G in E:await asyncio.sleep(int(E[_G]))
			try:await D.dal.handle_post_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D)
			except(dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_h,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except(PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_L,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise B
			D.val.inst=D.val.inst2;D.val.inst2=_A;await D.shared_post_commit_logic();return web.Response(status=201)
	async def handle_put_config_request(A,request):
		B=request;D,G=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);E=await A._check_auth(B,D)
		if E.status==401:return E
		F,K=utils.check_http_headers(B,A.supported_media_types,accept_required=_K)
		if isinstance(F,web.Response):C=F;return C
		try:H=await B.json()
		except json.decoder.JSONDecodeError as I:C=web.Response(status=400);J=utils.gen_rc_errors(_C,_d,error_message=_e+str(I));C.text=json.dumps(J,indent=2);return C
		return await A.handle_put_config_request_lower_half(D,G,H)
	async def handle_put_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write),BinaryTypePatcher():
			try:await D.val.handle_put_config_request(F,E,G)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except(val.NonexistentSchemaNode,val.ValidationFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except(val.InvalidInputDocument,val.UnrecognizedQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_f,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_D,_g,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_L,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_Q)and _G in E:await asyncio.sleep(int(E[_G]))
			try:H=await D.dal.handle_put_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D.delete_callbacks,D)
			except(dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_h,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except(PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_L,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise B
			D.val.inst=D.val.inst2;D.val.inst2=_A;await D.shared_post_commit_logic()
			if H is _J:return web.Response(status=201)
			return web.Response(status=204)
	async def handle_delete_config_request(A,request):
		B=request;C,F=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);assert len(F)==0;D=await A._check_auth(B,C)
		if D.status==401:return D
		E,H=utils.check_http_headers(B,A.supported_media_types,accept_required=_K)
		if isinstance(E,web.Response):G=E;return G
		return await A.handle_delete_config_request_lower_half(C)
	async def handle_delete_config_request_lower_half(A,data_path):
		E=data_path
		async with A.fifolock(Write),BinaryTypePatcher():
			try:await A.val.handle_delete_config_request(E)
			except val.NonexistentSchemaNode as C:B=web.Response(status=400);D=utils.gen_rc_errors(_D,_E,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.NodeNotFound as C:B=web.Response(status=404);D=utils.gen_rc_errors(_C,_H,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.ValidationFailed as C:B=web.Response(status=400);D=utils.gen_rc_errors(_D,_E,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			try:await A.dal.handle_delete_config_request(E,A.delete_callbacks,A.change_callbacks,A)
			except Exception as C:raise C
			A.val.inst=A.val.inst2;A.val.inst2=_A;await A.shared_post_commit_logic();return web.Response(status=204)
	async def shared_post_commit_logic(A):0
	async def handle_action_request(A,request):raise NotImplementedError(_V)
	async def handle_rpc_request(A,request):raise NotImplementedError(_V)
async def _handle_tenant_created(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError('Multitenancy support removed')
async def _handle_transport_changed(watched_node_path,jsob,jsob_data_path,obj):assert watched_node_path is not _A;assert jsob is not _A;assert jsob_data_path is not _A;assert obj is not _A;os.kill(os.getpid(),signal.SIGHUP)
async def _handle_transport_delete(watched_node_path,nvh):raise NotImplementedError(_V)
async def _handle_plugin_created(watched_node_path,jsob,jsob_data_path,nvh):
	C=nvh;assert watched_node_path is not _A;assert jsob_data_path is not _A;B=jsob[_N][_O];E=re.sub('\\..*','',__name__);D=E+_i+B
	if B in C.plugins:F=sys.modules[D];del sys.modules[D];del F;del C.plugins[B]
	try:G=importlib.import_module(D)
	except ModuleNotFoundError as A:raise PluginNotFound(str(A))from A
	except SyntaxError as A:raise PluginSyntaxError('SyntaxError: '+str(A))from A
	C.plugins[B]={_j:G,_I:{}}
async def _handle_plugin_deleted(watched_node_path,nvh):A=re.sub(_W,_X,watched_node_path);C=re.sub('\\..*','',__name__);B=C+_i+A;D=sys.modules[B];del sys.modules[B];del D;del nvh.plugins[A]
async def _handle_function_created(watched_node_path,jsob,jsob_data_path,nvh):
	assert watched_node_path is not _A;B=re.sub(_W,_X,jsob_data_path);A=jsob[_T][_O]
	try:C=getattr(nvh.plugins[B][_j],A)
	except AttributeError as D:raise FunctionNotFound(str(D))from D
	if not callable(C):raise FunctionNotCallable("The plugin function name '"+A+"' is not callable.")
	nvh.plugins[B][_I][A]=C
async def _handle_function_deleted(watched_node_path,nvh):A=watched_node_path;B=re.sub(_W,_X,A);C=A.rsplit('=',1)[1];del nvh.plugins[B][_I][C]
async def _handle_user_passwd_created(watched_node_path,jsob,jsob_data_path,nvh):
	B='password';assert watched_node_path is not _A;assert jsob_data_path is not _A;assert nvh is not _A;A=jsob['user']['authentication']['password-based'];A['password-last-modified']=datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
	if B in A and A[B].startswith('$0$'):A[B]=sha256_crypt.using(rounds=1000).hash(A[B][3:])
	else:0
async def _handle_user_passwd_changed(watched_node_path,jsob,jsob_data_path,nvh):await _handle_user_passwd_created(watched_node_path,jsob,jsob_data_path,nvh)
async def _handle_ref_stat_parent_created(watched_node_path,jsob,jsob_data_path,nvh,ns=_A):
	assert nvh is not _A;assert watched_node_path==jsob_data_path
	def A(item):
		A=_a
		if ns is not _A:A='yangcore:reference-statistics'
		item[A]={'reference-count':0,'last-referenced':'never'}
	B=next(iter(jsob));A(jsob[B])
async def _handle_ref_stat_parent_created_yc(watched_node_path,jsob,jsob_data_path,nvh):await _handle_ref_stat_parent_created(watched_node_path,jsob,jsob_data_path,nvh,_b)
async def _handle_asymmetric_public_key_created_or_changed(watched_node_path,jsob,jsob_data_path,nvh):
	R='The asymmetric-key has a mismatched public/private key pair: ';Q='ietf-crypto-types:rsa-private-key-format';P='ietf-crypto-types:ec-private-key-format';O='private-key-format';D=nvh;C=watched_node_path;A=jsob;assert jsob_data_path is not _A;F=A[_F][O];S=A[_F][_U];I=base64.b64decode(S)
	if F==P:E,E=decode_der(I,asn1Spec=rfc5915.ECPrivateKey())
	elif F==Q:E,E=decode_der(I,asn1Spec=rfc3447.RSAPrivateKey())
	else:raise dal.CreateOrChangeCallbackFailed('Parsing private key structure failed for '+A[_F][O]+') for '+C.rsplit(_B,1)[0])
	K=serialization.load_der_private_key(I,_A,_A);T=A[_F][_P];L=base64.b64decode(T)
	try:E,E=decode_der(L,asn1Spec=rfc5280.SubjectPublicKeyInfo())
	except PyAsn1Error as B:raise dal.CreateOrChangeCallbackFailed('Parsing public key structure failed for '+C.rsplit(_B,1)[0]+' ('+str(B)+')')from B
	M=serialization.load_der_public_key(L);G=b"this is some data I'd like to sign"
	if F==P:
		J=K.sign(G,ec.ECDSA(hashes.SHA256()))
		try:M.verify(J,G,ec.ECDSA(hashes.SHA256()))
		except InvalidSignature as B:raise dal.CreateOrChangeCallbackFailed(R+C.rsplit(_B,1)[0])from B
	elif F==Q:
		H=hashes.SHA256();J=K.sign(G,padding.PSS(mgf=padding.MGF1(H),salt_length=padding.PSS.MAX_LENGTH),H)
		try:M.verify(J,G,padding.PSS(mgf=padding.MGF1(H),salt_length=padding.PSS.MAX_LENGTH),H)
		except InvalidSignature as B:raise dal.CreateOrChangeCallbackFailed(R+C.rsplit(_B,1)[0])from B
	if _R in A[_F]:
		if _M in A[_F][_R]:
			if D.dal.post_dal_callbacks is _A:D.dal.post_dal_callbacks=[]
			N=_handle_verify_asymmetric_key_and_certs_post_sweep,C.rsplit(_B,1)[0],D
			if N not in D.dal.post_dal_callbacks:return
			D.dal.post_dal_callbacks.append(N)
async def _handle_asymmetric_private_key_created_or_changed(watched_node_path,jsob,jsob_data_path,nvh):await _handle_asymmetric_public_key_created_or_changed(watched_node_path,jsob,jsob_data_path,nvh)
async def _handle_asymmetric_key_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,nvh):
	I='End entity certificates must not encode superfluous certificates. ';C=nvh;B=watched_node_path;assert jsob_data_path is not _A;J=jsob[_M][_Y];K=base64.b64decode(J);L,P=decode_der(K,asn1Spec=rfc5652.ContentInfo());M=utils.degenerate_cms_obj_to_ders(L);A=[]
	for N in M:O=x509.load_der_x509_certificate(N);A.append(O)
	E=[A for A in A if A.extensions.get_extension_for_oid(ExtensionOID.BASIC_CONSTRAINTS).value.ca is _K]
	if len(E)==0:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a certificate '+'having "basic" constraint "ca" with value "False": '+B.rsplit(_B,1)[0])
	if len(E)>1:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode no more than one certificate having '+'"basic" constraint "ca" with value "False" ('+str(len(E))+_k+B.rsplit(_B,1)[0])
	G=E[0];A.remove(G);D=G
	while len(A)!=0:
		F=[A for A in A if A.subject==D.issuer]
		if len(F)==0:raise dal.CreateOrChangeCallbackFailed(I+'Found certificates unconnected to chain from the "leaf" '+'certificate while looking for "'+str(D.subject)+_Z+B.rsplit(_B,1)[0])
		if len(F)>1:raise dal.CreateOrChangeCallbackFailed(I+'CMS encodes multiple certificates having the same "subject" value ('+str(D.issuer)+'): '+B.rsplit(_B,1)[0])
		D=F[0];A.remove(D)
	if C.dal.post_dal_callbacks is _A:C.dal.post_dal_callbacks=[]
	else:
		H=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_B,3)[0],C
		if H not in C.dal.post_dal_callbacks:return
	C.dal.post_dal_callbacks.append(H)
async def _handle_verify_asymmetric_key_and_certs_post_sweep(watched_node_path,conn,opaque):
	I='record_id';B=conn;A=watched_node_path;C=opaque;E=C.dal._get_row_data_for_list_path(A,B);F=re.sub('=[^/]*','',A);D=C.dal._get_jsob_for_record_id_in_table(F,E[I],B);J=D[_F][_P];K=base64.b64decode(J);L=serialization.load_der_public_key(K);assert _R in D[_F];assert _M in D[_F][_R];M=F+'/certificates/certificate';N=C.dal._find_rows_in_table_having_parent_id(M,E[I],{},B);G=N.fetchall();assert len(G)!=0
	for H in G:
		O=H['jsob'][_M][_Y];P=base64.b64decode(O);Q,V=decode_der(P,asn1Spec=rfc5652.ContentInfo());R=utils.degenerate_cms_obj_to_ders(Q)
		for S in R:
			T=x509.load_der_x509_certificate(S);U=L.public_numbers()
			if T.public_key().public_numbers()==U:break
		else:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a "leaf" certificate '+"having a public key matching the asymmetric key's public key: "+A+'/certificates/certificate='+H[_O])
async def _handle_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,nvh):
	B=watched_node_path;assert jsob_data_path is not _A;assert nvh is not _A;G=jsob[_M][_Y];H=base64.b64decode(G)
	try:I,N=decode_der(H,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as J:raise dal.CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B.rsplit(_B,1)[0]+' ('+str(J)+')')
	K=utils.degenerate_cms_obj_to_ders(I);A=[]
	for L in K:M=x509.load_der_x509_certificate(L);A.append(M)
	D=[A for A in A if A.subject==A.issuer]
	if len(D)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) '+'certificate: '+B.rsplit(_B,1)[0])
	if len(D)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root '+'(self-signed) certificate ('+str(len(D))+_k+B.rsplit(_B,1)[0])
	F=D[0];A.remove(F);C=F
	while len(A)!=0:
		E=[A for A in A if A.issuer==C.subject]
		if len(E)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.'+'Discovered additional certificates while looking for the issuer of "'+str(C.subject)+_Z+B.rsplit(_B,1)[0])
		if len(E)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of '+'certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+_Z+B.rsplit(_B,1)[0])
		C=E[0];A.remove(C)
async def _check_expirations(nvh):assert nvh is not _A