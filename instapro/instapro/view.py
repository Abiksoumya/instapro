from django.http import JsonResponse
from instagram_private_api import Client
import instaloader


def get_profile(request):
    # Retrieve the username from the API request
    username = request.GET.get('username')
    print(username)

    try:
        # Retrieve the user's profile by username
        loader = instaloader.Instaloader()

        # Retrieve profile details
        profile = instaloader.Profile.from_username(loader.context, username)

        # Extract the profile details
        response = {
            'username': profile.username,
            'full_name': profile.full_name,
            'bio': profile.biography,
            'followers': profile.followers,
            'following': profile.followees,
            'posts': profile.mediacount,
            'website': profile.external_url,
        }

        # Print profile data
        print(response)

        # Retrieve the user's stories
        # ...

        # Return the profile details as a JSON response
        return JsonResponse(response)

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return JsonResponse(response, status=400)
