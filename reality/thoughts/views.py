from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.shortcuts import render
from .forms import thoughtform
from django.shortcuts import redirect
from .models import bella
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dal import autocomplete
from .models import UserProfile
from .forms import SearchForm
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django import forms
from django.views.generic.edit import FormView
import json
from .utils import format_quote, get_user_model, get_username_field
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseForbidden
from .forms import UserProfileForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.sites.models import Site

User = get_user_model()

# Create your views here.

#def post_detail(request):
#   thots = thought.objects.all()
#   return render(request, 'mythots.html', {'thots': thots})


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return User.objects.none()
        
        qs = User.objects.all()
        #qs = UserProfile.tags.all()
        
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        
        return qs

class UpdateView(generic.UpdateView):
    model = User
    form_class = SearchForm
    template_name = 'message.html'
    success_url = reverse_lazy('search')
    def get_object(self):
        return UserProfile.objects.first()

class Update2View(generic.UpdateView):
    model = UserProfile
    form_class = SearchForm
    template_name = 'mythots.html'
    success_url = reverse_lazy('search')
    def get_object(self):
        ctx = UserProfile.objects.first()
        return ctx

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        user_id = form.data['username']
        user = User.objects.get(id=user_id)
        return redirect('found', user)

def my_thoughts(request):
    thots = thought.objects.filter(creation_date__lte=timezone.now()).order_by('creation_date')
    template = loader.get_template('thotpage.html')
    context = {
        'thots': thots,
    }
    
    return HttpResponse(template.render(context, request))

def home(request):
    thots = bella.objects.filter(creation_date__lte=timezone.now()).order_by('creation_date')
    template = loader.get_template('homepage.html')
    form = UserProfileForm()
    context = {
        'form':form,
        'thots': thots
    }
    
    return HttpResponse(template.render(context, request))


def tech(request):
    thots = bella.objects.filter(creation_date__lte=timezone.now()).order_by('creation_date')
    template = loader.get_template('Categories.html')
    context = {
        'thots': thots
    }
    
    return HttpResponse(template.render(context, request))

def post_detail(request, pk):
    thots = get_object_or_404(bella, pk=pk)
    template = loader.get_template('thought_detail.html')
    context = {
    'thots': thots,
    'pk': pk,
    }
    return HttpResponse(template.render(context, request))

def RegisterView(request):
    message = ""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        print form.errors
        if form.is_valid():
            return handle_uploaded_file(request, request.FILES['file'])
        else:
            form = UserProfileForm()
        return render(request, 'pls.html',{'form': form, 'message':message})
    else:
        form = UserProfileForm()
        return render(request, 'pls.html',{'form': form, 'message':message})
        '''if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                m = UserProfile.objects.get(pk=course_id)
                m.model_pic = form.cleaned_data['image']
                m.save()
                return HttpResponse('image upload success')'''

def handle_uploaded_file(request, f):
    
    response = {}
    
    image = ""
    
    FILE_URL_PATH = getattr(settings, "FILE_URL_PATH", None)
    
    FILE_SAVE_PATH = getattr(settings, "FILE_SAVE_PATH", None)
    if request.user.is_authenticated():
        user = request.user
    
    FILE_SAVE_PATH = FILE_SAVE_PATH + '/' +  user.username + '/'

    OVERWRITE_PREVIOUS_FILES = getattr(settings, "OVERWRITE_PREVIOUS_FILES", None)
    
    ## this determines whether user file already exist, if not it creates one.  If one exist it deletes what's there to replace
    try:
        os.makedirs(FILE_SAVE_PATH)
    except OSError as exception:
    ## true by default unless overridden by settings.py
        if OVERWRITE_PREVIOUS_FILES != False:
            for the_file in os.listdir(FILE_SAVE_PATH):
                file_path = os.path.join(FILE_SAVE_PATH, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    pass
    if exception.errno != errno.EEXIST:
        raise

    try:
        size = (100, 100)
        image = Image.open(f)
        image.thumbnail(size,Image.ANTIALIAS)
        image.save(FILE_SAVE_PATH + f.name, image.format)
        ## create the user avatar if one if not created
        insert = Easy_Avatar.objects.get_or_create(user=user)
        ## now that a user is created we can update it's avatar image location
        avatar = Easy_Avatar.objects.get(user=user)
        avatar.docfile = FILE_SAVE_PATH + f.name
        avatar.image_url = FILE_URL_PATH + user.username + '/' + f.name
        avatar.save()
        response["message"] = "Success"
        response["image_url"] = FILE_URL_PATH + user.username + '/' + f.name
    
    except:
        response["message"] = "I'm sorry we could not upload your image"
        response["image_url"] = ""



    return HttpResponse(json.dumps(response), content_type="application/json")



def new_thought(request):
    if request.method == 'POST':
        form = thoughtform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', post.pk)

        form = thoughtform()
        context = {
            'media': form.media,
            'form':form,
    }
        template = loader.get_template('thot.html')
        return HttpResponse(template.render(context, request))
    
    else:
        form = thoughtform()
        context = {
            'form':form
        }
        template = loader.get_template('thot.html')
    return HttpResponse(template.render(context, request))


@login_required
def users(request, username="", ribbit_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        thoughts = bella.objects.filter(user=user.id)
        fs = len(Follow.objects.followers(user = User.objects.get(username=username)))
        fg = len(Follow.objects.following(user = User.objects.get(username=username)))
        if username == request.user.username:
            print 'a'
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'thoughts': thoughts, "followers":fs, "following":fg,})
        if User.objects.get(username=username) in Follow.objects.following(request.user):
            print 'b'
            return render(request, 'user.html', {'user': user, 'thoughts': thoughts, 'unfollow': True, "followers":fs, "following":fg,})
        print 'c'
        return render(request, 'user.html', {'user': user, 'thoughts': thoughts, 'follow': True, "followers":fs, "following":fg,})
    users = User.objects.all()
    thoughts = map(get_latest, users)
    obj = zip(users, thoughts)
    ribbit_form = ribbit_form or thoughtform()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                  'ribbit_form': ribbit_form,
                  'username': request.user.username, })

def my_thoughts(request):
    thots = bella.objects.filter(creation_date__lte=timezone.now()).order_by('creation_date')
    template = loader.get_template('thotpage.html')
    context = {
        'thots': thots
    }
    
    return HttpResponse(template.render(context, request))

@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                Follow.objects.add_follower(request.user, user)
                return redirect('/thoughts/users/')
            except ObjectDoesNotExist:
                return redirect('/thoughts/users/')

def get_latest(user):
    try:
        return bella.objects.all()
    except IndexError:
        return ""

@login_required
def unfollow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                Follow.objects.remove_follower(request.user, user)
                return redirect('/thoughts/users/')
            except ObjectDoesNotExist:
                return redirect('/thoughts/users/')

@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        bela = get_object_or_404(bella, pk = pk)
        if bela.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            bela.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            bela.likes.add(user)
            message = 'You liked this'
    ctx = {'likes_count': bela.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@require_POST
def pls(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        thoughts = bella.objects.filter(user=user.id)
        thots = []
        links = []
        for thought in thoughts:
            thots.append(str(thought.image))
            links.append(str(thought.pk))
    ctx = {'thots': thots, 'links':links}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@require_POST
def FollowerFollowing(request):
    if request.method == 'POST':
        user = request.user
        fs = (Follow.objects.followers(user))
        fg = (Follow.objects.following(user))
        followers = []
        following = []
        for object in fs:
            followers.append(object.username)
        for object in fg:
            following.append(object.username)
        if (len(followers)==0):
            followers.append("No Followers")
        if (len(following)==0):
            following.append("Not Following Anybody")
    ctx = {'followers': followers, 'following':following}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

