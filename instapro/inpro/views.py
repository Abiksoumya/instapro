from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from instagram_private_api import Client
from .form import ProfileForm
import instaloader


def profile_view(request):
    form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Authenticate with Instagram
            
            try:
                # Retrieve the user's profile by username
                
                loader = instaloader.Instaloader()
                # Extract the profile details
                profile = instaloader.Profile.from_username(loader.context, username)
                stories = []
                for story in loader.get_stories():
                    loader.download_storyitem(story, username)
                    stories.append({
                        'media_url': story.url,
                        
                    })
                response = {
                    'username': profile.username,
                    'full_name': profile.full_name,
                    'bio': profile.biography,
                    'followers': profile.followers,
                    'following': profile.followees,
                    'posts': profile.mediacount,
                    'website': profile.external_url,
                    'stories': stories, 
                }
                
                
                return render(request, 'profile.html', {'form': form, 'response': response})
            
            except Exception as e:
                error_message = str(e)
                response = {'error': error_message}
                return render(request, 'profile.html', {'form': form, 'response': response})

    return render(request, 'profile.html', {'form': form})

