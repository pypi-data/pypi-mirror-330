# Copyright (c) 2019-2025 Watsen Networks. All Rights Reserved.

from __future__ import annotations
_C='/ds/ietf-datastores:operational'
_B='/ds/ietf-datastores:running'
_A=None
import tempfile,base64,ssl
from aiohttp import web
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
from.import utils
from.handler import RouteHandler
class RestconfServer:
	root='/restconf';prefix_running=root+_B;prefix_operational=root+_C;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler):
		v='client-certs';u='central-truststore-reference';t='ca-certs';s='client-authentication';r='utf-8';q='\n-----END CERTIFICATE-----\n';p='-----BEGIN CERTIFICATE-----\n';o=False;n='cert-data';m='private-key-format';l='/ietf-keystore:keystore/asymmetric-keys/asymmetric-key=';k='central-keystore-reference';j='server-identity';i='http-over-tcp';V='ASCII';U='ietf-keystore:asymmetric-key';M='certificate';L='tls-server-parameters';K='/ds/ietf-datastores:running{tail:.*}';D='http-over-tls';C=endpoint_config;B=view_handler;A.len_prefix_running=len(A.root+_B);A.len_prefix_operational=len(A.root+_C);A.loop=loop;A.dal=dal;A.name=C['name'];A.view_handler=B;A.app=web.Application(client_max_size=33554432)
		async def w(request,response):assert request is not _A;response.headers['Server']='<redacted>'
		A.app.on_response_prepare.append(w);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,B.handle_get_restconf_root);A.app.router.add_get(A.root+'/',B.handle_get_restconf_root);A.app.router.add_get(A.root+'/yang-library-version',B.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',B.handle_get_opstate_request);A.app.router.add_get(A.root+K,B.handle_get_config_request);A.app.router.add_put(A.root+K,B.handle_put_config_request);A.app.router.add_post(A.root+K,B.handle_post_config_request);A.app.router.add_delete(A.root+K,B.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',B.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',B.handle_rpc_request)
		if i in C:G=i
		else:assert D in C;G=D
		H=C[G]['tcp-server-parameters']['local-bind'];assert isinstance(H,list);assert len(H)==1;A.local_address=H[0]['local-address'];A.local_port=H[0]['local-port'];E=_A
		if G==D:
			W=C[D][L][j][M][k]['asymmetric-key'];N=A.dal.handle_get_config_request(l+W,{});O=A.loop.run_until_complete(N);P=O[U][0]['cleartext-private-key'];X=base64.b64decode(P)
			if O[U][0][m]=='ietf-crypto-types:ec-private-key-format':Q,F=der_decoder(X,asn1Spec=rfc5915.ECPrivateKey());x=der_encoder(Q);Y=base64.b64encode(x).decode(V);assert P==Y;Z='-----BEGIN EC PRIVATE KEY-----\n'+Y+'\n-----END EC PRIVATE KEY-----\n'
			elif O[U][0][m]=='ietf-crypto-types:rsa-private-key-format':Q,F=der_decoder(X,asn1Spec=rfc3447.RSAPrivateKey());y=der_encoder(Q);a=base64.b64encode(y).decode(V);assert P==a;Z='-----BEGIN RSA PRIVATE KEY-----\n'+a+'\n-----END RSA PRIVATE KEY-----\n'
			else:raise NotImplementedError('this line can never be reached')
			z=C[D][L][j][M][k][M];N=A.dal.handle_get_config_request(l+W+'/certificates/certificate='+z,{});A0=A.loop.run_until_complete(N);A1=A0['ietf-keystore:certificate'][0][n];A2=base64.b64decode(A1);A3,F=der_decoder(A2,asn1Spec=rfc5652.ContentInfo());A4=A3.getComponentByName('content');A5,F=der_decoder(A4,asn1Spec=rfc5652.SignedData());A6=A5.getComponentByName('certificates');I=''
			for(F,A7)in enumerate(A6):
				b=A7[0];R=_A
				for c in b['tbsCertificate']['extensions']:
					if c['extnID']==rfc5280.id_ce_basicConstraints:R,F=der_decoder(c['extnValue'],asn1Spec=rfc5280.BasicConstraints())
				A8=der_encoder(b);d=base64.b64encode(A8).decode(V)
				if R is not _A and R['cA']is o:I=p+d+q+I
				else:I+=p+d+q
			E=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);E.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as e:
				f=e+'key.pem';g=e+'certs.pem'
				with open(f,'w',encoding=r)as A9:A9.write(Z)
				with open(g,'w',encoding=r)as AA:AA.write(I)
				E.load_cert_chain(g,f)
			if s in C[D][L]:
				J=C[D][L][s]
				def h(truststore_ref):
					C=dal.handle_get_config_request('/ietf-truststore:truststore/certificate-bags/certificate-bag='+truststore_ref,{});D=A.loop.run_until_complete(C);B=[]
					for E in D['ietf-truststore:certificate-bag'][0][M]:F=base64.b64decode(E[n]);G,H=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not H;B+=utils.degenerate_cms_obj_to_ders(G)
					return B
				S=[]
				if t in J:T=J[t][u];S+=h(T)
				if v in J:T=J[v][u];S+=h(T)
				AB=utils.der_dict_to_multipart_pem({'CERTIFICATE':S});E.load_verify_locations(cadata=AB)
		if G==D:assert not E is _A
		else:assert E is _A
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=E,reuse_port=o);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):assert request is not _A;A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A