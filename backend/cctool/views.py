from                 django.contrib import auth
from django.core.context_processors import csrf
from     django.contrib.auth.models import User
from                   django.views import generic
from   django.views.decorators.csrf import ensure_csrf_cookie
from        django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from               django.shortcuts import render, render_to_response, get_object_or_404
from                    django.http import HttpResponse, HttpResponseRedirect, Http404
from                  cctool.models import Graph
from             cctool.serializers import UserSerializer, GraphSerializer, ImplicationsSerializer
from             cctool.permissions import IsOwnerOrAdmin
from                   cctool.forms import GraphForm, RegistrationForm
from                 rest_framework import permissions, viewsets


# PAGE: Homepage (either the landing page or the user dashboard)
class HomeView(generic.TemplateView):
	def get(self, request):
		if request.user.is_authenticated():
			return render_to_response('cctool/dashboard/index.html', {'user':request.user})
		else:
			return render_to_response('cctool/site_home.html')

# GET: Login Page
class LoginView(generic.View):
	def get(self, request):
		args={}
		args.update(csrf(request))
		return render_to_response('cctool/user_login.html', args)

# POST: Authorise user
class LoginAuthView(generic.View):
	def post(self, request):
		username=request.POST.get('username','')
		password=request.POST.get('password','')
		user=auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request,user)
			return HttpResponseRedirect('/cctool/')
		else:
			return HttpResponseRedirect('/cctool/invalid_login')

# GET: User Page
class CCToolView(generic.View):
	@method_decorator(login_required(login_url='/cctool/login/'))
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		return render_to_response('cctool/dashboard/index.html', {'user':request.user})

# GET: Invalid user
class InvalidLoginView(generic.View):
	def get(self, request):
		return render_to_response('cctool/user_invalid.html')

# GET: Logout user
class LogoutView(generic.View):
	def get(self, request):
		auth.logout(request)
		return render_to_response('cctool/site_home.html')

# POST: Register user
class RegisterUserView(generic.View):
	def get(self, request):
		args = {}
		args.update(csrf(request))
		args['form'] = RegistrationForm()
		return render_to_response('cctool/user_register.html',args)

	def post(self, request):
		args = {}
		form = RegistrationForm(request.POST)
		if form.is_valid():
			# TODO: For more security, have an email to confirm (etc)
			form.save()
			return HttpResponseRedirect('/cctool/login')
		args.update(csrf(request))
		args['form'] = RegistrationForm()
		return render_to_response('cctool/user_register.html',args)

# POST: Sucessful registration
class RegisterSuccessView(generic.View):
	def get(self, request):
		return render_to_response('cctool/user_register_success.html')

# -- Django Rest Framework --
# Provide list/detail actions for users.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset           = User.objects.all()
	serializer_class   = UserSerializer
	permission_classes = (permissions.IsAdminUser,)

# Provide list/create/retrieve/update/destroy actions for graphs.
class GraphViewSet(viewsets.ModelViewSet):
	serializer_class   = GraphSerializer
	permission_classes = (IsOwnerOrAdmin,)

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Graph.objects.all()
		return Graph.objects.filter(owner=user)

	def parseData(self, dataToParse, validatedData):
		# Generate Labels, Functions, Controllabilities, Importances
		labels = []
		functions = []
		coordinates = []
		controllability = []
		importance = []

		nodes = dataToParse['nodes']
		edges = dataToParse['edges']

		# Replace node id with enumatation,
		# add label, function, controllability and importance to arrays.
		node_index=0
		node_ids = {}
		for node in nodes:
			current_id = node['id']
			node_ids[current_id] = str(node_index)
			node['id'] = str(node_index)
			labels.append( node['label'] )
			functions.append( node['cctool']['function'] )
			coordinates.append( str(node['x'])+" "+str(node['y']) )
			controllability.append( node['cctool']['controllability'] )
			importance.append( node['cctool']['importance'] )
			node_index += 1

		# Create matrix (nodes*nodes)
		structure = [ [0 for x in range(node_index)] for y in range(node_index) ]

		# Replace edge id / to / from to new node ids
		# add structure
		edge_index = 0
		for edge in edges:
			nodeFromId = node_ids[ edge['from'] ]
			nodeToId = node_ids[ edge['to'] ]
			edge['id'] = nodeFromId +'-'+ nodeToId
			edge['from'] = nodeFromId
			edge['to'] = nodeToId
			structure[int(nodeFromId)][int(nodeToId)] = edge['cctool']['weight']

		# Set object fields from given graph data.
		validatedData['title'] = dataToParse['details']['title']
		validatedData['description'] = dataToParse['details']['description']
		validatedData['moredescription'] = dataToParse['details']['moredescription']
		validatedData['structure'] = ','.join([' '.join(str(j) for j in i) for i in structure])
		validatedData['labels'] = ','.join(labels)
		validatedData['functions'] = ' '.join(functions)
		validatedData['coordinates'] = ','.join(coordinates)
		validatedData['controllability'] = ' '.join(controllability)
		validatedData['importance'] = ' '.join(importance)

	def perform_create(self, serializer):
		self.parseData(serializer.initial_data, serializer.validated_data)
		serializer.save(owner=self.request.user)

# Provide list/create/retrieve/update/destroy actions for graphs.
class AdminGraphViewSet(viewsets.ModelViewSet):
	serializer_class   = GraphSerializer
	permission_classes = (permissions.IsAdminUser,)

	def get_queryset(self):
		return Graph.objects.all()

# Provide implications link for graphs.
class Implications(viewsets.ModelViewSet):
	serializer_class   = ImplicationsSerializer
	permission_classes = (IsOwnerOrAdmin,)

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Graph.objects.all()
		return Graph.objects.filter(owner=user)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
